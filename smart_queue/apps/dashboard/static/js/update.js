// Check queue
setInterval( function() {
    $('div#queue').empty();
    $('div#queue').replaceWith(location.href + " #queue-content");
}, 30000); // each 30 sec

// Check patient
setInterval( function() {
    $('div#patient').empty();
    $('div#patient').replaceWith(location.href + " #patient-content");
}, 30000); // each 30 sec


