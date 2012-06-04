<?php require_once 'thought-logger/credentials.php'; ?><!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
    <meta name="apple-mobile-web-app-capable" content="yes">
    <title>Kalle's thought-logger</title>
    <link rel="apple-touch-icon" href="thought-logger-icon.png" />
    <link rel="apple-touch-icon-precomposed" href="thought-logger-icon.png" />

    <style type="text/css">
        input {
            width: 100%;
            font-size: 2em;
            border: 0;
        }
    </style>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            // Hack around autocomplete="off" issue on Android
            $("#content").attr("name", "field_" + (new Date().getTime()));
            
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
	<form action="<?php echo THOUGHT_LOGGER_SERVER_URL; ?>" method="post" id="form" autocomplete="off">
		<input name="content" id="content" type="text" autocomplete="off" x-webkit-speech="x-webkit-speech" />
	</form>
</body>

</html>
