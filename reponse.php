<?php include '/var/www/html/ModuleAir_Pi/global.php'; ?> 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Réponse</title>
</head>
<body>
<div class="response-container">
        <h1>Réponse :</h1>
        <link rel="stylesheet" href="../styles.css">
        <p>
        <?php

            $reponseSexe = isset($_GET['reponseSexe']) ? $_GET['reponseSexe'] : 'Non spécifié';
            $reponseBE = isset($_GET['reponseBE']) ? $_GET['reponseBE'] : 'Non spécifié';
            $reponsesA = isset($_GET['reponseA']) ? $_GET['reponseA'] : 'Non spécifié';
            echo "Vous êtes un(e) : " . htmlspecialchars($reponseSexe) . "<br>" . "<br>";
            echo "Vous avez répondu : " . htmlspecialchars($reponseBE). "<br>" . "<br>";
            echo "Vous avez fait : " . htmlspecialchars($reponsesA); ?>

        </p>
            <p>La temperature est de <?php $pythonscript_temp = "Read_data_temp.py"; $output_temp = shell_exec('python ' . $pythonscript_temp ); echo $output_temp; // attention STRING not FLOAT ?> °C</p>
            <p>Le taux d'humidité est de <?php $pythonscript_hum = "Read_data_hum.py"; $output_hum = shell_exec('python ' . $pythonscript_hum ); echo $output_hum; // attention STRING not FLOAT?> %</p>
            <p>La temperature est de <?php $pythonscript_press = "Read_data_press.py"; $output_press = shell_exec('python ' . $pythonscript_press ); echo $output_press; ?> hPa</p>
            
            
            <?php 
            
            //GET PM data (ATTENTION output String not Float)
            $pythonscript_PM1 = "Read_data_PM1.py"; 
            $output_PM1 = shell_exec('python ' . $pythonscript_PM1 );
            $pythonscript_PM25 = "Read_data_PM25.py"; 
            $output_PM25 = shell_exec('python ' . $pythonscript_PM25 );
            $pythonscript_PM10 = "Read_data_PM10.py"; 
            $output_PM10 = shell_exec('python ' . $pythonscript_PM10 );
            
            date_default_timezone_set('Europe/Paris'); 
            $t = time(); $fullDate = date("Y-m-d H:i:s", $t); 
            $r= $_GET["reponseBE"]; $rs= $_GET["reponseSexe"]; 
            $reponsesA = isset($_GET['reponseA']) ? explode(',', $_GET['reponseA']) : []; $reponsesAC = implode(',', $reponsesA);
            $press = round($output_press); 
            $myfile = fopen("/sys/class/thermal/thermal_zone0/temp", "r"); 
            $temp_core = fread($myfile,filesize("/sys/class/thermal/thermal_zone0/temp")); 
            fclose($myfile); $temp_core = $temp_core/1000;  

            //Connexion to PSQL database to insert data locally
            $conn = pg_connect("host=localhost dbname=cnrs user=airlab_test password=123plouf"); $query = "INSERT INTO reponses (reponse, temperature, humidity, date_reponse, pressure, device_id, temprature_core, pm1, pm25, pm10, sexe, activites) VALUES ('$r', '$output_temp' , '$output_hum', '$fullDate','$press','".DEVICE_ID."', '$temp_core', '$output_PM1', '$output_PM25', '$output_PM10', '$rs','$reponsesAC')";
            $result = pg_query($conn, $query); pg_close($conn); 

            //Send data to AirCarto Server
            require __DIR__ .'/vendor/autoload.php';
            $CNRS_endpoint = 'https://data.moduleair.fr/cnrs_biblio/data_users.php';
            $headers = ['Content-Type' => 'application/json'];
            
            $data_CNRS = array(
                'device' => DEVICE_ID,
                'time' => $fullDate,
                'temp' => floatval($output_temp),
                'hum' => floatval($output_hum),
                'press' => $press,
                'pm1' => floatval($output_PM1),
                'pm25' => floatval($output_PM25),
                'pm10' => floatval($output_PM10),
                'genre' => $rs
            );
            //$data_CNRS = json_encode($data_CNRS);
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

  <div class="response-container">
    <a href="index.html" class="next-button">J'ai terminé !</a>
  </div>

    <script>
    setTimeout(function() { window.location.href = 'index.html'; }, 30000); 
    </script>


</body>
</html>





          