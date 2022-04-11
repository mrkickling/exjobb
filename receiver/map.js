function generateList(json) {
    result = ""
    for (var i = json.length - 1; i >= 0; i--) {
        result += "<b>" + json[i]['time'] + " </b>: " + json[i]["lat"] + ", " + json[i]["lon"] + "<br>";
    }
    return result;
}

function linesBetweenPoints(json1, json2) {
    var latlngs = [];

    var j = 0;
    for (var i = json1.length - 1; i >= 0; i--) {
        //Get latlng from first marker
        var date1 = new Date(json1[i]['time']);

        for (var j = json2.length - 1; j >= 0; j--) {
          var date2 = new Date(json2[j]['time']);
          var diff = date2 - date1;
          if (Math.abs(diff) < 20 * 1000 && json2[j]) {
              console.log(diff);
              latlngs.push([[json1[i]['lat'], json1[i]['lon']], [json2[j]['lat'], json2[j]['lon']]]);
          }

        }
    }
    //From documentation http://leafletjs.com/reference.html#polyline
    // create a red polyline from an arrays of LatLng points
    var polyline = L.polyline(latlngs, {color: 'red'}).addTo(mymap);
}

function generatePoints(json, icon) {
    for (var i = json.length - 1; i >= 0; i--) {
        L.marker([json[i]['lat'], json[i]['lon']], {icon: icon}).addTo(mymap).bindPopup(json[i]['time'] + "<br>" + json[i]['lat'] + ", " + json[i]['lon']);
    }
    mymap.panTo(new L.LatLng(json[0]['lat'], json[0]['lon']));
}

function run() {
    getRecords(record1.value, record1result, greenIcon).then(function(rec1) {
        getRecords(record2.value, record2result, redIcon).then(function(rec2) {
            linesBetweenPoints(rec1, rec2);
        });
    });
}
async function getRecords(record, textBox, icon) {
    let response = await fetch("https://joakimloxdal.se/exjobb/receiver/getrecords.php?q_session=" + record, {
        "method": "GET",
        "mode": "cors"
    });
    if (response.ok) { // if HTTP-status is 200-299
      let json = await response.json();
      console.log(json);
      textBox.innerHTML = "<h2>" + record + "</h2>" + generateList(json);
      generatePoints(json, icon);
      return json;
    } else {
      alert("HTTP-Error: " + response.status);
    }
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
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

button = document.getElementById("button");
button.addEventListener('click', run);

record1 = document.getElementById("record1");
record2 = document.getElementById("record2");

record1result = document.getElementById("left");
record2result = document.getElementById("right");


