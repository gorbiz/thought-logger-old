<?php
if (! isset($_REQUEST['content']) || empty($_REQUEST['content'])) exit;
$entry = array('time' => date('Y-m-d H:i:s'), 'content' => $_REQUEST['content'], 'poster' => $_SERVER['REMOTE_ADDR']);
file_put_contents('../../../thought.log', json_encode($entry) . PHP_EOL, FILE_APPEND);