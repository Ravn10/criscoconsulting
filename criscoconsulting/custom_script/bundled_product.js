// Added Custom Script From Front End -by Pranali


// calculate sales incentive
frappe.ui.form.on("Bundled Product", { 
    refresh: function(frm) {       
  // calculate incentives for each person on the deal 
        amount = 0        
	 $.each(frm.doc.bundled_product, function(i, d) {  
            // calculate incentive
             var a = 0;
             d.a = flt(frm.doc.rate) *flt(frm.doc.qty);
         });
          frm.doc.amount = a ;
     } 
    });   

    // End -------------------