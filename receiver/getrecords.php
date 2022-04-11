<?php
	require "passwords.php";
    header('Content-Type: application/json');
?>

<?php
$c = new mysqli("joakimloxdal.se.mysql", "joakimloxdal_se", $sql_pass, 'joakimloxdal_se');
if ($c->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}

	function addRecord($conn, $session, $lat, $lon, $data) {
		if ($stmt = $conn->prepare("INSERT INTO requestcatcher(session, lat, lon, data) VALUES(?, ?, ?, ?);")) {
			$stmt->bind_param("ssss", $session, $lat, $lon, $data);
			$stmt->execute();
			$stmt->close();
		} else {
			echo $conn->error;
		}
	}

	function JSONify($positions, $icon) {
		echo "{";
		foreach ($positions as $id => $pos) {
			echo "'lat' :" . $pos['lat'] . ", \n";
			echo "'lon' :" . $pos['lon'] . ", \n";
			echo "'time' :" . $pos['time'] . ", \n";
			echo ", \n";
		}
		echo "}";
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

	$q_session = $_GET['q_session'];
	echo json_encode(getAllRequests($c, $q_session)); 

?>
