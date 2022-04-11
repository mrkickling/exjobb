<?php
	require "passwords.php";
	function addRecord($conn, $session, $lat, $lon, $data) {
		if ($stmt = $conn->prepare("INSERT INTO requestcatcher(session, lat, lon, data) VALUES(?, ?, ?, ?);")) {
			$stmt->bind_param("ssss", $session, $lat, $lon, $data);
			$stmt->execute();
			$stmt->close();
		} else {
			echo $conn->error;
		}
	}

	function generatePoints($positions, $icon) {
		foreach ($positions as $id => $pos) {
			echo "L.marker([" . $pos['lat'] . "," . $pos['lon'] . "], {icon: ". $icon ."}).addTo(mymap).bindPopup('" . $pos['time'] ."'); \n";

		}
	}

	function getAllSessions($conn) {
		$sessions = [];
		if ($stmt = $conn->prepare("SELECT DISTINCT session FROM requestcatcher")) {
			$stmt->execute();
			$result = $stmt->get_result();
			while ($data = $result->fetch_assoc()) {
				$sessions[] = $data;
			}
			$stmt->close();
			return $sessions;
		} else {
			echo $conn->error;
		}
	}

	function getAllRequests($conn, $session) {
		$requests = [];
		if ($stmt = $conn->prepare("SELECT * FROM requestcatcher WHERE session = ? ORDER BY time DESC")) {
			$stmt->bind_param("s", $session);
			$stmt->execute();
			$result = $stmt->get_result();
			while ($data = $result->fetch_assoc()) {
				$requests[] = $data;
			}
			$stmt->close();
			return $requests;
			$stmt->close();
		} else {
			echo $conn->error;
		}
	}

	$c = new mysqli("joakimloxdal.se.mysql", "joakimloxdal_se", $sql_pass, 'joakimloxdal_se');
	if ($c->connect_errno) {
	    printf("Connect failed: %s\n", $mysqli->connect_error);
	    exit();
	}

	$session = $_POST['session'];
	$key = $_POST['key'];
	$lat = $_POST['lat'];
	$lon = $_POST['lon'];
	$data = $_POST['data'];

	if ($key == $post_pass) {
		echo "Pass correct!";
		addRecord($c, $session, $lat, $lon, $data);
	}

	$sessions = getAllSessions($c);

	$q_session1 = $_GET['q_session1'];
	$q_session2 = $_GET['q_session2'];

?>
<html>
	<head>
		<link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css"
		  integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
		  crossorigin=""/>

		<script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"
	    integrity="sha512-gZwIG9x3wUXg2hdXF6+rVkLF/0Vi9U8D2Ntg4Ga5I5BZpVkVxlJWbSQtXPSiUTtC0TjtGOmxa1AJPuV0CPthew=="
	    crossorigin=""></script>
	    <link rel="stylesheet" href="style.css?lol">  

	</head>
	<body>
		<h2>Request catcher 1.0 - exjobb</h2>
		<form method="get">
			Trace 1:
			<select name = "q_session1">
			<?php
				foreach ($sessions as $key => $request):
			?>
				<option value="<?php echo $request["session"]; ?>"><?php echo $request["session"]; ?></option>
			<?php
				endforeach;
			?>
			</select><br>
			Trace 2:
			<select name = "q_session2">
			<?php
				foreach ($sessions as $key => $request):
			?>
				<option value="<?php echo $request["session"]; ?>"><?php echo $request["session"]; ?></option>
			<?php
				endforeach;
			?>
			</select><br>

			<input type="submit">
		</form>

		<div id="left">
			Left
		</div>
		<div id="main-map"></div>
		<div id="right">
			Right
		</div>

<script type="text/javascript">
	var mymap = L.map('main-map').setView([56, 17], 13);

	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/streets-v11',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(mymap);
	var redIcon = new L.Icon({
	  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
	  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	  iconSize: [25, 41],
	  iconAnchor: [12, 41],
	  popupAnchor: [1, -34],
	  shadowSize: [41, 41]
	});
	var greenIcon = new L.Icon({
	  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
	  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
	  iconSize: [25, 41],
	  iconAnchor: [12, 41],
	  popupAnchor: [1, -34],
	  shadowSize: [41, 41]
	});

<?php
if (strlen($q_session1)) {
	generatePoints(getAllRequests($c, $q_session1), "greenIcon"); 
}
if (strlen($q_session2)) {
	generatePoints(getAllRequests($c, $q_session2), "redIcon"); 
}
?>
</script>

	</body>

</html>




