frappe.ui.form.on("Sales Order","refresh", function(){
			for (var i =0; i < cur_frm.doc.items.length; i++){
					cur_frm.doc.items[i].cost_center = cur_frm.doc.cost_center
					cur_frm.doc.items[i].delivery_warehouse=cur_frm.doc.warehouse;
					cur_frm.doc.items[i].warehouse = cur_frm.doc.from_warehouse;
					}
						cur_frm.refresh_field('items')


						
});

frappe.ui.form.on("Sales Order", "refresh", function(frm) {
	cur_frm.fields_dict['to_warehouse'].get_query = function(doc) {
	return {
		filters: [[
			'Warehouse', 'is_wip', '=', "1"
		]]
	
	}
	};
	
	});
	
	frappe.ui.form.on("Sales Order", "refresh", function(frm) {
	cur_frm.fields_dict['from_warehouse'].get_query = function(doc) {
	return {
		filters: [[
			'Warehouse', 'is_group', '=', "0"
		],[
			'Warehouse', 'is_wip', '=', "0"
		]]
	
	}
	};
	
	});


frappe.ui.form.on("Sales Order",{refresh:function(frm) {cur_frm.fields_dict['items'].grid.get_field('warehouse').get_query = function(doc) {
        return {
            filters: [[
                'Warehouse', 'is_group', '=', "0"
            ]]
		//filters: {
		//	"divison": doc.item_group_allowed,
		//	"company":doc.company
		//}
        }
	};
},
	delivery_warehouse:function(){
		if(cur_frm.doc.delivery_warehouse){
			for(var i=0;i<cur_frm.doc.items.length;i++){
			var ware = cur_frm.doc.delivery_warehouse;
			cur_frm.doc.items[i].warehouse = ware;
		}
		}
	}
});

frappe.ui.form.on("Sales Order Item",{
	items_add:function(frm,dt,dn){
		var ware = cur_frm.doc.delivery_warehouse;
		var row = locals[dt][dn];
		row.warehouse = ware;
		refresh_field("warehouse");
	}
	});


// Added Custom Script From Front End -by Pranali





frappe.ui.form.on("Sales Order", "refresh", function(frm) {cur_frm.fields_dict['items'].grid.get_field('warehouse').get_query = function(doc) {
return {
	filters: [[
		'Warehouse', 'is_group', '=', "0"
	]]
//filters: {
//	"divison": doc.item_group_allowed,
//	"company":doc.company
//}
}
};
});

frappe.ui.form.on('Sales Order', {
refresh: function(frm) {
frm.add_custom_button(__('Make WIP Delivery'), function() {
	frappe.model.with_doctype('Stock Entry', function() {
		var mr = frappe.model.get_new_doc('Stock Entry');
		var items = frm.get_field('items').grid.get_selected_children();
		if(!items.length) {
			items = frm.doc.items;
		}
		items.forEach(function(item) {
			var mr_item = frappe.model.add_child(mr, 'items');
			mr_item.item_code = item.item_code;
			mr_item.item_name = item.item_name;
			mr_item.uom = item.uom;
			mr_item.stock_uom = item.stock_uom;
			mr_item.transfer_qty = item.stock_qty;
			mr_item.conversion_factor = item.conversion_factor;
			mr_item.item_group = item.item_group;
			mr_item.description = item.description;
			mr_item.image = item.image;
			mr_item.qty = item.qty;
			mr_item.cost_center = item.cost_center;

			//mr_item.s_warehouse = "Hi";
			mr.purpose ="Material Transfer"
			console.log(mr_item.warehouse)
			console.log(item.s_warehouse)
			//mr_item.warehouse = item.s_warehouse;
		//	mr_item.t_warehouse = "in mr item";
			mr_item.required_date = frappe.datetime.nowdate();
		});
		var stock_entry = frm.get_field('stock_entry');
		mr.stock_entry = frm.doc.stock_entry;
		var cost_center = frm.get_field('cost_center');
		mr.cost_center = frm.doc.cost_center;
		frappe.set_route('Form', 'Stock Entry', mr.name);
		//mr.from_warehouse="hi";
		var to_warehouse = frm.get_field('to_warehouse');
		mr.to_warehouse=frm.doc.to_warehouse;
		var from_warehouse = frm.get_field('from_warehouse');
		mr.from_warehouse=frm.doc.from_warehouse;
		var customer = frm.get_field('customer');
		mr.customer=frm.doc.customer;
						mr.sales_order = frm.doc.name;

	//  mr.naming_series="WIP-"
	});
});}});



frappe.ui.form.on("Sales Order","validate",function(){
	for (var i =0; i < cur_frm.doc.taxes.length; i++){
			console.log("in taxes")
			cur_frm.doc.taxes[i].cost_center = cur_frm.doc.cost_center;
			}
				cur_frm.refresh_field('taxes')
});

// End ---------------------------------------------------------------------------------

