// frappe.ui.form.on('Journal Entry', {
//     refresh: function(frm){
//         cur_frm.trigger('common');
//         cur_frm.trigger('cost_ce');
//     },
//     voucher_type: function(frm){
//         cur_frm.trigger('common');
//         cur_frm.trigger('cost_ce');
//     },
//     common:function(frm){
//         if(cur_frm.doc.accounts.length > 0){
//             for(var i = 0; i<cur_frm.doc.accounts.length; i++){
//                     cur_frm.doc.accounts[i].narration = "JVENTRY"
//             }
//         }
//     },
//     cost_ce:function(frm){
//         if(["Journal Entry","Opening Entry"].includes(cur_frm.doc.voucher_type)){
//             cur_frm.set_value("cost_center","Al-Khobar - SAM")
//         }else{
//             cur_frm.set_value("cost_center",undefined)
//         }
//     },
//     cost_center: function(frm){
//         if (cur_frm.doc.accounts){
//             $.each(cur_frm.doc.accounts, function(i,v){
//                 frappe.model.set_value(v.doctype,v.name,"cost_center",cur_frm.doc.cost_center)
//             })
//         }
//     }
// });

frappe.ui.form.on('Journal Entry', {
    validate: function(frm){
        for (var i = 0; i < cur_frm.doc.accounts.length; i++) {
			cur_frm.doc.accounts[i].cost_center = cur_frm.doc.cost_center;
        }
        cur_frm.refresh_field('accounts');
        

        if (cur_frm.doc.total_debit == cur_frm.doc.total_credit)
        {
            cur_frm.set_value("total_amount",cur_frm.doc.total_debit)
            cur_frm.refresh_field("total_amount")
        }
        else
        {
            cur_frm.set_value("total_amount",undefined)
            cur_frm.refresh_field("total_amount")
        }
        
    },
    // fill narration in child table as per header field of narration - by suvarna
    narration:function(frm)
    {
        if(cur_frm.doc.narration){
            $.each(cur_frm.doc.accounts, function (i, v) {
                frappe.model.set_value(v.doctype, v.name, "narration", cur_frm.doc.narration)
            });
        }
        else{
            $.each(cur_frm.doc.accounts, function (i, v) {
                frappe.model.set_value(v.doctype, v.name, "narration", undefined)
            });
        }
    }
});

// fill narration in child table as per header field of narration - by suvarna
frappe.ui.form.on('Journal Entry Account', {
    accounts_add:function(frm,cdt,cdn){
        var child_tab = locals[cdt][cdn]
        if(cur_frm.doc.narration)
        {
            frappe.model.set_value(child_tab.doctype, child_tab.name, "narration", cur_frm.doc.narration)

        }
        else{
            frappe.model.set_value(child_tab.doctype, child_tab.name, "narration", undefined)

        }
        
    }
});



// Hide or Show Cancel/Amend Button --By pranali
frappe.ui.form.on("Journal Entry", "refresh", function(frm, cdt, cdn) {
    $('[data-fieldname="voucher_type"] option[value="Cash Entry"]').hide()
    $('[data-fieldname="voucher_type"] option[value="Bank Entry"]').hide()
    if(cur_frm.doc.reference_of_bank_entry || cur_frm.doc.reference_cash_entry){
        $($("span:contains('Cancel')").parent("button")).css("display","none")
        $("a:contains('Delete')").css("display","none")
        $($("span:contains('Amend')").parent("button")).css("display","none")
    }
    else{
        $($("span:contains('Cancel')").parent("button")).css("display","")
        $($("span:contains('Amend')").parent("button")).css("display","")
        $("a:contains('Delete')").css("display","")
    }

    if(cur_frm.doc.__islocal==1)
    {
        for (var i = 0; i < cur_frm.doc.accounts.length; i++) {
			cur_frm.doc.accounts[i].narration = cur_frm.doc.narration;
        }
        cur_frm.refresh_fields()
    }

});

//  End -------------------------------------------------


//  Update Clearance_date in Bank Entry

// frappe.ui.form.on("Bank Entry", "validate", function(frm, cdt, cdn) {
//    if(cur_frm.doc.clearance_date && cur_frm.doc.reference_of_bank_entry){
//   frappe.call({
//       "method":"criscoconsulting.criscoconsulting.doctype.bank_entry.bank_entry.update_clearance_date",
//       "args":{
//             "clearance_date":cur_frm.doc.clearance_date,
//             "reference_of_bank_entry": cur_frm.doc.reference_of_bank_entry
//       },
//       callback: function(r){
//           console.log("updated clearance Date.")
//       }
//   })
//    }
// });

// End --------------------------------