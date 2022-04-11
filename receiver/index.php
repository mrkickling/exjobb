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

	if ($key == "regnbagshund") {
		echo "Pass correct!";
		addRecord($c, $session, $lat, $lon, $data);
	}

	$sessions = getAllSessions($c);

	$q_session = $_GET['q_session'];
	echo $q_session;

?>
<html>
	<head>
		<link rel="stylesheet" href="style.css">
	</head>
	<h2>Request catcher 1.0 - exjobb</h2>
	<form method="get">
		<select name = "q_session">
		<?php
			foreach ($sessions as $key => $request):
		?>
			<option value="<?php echo $request["session"]; ?>"><?php echo $request["session"]; ?></option>
		<?php
			endforeach;
		?>
		</select>
		<input type="submit">
	</form>

<?php 
		if (strlen($q_session)):
			$requests = getAllRequests($c, $q_session); 
?>	
			<h2>Requests:</h2>

<?php 
			foreach ($requests as $key => $request): 
?>
				<div class="record">
					<b>Time</b>: <?php echo $request['time']; ?><br>
					<b>Coordinates</b>: <?php echo $request['lat']; ?>, <?php echo $request['lon']; ?>
					<b>Data</b>: <?php echo $request['data']; ?>
				</div>
<?php
			endforeach;
		endif;
?>



</html>




