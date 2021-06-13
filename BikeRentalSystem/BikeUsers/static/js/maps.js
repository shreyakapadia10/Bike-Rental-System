function loadMapScenario() {
    var map = new Microsoft.Maps.Map(document.getElementById('myMap'), {
        /* No need to set credentials if already passed in URL */
        center: new Microsoft.Maps.Location(22.3519, 79.3627),
        zoom: 5
    });
    Microsoft.Maps.loadModule('Microsoft.Maps.AutoSuggest', function () {
        var options = {
            addressSuggestions: true,
            businessSuggestions: true,
            autoDetectLocation: true,
            placeSuggestions: true,
            maxResults: 10,
            map: map
        };
        var manager = new Microsoft.Maps.AutosuggestManager(options);
        manager.attachAutosuggest('#searchBox', '#searchBoxContainer', selectedSuggestion);
    });
    function selectedSuggestion(suggestionResult) {
        map.entities.clear();
        map.setView({ bounds: suggestionResult.bestView });
        var pushpin = new Microsoft.Maps.Pushpin(suggestionResult.location);
        map.entities.push(pushpin);
        let address = suggestionResult.formattedSuggestion;
        let lat = suggestionResult.location.latitude;
        let lng = suggestionResult.location.longitude;
        let postalCode = suggestionResult.address.postalCode;
        let countryRegion = suggestionResult.address.countryRegion;

        var temp_button_text;

        function CustomFormSubmitPost(e) {
            var el = $(e);
            temp_button_text = el.text()
            el.attr('disabled', 'disabled').text("").append('<class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>Loading...');
        };

        function CustomFormSubmitResponse(e) {
            var el = $(e);
            el.removeAttr('disabled').text(temp_button_text);
        };

        var saveform = function () {

            var form = $('#mapsform')
            form.submit(function (event) {
                event.preventDefault();
                CustomFormSubmitPost($('#mapsform button[type=submit]'));

                var formdata = form.serialize()
                $.ajax({
                    url: form.attr("action"),
                    method: form.attr("method"),
                    data: formdata,
                    success: function (json) {
                        CustomFormSubmitResponse($('#mapsform button[type=submit]'));
                        alert(json["message"]);
                        window.location.assign("/add_station")
                    },
                    error: function (xhr) {
                        CustomFormSubmitResponse($('#mapsform button[type=submit]'));
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                })

            })
        }();


        $('#id_address').val(address)

        if (postalCode != undefined) {
            $('#id_post_code').val(postalCode)
        }

        $('#id_country').val(countryRegion)
        $('#id_longitude').val(lng)
        $('#id_latitude').val(lat)

        //find all hidden inputs & ignore csrf token
        var x = $("input:hidden");
        for (let i = 0; i < x.length; i++) {
            if (x[i].name != "csrfmiddlewaretoken")
                x[i].type = "text";
            x.eq(x).attr("class", 'hidden-el')
        }

        //fade in the completed form
        $('.hidden-el').fadeIn()

    }
}