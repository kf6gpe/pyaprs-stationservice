async function getMapUrl(id, callsign, zoom, width, height, maptype) {
    zoom = zoom || 15;
    console.log(zoom);
    maptype = maptype || 'hybrid';
    width = width || 300;
    height = height || 200;
    var serviceUrl = 'http://kf6gpe.dyndns.org:8080/callsign/' + callsign;
    response = await fetch(serviceUrl);
    const json = await response.json();
    if (response.status != 200) {
	return 'brokenimage.png';
    }
    else {
	var base = 'https://maps.googleapis.com/maps/api/staticmap?';
        var pos = json.latitude + ',' + json.longitude;
	var center = "position=" + pos + '&';
        var zoom = 'zoom=' + zoom + '&';
	var size = 'size=' + width + 'x' + height + '&';
	var maptype = 'maptype=' + maptype + '&';
	var markers = 'markers=color:orange%7C' + pos + '%7C&';
	var key = 'key=AIzaSyD-nFWgulyfBaD2tPsta1DBWxzQ-Qb6lf0';
	var url =  base +
	    center +
	    zoom +
	    size +
	    maptype +
	    markers +
	    key;
	console.log(url);
	document.getElementById(id).src=url;
    }
}
