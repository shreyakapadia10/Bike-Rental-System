/* ----- To prevent user from selecting any past date start ---- */
$(function () {
    var dtToday = new Date();

    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();

    if (month < 10)
        month = '0' + month.toString();
    if (day < 10)
        day = '0' + day.toString();

    var maxDate = year + '-' + month + '-' + day;
    $('#floatingFromDate').attr('min', maxDate);
    $('#floatingToDate').attr('min', maxDate);
});
/* ----- To prevent user from selecting any past date end ---- */


// Loading Date Time Selection Modal on opening the page
$(window).on('load', function () {
    // Creating instance of modal
    const myModal = new bootstrap.Modal(document.getElementById('DateTimeModal'), {
        keyboard: false
    });
    myModal.show();

    $('#checkAvailabilityBtn').on('click', function () {
        var forms = document.querySelectorAll('.needs-validation')

        // Loop over them and prevent submission
        Array.prototype.slice.call(forms)
            .forEach(function (form) {
                form.addEventListener('submit', function (event) {
                    if (!form.checkValidity()) {
                        event.preventDefault();
                        event.stopPropagation();
                        form.classList.add('was-validated');
                    }
                    else {
                        myModal.hide();
                    }
                }, false)
            })
    });
});

const csrftoken = getCookie('csrftoken');

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

$('#availabilityForm').on('submit', function (e) {
    const station_id = JSON.parse(document.getElementById('station_id').textContent);
    e.preventDefault();

    /* -----Preventing user to select atleast 1 hour----- */

    from_date = $('#floatingFromDate').val();
    to_date = $('#floatingToDate').val();
    from_time = $('#floatingFromTime').val();
    to_time = $('#floatingToTime').val();

    /* Getting hours from time */
    time1 = from_time.split(":")[0];
    time2 = to_time.split(":")[0];

    /* Getting minutes from time */
    // minutes1 = from_time.split(":")[1];
    // minutes2 = to_time.split(":")[1];

    /* Getting date from time */
    date1 = from_date.split("-")[2];
    date2 = to_date.split("-")[2];

    /*if(minutes1 != 00 || minutes2 != 00){
        alert('Please Select Time in round figures!')
    }

    else*/ if(time2 - time1 < 0 & date1 == date2){
        alert('Please Select Appropriate Time!')
    }
    
    else if(date2 - date1 < 0){
        alert('Please Select Appropriate Date!') 
    }

    /* Checking if the selected time is of minimum 1 hour */
    else if (time2 - time1 < 1 && date2 - date1 < 1) {
        alert('You need to select minimum 1 hour of time!');
    }

    else {
        $.ajax({
            type: "POST",
            url: '/check_bikes/',
            data: {
                station_id: station_id,
                from_date: from_date,
                from_time: from_time,
                to_date: to_date,
                to_time: to_time,
                csrfmiddlewaretoken: csrftoken,
                dataType: "json",
            },

            success: function (data) {
                available_bikes = JSON.parse(data.bikes);
                output = ""

                if (available_bikes.length == 0) {
                    output += `<h1 class="text-center mt-2">Sorry, no bike is available between given date and time range!</h1>`;
                }
                else {
                    days = JSON.parse(data.days);
                    hours = JSON.parse(data.hours);
                    minutes = JSON.parse(data.minutes);

                    output += `<h1 class="text-center mt-2">Available Bikes</h1>`;
                    for (let i = 0; i < available_bikes.length; i++) {

                        days_price = days * available_bikes[i]['fields']['price_day'];
                        hours_price = hours * available_bikes[i]['fields']['price_hr'];
                        minutes_price = (minutes * available_bikes[i]['fields']['price_hr'])/60;

                        cost = parseFloat(days_price + hours_price + minutes_price).toFixed(2);

                        bike_details = function (i) {
                            return {
                                'id': available_bikes[i]['pk'],
                                'name': available_bikes[i]['fields']['bikename'],
                                'days': days,
                                'hours': hours,
                                'cost': parseFloat(hours * available_bikes[i]['fields']['price_hr'] + days * available_bikes[i]['fields']['price_day'] + (minutes * available_bikes[i]['fields']['price_hr'])/60).toFixed(2),
                                'from_date': from_date,
                                'from_time': from_time,
                                'to_date': to_date,
                                'to_time': to_time
                            }
                        };

                        output += `<div class="card body col-md-4 mx-2 my-2" style='width:410px'>
                            <h3 class="text-center mt2-">${available_bikes[i]['fields']['bikename']}</h3>
    
                            <img src="/media/${available_bikes[i]['fields']['bike_image']}" alt="${available_bikes[i]['fields']['bike_image']}" height="370px" width="370px">
                            
                            <h5 class="text-center">Cost: &#8377;${cost}</h5>
    
                            <div class="mb-2">
                                <big>
                                    <span style="float: left">&#8377;${available_bikes[i]['fields']['price_hr']}/hr</span>
    
                                    <span style="float: right">&#8377;${available_bikes[i]['fields']['price_day']}/day</span>
                                
                                </big>
                            </div>

                            <div class="row">
                                <a href="/bike/${available_bikes[i]['pk']}" class="btn btn-md btn-success mx-2 mb-2 col-md-5" target="_blank">View Bike Details</a>
                                
                                <button class="btn btn-md btn-warning mb-2 mx-1 col-md-6" onclick="makePaymentModal(bike_details(${i}))">Take Ride</button>
                            </div>
                        </div>`
                    }
                }

                $('#availableBikes').html(output);
            },

            failure: function (data) {
                output += `<h1 class="text-center mt-2">Sorry, an error occured!</h1>`;
                $('#availableBikes').html(output);
            }
        });
    }
});


/* Payment Modal Function Start */

function makePaymentModal(bike) {
    let id = bike["id"];
    let bikeName = bike["name"];
    let days = bike["days"];
    let hours = bike["hours"];
    let cost = bike["cost"];
    let from_date = bike["from_date"];
    let from_time = bike["from_time"];
    let to_date = bike["to_date"];
    let to_time = bike["to_time"];

    let paymentOptions = `<form id = 'paymentOptionsForm'>
        <input type = "hidden" value = "${id}" name = "bikeId" id = "bikeId">
        <input type = "hidden" value = "${cost}" name = "cost" id = "cost">
        <input type = "hidden" value = "${from_date}" name = "from_date" id = "from_date">
        <input type = "hidden" value = "${from_time}" name = "from_time" id = "from_time">
        <input type = "hidden" value = "${to_date}" name = "to_date" id = "to_date">
        <input type = "hidden" value = "${to_time}" name = "to_time" id = "to_time">
        <input type = "radio" name = "payment_mode" value="COD" checked> Cash on Delivery<br>
        <input type = "radio" name = "payment_mode" value="CRE"> Credit Card<br>
        <input type = "radio" name = "payment_mode" value="DEB"> Debit Card<br>
        <input type = "radio" name = "payment_mode" value="PAY"> PayTM</form>`;

    let output = "";

    if (hours != 0 && days != 0) {
        output += `<p>You have selected ${bikeName} from ${from_date} ${from_time} to ${to_date} ${to_time} which is ${days} day(s) and ${hours} hour(s), and it costs &#8377;${cost}.</p> ${paymentOptions}`;
    }
    else if (hours == 0) {
        output += `<p>You have selected ${bikeName} from ${from_date} ${from_time} to ${to_date} ${to_time} which is ${days} day(s), and it costs &#8377;${cost}.</p>${paymentOptions}`;
    }
    else {
        output += `<p>You have selected ${bikeName} from ${from_date} ${from_time} to ${to_date} ${to_time} which is ${hours} hour(s), and it costs &#8377;${cost}.</p>${paymentOptions}`;
    }

    $('#PaymentModalBody').html(output);

    var paymentModal = new bootstrap.Modal(document.getElementById('PaymentModal'), {
        keyboard: true
    });

    paymentModal.show();
}

/* Payment Modal Function End*/


/* Payment Process Starts  */

$('#MakePaymentBtn').on('click', function () {
    // Getting payment mode's value    
    let bikeId = $('#bikeId').val();
    let cost = $('#cost').val();
    let from_date = $('#from_date').val();
    let from_time = $('#from_time').val();
    let to_date = $('#to_date').val();
    let to_time = $('#to_time').val();
    let payment_mode = $('input[name="payment_mode"]:checked').val();

    // If payment mode is Cash On Delivery
    if (payment_mode == "COD") {
        // Sending AJAX request 
        $.ajax({
            type: "POST",
            url: '/payment/',
            data: {
                bikeId: bikeId,
                payment_mode: payment_mode,
                cost: cost,
                from_date: from_date,
                from_time: from_time,
                to_date: to_date,
                to_time: to_time,
                csrfmiddlewaretoken: csrftoken,
                dataType: "json",
            },

            success: function (data) {
                $('#PaymentModal').modal('hide');
                alert(data.message);
                location.reload();
            },
            
            failure: function (data) {
                $('#PaymentModal').modal('hide');
                alert(data.message);
            }
        });
    }
});

/* Payment Process Ends  */