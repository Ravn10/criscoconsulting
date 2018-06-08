
frappe.ui.form.on("Delivery Note", {
  cost_center: function(){
			for (var i =0; i < cur_frm.doc.items.length; i++){
				        cur_frm.doc.items[i].cost_center = cur_frm.doc.cost_center;
					
					}
					console.log("test");
						cur_frm.refresh_field('items')
				
}});