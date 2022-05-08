function remove() {
    var rowId = event.target.parentNode.parentNode.id;

    fetch('/conditions', {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"id": rowId})
    }).then((response) => {
        // If response is ok
        if (response.status == 200) {
            console.log("success");
        } else{
            console.log("fail");
        }

        location.reload();
    });

}
