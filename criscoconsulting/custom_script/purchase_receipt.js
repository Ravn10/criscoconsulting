frappe.ui.form.on("Purchase Receipt", "refresh", function(frm) {cur_frm.fields_dict['items'].grid.get_field('warehouse').get_query = function(doc) {
        return {
            filters: [[
                'Warehouse', 'is_group', '=', "0"
            ]]
		
        }
    };
});


frappe.ui.form.on("Purchase Receipt","validate", function(){
			for (var i =0; i < cur_frm.doc.items.length; i++){
					cur_frm.doc.items[i].warehouse = cur_frm.doc.warehouse;
				
					}
						cur_frm.refresh_field('items')
});
