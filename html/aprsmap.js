async function getMapUrl(id, timestampId, callsign, zoom, width, height, maptype) {
    zoom = zoom || 15;
    maptype = maptype || 'hybrid';
    width = width || 300;
    height = height || 200;
    var serviceUrl = 'http://kf6gpe.dyndns.org:8080/callsign/' + callsign;
    response = await fetch(serviceUrl);
    const json = await response.json();
    if (response.status != 200) {
	document.getElementById(id).src='brokenimage.png';
    }
    else {
	var base = 'https://maps.googleapis.com/maps/api/staticmap?';
        var pos = json.latitude + ',' + json.longitude;
	var center = "position=" + pos + '&';
        var zoom = 'zoom=' + zoom + '&';
	var size = 'size=' + width + 'x' + height + '&';
	var maptype = 'maptype=' + maptype + '&';
	var markers = 'markers=color:orange%7C' + pos + '%7C&';
	var key = 'key=API_KEY';
	var url =  base +
	    center +
	    zoom +
	    size +
	    maptype +
	    markers +
	    key;
	document.getElementById(id).src=url;
	document.getElementById(timestampId).innerHTML = new Date(json.timestamp * 1000).toLocaleDateString('en-US') + ' ' +
	    new Date(json.timestamp * 1000).toLocaleTimeString('en-US');
    }
}
