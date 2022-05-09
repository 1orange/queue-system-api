// Check queue
setInterval( function() {
    if(document.getElementById("no-queue-content") !== null)
    {
        $.ajax({
            url:location.href,
            type:'GET',
            success: function(data) {
                var content = $('<div>').append(data).find('#queue-content');
                $('div#queue-tmp').html( content );

            }
        });

        // $('div#no-queue-content').empty();
        // $('div#no-queue-content').load(location.href + " #queue-content");
        // $('div#no-queue-content').attr("id", "queue-content")    
    }
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


