from flask import Flask
from modules.action.controllers.api.v1.action_controller import action_v1_api
from modules.policy.controllers.api.v1.role_group_policy_controller import role_group_policy_v1_api
from modules.role.controllers.api.v1.role_controller import role_v1_api
from modules.role.controllers.api.v1.role_group_controller import role_group_v1_api

app = Flask(__name__)

app.register_blueprint(role_group_policy_v1_api)
app.register_blueprint(action_v1_api)
app.register_blueprint(role_v1_api)
app.register_blueprint(role_group_v1_api)


@app.route("/", methods=["GET"])
def health_check():
    """ GET healthcheck
    Returns:
        tuple
    """
    return {
        "test": "hello world"
    }, 200
