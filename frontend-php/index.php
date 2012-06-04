<?php require_once 'thought-logger/credentials.php'; ?><!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Kalle's thought-logger</title>
    <link rel="apple-touch-icon" href="thought-logger-icon.png" />
    <link rel="apple-touch-icon-precomposed" href="thought-logger-icon.png" />

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        $(document).ready(function() {

            // "Hide" the browser bar on load
            if(navigator.userAgent.match(/Android/i)){
                window.scrollTo(0,1);
            }

            $("#content").focus();

            $("#form").submit(function() {
                var data = {content: $("#content").val()};
                $("#content").val("");
                $("#content").focus();
                $.post(this.action, data, function(data) {
                    // TODO Make sure that this always works.
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
