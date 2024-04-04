<?php $pythonscript = "/var/www/html/CNRS/Read_data_temp.py"; $output = shell_exec('python ' . $pythonscript ); echo $output; ?>
