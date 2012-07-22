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
        body {
            position: relative;
            height: 100%;
            background: #000;
        }
        input {
            width: 100%;
            margin-top: -20px; /* Compensate for permanent header */
            font-size: 3em;
            border: 0;
            text-align: center;
            background: #000;
            color: #119090;
            font-family: Helvetica, arial, sans-serif;
        }

        input:focus {
            outline: none;
        }
        * {
            -webkit-tap-highlight-color: rgba(0, 0, 0, 0);	
        }
    </style>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <script type="text/javascript">
        $(document).ready(function() {
            
            jQuery.fn.vertical_center = function () {
                this.css("position","absolute");
                this.css("top",
                        (($(window).height() - this.outerHeight()) / 2) + 
                        $(window).scrollTop() + "px");
                return this;
            }            

            // Hack around autocomplete="off" issue on Android
            $("#content").attr("name", "field_" + (new Date().getTime()));
            
            function hideAddressBar(){
                if (document.documentElement.scrollHeight < window.outerHeight / window.devicePixelRatio)
                    document.documentElement.style.height = (window.outerHeight / window.devicePixelRatio + 1) + 'px';
                setTimeout(function() { window.scrollTo(1, 1) } ,0);
            }
            window.addEventListener("load", function() { hideAddressBar(); });
            window.addEventListener("orientationchange", function() { hideAddressBar(); });

            // Very specific to my HTC Desire Z
            // should not cause too much damage on most devices though
            $("#content").css('height', $(window).height() - 26);
            // Vertical alignment
            $("#content").vertical_center();
            $(window).bind('resize', function() {
                $("#content").vertical_center();
            });
            
            // Keep the focus on the text field
            $("#content").focus();
            $("html").live('click', function() {
                $("#content").focus();
            });

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
		<input name="content" id="content" type="text" autocomplete="off" />
	</form>
</body>

</html>
