// Check queue
setInterval( function() {
    $('div#queue').load('http://localhost:5000 #queue');
}, 30000); // each 30 sec

// Check patient
setInterval( function() {
    $('div#patient').load('http://localhost:5000 #patient');
}, 30000); // each 30 sec


