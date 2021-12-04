// Copyright (c) 2016, DPI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Costing"] = {
	"filters": [

		{
			"fieldname":"voucher_type",
			"label": __("Trans type"),
			"fieldtype": "Link",
			"options": "DocType"
						
		},
		{
			"fieldname":"voucher_no",
			"label": __("Trans ref No"),
			"fieldtype": "Dynamic Link",
			"options": "voucher_type"
						
		}
		// {
		// 	"fieldname":"posting_date",
		// 	"label": __("Posting Date"),
		// 	"fieldtype": "Date"
			
		// },


	]
}
