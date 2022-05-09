// Check queue
setInterval( function() {
    if(document.getElementById("no-queue-content") !== null)
    {
        $('div#queue-tmp').load(location.href + " #queue-content");

        $('div#queue-content').remove();
        $('div#queue-tmp').attr("id", "queue-content");
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


