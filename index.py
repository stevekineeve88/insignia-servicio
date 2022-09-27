from flask import Flask
from modules.policy.controllers.api.v1.role_group_policy_controller import role_group_policy_v1_api

app = Flask(__name__)

app.register_blueprint(role_group_policy_v1_api)


@app.route("/", methods=["GET"])
def health_check():
    """ GET healthcheck
    Returns:
        tuple
    """
    return {
        "test": "hello world"
    }, 200
