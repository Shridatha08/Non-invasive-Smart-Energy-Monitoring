<?php

$servername = "localhost";
$dbname = "esp_data";
$username = "admin";
$password = "pi";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT id, value1, date_stamp,time_stamp,reading_time FROM SensorData order by reading_time desc limit 40";

$result = $conn->query($sql);

while ($data = $result->fetch_assoc()){
    $sensor_data[] = $data;
}

$readings_time = array_column($sensor_data, 'reading_time');

$value1 = json_encode(array_reverse(array_column($sensor_data, 'value1')), JSON_NUMERIC_CHECK);
$reading_time = json_encode(array_reverse($readings_time), JSON_NUMERIC_CHECK);

$result->free();
$conn->close();
?>

<!DOCTYPE html>
<html>
<meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://code.highcharts.com/highcharts.js"></script>
  <style>
    body {
      min-width: 310px;
    	max-width: 1280px;
    	height: 500px;
      margin: 0 auto;
    }
    h2 {
      font-family: Arial;
      font-size: 2.5rem;
      text-align: center;
    }
  </style>
  <body>
    <h2>ESP Logger</h2>
    <div id="chart-velocity" class="container"></div>
<script>

var value1 = <?php echo $value1; ?>;
var reading_time = <?php echo $reading_time; ?>;

var chartT = new Highcharts.Chart({
  chart:{ renderTo : 'chart-velocity' },
  title: { text: 'velocity' },
  series: [{
    showInLegend: false,
    data: value1
  }],
  plotOptions: {
    line: { animation: false,
      dataLabels: { enabled: true }
    },
    series: { color: '#059e8a' }
  },
  xAxis: { 
    type: 'datetime',
    categories: reading_time
  },
  yAxis: {
    title: { text: 'velocity(m/s)' 
  },
  credits: { enabled: false }
});


</script>
</body>
</html>