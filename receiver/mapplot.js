
function generatePoints(json, icon) {
    for (var i = json.length - 1; i >= 0; i--) {
        L.marker([json[i]['lat'], json[i]['lon']], {icon: icon}).addTo(mymap).bindPopup(json[i]['time'] + "<br>" + json[i]['lat'] + ", " + json[i]['lon']);
    }
}


function connectTheDots(data){
    var c = [];
    for(i in data) {
        var x = data[i]["lat"];
        var y = data[i]["lon"];
        c.push([x, y]);
    }
    return c;
}

function run() {
    json = displayPoints(points.value, redIcon);
    pathCoords = connectTheDots(json);
    var pathLine = L.polyline(pathCoords).addTo(mymap);
}

function displayPoints(points_text, icon) {
	json = []
    points_text = points.value;
    rows = points_text.split("\n");
    for (var i = 0; i < rows.length; i++) {
    	values = rows[i].split(",");
    	json.push({"lat": values[0], "lon": values[1]});
   	}
   	mymap.panTo(new L.LatLng(json[0]['lat'], json[0]['lon']));
    generatePoints(json, icon);
    return json;
}

mymap = L.map('main-map').setView([56, 17], 13);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

redIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [5, 10],
  iconAnchor: [3, 5],
  popupAnchor: [1, -34],
  shadowSize: [5, 5]
});

button = document.getElementById("button");
button.addEventListener('click', run);
points = document.getElementById("points");


