<?php require_once 'thought-logger/credentials.php'; ?><!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Kalle's thought-logger</title>
    <link rel="apple-touch-icon" href="thought-logger-icon.png" />
    <link rel="apple-touch-icon-precomposed" href="thought-logger-icon.png" />

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        $(document).ready(function() {

            function hideAddressBar(){
                if (document.documentElement.scrollHeight<window.outerHeight/window.devicePixelRatio)
                    document.documentElement.style.height=(window.outerHeight/window.devicePixelRatio)+'px';
                setTimeout(function() { window.scrollTo(1,1) } ,0);
            }
            window.addEventListener("load",function(){hideAddressBar();});
            window.addEventListener("orientationchange",function(){hideAddressBar();});

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
