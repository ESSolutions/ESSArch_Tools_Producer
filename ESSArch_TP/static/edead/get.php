<?php
    header('Content-type: text/xml');
	$id = $_POST['id'];
	$xmlName = "example_".$id.".xml";
	$xml=file_get_contents($xmlName);
	echo $xml;
?>