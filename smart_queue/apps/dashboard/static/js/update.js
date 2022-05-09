// Check queue
setInterval( function() {
    console.log("Queue fetch");

    $.ajax({
        url:location.href,
        type:'GET',
        success: function(data) {
            console.log("Loading");
            var tmp = $('<div>').append(data).find('#queue-content').attr("id", "queue-tmp");
            
            $(tmp).appendTo('div#queue');

            $('div#queue-content').remove();
            $('div#queue-tmp').attr("id", "queue-content");
        }
    });

}, 30000); // each 30 sec

// Check patient
setInterval( function() {
    if(document.getElementById("no-patient-content") !== null)
    {   
        $('div#no-patient-content').empty();
        $('div#no-patient-content').load(location.href + " #patient-content");
        $('div#no-patient-content').attr("id", "patient-content")    
    }
}, 30000); // each 30 sec


