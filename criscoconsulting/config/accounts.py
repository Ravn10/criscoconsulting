from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Billing"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "report",
					"name": "Accounts Receivable SAM",
					"doctype": "Sales Invoice",
					"is_query_report": True
				},
				{
					"type": "report",
					"name": "Accounts Payable SAM",
					"doctype": "Purchase Invoice",
					"is_query_report": True
				},
				{
					"type": "doctype",
					"name": "Entry of Receipt",
					"description": _("Entry of Receipt"),
				},
				{
					"type": "doctype",
					"name": "Entry Of Payment",
					"description": _("Entry Of Payment"),
				},
				{
					"type": "doctype",
					"name": "Bank Entry",
					"description": _("Entry of Bank"),
				},
				{
					"type": "doctype",
					"name": "Cash Entry",
					"description": _("Entry Of Cash"),
				},
			]
		},
	]


