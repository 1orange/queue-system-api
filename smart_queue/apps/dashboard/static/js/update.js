// Check queue
setInterval( function() {
    console.log("Queue fetch");

    $('div#queue-tmp').load(location.href + " #queue-content");
    $('div#queue-tmp').removeClass("hidden");
    $('div#queue-content').remove();
    $('div#queue-tmp').attr("id", "queue-content");

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


