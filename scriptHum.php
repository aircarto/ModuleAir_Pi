<?php

shell_exec('python ' . "/var/www/html/CNRS/Write_data_BME280.py" ); 
$pythonscript = "/var/www/html/CNRS/Read_data_hum.py";


$output = shell_exec('python ' . $pythonscript );

echo $output;

?>