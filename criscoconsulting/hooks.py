# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "criscoconsulting"
app_title = "KSATB"
app_publisher = "DPI"
app_description = "criscoconsulting"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "contact@digitalprizm.net"
app_license = "MIT"

# Includes in <head>
# ------------------
fixtures = ['Custom Field', 'Property Setter', "Custom Script","Print Format"]

# include js, css files in header of desk.html
# app_include_css = "/assets/criscoconsulting/css/criscoconsulting.css"
# app_include_js = "/assets/criscoconsulting/js/criscoconsulting.js"

# include js, css files in header of web template
# web_include_css = "/assets/criscoconsulting/css/criscoconsulting.css"
# web_include_js = "/assets/criscoconsulting/js/criscoconsulting.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}
doctype_js = {
    "Customer":["custom_script/customer.js"],
    "Delivery Note":["custom_script/delivery_note.js"],
    "Material Request":["custom_script/material_request.js"],
    "Material Transfer":["custom_script/material_transfer.js"],
    "Purchase Invoice":["custom_script/purchase_invoice.js"],
    "Purchase Order":["custom_script/purchase_order.js"],
    "Purchase Receipt":["custom_script/purchase_receipt.js"],
    "Sales Invoice":["custom_script/sales_invoice.js"],
    "Sales Order":["custom_script/sales_order.js"]
}
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "criscoconsulting.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "criscoconsulting.install.before_install"
# after_install = "criscoconsulting.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "criscoconsulting.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Material Request": {
		"validate": "criscoconsulting.custom_method.material_request_data"
		
	},
    "Material Transfer": {
        "after_insert": "criscoconsulting.custom_method.add_to_on_material_transfer",
        "validate": "criscoconsulting.custom_method.update_material_request_data"
        
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"criscoconsulting.tasks.all"
# 	],
# 	"daily": [
# 		"criscoconsulting.tasks.daily"
# 	],
# 	"hourly": [
# 		"criscoconsulting.tasks.hourly"
# 	],
# 	"weekly": [
# 		"criscoconsulting.tasks.weekly"
# 	]
# 	"monthly": [
# 		"criscoconsulting.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "criscoconsulting.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "criscoconsulting.event.get_events"
# }

