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

                $reponseSexe = isset($_GET['reponseSexe']) ? $_GET['reponseSexe'] : 'Non_specifie';
                $r1 = isset($_GET['r1']) ? $_GET['r1'] : 'Non_specifie';
                $r2 = isset($_GET['r2']) ? $_GET['r2'] : 'Non_specifie';
                $r3 = isset($_GET['r3']) ? $_GET['r3'] : 'Non_specifie';
                $r4 = isset($_GET['r4']) ? $_GET['r4'] : 'Non_specifie';
                $r5 = isset($_GET['r5']) ? $_GET['r5'] : 'Non_specifie';
                $r6 = isset($_GET['r6']) ? $_GET['r6'] : 'Non_specifie';
                $r7 = isset($_GET['r7']) ? $_GET['r7'] : 'Non_specifie';
                $r8 = isset($_GET['r8']) ? $_GET['r8'] : 'Non_specifie';
                $r9 = isset($_GET['r9']) ? $_GET['r9'] : 'Non_specifie';
                $r10 = isset($_GET['r10']) ? $_GET['r10'] : 'Non_specifie';
                $r11 = isset($_GET['r11']) ? $_GET['r11'] : 'Non_specifie';
                $r12 = isset($_GET['r12']) ? $_GET['r12'] : 'Non_specifie';
                $r13 = isset($_GET['r13']) ? $_GET['r13'] : 'Non_specifie';
                $r14 = isset($_GET['r14']) ? $_GET['r14'] : 'Non_specifie';
                $r15 = isset($_GET['r15']) ? $_GET['r15'] : 'Non_specifie';
                $r16 = isset($_GET['r16']) ? $_GET['r16'] : 'Non_specifie';
                $r17 = isset($_GET['r17']) ? $_GET['r17'] : 'Non_specifie'; ?>

        </p>
            <p>La temperature est de <?php $pythonscript_temp = "Read_data_temp.py"; $output_temp = shell_exec('python ' . $pythonscript_temp ); echo $output_temp; // attention STRING not FLOAT ?> °C</p>
            <p>Le taux d'humidité est de <?php $pythonscript_hum = "Read_data_hum.py"; $output_hum = shell_exec('python ' . $pythonscript_hum ); echo $output_hum; // attention STRING not FLOAT?> %</p>
            
            
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
            $press = round($output_press); 
            $myfile = fopen("/sys/class/thermal/thermal_zone0/temp", "r"); 
            $temp_core = fread($myfile,filesize("/sys/class/thermal/thermal_zone0/temp")); 
            fclose($myfile); $temp_core = $temp_core/1000;  

            //Connexion to PSQL database to insert data locally
            $conn = pg_connect("host=localhost dbname=cnrs user=airlab_test password=123plouf"); $query = "INSERT INTO reponses (
                temperature, humidity, date_reponse, pressure, device_id, temprature_core, pm1, pm25, pm10, sexe,
                r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30) VALUES (
                '$output_temp', '$output_hum', '$fullDate', '$press', '".DEVICE_ID."', '$temp_core', '$output_PM1', '$output_PM25', '$output_PM10', '$reponseSexe', 
                '$r1', '$r2', '$r3', '$r4', '$r5', '$r6', '$r7', '$r8', '$r9', '$r10', '$r11', '$r12', '$r13', '$r14', '$r15', '$r16', '$r17', '$r18', '$r19', '$r20', '$r21', '$r22', '$r23', '$r24', '$r25', '$r26', '$r27', '$r28', '$r29', '$r30'
            )"; 
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
                'genre' => $reponseSexe,
                'r1' => $r1,
                'r2' => $r2,
                'r3' => $r3,
                'r4' => $r4,
                'r5' => $r5,
                'r6' => $r6,
                'r7' => $r7,
                'r8' => $r8,
                'r9' => $r9,
                'r10' => $r10,
                'r11' => $r11,
                'r12' => $r12,
                'r13' => $r13,
                'r14' => $r14,
                'r15' => $r15,
                'r16' => $r16,
                'r17' => $r17
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





          