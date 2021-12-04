


frappe.ui.form.on('Material Request', {
	refresh: function(frm) {
	setTimeout(function(){ 
		if(cur_frm.doc.material_request_type=="Material Transfer") {
			$('.btn-group[data-label="Make"]').hide();

		}
	}, 1500);

	
		var me = this;
		if(frm.doc.material_request_type=="Material Transfer" && !cint(frm.doc.is_local)) {
		cur_frm.add_custom_button(__("Create IBST"),
				function() {

							console.log("in material_transfer");
							cur_frm.cscript.make_material_transfer_custom(frm.doc.warehouse);
	

				})
			};

	},
});
cur_frm.cscript.make_material_transfer_custom = function(frm) {
		console.log("in material_transfer");	//

		frappe.model.open_mapped_doc({
			method: "criscoconsulting.criscoconsulting.doctype.material_transfer.material_transfer.make_stock_entry_custom",
			frm: cur_frm
		});
		
}



// Added Custom Script From Front End -by Pranali


//To set warehouse and  Cost Center  default to branch
frappe.ui.form.on("Material Request", {
	validate: function(frm) {
  		if(cur_frm.doc.material_request_type=="Material Transfer"){
			for (var i =0; i < cur_frm.doc.items.length; i++){
			    cur_frm.doc.items[i].cost_center = cur_frm.doc.cost_center;
				cur_frm.doc.items[i].warehouse = cur_frm.doc.target_warehouse;
				cur_frm.doc.items[i].source_warehouse = cur_frm.doc.for_warehouse;
			}
			cur_frm.refresh_field('items');
		}
	},
	onload: function(frm) {
		frm.set_query("for_warehouse", function() {
			return {
				"filters": {
					"is_group": 0
				}
			};
		});
		frm.set_query("target_warehouse", function() {
			return {
				"filters": {
					"is_group": 0
				}
			};
		});
	}


});

frappe.ui.form.on("Material Request", "refresh", function(frm) {cur_frm.fields_dict['items'].grid.get_field('warehouse').get_query = function(doc) {
        return {
            filters: [[
                'Warehouse', 'is_group', '=', "0"
            ]]
		
        }
    };

});

// End ------------------------------------------------
