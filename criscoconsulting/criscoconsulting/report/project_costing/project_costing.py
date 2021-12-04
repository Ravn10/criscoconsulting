# Copyright (c) 2013, DPI and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	if not filters: filters = {}
	dict=frappe.db.sql("CALL `projectanalysis`(null,null)",as_dict=1)

	if ('voucher_type' in filters.keys()) and ( not 'voucher_no' in filters.keys()) :
		dict=frappe.db.sql("CALL `projectanalysis`('{0}','None')".format(filters['voucher_type']), as_dict=1)
	
	if (not 'voucher_type' in filters.keys()) and ( 'voucher_no' in filters.keys()):
		frappe.throw("Please Select Trans Ref Type First")
	

	if ('voucher_type' in filters.keys()) and ( 'voucher_no' in filters.keys()):
		dict=frappe.db.sql("CALL `projectanalysis`('{0}','{1}')".format(filters['voucher_type'],filters['voucher_no']), as_dict=1)
		
	
	
	columns = get_columns(dict)
	data= get_values_list(dict)
	return columns, data
	
	




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






