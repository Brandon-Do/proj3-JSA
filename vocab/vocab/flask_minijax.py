"""
Tiny demo of Ajax interaction
"""

import flask
import logging
import config


###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Sign my cookies


###
# Pages
###

@app.route("/")
def index():
    return flask.render_template('minijax.html')

###############
# AJAX request handlers
#   These return JSON to the JavaScript function on
#   an existing page, rather than rendering a new page.
###############


@app.route("/_countem")
def countem():
    """
    Brandon's Notes to Self:
    input:
        Takes argument "text" taken from the html file. The HTML argument is the following:

        <form id="entry">
            <label for="attempt">Word:</label>
            <input id="attempt" name="attempt" type="text" width="15" autocomplete="off"  autofocus />
        </form>

        Notice the "For" loop created by AJAX (?), For each letter create a box with the letter INSIDE OF IT.

    output:
        Returns "long_enough' message iff length >=5

    properties:
        NOTICE: Result goes here:

       $.getJSON( "/_countem", { text: txt },
                  function(data) {
                    ...<code>...
                    rsval = data.result.long_enough;
                    ...<code>...
                   }
               );
       });

    """
    text = flask.request.args.get("text", type=str)
    length = len(text)
    rslt = {"long_enough": length >= 5}
    return flask.jsonify(result=rslt)

#############


if __name__ == "__main__":
    # Standalone (not running under green unicorn or similar)
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
    app.logger.info("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
