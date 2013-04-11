from __future__ import unicode_literals
import i18n

def main(**kwargs):
    #title=toolname
    #stuff=html content
    path = '//tools.wmflabs.org/matilda/bootstrap'
    nav = """<!--<li><a href="//tools.wmflabs.org/matilda/cgi-bin/home.py">matilda</a></li>-->
    <li><a href="//www.wikidata.org/wiki/User:Legoktm/matilda">{}</a></li>
    <li><a href="//tools.wmflabs.org/matilda/cgi-bin/new.py">{}</a></li>
    <li><a href="//toosl.wmflabs.org/matilda/cgi-bin/current.py">{}</a></li>
    """.format(i18n.translate('navbar-help'),
               i18n.translate('navbar-newjobs'),
               i18n.translate('navbar-currun'),
               )

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <title>{title}</title>

    <!-- Le styles -->
    <link href="{path}/css/bootstrap.min.css" rel="stylesheet">
    <style>
    body {{
             padding-top: 60px; /* 60px to make the container go all the way to the bottom of the topbar */
    }}
    </style>
    <link href="{path}/css/bootstrap-responsive.min.css" rel="stylesheet">
    <link href="//tools.wmflabs.org/matilda/local.css" rel="stylesheet">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
    <script src="{path}/js/html5shiv.js"></script>
    <![endif]-->
    </head>

    <body>

    <div class="navbar navbar-inverse navbar-fixed-top">
    <div class="navbar-inner">
    <div class="container">
    <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    <span class="icon-bar"></span>
    </button>
    <a class="brand" href="#">matilda</a>
    <div class="nav-collapse collapse">
    <ul class="nav">
    {nav}
    </ul>
    </div><!--/.nav-collapse -->
    </div>
    </div>
    </div>

    <div class="container">

    {stuff}

    </div> <!-- /container -->

    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="{path}/js/jquery.js"></script>

    </body>
    </html>
    """.format(path=path, nav=nav, **kwargs).encode('utf-8')
