// Copyright (c) 2016, DPI and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Accounts Payable SAM"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			on_change: () => {
				var supplier = frappe.query_report_filters_by_name.supplier.get_value();
				frappe.db.get_value('Supplier', supplier, "tax_id", function(value) {
					frappe.query_report_filters_by_name.tax_id.set_value(value["tax_id"]);
				});
			}
		},
		{
			"fieldname":"report_date",
			"label": __("As on Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"ageing_based_on",
			"label": __("Ageing Based On"),
			"fieldtype": "Select",
			"options": 'Posting Date\nDue Date',
			"default": "Posting Date"
		},
		{
			"fieldtype": "Break",
		},
		{
			"fieldname":"range1",
			"label": __("Ageing Range 1"),
			"fieldtype": "Int",
			"default": "30",
			"reqd": 1
		},
		{
			"fieldname":"range2",
			"label": __("Ageing Range 2"),
			"fieldtype": "Int",
			"default": "60",
			"reqd": 1
		},
		{
			"fieldname":"range3",
			"label": __("Ageing Range 3"),
			"fieldtype": "Int",
			"default": "90",
			"reqd": 1
		},
		{
			"fieldname":"range4",
			"label": __("Ageing Range 4"),
			"fieldtype": "Int",
			"default": "120",
			"reqd": 1
		},
		{
			"fieldname":"range5",
			"label": __("Ageing Range 5"),
			"fieldtype": "Int",
			"default": "180",
			"reqd": 1
		},
		{
			"fieldname":"range6",
			"label": __("Ageing Range 6"),
			"fieldtype": "Int",
			"default": "270",
			"reqd": 1
		},
		{
			"fieldname":"tax_id",
			"label": __("Tax Id"),
			"fieldtype": "Data",
			"hidden": 1
		}
	],
	onload: function(report) {
		report.page.add_inner_button(__("Accounts Payable Summary SAM"), function() {
			var filters = report.get_values();
			frappe.set_route('query-report', 'Accounts Payable Summary SAM', {company: filters.company});
		});
	}
}
