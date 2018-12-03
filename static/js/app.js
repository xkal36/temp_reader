function onDocumentReady() {
    var displaynumber = document.getElementById('display');
	var powerGauge = gauge('#power-gauge', {
		size: 700,
		clipWidth: 700,
		clipHeight: 500,
		ringWidth: 60,
		maxValue: 100,
		transitionMs: 4000,
    });

    d3.select("#power-gauge").attr("align","center");
        
    powerGauge.render();

    var socket = io.connect('http://' + document.domain + ':' + location.port + '/app');
    socket.on('new_result', function(msg) {
        var result = msg.result;
        powerGauge.update(result);

        var temp = result + 'ºC';
        if (result <= 10) {
            displaynumber.innerHTML = "<span style='color: blue;'>" + temp + "</span>";
        } else {
             displaynumber.innerHTML = "<span style='color: red;'>" + temp + "</span>";
        }
    });
}

if (!window.isLoaded) {
	window.addEventListener("load", function() {
        onDocumentReady();
	}, false);
} else {
	onDocumentReady();
}