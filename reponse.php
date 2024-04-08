<?php include '/var/www/html/ModuleAir_Pi/global.php'; ?> 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Réponse</title>
</head>
<body>
    <div class="container">
        <h1>Réponse :</h1>
        <link rel="stylesheet" href="styles.css">
        <p>
            <script>
                function getParameterByName(name, url) {
                    if (!url) url = window.location.href;
                    name = name.replace(/[\[\]]/g, "\\$&");
                    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
                        results = regex.exec(url);
                    if (!results) return null;
                    if (!results[2]) return '';
                    return decodeURIComponent(results[2].replace(/\+/g, " "));
                }
                var reponse = getParameterByName('reponse');
               document.write("Vous avez répondu : " + reponse)
            </script>
            <p>La temperature est de <?php $pythonscript_temp = "/var/www/html/ModuleAir_Pi/Read_data_temp.py"; $output_temp = shell_exec('python ' . $pythonscript_temp ); echo $output_temp; ?> °C</p>
            <p>Le taux d'humidité est de <?php $pythonscript_hum = "/var/www/html/ModuleAir_Pi/Read_data_hum.py"; $output_hum = shell_exec('python ' . $pythonscript_hum ); echo $output_hum; ?> %</p>
            <p>La temperature est de <?php $pythonscript_press = "/var/www/html/ModuleAir_Pi/Read_data_press.py"; $output_press = shell_exec('python ' . $pythonscript_press ); echo $output_press; ?> hPa</p>
            <?php $pythonscript_PM1 = "/var/www/html/ModuleAir_Pi/Read_data_PM1.py"; $output_PM1 = shell_exec('python ' . $pythonscript_PM1 );?>
            <?php $pythonscript_PM25 = "/var/www/html/ModuleAir_Pi/Read_data_PM25.py"; $output_PM25 = shell_exec('python ' . $pythonscript_PM25 );?>
            <?php $pythonscript_PM10 = "/var/www/html/ModuleAir_Pi/Read_data_PM10.py"; $output_PM10 = shell_exec('python ' . $pythonscript_PM10 );?>
            <?php date_default_timezone_set('Europe/Paris'); $t = time(); $fullDate = date("Y-m-d H:i:s", $t); 
            $r= $_GET["reponse"]; ?>
            <?php $press = round($output_press); ?>
            <?php $myfile = fopen("/sys/class/thermal/thermal_zone0/temp", "r"); $temp_core = fread($myfile,filesize("/sys/class/thermal/thermal_zone0/temp")); fclose($myfile); $temp_core = $temp_core/1000; ?> 
            <?php $conn = pg_connect("host=172.16.13.90 dbname=cnrs user=airlab_test password=123plouf"); $query = "INSERT INTO reponses (reponse, temperature, humidity, date_reponse, pressure, device_id, temprature_core, pm1, pm25, pm10) VALUES ('$r', '$output_temp' , '$output_hum', '$fullDate','$press','".DEVICE_ID."', '$temp_core', '$output_PM1', '$output_PM25', '$output_PM10')";
            $result = pg_query($conn, $query); pg_close($conn); ?> 

            <?php require __DIR__ .'/vendor/autoload.php';
            $CNRS_endpoint = 'https://data.moduleair.fr/cnrs_biblio.php';
            $headers = [
                "Content-Type" => "application/json"];
            $data_CNRS = ["sensordatavalues" => [["mesure" => "temperature", "value" => $output_temp],["mesure" => "humidity", "value" => $output_hum],["mesure" => "pressure", "value" => $press],["mesure" => "reponse", "value" => $r],["mesure" => "date_reponse", "value" => $fullDate],["mesure" => "device", "value" => DEVICE_ID],["mesure" => "pm1", "value" => $output_PM1],["mesure" => "pm25", "value" => $output_PM25],["mesure" => "pm10", "value" => $output_PM10]],];
            $client = new \GuzzleHttp\Client();   
            $resonse_CNRS = null;
            try {
                $resonse_CNRS = $client->post($CNRS_endpoint, [
                    'headers' => $headers,
                    'json' => $data_CNRS,]);
                if ($resonse_CNRS->getStatusCode() != 200) {
                    error_log($resonse_CNRS->getStatusCode(), 0);
                        }
                if ($resonse_CNRS->getStatusCode() == 200) {
                error_log("Send CNRS ok", 0);
                    }
                } catch (\Exception $e) {
                error_log('ERROR CNRS: ' . json_encode($e->getMessage()));
                    }

            ?>     
        </p>
    </div>
</body>
</html>





          