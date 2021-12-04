# -*- coding: utf-8 -*-
# Copyright (c) 2015, avu and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe, erpnext
import frappe.defaults
from frappe.utils import nowdate, cstr, flt, cint, now, getdate
from frappe import throw, _
from frappe.utils import formatdate, get_number_format_info
from six import iteritems
# imported to enable erpnext.accounts.utils.get_account_currency
from erpnext.accounts.doctype.account.account import get_account_currency
from erpnext.accounts.doctype.payment_entry.payment_entry import  get_company_defaults

class FiscalYearError(frappe.ValidationError): pass


def reconcile_against_document(args):
	"""
		Cancel JV, Update aginst document, split if required and resubmit jv
	"""
	for d in args:

		check_if_advance_entry_modified(d)
		validate_allocated_amount(d)

		# cancel advance entry
		doc = frappe.get_doc(d.voucher_type, d.voucher_no)

		doc.make_gl_entries(cancel=1, adv_adj=1)

		# update ref in advance entry
		if d.voucher_type == "Journal Entry":
			update_reference_in_journal_entry(d, doc)
		else:
			update_reference_in_payment_entry(d, doc)

		# re-submit advance entry
		doc = frappe.get_doc(d.voucher_type, d.voucher_no)
		doc.make_gl_entries(cancel = 0, adv_adj =1)


def check_if_advance_entry_modified(args):
	"""
		check if there is already a voucher reference
		check if amount is same
		check if jv is submitted
	"""
	ret = None
	if args.voucher_type == "Journal Entry":
		ret = frappe.db.sql("""
			select t2.{dr_or_cr} from `tabJournal Entry` t1, `tabJournal Entry Account` t2
			where t1.name = t2.parent and t2.account = %(account)s
			and t2.party_type = %(party_type)s and t2.party = %(party)s
			and (t2.reference_type is null or t2.reference_type in ("", "Sales Order", "Purchase Order"))
			and t1.name = %(voucher_no)s and t2.name = %(voucher_detail_no)s
			and t1.docstatus=1 """.format(dr_or_cr = args.get("dr_or_cr")), args)
	else:
		party_account_field = "paid_from" if args.party_type == "Customer" else "paid_to"
		if args.voucher_detail_no:
			ret = frappe.db.sql("""select t1.name
				from `tabPayment Entry` t1, `tabPayment Entry Reference` t2
				where
					t1.name = t2.parent and t1.docstatus = 1
					and t1.name = %(voucher_no)s and t2.name = %(voucher_detail_no)s
					and t1.party_type = %(party_type)s and t1.party = %(party)s and t1.{0} = %(account)s
					and t2.reference_doctype in ("", "Sales Order", "Purchase Order")
					and t2.allocated_amount = %(unadjusted_amount)s
			""".format(party_account_field), args)
		else:
			ret = frappe.db.sql("""select name from `tabPayment Entry`
				where
					name = %(voucher_no)s and docstatus = 1
					and party_type = %(party_type)s and party = %(party)s and {0} = %(account)s
					and unallocated_amount = %(unadjusted_amount)s
			""".format(party_account_field), args)

	if not ret:
		throw(_("""Payment Entry has been modified after you pulled it. Please pull it again."""))

def validate_allocated_amount(args):
	if args.get("allocated_amount") < 0:
		throw(_("Allocated amount can not be negative"))
	elif args.get("allocated_amount") > args.get("unadjusted_amount"):
		throw(_("Allocated amount can not greater than unadjusted amount"))



def update_reference_in_journal_entry(d, jv_obj):
	"""
		Updates against document, if partial amount splits into rows
	"""
	jv_detail = jv_obj.get("accounts", {"name": d["voucher_detail_no"]})[0]
	jv_detail.set(d["dr_or_cr"], d["allocated_amount"])
	jv_detail.set('debit' if d['dr_or_cr']=='debit_in_account_currency' else 'credit',
		d["allocated_amount"]*flt(jv_detail.exchange_rate))

	original_reference_type = jv_detail.reference_type
	original_reference_name = jv_detail.reference_name

	jv_detail.set("reference_type", d["against_voucher_type"])
	jv_detail.set("reference_name", d["against_voucher"])

	if d['allocated_amount'] < d['unadjusted_amount']:
		jvd = frappe.db.sql("""
			select cost_center, balance, against_account, is_advance,
				account_type, exchange_rate, account_currency
			from `tabJournal Entry Account` where name = %s
		""", d['voucher_detail_no'], as_dict=True)

		amount_in_account_currency = flt(d['unadjusted_amount']) - flt(d['allocated_amount'])
		amount_in_company_currency = amount_in_account_currency * flt(jvd[0]['exchange_rate'])

		# new entry with balance amount
		ch = jv_obj.append("accounts")
		ch.account = d['account']
		ch.account_type = jvd[0]['account_type']
		ch.account_currency = jvd[0]['account_currency']
		ch.exchange_rate = jvd[0]['exchange_rate']
		ch.party_type = d["party_type"]
		ch.party = d["party"]
		ch.cost_center = cstr(jvd[0]["cost_center"])
		ch.balance = flt(jvd[0]["balance"])

		ch.set(d['dr_or_cr'], amount_in_account_currency)
		ch.set('debit' if d['dr_or_cr']=='debit_in_account_currency' else 'credit', amount_in_company_currency)

		ch.set('credit_in_account_currency' if d['dr_or_cr']== 'debit_in_account_currency'
			else 'debit_in_account_currency', 0)
		ch.set('credit' if d['dr_or_cr']== 'debit_in_account_currency' else 'debit', 0)

		ch.against_account = cstr(jvd[0]["against_account"])
		ch.reference_type = original_reference_type
		ch.reference_name = original_reference_name
		ch.is_advance = cstr(jvd[0]["is_advance"])
		ch.docstatus = 1
		

	# will work as update after submit
	jv_obj.flags.ignore_validate_update_after_submit = True
	jv_obj.save(ignore_permissions=True)


def update_reference_in_payment_entry(d, payment_entry):
	reference_details = {
		"reference_doctype": d.against_voucher_type,
		"reference_name": d.against_voucher,
		"total_amount": d.grand_total,
		"outstanding_amount": d.outstanding_amount,
		"allocated_amount": d.allocated_amount,
		"exchange_rate": d.exchange_rate
	}
	# frappe.errprint("payment_entry>>"+str(payment_entry))
	# frappe.errprint("d>>"+str(d))
	# frappe.errprint("reference_details>>"+str(reference_details))
	if d.voucher_detail_no:
		existing_row = payment_entry.get("references", {"name": d["voucher_detail_no"]})[0]
		# frappe.errprint("existing_row>>"+str(existing_row))
		original_row = existing_row.as_dict().copy()
		# frappe.errprint("original_row>>"+str(original_row))
		existing_row.update(reference_details)
		# frappe.errprint("existing_rowupdate>>"+str(existing_row))

		if d.allocated_amount < original_row.allocated_amount:
			new_row = payment_entry.append("references")
			new_row.docstatus = 1
			for field in list(reference_details):
				new_row.set(field, original_row[field])

			new_row.allocated_amount = original_row.allocated_amount - d.allocated_amount
	else:
		new_row = payment_entry.append("references")
		new_row.docstatus = 1
		new_row.update(reference_details)

	payment_entry.flags.ignore_validate_update_after_submit = True
	payment_entry.setup_party_account_field()
	payment_entry.set_missing_values()
	payment_entry.set_amounts()
	payment_entry.set("deductions",[])
	payment_entry.set_amounts()
	# frappe.errprint("payment_entry.difference_amount()"+str(payment_entry.difference_amount))
	# frappe.errprint("payment_entry.unallocated_amount()"+str(payment_entry.unallocated_amount))
	if float(payment_entry.difference_amount)!=0.0:
		payment_entry=adjust_gain_or_loss(payment_entry,payment_entry.difference_amount,"difference_amount")
	# elif float(payment_entry.target_exchange_rate)!=d.exchange_rate:
	# 	gain_or_loss=(payment_entry.target_exchange_rate*d.allocated_amount)-(d.exchange_rate*d.allocated_amount)
	# 	payment_entry=adjust_gain_or_loss(payment_entry,gain_or_loss,"gain_or_loss")
	
	payment_entry.save(ignore_permissions=True)


def adjust_gain_or_loss(payment_entry,difference_amount,source):
		# payment_entry.unallocated_amount=float(payment_entry.received_amount)-float(payment_entry.total_allocated_amount) if source=="gain_or_loss" else float(payment_entry.unallocated_amount)
		difference_amount=float(difference_amount)
		# frappe.errprint("difference_amount>"+str(difference_amount))
		total_deductions = sum([flt(d.amount) for d in payment_entry.get("deductions")])
		difference_amount+=total_deductions
		# frappe.errprint("difference_amount>"+str(difference_amount))
		company_defaults=get_company_defaults(payment_entry.company)
		rows=[]
		each_row={}
		each_row["amount"]=0.0
		each_row["account"] =company_defaults["exchange_gain_loss_account"]
		each_row["cost_center"] = company_defaults["cost_center"]
		each_row["amount"] =  difference_amount
		total_deductions=float(each_row["amount"] )
		rows.append(each_row)
		payment_entry.set("deductions",rows)
		payment_entry.difference_amount=0
		# frappe.errprint("")
		return payment_entry


def update_reference_in_journal_entry(d, jv_obj):
	"""
		Updates against document, if partial amount splits into rows
	"""
	jv_detail = jv_obj.get("accounts", {"name": d["voucher_detail_no"]})[0]
	jv_detail.set(d["dr_or_cr"], d["allocated_amount"])
	jv_detail.set('debit' if d['dr_or_cr']=='debit_in_account_currency' else 'credit',
		d["allocated_amount"]*flt(jv_detail.exchange_rate))

	original_reference_type = jv_detail.reference_type
	original_reference_name = jv_detail.reference_name

	jv_detail.set("reference_type", d["against_voucher_type"])
	jv_detail.set("reference_name", d["against_voucher"])

	if d['allocated_amount'] < d['unadjusted_amount']:
		jvd = frappe.db.sql("""
			select cost_center, balance, against_account, is_advance,
				account_type, exchange_rate, account_currency
			from `tabJournal Entry Account` where name = %s
		""", d['voucher_detail_no'], as_dict=True)

		amount_in_account_currency = flt(d['unadjusted_amount']) - flt(d['allocated_amount'])
		amount_in_company_currency = amount_in_account_currency * flt(jvd[0]['exchange_rate'])

		# new entry with balance amount
		ch = jv_obj.append("accounts")
		ch.account = d['account']
		ch.account_type = jvd[0]['account_type']
		ch.account_currency = jvd[0]['account_currency']
		ch.exchange_rate = jvd[0]['exchange_rate']
		ch.party_type = d["party_type"]
		ch.party = d["party"]
		ch.cost_center = cstr(jvd[0]["cost_center"])
		ch.balance = flt(jvd[0]["balance"])

		ch.set(d['dr_or_cr'], amount_in_account_currency)
		ch.set('debit' if d['dr_or_cr']=='debit_in_account_currency' else 'credit', amount_in_company_currency)

		ch.set('credit_in_account_currency' if d['dr_or_cr']== 'debit_in_account_currency'
			else 'debit_in_account_currency', 0)
		ch.set('credit' if d['dr_or_cr']== 'debit_in_account_currency' else 'debit', 0)

		ch.against_account = cstr(jvd[0]["against_account"])
		ch.reference_type = original_reference_type
		ch.reference_name = original_reference_name
		ch.is_advance = cstr(jvd[0]["is_advance"])
		ch.docstatus = 1

	# will work as update after submit
	jv_obj.flags.ignore_validate_update_after_submit = True
	jv_obj.save(ignore_permissions=True)


# def set_deductions_entry(doc,account,modified_exchange_rate,difference_amount,base_total_allocated_amount,total_amount_in_foreign_currency):
# 	frappe.errprint("myfunction"+str(difference_amount))
# 	if (doc.target_exchange_rate!=modified_exchange_rate) and (doc.target_exchange_rate!=modified_exchange_rate):
# 		frappe.errprint(get_company_defaults(doc.company))
# 		company_defaults=get_company_defaults(doc.company)
# 		if get_company_defaults(doc.company):
# 			rows=[]
# 			total_deductions=total_deductions_in_foreign_currency=0.0
# 			if len(doc.get("deductions"))==0 and float(difference_amount)!=0.0:
# 				each_row={}
# 				each_row["amount"]=0.0
# 				each_row["account"] =company_defaults[account]
# 				each_row["cost_center"] = company_defaults["cost_center"]
# 				each_row["amount"] =  difference_amount
# 				total_deductions=float(each_row["amount"] )
# 				frappe.errprint("total_deductions>>"+str(total_deductions))
# 				# total_deductions_in_foreign_currency=float(each_row["amount"] )
# 				rows.append(each_row)
# 				frappe.errprint("rows>>"+str(rows))
# 				doc.set("deductions",rows)
# 				doc.base_total_allocated_amount=base_total_allocated_amount
# 				set_unallocated_amount(doc,total_deductions,total_amount_in_foreign_currency)
# 			elif len(doc.get("deductions"))!=0 and float(difference_amount)!=0.0:
# 				for row in doc.get("deductions"):
# 					total_deductions+=row.amount
# 				total_deductions+=difference_amount
# 				frappe.errprint("total_deductions>>"+str(total_deductions))
# 				each_row={}
# 				each_row["amount"]=0.0
# 				each_row["account"] =company_defaults[account]
# 				each_row["cost_center"] = company_defaults["cost_center"]
# 				each_row["amount"] = float(each_row["amount"] ) + difference_amount
# 				rows.append(each_row)
# 				frappe.errprint("rows>>"+str(rows))
# 				doc.set("deductions",rows)
# 				doc.base_total_allocated_amount=base_total_allocated_amount
# 				# set_unallocated_amount(doc,total_deductions,total_amount_in_foreign_currency)



# def set_unallocated_amount(doc,total_deductions,total_amount_in_foreign_currency):
# 	unallocated_amount = 0
# 	if doc.party:
# 		# doc.base_total_allocated_amount
# 		# frappe.errprint("base_total_allocated_amount>"+str(doc.base_total_allocated_amount)+"base_received_amount"+str(doc.base_received_amount)+"total_deductions"+str(total_deductions) +"base_received_amount+total_deductions"+str(doc.base_received_amount + total_deductions))
# 		# frappe.errprint("total_allocated_amount>"+str(doc.total_allocated_amount)+"paid_amount>>"+  str(doc.paid_amount) + "total_deductions>"+str(total_deductions )+ "doc.target_exchange_rate"+str( doc.target_exchange_rate)+ "total_deductions/doc.target_exchange_rate"+str(total_deductions / doc.target_exchange_rate))
# 		if doc.payment_type == "Receive" and doc.base_total_allocated_amount < doc.base_received_amount + total_deductions and doc.total_allocated_amount < doc.paid_amount + (total_deductions / doc.source_exchange_rate):
# 			unallocated_amount = (doc.base_received_amount + total_deductions
# 						- doc.base_total_allocated_amount) / doc.source_exchange_rate
# 		elif doc.payment_type == "Pay" and doc.base_total_allocated_amount < doc.base_paid_amount - total_deductions and doc.total_allocated_amount < doc.received_amount + (total_deductions / doc.target_exchange_rate):
# 			unallocated_amount = (doc.base_paid_amount - (total_deductions+doc.base_total_allocated_amount)) / doc.target_exchange_rate
# 		doc.unallocated_amount=unallocated_amount
# 		frappe.errprint("unallocated_amount>"+str(unallocated_amount))

				
			# for row in doc.get("deductions"):
			# 	row.account==company_defaults[account] if row else None
			# 	frappe.errprint("row>"+str(row.account))