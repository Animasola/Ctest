jQuery(function ($) {

    var myinfo = {};
    if (this.myinfo !== undefined) {
        myinfo = this.myinfo;
    } else {
        this.myinfo = myinfo;
    }

    myinfo.edit_contacts = {
        init:function() {
            myinfo.edit_contacts.cacheElements();
            myinfo.edit_contacts.bindEvents();
        },
        cacheElements:function() {
            myinfo.edit_contacts.$photo_field = $('#id_photo');
            myinfo.edit_contacts.$img_prev = $('#img_prev');
            myinfo.edit_contacts.$edit_contacts_form = $('#editmyinfo');
            myinfo.edit_contacts.$form_elems = $('#editmyinfo').find('input, textarea, button');
            myinfo.edit_contacts.$message = $('#error_message');
        },
        bindEvents:function() {
            myinfo.edit_contacts.$photo_field.on('change', myinfo.edit_contacts.photo_preview);
            myinfo.edit_contacts.$edit_contacts_form.on('submit', myinfo.edit_contacts.contacts_form_submit);
        },

        photo_preview:function(){
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {
                    myinfo.edit_contacts.$img_prev.attr('src', e.target.result);
                }
                reader.readAsDataURL(this.files[0])
            }
        },

        contacts_form_submit:function() {
            var ajax_options = {
                type: 'post',
                dataType: 'json',
                success: myinfo.edit_contacts.submit_response_func
            };
            myinfo.edit_contacts.$message.removeClass("success alert")
            $(this).ajaxSubmit(ajax_options)
            myinfo.edit_contacts.$form_elems.prop("disabled", true)
            myinfo.edit_contacts.$message.toggleClass("warning")
            myinfo.edit_contacts.$message.text("Loading data, it may take a few moments...").fadeIn("slow");
            return false;
        },

        submit_response_func:function(data, responseText, statusText, xhr, $form) {
            var e_msg = "",
                errors = {};

            myinfo.edit_contacts.$form_elems.prop("disabled", false)
            myinfo.edit_contacts.$message.toggleClass("warning")
            $('small.error').remove()
            $('div.error').removeClass('error')
            myinfo.edit_contacts.$message.fadeOut('slow');
            if (data['result'] == 'success') {
                e_msg = "Contacts successfully updated! "
                myinfo.edit_contacts.$message.addClass("success")
            } else if (data['result'] == 'error') {
                errors = data['form_errors']
                e_msg = "Contact form contains some errors, fix it before saveing."
                myinfo.edit_contacts.$message.addClass("alert")
                for (var error in errors) {
                    myinfo.edit_contacts.$edit_contacts_form
                    .find('div[id=' + error + ']').addClass("error")
                    .after('<small class="error" >' + errors[error] + '</small>');
                }
            }
            myinfo.edit_contacts.$message.text( e_msg ).fadeIn("slow");
        }
    };

    myinfo.edit_contacts.init();

});