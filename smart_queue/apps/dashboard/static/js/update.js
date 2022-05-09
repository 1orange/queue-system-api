// Check queue
setInterval( function() {
    $('div#queue').empty();
    $('div#queue').load(location.href + " #queue");
}, 30000); // each 30 sec

// Check patient
setInterval( function() {
    $('div#patient').empty();
    $('div#patient').load(location.href + " #patient");
}, 30000); // each 30 sec


