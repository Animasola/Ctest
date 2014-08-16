 jQuery(function ($) {

    var myinfo = {};
    if (this.myinfo !== undefined) {
        myinfo = this.myinfo;
    } else {
        this.myinfo = myinfo;
    }

    myinfo.inline_edit = {
        init:function() {
            myinfo.inline_edit.cacheElements();
            myinfo.inline_edit.bindEvents();
        },
        cacheElements:function() {
            myinfo.inline_edit.$contacts_data = $('div.data');
            myinfo.inline_edit.$alert_box = $('div.alert-box');
            myinfo.inline_edit.$alert_text = myinfo.inline_edit.$alert_box.find('div.js-alert-text');
        },
        bindEvents:function() {
            $('div.field').on('click', myinfo.inline_edit.click_on_data_holder);
            $('a.close').on('click', myinfo.inline_edit.close_alert);
            $('body').on('keydown', myinfo.inline_edit.ctrl_enter_press);
        },
        click_on_data_holder:function() {
            var $row = $(this),
                prevContent = $row.text(),
                new_val = '<input type="text" class="newValue" value="' + prevContent + '" />';

            if ($row.children().length == 0) {
                $row.html(new_val).find('input[type=text]').focus().css('width','60%')
                myinfo.inline_edit.attach_widget($row, prevContent);
                $row.on('click', function(){return false});
                // Press Esc to restore old value
                $row.on('keydown',function(e) {
                    if (e.keyCode == 27) {
                        $row.text(prevContent);
                    }
                });
            }
            // focusout behavior for all except datepicker
            $row.focusout(function () {
                if ($row.find('.newValue').val() == prevContent && $row.attr('id') != 'birth_date' && prevContent != "") {
                    $row.text(prevContent);
                }
            });
            // for datepicker we'll use 'change'
            $row.change(function(){
                if ($row.attr('id') == 'birth_date' && $row.find('.newValue').val() == prevContent && prevContent != "") {
                    $row.text(prevContent)
                }
            })

        },
        attach_widget:function(field, prevContent) {
            // Attaching Datepicker to birth_date field
            if (field.attr('id') == 'birth_date') {
                var date_input =  field.find('input.newValue'),
                    date_parts = prevContent.match(/(\d+)/g);
                if (date_parts == null) {
                    var realDate = new Date();
                } else {
                    var realDate = new Date(date_parts[0], date_parts[1] - 1, date_parts[2]);
                }

                date_input.addClass("date-pick")
            }
            // Init datepicker
            $('.date-pick').each(function(){
                $(this).datepicker({
                    dateFormat: 'yy-mm-dd',
                    onClose: function() {
                        field.on('click', function(){return false});
                        if ($(this).val() == prevContent) {
                            field.text(prevContent);
                            // field.off('click')
                        }
                    }
                });
            });
            // setting date and showing datepicker
            var datepick = field.find('.date-pick');
            datepick.datepicker("setDate", realDate)
            datepick.val(prevContent).datepicker("show")
        },
        ctrl_enter_press:function(e){
            if (e.ctrlKey && e.keyCode == 13) {
                myinfo.inline_edit.update_contacts()
            }
        },
        update_contacts:function() {
            var data = {},
                fields = {};
            data['instance_id'] = window.myinfo.instance_id
            $('input.newValue').each(function() {
                var field_name = $(this).closest('div').attr('id');

                if ($(this).val() == '') {
                    alert("NULL!")
                    fields[field_name] = null
                } else {
                    fields[field_name] = $(this).val()
                }

                data['fields'] = JSON.stringify(fields)

            })
            $.ajax({
                type: 'POST',
                url: window.myinfo.inline_edit_url,
                dataType: 'json',
                data: data
            }).done(function(data) {
                var result = data['result'];
                if (result == 'success') {
                    myinfo.inline_edit.$alert_text.text("Contacts have been successfully updated!")
                    myinfo.inline_edit.$alert_box.removeClass('success warning alert')
                    myinfo.inline_edit.$alert_box.addClass('success')
                    myinfo.inline_edit.$alert_box.show("slow")
                } else {
                    if (result == 'empty') {
                        myinfo.inline_edit.$alert_text.text(data['msg'])
                        myinfo.inline_edit.$alert_box.removeClass('success warning alert')
                        myinfo.inline_edit.$alert_box.addClass('warning')
                        myinfo.inline_edit.$alert_box.show("slow")
                    } else {
                        if (result == 'error') {
                            myinfo.inline_edit.$alert_text.text(data['msg'])
                            myinfo.inline_edit.$alert_box.removeClass('success warning alert')
                            myinfo.inline_edit.$alert_box.addClass('alert')
                            myinfo.inline_edit.$alert_box.show("slow")
                        }
                    }
                }

                if (result != 'error') {
                    $('input.newValue').each(function(){
                        $(this).closest('div').html($(this).val())
                    })
                }

            });
        },
        close_alert:function(e) {
            e.preventDefault();
            $(this).closest('div').fadeOut('slow')
        }

    };



    myinfo.inline_edit.init();





});