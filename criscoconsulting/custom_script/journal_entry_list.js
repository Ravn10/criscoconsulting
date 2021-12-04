frappe.listview_settings['Journal Entry'] = {
	onload:function(listview){
        frappe.route_options = {"voucher_type": ["=", "Journal Entry"]};
        frappe.route_options = {"voucher_type": ["not in", "Cash Entry,Bank Entry"]};
        $('[data-fieldname="voucher_type"] option[value="Cash Entry"]').hide()
        $('[data-fieldname="voucher_type"] option[value="Bank Entry"]').hide()
        // frappe.route_options = {
		// 	"voucher_type": "Journal Entry"
        // };
        // listview.page.add_menu_item(__("Set as Open"), function() {
		// 	listview.call_for_selected_items(method, {"status": "Open"});
		// });
        // // frappe.throw("hi")
        // $('[data-fieldname="voucher_type"] option[value="Cash Entry"]').hide()
        // $('[data-fieldname="voucher_type"] option[value="Bank Entry"]').hide()
        // console.log(listview)
        // $(".list-count").on("DOMSubtreeModified",()=>{
        //     // console.log("in")
        //     $("button:contains('Amend')").show()
        //     $("li:contains('Delete')").hide()
        //     $("li:contains('Cancel')").hide()
        // })
    },
    refresh:function(){
        // frappe.route_options = {"voucher_type": ["=", "Journal Entry"]};
        // frappe.route_options = {"voucher_type": ["not in", "Cash Entry,Bank Entry"]};
        $('[data-fieldname="voucher_type"] option[value="Cash Entry"]').hide()
        $('[data-fieldname="voucher_type"] option[value="Bank Entry"]').hide()
    }
};
