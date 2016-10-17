<?php

$fileName = $_POST["filename"];
$content = $_POST["content"];
$file = fopen($fileName, "w");
fwrite($file, $content);
fclose($file);
?>