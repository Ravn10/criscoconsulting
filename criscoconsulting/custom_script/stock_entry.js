//cur_frm.set_value("transit_warehouse","Transit - SAM")

cur_frm.add_fetch("sales_order", "customer", "customer")
cur_frm.add_fetch("sales_order", "customer_name", "cname")
cur_frm.add_fetch("sales_order", "customer_name_in_arabic", "customer_name_in_arabic")
// cur_frm.add_fetch("customer", "customer_name", "cn")
cur_frm.add_fetch("sales_order", "project", "project")

//To Set Naming Series

frappe.ui.form.on("Stock Entry", {
	purpose: function (frm) {
		naming_series(frm);
	},

	cost_center: function (frm) {
		naming_series(frm);
	},

	validate: function (frm) {

		//To set warehouse and  Cost Center 
		for (var i = 0; i < cur_frm.doc.items.length; i++) {
			cur_frm.doc.items[i].cost_center = cur_frm.doc.cost_center;
		}
		


		// To set account
		if (cur_frm.doc.purpose == "Material Issue") {
			for (var i = 0; i < cur_frm.doc.items.length; i++) {
				cur_frm.doc.items[i].expense_account = "140041 - Internal Consumption الاستهلاك الداخلي - SAM";
			}
			// cur_frm.refresh_field('items');
		}

		//To set stock difference account in stock entry 
		// if (cur_frm.doc.purpose == "Material Issue") {
		// 	for (var i = 0; i < cur_frm.doc.items.length; i++) {
		// 		cur_frm.doc.items[i].expense_account = "140041 - Internal Consumption - SAM";
		// 		cur_frm.doc.item[i].cost_center = cur_frm.doc.cost_center;
		// 	}
		// }

		cur_frm.refresh_field('items');
	}
});

function naming_series(frm) {
	// console.log("welcome")
	switch (cur_frm.doc.cost_center) {
		case 'Al-Khobar - SAM':
			if (cur_frm.doc.purpose == "Material Transfer") {
				cur_frm.set_value("naming_series", "AWIP-3-")
			}
			else if (cur_frm.doc.purpose == "Material Issue") {
				cur_frm.set_value("naming_series", "AISU-3-");
			}
			else
			{
				cur_frm.set_value("naming_series", "stock_entry_series.");
			}
			break;
		case 'Riyadh - SAM':
			if (cur_frm.doc.purpose == "Material Transfer") {
				cur_frm.set_value("naming_series", "RWIP-1-");
			}
			else if (cur_frm.doc.purpose == "Material Issue") {
				cur_frm.set_value("naming_series", "RISU-1-");
			}
			else
			{
				cur_frm.set_value("naming_series", "stock_entry_series.");
			}
			break;
		case 'Jeddah - SAM':
			if (cur_frm.doc.purpose == "Material Transfer") {
				cur_frm.set_value("naming_series", "JWIP-2-");
			}
			else if (frm.doc.purpose == "Material Issue") {
				cur_frm.set_value("naming_series", "JISU-2-");
			}
			else
			{
				cur_frm.set_value("naming_series", "stock_entry_series.");
			}
			break;
		default:
			cur_frm.set_value("naming_series", "stock_entry_series.");
	}
}



