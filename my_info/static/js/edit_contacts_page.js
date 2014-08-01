jQuery(function ($) {
    var $photo_field = $('#id_photo');


    $photo_field.change(function() {

        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#img_prev').attr('src', e.target.result);
            }

            reader.readAsDataURL(this.files[0]);
        }
    });


});