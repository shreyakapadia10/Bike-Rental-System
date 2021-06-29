/* -----For displaying pushpins on map start----- */
const csrftoken = getCookie('csrftoken');
const tbody = document.getElementById('tbody');
const data = JSON.parse(document.getElementById('data').textContent);
let stations = JSON.parse(data)

var pinInfobox;

function loadMapScenario() {

    var pushpinInfos = [];
    for (let i = 0; i < stations.length; i++) {
        pushpinInfos[i] = { 'lat': parseFloat(stations[i]['fields']['latitude']), 'lng': parseFloat(stations[i]['fields']['longitude']), 'title': stations[i]['fields']['name'], 'description': stations[i]['fields']['address'] + '(' + stations[i]['fields']['post_code'] + ')', 'icon': 'https://icons.iconarchive.com/icons/icons-land/vista-map-markers/32/Map-Marker-Marker-Outside-Pink-icon.png' };
    }

    var infoboxLayer = new Microsoft.Maps.EntityCollection();
    var pinLayer = new Microsoft.Maps.EntityCollection();
    var apiKey = "AoCKO8_fba-FuLiqndRFZjJCyLW6_xi7ABuWX_PJFzffKtBFStyV5kPFPTWK-ADu";
    var map = new Microsoft.Maps.Map(document.getElementById("myMap"), { credentials: apiKey });

    // Create the info box for the pushpin
    pinInfobox = new Microsoft.Maps.Infobox(new Microsoft.Maps.Location(22.3519, 79.3627), { visible: false });
    infoboxLayer.push(pinInfobox);
    var locs = [];
    for (var i = 0; i < pushpinInfos.length; i++) {
        locs[i] = new Microsoft.Maps.Location(pushpinInfos[i].lat, pushpinInfos[i].lng);
        var pin = new Microsoft.Maps.Pushpin(locs[i], { icon: pushpinInfos[i].icon, width: '30px', height: '30px' });
        pin.Title = pushpinInfos[i].title;
        pin.Description = pushpinInfos[i].description;
        pinLayer.push(pin);
        Microsoft.Maps.Events.addHandler(pin, 'click', displayInfobox);
    }
    map.entities.push(pinLayer);
    map.entities.push(infoboxLayer);
    var bestview = Microsoft.Maps.LocationRect.fromLocations(locs);
    map.setView({ center: bestview.center, zoom: 5 });


    /* For autosuggest feature start  */
    Microsoft.Maps.loadModule('Microsoft.Maps.AutoSuggest', function() {
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
        // map.entities.clear();
        map.setView({ bounds: suggestionResult.bestView });
        // myMap.style.display = "unset";
        // var pushpin = new Microsoft.Maps.Pushpin(suggestionResult.location);
        // map.entities.push(pushpin);
    }
    /* For autosuggest feature end  */
}

function displayInfobox(e) {
    pinInfobox.setOptions({ title: e.target.Title, description: e.target.Description, visible: true, offset: new Microsoft.Maps.Point(0, 25) });
    pinInfobox.setLocation(e.target.getLocation());
}

function hideInfobox(e) {
    pinInfobox.setOptions({ visible: false });
}

/* -----For displaying pushpins on map end----- */


/* -----For search by pincode start----- */
$(window).on('load', function() {
    // const myMap = document.getElementById('myMap');
    // myMap.style.display = "none";

    // When search by pincode gets clicked
    const pincodeSearchBtn = document.getElementById('pincodeSearch');
    pincodeSearchBtn.addEventListener('click', () => {
        document.getElementById('pinCodeForm').style.display = "flex";
        document.getElementById('searchBoxContainer').style.display = "none";
        document.getElementById('CityForm').style.display = "none";
        document.getElementById('stationTable').style.display = "none";
    });

    // When search by maps gets clicked
    const mapSearchBtn = document.getElementById('mapSearch');
    mapSearchBtn.addEventListener('click', () => {
        document.getElementById('pinCodeForm').style.display = "none";
        document.getElementById('searchBoxContainer').style.display = "unset";
        document.getElementById('CityForm').style.display = "none";
        document.getElementById('stationTable').style.display = "none";
    });

    // When search by city gets clicked
    const citySearchBtn = document.getElementById('citySearch');
    citySearchBtn.addEventListener('click', () => {
        document.getElementById('pinCodeForm').style.display = "none";
        document.getElementById('searchBoxContainer').style.display = "none";
        document.getElementById('CityForm').style.display = "block";
        document.getElementById('stationTable').style.display = "none";
    });
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/* -----Sending AJAX request to search for stations having given pincode start----- */
$('#pinCodeForm').on('submit', function(e) {
    e.preventDefault();

    $.ajax({
        type: "POST",
        url: URL,
        data: {
            is_pincode: true,
            pincodeText: $('#pincodeText').val(),
            csrfmiddlewaretoken: csrftoken,
            dataType: "json",
        },

        success: function(data) {
            output = "";
            document.getElementById('stationTable').style.display = "inline-table";
            if (data.stations == '') {
                output += '<center><h3>Unable to fetch any station details for given pincode.</h3></center>';
            } else {
                response = JSON.parse(data.stations);

                for (let i = 0; i < response.length; i++) {
                    output += `<tr scope='row'>
                    <td>${i + 1}</td>
                    <td>${response[i].fields.name}</td>
                    <td>${response[i].fields.post_code}</td>
                    <td style='max-width: 300px'>${response[i].fields.address}</td>
                    <td><a href = 'get_map/${response[i].pk}' target='_blank'>Show Directions</a></td>
                    <td><a href = 'viewbike/${response[i].pk}' target='_blank'>Show Bikes</a></td>
                    </tr>`
                }
            }
            $('#tbody').html(output); /* response message */
        },

        failure: function(data) {
            $('#tbody').html(data); /* response message */
        }
    });
});
/* -----Sending AJAX request to search for stations having given pincode end----- */

/* -----For search by pincode end----- */


/* -----For search by city start----- */

/* -----Sending AJAX request to search for stations having given pincode start----- */
const state = document.getElementById('id_state');
const city = document.getElementById('id_name');
state.addEventListener('change', getCity);
city.addEventListener('change', getStations);

/* ----This function will fetch cities associated with the selected state start---- */
function getCity() {
    $.ajax({
        type: "POST",
        url: URL1,
        data: {
            state: $('#id_state').val(),
            csrfmiddlewaretoken: csrftoken,
            dataType: "json",
        },

        success: function(data) {
            let output = "";
            response = JSON.parse(data.cities);

            output += "<option selected>---------</option>";
            for (let i = 0; i < response.length; i++) {
                let city_id = response[i].pk;
                let city = response[i].fields.name;
                output += `<option value='${city_id}'>${city}</option>`;
            }
            $('#id_name').html(output);
        }
    });
}
/* ----This function will fetch cities associated with the selected state end---- */



/* ----This function will fetch cities associated with the selected city start---- */
function getStations() {
    $.ajax({
        type: "POST",
        url: URL,
        data: {
            is_city: true,
            city: $('#id_name').val(),
            csrfmiddlewaretoken: csrftoken,
            dataType: "json",
        },

        success: function(data) {
            output = "";
            document.getElementById('stationTable').style.display = "inline-table";
            if (data.stations == '') {
                output += '<center><h3>Unable to fetch any station details for selected city.</h3></center>';
            } else {
                response = JSON.parse(data.stations);

                for (let i = 0; i < response.length; i++) {
                    output += `<tr scope='row'>
                    <td>${i + 1}</td>
                    <td>${response[i].fields.name}</td>
                    <td>${response[i].fields.post_code}</td>
                    <td style='max-width: 300px'>${response[i].fields.address}</td>
                    <td><a href = 'get_map/${response[i].pk}' target='_blank'>Show Directions</a></td>
                    <td><a href = 'viewbike/${response[i].pk}' target='_blank'>Show Bikes</a></td>
                    </tr>`
                }
            }
            $('#tbody').html(output); /* response message */
        },

        failure: function(data) {
            $('#tbody').html(data); /* response message */
        }
    })
}
/* ----This function will fetch cities associated with the selected city end---- */

/* -----Sending AJAX request to search for stations having given city end----- */

/* -----For search by city end----- */