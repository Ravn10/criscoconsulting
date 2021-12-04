// Copyright (c) 2016, DPI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase VAT"] = {
	"filters": [

		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
	  "default":frappe.datetime.get_today(),
			"reqd": 1,
			"width": "50px"
	 },
 {
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
	  "default":frappe.datetime.get_today(),
			"reqd": 1,
			"width": "50px"
	 },
	 
	 {
		"fieldname":"voucher_number",
		"label": __("Voucher Number"),
		"fieldtype": "Data",
		  "default":"",
		"reqd": 0,
		"width": "50px"
	 },
	 
	 {
		"fieldname":"supplier_name",
		"label": __("Supplier Name"),
		"fieldtype": "Link",
		"options": "Supplier",
		"reqd": 0,
		"width": "50px"
	 },
	 {
		"fieldname":"cost_center",
		"label": __("Cost Center"),
		"fieldtype": "Link",
		"options": "Cost Center",
		"width": "50px",
		"get_query": function(){
				var company = frappe.query_report.get_filter_value('company')
				return{
				"doctype": "Cost Center",
				"filters":{
				"is_group":0,
				}
				}
				}
	 },
	 
	 {
		"fieldname":"voucher_type",
		"label": __("Voucher Type"),
		"fieldtype": "Select",
		"options": ' \nPurchase Invoice\nJournal Entry',
		  "default":" ",
		"reqd": 0,
		"width": "50px"
 	}

	]
}
