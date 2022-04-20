<?php
    header('Content-Type: application/json');
?>

<?php 	
	include "passwords.php";

	$c = new mysqli("joakimloxdal.se.mysql", "joakimloxdal_se", "Kaninen123", 'joakimloxdal_se');
	if ($c->connect_errno) {
	    printf("Connect failed: %s\n", $mysqli->connect_error);
	    exit();
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
		if ($stmt = $conn->prepare("SELECT * FROM requestcatcher WHERE session = ? ORDER BY time")) {
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
