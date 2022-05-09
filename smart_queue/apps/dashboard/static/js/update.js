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

}, 10000); // each 30 sec

// Check patient
setInterval( function() {
    $.ajax({
        url:location.href,
        type:'GET',
        success: function(data) {
            console.log("Loading");
            var tmp = $('<div>').append(data).find('#patient-content').attr("id", "patient-tmp");
            
            $(tmp).appendTo('div#patient');

            $('div#patient-content').remove();
            $('div#patient-tmp').attr("id", "patient-content");
        }
    });
}, 10000); // each 30 sec


