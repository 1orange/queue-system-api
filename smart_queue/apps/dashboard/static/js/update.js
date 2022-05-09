// Check queue
setInterval( function() {
    $('div#queue-content').empty();
    $('div#queue').load(location.href + " #queue-content");
}, 30000); // each 30 sec

// Check patient
setInterval( function() {
    $('div#patient-content').empty();
    $('div#patient').load(location.href + " #patient-content");
}, 30000); // each 30 sec


