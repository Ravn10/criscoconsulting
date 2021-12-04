# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	
	get_sql_list = "Select * from `VATReport_Purchase_GLEntry_Final` where `01#Date::100`>='{0}' and `01#Date::100`<='{1}' and `11#Voucher Type::100` = ifnull({2},`11#Voucher Type::100`) and `02#Invoice No:Dynamic Link/Voucher Type:150` = ifnull({3},`02#Invoice No:Dynamic Link/Voucher Type:150`) and ifnull(`03#Supplier Name:Link/Supplier:200`,0) = ifnull({4},ifnull(`03#Supplier Name:Link/Supplier:200`,0))  and ifnull(`13#Cost Center:Link/Cost Center:50`,0)=ifnull({5},ifnull(`13#Cost Center:Link/Cost Center:50`,0))".format(filters.get('from_date'),filters.get('to_date'),json.dumps(filters.get('voucher_type')),json.dumps(filters.get('voucher_number')),json.dumps(filters.get('supplier_name')),json.dumps(filters.get('cost_center')))
	
	get_list=frappe.db.sql(get_sql_list, as_dict=1)
	
	columns = get_columns(get_list)
	data= get_values_list(get_list)
	return columns, data

# def validate_filters(filters):

# 	if (filters.get("voucher_no")
# 		and filters.get("group_by") in [_('Group by Voucher'), _('Group by Voucher (Consolidated)')]):
# 		frappe.throw(_("Can not filter based on Voucher No, if grouped by Voucher"))


def get_columns(data):
	column = []
	if len(data)!=0:
		for _key in sorted(data[0].keys()):
			_charidx = _key.find('#') + 1 if _key.find('#') > 0 else 0
			column.append(_key[_charidx:])
	return column

def get_values_list(data):
	rows = []
	if len(data)!=0:
		for idx in range(0,len(data)):
			val = []
			for _key in sorted(data[0].keys()):
				val.append(data[idx][_key])
			rows.append(val)		
	return rows
