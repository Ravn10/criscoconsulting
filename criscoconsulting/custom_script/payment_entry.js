frappe.ui.form.on("Payment Entry", "refresh", function(frm, cdt, cdn) {

    if(cur_frm.doc.entry_of_receipt){
        $($("span:contains('Cancel')").parent("button")).css("display","none")
        $("a:contains('Delete')").css("display","none")
        $($("span:contains('Amend')").parent("button")).css("display","none")


    }
    else{
        $($("span:contains('Cancel')").parent("button")).css("display","")
        $($("span:contains('Amend')").parent("button")).css("display","")
        $("a:contains('Delete')").css("display","")


    }
});


// Added Custom Script From Front End -by Pranali

function namingseries(frm)
{
    
    if(frm.doc.cost_center && frm.doc.type){

        if(frm.doc.ho){
            if(frm.doc.type=="Cash"  && frm.doc.ho==1){
                console.log("Cash")
                frm.set_value("naming_series","HCPV-2-");
            }
            else if(frm.doc.type=="Bank" && frm.doc.ho==1){
                frm.set_value("naming_series","HBPV-2-");
            }
        }
        else{
           
            switch(frm.doc.cost_center) {
                case 'Al-Khobar - SAM':
                if(frm.doc.type=="Cash"){
                    
                    frm.set_value("naming_series","ACPV-3-");
                }
                else if(frm.doc.type=="Bank"){
                    frm.set_value("naming_series","ABPV-3-");
                }
                break;
                case 'Riyadh - SAM':
                if(frm.doc.type=="Cash"){
                    frm.set_value("naming_series","RCPV-1-");
                }
                else if(frm.doc.type=="Bank"){
                    frm.set_value("naming_series","RBPV-1-");
                } 

                break;
                case 'Jeddah - SAM':
                if(frm.doc.type=="Cash"){
                    frm.set_value("naming_series","JCPV-2-");
                }
                else if(frm.doc.type=="Bank"){
                    frm.set_value("naming_series","JBPV-2-");
                }
                break;
            }
        }


    }    
}




frappe.ui.form.on("Payment Entry", {
    mode_of_payment: function(frm) {
        namingseries(frm);
    },
    cost_center: function(frm) {
        namingseries(frm);
    },
    ho: function(frm) {
        namingseries(frm);
    },
});


//cur_frm.set_value("test_user_",frappe.session.user)

//cur_frm.cscript.onload_post_render = function(frm,dt,dn){

//if(doc.test_user == 'ahmed'){
//}else {
//cur_frm.set_value("payment_type","Receive")
//}else if(doc.company == 'Company 3'){
//cur_frm.set_value("naming_series","COM3SO")
//}

//}

//End -----------------------------------------------------------------------------------