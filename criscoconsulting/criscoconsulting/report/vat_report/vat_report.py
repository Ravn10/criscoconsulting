# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if not filters: filters = {}

	dict=frappe.db.sql("Select * from `VATReport_GLEntry_Final` where `01#Posting Date:Date:100`>=(%s) and `01#Posting Date:Date:100`<=(%s) ", (filters['from_date'], filters['to_date']), as_dict=1)
	
	columns = get_columns(dict)
	data = get_values_list(dict)
	return columns, data

def get_columns(data):
	column = []
	if len(data)!=0:
		for _key in sorted(data[0].keys()):
			_charidx = _key.find('#') + 1 if _key.find('#') > 0 else 0
			field_setting = str(_key[_charidx:]).split(":")
			
			fieldtype, options, width = "Data", None, 100
			if len(field_setting) > 1:
				if '.' in field_setting[1]: continue

				if field_setting[1]:
					fieldtype, options = field_setting[1], None
					if fieldtype and '/' in fieldtype:
						fieldtype, options = fieldtype.split('/')
					
				if str(field_setting[-1]).isdigit():
					width = int(field_setting[-1])
			
			column.insert(int(_key[:_charidx - 1]),
			# column.append(
				frappe._dict(label=_(field_setting[0]),
					fieldtype=fieldtype,
					fieldname=field_setting[0],
					options=options,
					width=width)
				)
	return column

def get_values_list(data):
	rows = []
	if len(data)!=0:
		for idx in range(0,len(data)):
			val = {}
			for _key in sorted(data[0].keys()):
				_charidx = _key.find('#') + 1 if _key.find('#') > 0 else 0
				field_setting = str(_key[_charidx:]).split(":")
				val[field_setting[0]] = data[idx][_key]
			rows.append(val)
	return rows