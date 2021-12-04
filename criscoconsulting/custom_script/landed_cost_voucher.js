
// Added Custom Script From Front End -by Pranali

//To set  Cost Center 
    frappe.ui.form.on("Landed Cost Voucher", {
        validate: function(frm) {
                for (var i =0; i < cur_frm.doc.items.length; i++){
                    cur_frm.doc.items[i].cost_center = cur_frm.doc.cost_center;
                }
                cur_frm.refresh_field('items');
        }
});

// End ----------------------------------------------