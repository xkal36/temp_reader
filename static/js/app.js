$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/app');
    var results_received = [];

    //receive details from server
    socket.on('new_result', function(msg) {
        console.log("Received result" + msg.result);
        //maintain a list of ten numbers
        if (results_received.length >= 10){
            results_received.shift();
        }            
        results_received.push(msg.result);
        results_string = '';
        for (var i = 0; i < results_received.length; i++){
            results_string = results_string + '<p>' + results_received[i].toString() + '</p>';
        }
        $('#log').html(results_string);
    });

});
