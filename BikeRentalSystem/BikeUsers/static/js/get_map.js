
/* -----Functions to calculate time and distance of each stations start----- */
const data = JSON.parse(document.getElementById('data').textContent);
let station = JSON.parse(data)
const lat = station[0].fields.latitude
const lng = station[0].fields.longitude

var map;
var directionsManager;

function GetMap() {
    map = new Microsoft.Maps.Map('#myMap', {
        credentials: 'AoCKO8_fba-FuLiqndRFZjJCyLW6_xi7ABuWX_PJFzffKtBFStyV5kPFPTWK-ADu'
    });

    //Request the user's location
    // navigator.geolocation.getCurrentPosition(function (position) {
    //     var loc = new Microsoft.Maps.Location(
    //         position.coords.latitude,
    //         position.coords.longitude);

    //     //Add a pushpin at the user's location.
    //     // var pin = new Microsoft.Maps.Pushpin(loc);
    //     // map.entities.push(pin);

    //     // //Center the map on the user's location.
    //     return loc;
    // });
    map.setView({ center: navigator.geolocation.getCurrentPosition(function (position) {
        var loc = new Microsoft.Maps.Location(
            position.coords.latitude,
            position.coords.longitude);

        //Add a pushpin at the user's location.
        // var pin = new Microsoft.Maps.Pushpin(loc);
        // map.entities.push(pin);

        // //Center the map on the user's location.
        return loc;
    }), zoom: 15 });


    //Load the directions module.
    Microsoft.Maps.loadModule('Microsoft.Maps.Directions', function () {
        //Create an instance of the directions manager.
        directionsManager = new Microsoft.Maps.Directions.DirectionsManager(map);
        directionsManager.setRequestOptions({
            routeMode: Microsoft.Maps.Directions.RouteMode.driving
        });
       
        var destinationLocation = new Microsoft.Maps.Location(
            lat,
            lng);

        //Create waypoints to route between.
        var seattleWaypoint = new Microsoft.Maps.Directions.Waypoint({ location: map.getCenter() });
        directionsManager.addWaypoint(seattleWaypoint);

        var workWaypoint = new Microsoft.Maps.Directions.Waypoint({ location: destinationLocation });
        directionsManager.addWaypoint(workWaypoint);

        //Add event handlers to directions manager.
        Microsoft.Maps.Events.addHandler(directionsManager, 'directionsError', directionsError);
        Microsoft.Maps.Events.addHandler(directionsManager, 'directionsUpdated', directionsUpdated);

        //Specify the element in which the itinerary will be rendered.
        directionsManager.setRenderOptions({ itineraryContainer: '#directionsItinerary' });
        
        //Calculate directions.
        directionsManager.calculateDirections();
    });
}

function directionsUpdated(e) {
    //Get the current route index.
    var routeIdx = directionsManager.getRequestOptions().routeIndex;

    //Get the distance of the route, rounded to 2 decimal places.
    var distance = Math.round(e.routeSummary[routeIdx].distance * 100) / 100;

    //Get the distance units used to calculate the route.
    var units = directionsManager.getRequestOptions().distanceUnit;
    var distanceUnits = '';

    if (units == Microsoft.Maps.Directions.DistanceUnit.km) {
        distanceUnits = 'km'
    } else {
        //Must be in miles
        distanceUnits = 'miles'
    }

    //Time is in seconds, convert to minutes and round off.
    var time = Math.round(e.routeSummary[routeIdx].timeWithTraffic / 60);

    document.getElementById('routeInfoPanel').innerHTML = 'Distance: ' + distance + ' ' + distanceUnits + '<br/>Time with Traffic: ' + time + ' minutes';
}

function directionsError(e) {
    alert('Error: ' + e.message + '\r\nResponse Code: ' + e.responseCode)
}


/* -----Functions to calculate time and distance of each stations end----- */