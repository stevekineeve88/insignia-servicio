from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    """ GET healthcheck
    Returns:
        tuple
    """
    return {
        "test": "hello world"
    }, 200
