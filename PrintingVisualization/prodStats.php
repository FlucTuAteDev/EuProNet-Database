<?php
session_start();
if (!isset($_SESSION["oldNumRows"])) {
    $_SESSION["oldNumRows"] = -2;
}

$servername = "localhost";
// $servername = "87.97.16.95";
$username = "php";
$password = "1234";
$database = "EUPRONET";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
// echo "Connected successfully";  
$numRowsSQL = "SELECT COUNT(id) FROM `queries` ";
$result = $conn->query($numRowsSQL);
$row = $result->fetch_row();
// die($_SESSION["oldNumRows"] );
if ($row[0] == $_SESSION["oldNumRows"] && $_GET["force"] == 0) {
    // var_dump(http_response_code(100));
    exit();
}


$_SESSION["oldNumRows"] = $row[0];

$prodStatsSQL =
    "SELECT name as color, IFNULL(started,0) - IFNULL(discarded,0) - IFNULL(finished,0) as inProgress, IFNULL(finished,0) as finished  
    FROM ((SELECT colors.name, colors.id FROM colors) as c
    LEFT JOIN
        (SELECT color, COUNT(id)  as started
        FROM `queries` 
        WHERE state = 1
        GROUP BY color) as s 
    ON s.color = c.id
    LEFT JOIN
        (SELECT color, COUNT(id)  as discarded
        FROM `queries` 
        WHERE state = 2
        GROUP BY color) as d 
    ON d.color = c.id
    LEFT JOIN
        (SELECT color, COUNT(id)  as finished
        FROM `queries` 
        WHERE state = 3
        GROUP BY color) as f 
    ON f.color = c.id )";

$result = $conn->query($prodStatsSQL);

$response = array();
while ($row = $result->fetch_array()) {
    $response[] = array(
        "color" => $row['color'],
        "inProgress" => $row['inProgress'],
        "finished" => $row['finished']
    );
}

echo json_encode($response);

$conn->close();
