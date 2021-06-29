$(document).ready(function() {
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


    /* Toggle Switch starts */
    $('.toggle-switch-check').change(function() {
        if ($(this).is(':checked')) {
            let bike_id = $(this).attr('data-bid');
            let bike_status = $(this).is(':checked');
            let myThis= this;
            
            $.ajax({
                url: URL,
                type: 'POST',
                data: {
                    id: bike_id, 
                    bike_status: bike_status,
                    csrfmiddlewaretoken: csrftoken,
                    dataType: "json",
                },
                
                success: function(response){
                    if(response.message == 'Success'){
                        $(myThis).closest("tr").fadeOut();             
                    }
                    else{
                        alert('Something went wrong, please try again!')
                    }
                },

                failure: function(error){
                    alert('Something went wrong, please try again!')
                }
            });
        }
    });     
    /* Toggle Switch ends */
});