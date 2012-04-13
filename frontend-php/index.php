<?php
require_once 'thought-logger/credentials.php';
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
	<title>Kalle's thought-logger</title>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            $("#content").focus();

            $("#form").submit(function() {
                var data = {content: $("#content").val()};
                $.post(this.action, data, function(data) {
                    $("#content").val("");
                    $("#content").focus();
                });
                return false;
            });
        });
    </script>
</head>

<body>
	<form action="<?php echo THOUGHT_LOGGER_SERVER_URL; ?>" method="post" id="form">
		<input name="content" id="content" type="text" style="width:100%; font-size: 2em;" x-webkit-speech="x-webkit-speech" /><br />
	</form>
</body>

</html>
