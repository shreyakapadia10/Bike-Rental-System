var temp_button_text;

function CustomFormSubmitPost(e){
    var el = $(e);
    temp_button_text = el.text()
    el.attr('disabled', 'disabled').text("").append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...');
};

function CustomFormSubmitResponse(e){
    var el = $(e);
    el.removeAttr('disabled').text(temp_button_text);
};


"use strict";
var FormControls = function () {

    var userprofile = function () {

        var form = $('#profileform')
        form.submit(function(event){
            event.preventDefault();
            CustomFormSubmitPost($('#profileform button[type=submit]'));
            
            var formdata = form.serialize() 
            $.ajax({
                url: form.attr("action"),
                method: form.attr("method"),
                data: formdata,
                success: function(json){
                    CustomFormSubmitResponse($('#profileform button[type=submit]'));
                    alert(json["message"]);
                    window.location.assign("/add_station")
                },
                error: function(xhr){
                    CustomFormSubmitResponse($('#profileform button[type=submit]'));
                    console.log(xhr.status + ": " + xhr.responseText);
                }
            }) 

        })    
    };
                        

    return {
        init: function() { 
            userprofile();

        }
    };
}();