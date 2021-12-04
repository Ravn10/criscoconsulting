from __future__ import unicode_literals

import frappe
import json
from frappe.utils import flt, getdate, nowdate, fmt_money

# Cancel JV when Cancelling CAsh/Bank Entry -by Pranali
def cancel_journal_entry(self,doc):
    journal_entry = frappe.get_doc("Journal Entry",self.name)
    if journal_entry.name:
        journal_entry.cancel()
        # frappe.db.commit()


# Create JV when Submitting CAsh/Bank Entry -by Pranali
def create_journal_entry(self):
    journal_entry_list=frappe.db.sql("select * from `tabJournal Entry` where name='"+self.name+"'",as_dict=1)
    if len(journal_entry_list)==0:
        jv_doc=frappe.new_doc("Journal Entry")
    else:
        jv_doc=frappe.get_doc("Journal Entry",self.name)
    jv_doc.title=self.title
    jv_doc.voucher_type=self.voucher_type
    jv_doc.naming_series=self.naming_series
    jv_doc.cost_center=self.cost_center
    jv_doc.posting_date=self.posting_date
    jv_doc.company=self.company
    jv_doc.cheque_no=self.cheque_no
    jv_doc.cheque_date=self.cheque_date
    jv_doc.user_remark=self.user_remark
    jv_doc.total_debit=self.total_debit
    jv_doc.total_credit=self.total_credit
    jv_doc.difference=self.difference
    jv_doc.get_balance=self.get_balance
    jv_doc.multi_currency=self.multi_currency
    jv_doc.total_amount_currency=self.total_amount_currency
    jv_doc.total_amount=self.total_amount
    jv_doc.total_amount_in_words=self.total_amount_in_words
    jv_doc.clearance_date=self.clearance_date
    jv_doc.remark=self.remark
    jv_doc.bill_no=self.bill_no
    jv_doc.bill_date=self.bill_date
    jv_doc.due_date=self.due_date
    jv_doc.write_off_based_on=self.write_off_based_on
    jv_doc.write_off_amount=self.write_off_amount
    jv_doc.letter_head=self.letter_head
    jv_doc.select_print_heading=self.select_print_heading
    jv_doc.is_opening=self.is_opening
    jv_doc.stock_entry=self.stock_entry
    jv_doc.subscription=self.subscription
    if self.amended_from:
            jv_doc.amended_from=self.amended_from
    if self.doctype=="Bank Entry":
        jv_doc.reference_of_bank_entry=self.name
    elif self.doctype=="Cash Entry":
        jv_doc.reference_cash_entry=self.name 
    jv_doc.accounts=[]  
    if self.get("accounts"):
        for acc in self.get("accounts"):
            create_jv_child(self,acc,jv_doc) 

    if self.amended_from==None and len(journal_entry_list)==0:
        tab_series = get_current_series(self.naming_series)
        if tab_series:
            update_current_series(self.current_series-1,self.naming_series)
        jv_doc.insert(ignore_permissions=True)
        if tab_series:
            update_current_series(tab_series,self.naming_series)
    elif self.amended_from!=None and len(journal_entry_list)==0:
        jv_doc.insert(ignore_permissions=True)
    else:
        jv_doc.save()
    # self.journal_entry=jv_doc.name
    # frappe.errprint(str(len(jv_doc.accounts)))
    # jv_doc.save()
    # frappe.msgprint("update")
    jv_doc.submit()

    

def create_jv_child(self,acc,jv_doc):
    jv_child=jv_doc.append("accounts")
    jv_child.account=acc.account
    jv_child.account_type=acc.account_type
    jv_child.balance=acc.balance
    jv_child.cost_center=acc.cost_center
    jv_child.narration=acc.narration
    jv_child.party_type=acc.party_type
    jv_child.party=acc.party
    jv_child.party_balance=acc.party_balance
    jv_child.account_currency=acc.account_currency
    jv_child.exchange_rate=acc.exchange_rate
    jv_child.debit_in_account_currency=acc.debit_in_account_currency
    jv_child.debit=acc.debit
    jv_child.credit_in_account_currency=acc.credit_in_account_currency
    jv_child.credit=acc.credit
    jv_child.reference_type=acc.reference_type
    jv_child.reference_name=acc.reference_name
    jv_child.project=acc.project
    jv_child.is_advance=acc.is_advance
    jv_child.against_account=acc.against_account
    return jv_doc

# Delete JV when Deleting CAsh/Bank Entry -by Pranali
def delete_jv(self,doc):     
    journal_entry_list=frappe.db.sql("select * from `tabJournal Entry` where name='"+self.name+"'",as_dict=1)
    if len(journal_entry_list)>0:      
        tab_series = get_current_series(self.naming_series)
        journal_entry=frappe.get_doc("Journal Entry",self.name)         
        journal_entry.delete()  
        if tab_series ==self.current_series-1 and self.amended_from == None:
            update_current_series(self.current_series,self.naming_series)          
        # frappe.db.commit()


#  Update Clearance Date in banck/Cash Entry once Bank Reconciliation Done -by Pranali
@frappe.whitelist() 
def update_clearance_date(doc):
	doc=json.loads(doc)
	jv_entry=frappe.get_doc("Journal Entry",doc["journal_entry"])
	if jv_entry.clearance_date:
		frappe.db.sql("""update `tab{0}` set clearance_date = '{1}', modified = '{2}' where name='{3}'""".format(doc["doctype"], jv_entry.clearance_date, nowdate(), doc["name"]))
		frappe.db.commit()
		# frappe.msgprint("bank Entry Updated.")
	return "Done"

# To Set doc series from name into field by Pranali
def separate_name(self):
    current_value=str(self.name)[len(self.naming_series):len(self.name)]
    self.current_series=current_value
    self.save()


# To Get Current Series for TabSeries by Suresh
def get_current_series(naming_series):
    tab_series = frappe.db.sql("select current from `tabSeries` where name='"+naming_series+"'",as_dict=1)
    if tab_series:
        return tab_series[0].current


# To Update Current Series to TabSeries by Suresh
def update_current_series(doc_series,naming_series):
    frappe.db.sql("update `tabSeries` set current="+str(doc_series)+" where name='"+naming_series+"'")
    frappe.db.commit()


# To Create Payment Entry on submit of Entry of Receipt page by Suresh N
def create_payment_entry(self):
    # frappe.msgprint("creating entry")
    # frappe.errprint(str(self.payment_entry_id)+str(self.amended_from))
    payment_entry_list=frappe.db.sql("select * from `tabPayment Entry` where name='"+self.name+"'",as_dict=1)
    if len(payment_entry_list)==0:
        doc = frappe.new_doc("Payment Entry")        
    else:
        doc=frappe.get_doc("Payment Entry",self.name)
    # frappe.throw(str(doc.entry_of_receipt))        
    doc.entry_of_receipt = self.name
    doc.naming_series = self.naming_series
    doc.payment_type = self.payment_type
    doc.posting_date = self.posting_date
    doc.company = self.company
    doc.mode_of_payment = self.mode_of_payment
    doc.cost_center = self.cost_center
    doc.party_type = self.party_type
    doc.party = self.party
    doc.party_name = self.party_name
    doc.party_balance = self.party_balance
    doc.paid_from = self.paid_from
    doc.paid_from_account_currency = self.paid_from_account_currency
    doc.paid_from_account_balance = self.paid_from_account_balance
    doc.paid_to = self.paid_to
    doc.paid_to_account_currency = self.paid_to_account_currency
    doc.paid_to_account_balance = self.paid_to_account_balance
    doc.paid_amount = self.paid_amount
    doc.source_exchange_rate = self.source_exchange_rate
    doc.base_paid_amount = self.base_paid_amount
    doc.received_amount = self.received_amount
    doc.target_exchange_rate = self.target_exchange_rate
    doc.base_received_amount = self.base_received_amount
    doc.allocate_payment_amount = self.allocate_payment_amount
    doc.total_allocated_amount = self.total_allocated_amount
    doc.base_total_allocated_amount = self.base_total_allocated_amount
    doc.unallocated_amount = self.unallocated_amount
    doc.difference_amount = self.difference_amount
    doc.reference_no = self.reference_no
    doc.reference_date = self.reference_date
    doc.clearance_date = self.clearance_date
    doc.project = self.project
    doc.remarks = self.remarks
    doc.letter_head = self.letter_head
    doc.print_heading = self.print_heading
    self.payment_entry_id=self.name
    if self.amended_from:
            doc.amended_from=self.amended_from
    
    doc.references=[]
    if self.get("references"):
        for references_list in self.get("references"):
            create_reference(doc,references_list)
    
    doc.deductions=[]
    if self.get("deductions"):
        for deduction_list in self.get("deductions"):
            create_deduction(doc,deduction_list)

    if self.amended_from==None and len(payment_entry_list)==0:
        tab_series = get_current_series(self.naming_series)
        if tab_series:
            update_current_series(self.current_series-1,self.naming_series)    
        doc.insert(ignore_permissions=True)
        if tab_series:
            update_current_series(tab_series,self.naming_series)
    elif self.amended_from!=None and len(payment_entry_list)==0:
        doc.insert(ignore_permissions=True)
    else:
        doc.save()
    doc.submit()
    

# Create Child of Payment Entry-by Pranali
def create_reference(doc,references_list):
    references = doc.append("references")
    references.reference_doctype = references_list.reference_doctype
    references.reference_name = references_list.reference_name
    references.due_date = references_list.due_date
    references.bill_no = references_list.bill_no
    references.total_amount = references_list.total_amount
    references.outstanding_amount = references_list.outstanding_amount
    references.allocated_amount = references_list.allocated_amount
    references.exchange_rate = references_list.exchange_rate

# Create Child of Payment Entry  -by Pranali
def create_deduction(doc,deduction_list):
    deduction = doc.append("deductions")
    deduction.account = deduction_list.account
    deduction.cost_center = deduction_list.cost_center
    deduction.amount = deduction_list.amount

#  Cancel payment Entry when Cancelling Entry of Receipt/Payment -by Pranali
def cancel_payment_entry(self,doc):
    # frappe.throw(str(self.name))
    payment_entry=frappe.get_doc("Payment Entry",self.name)
    if payment_entry.name:
        payment_entry.cancel()
        # frappe.db.commit()

#  Delete payment Entry when Deleting Entry of Receipt/Payment -by Pranali
def delete_payment_entry(self,doc):
    payment_entry_list=frappe.db.sql("select * from `tabPayment Entry` where name='"+self.name+"'",as_dict=1)
    if len(payment_entry_list)>0:
        tab_series = get_current_series(self.naming_series)
        payment_entry=frappe.get_doc("Payment Entry",self.name)
        payment_entry.delete()
        if tab_series ==self.current_series-1 and self.amended_from == None:
            update_current_series(self.current_series,self.naming_series)    
        # frappe.db.commit()










