def inject_js(content, path):
    if path == "/":
        inj = """</title>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
    <script type="text/javascript">
        jQuery('document').ready(function() {
           $('<div class="logout_bar"><a href="/logout?' + Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5) + '">Logout</a></logout_bar>').prependTo('body');
        });
    </script>
    <style>
    body {
        margin-top:30px;
    }
    .logout_bar {
        z-index: 1000;
        position: relative;
        text-align:right;
        background-color: #333;
        color: white;
        padding: 10px;
    }
    .logout_bar a {
        color: white !important;
        text-decoration: none;
    }
    </style>
        """
    elif "p/" in path:
        inj = """</title>
    <script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
    <script type="text/javascript">
        jQuery('document').ready(function() {
                $('<li data-type="button" data-key="logout"><a class="grouped-left buttonicon" title="Logout" href="/logout?'+Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5)+'" onClick="javascript: window.location.href=\\'/logout?'+Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 5)+'\\';" style="width:auto"> Logout </a></li>').appendTo('.menu_right')

           });
    </script>
        """
    else:
        inj = "</title>"

    return content.replace("</title>", inj)


