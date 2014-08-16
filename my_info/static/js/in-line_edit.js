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
        },
        bindEvents:function() {
            $('div.field').on('click', myinfo.inline_edit.click_on_data_holder);
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
            }
            // focusout behavior for all except datepicker
            $row.focusout(function () {
                if ($row.find('.newValue').val() == prevContent && $row.attr('id') != 'birth_date') {
                    $row.text(prevContent);
                }
            });
            // for datepicker we'll use 'change'
            $row.change(function(){
                if ($row.attr('id') == 'birth_date' && $row.find('.newValue').val() == prevContent) {
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
                // var model_name = $('table.js-table').attr('name');
                // testapp.models_preview.send_table_update(model_name)
                myinfo.inline_edit.update_contacts()
                alert(window.myinfo.instance_id)
            }
        },
        update_contacts:function() {
            var data = {};
            $('input.newValue').each(function() {
                var field_name = $(this).closest('div').attr('id'),
                    field_new_value = $(this).val();
                data[field_name] = field_new_value

            })
        }

    };



    myinfo.inline_edit.init();





});