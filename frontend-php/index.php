<?php
require_once 'thought-logger/credentials.php';
?><html>
<head>
	<title>Kalle's thought-logger</title>
</head>

<body>
	<form action="<?php echo THOUGHT_LOGGER_SERVER_URL; ?>" method="post">
		<input name="content" id="content" type="text" style="width:100%; font-size: 2em;" x-webkit-speech="x-webkit-speech" /><br />
		<input type="submit" style="font-size:5em;" />
		<input type="reset" style="font-size:5em;" />
	</form>
</body>

</html>
