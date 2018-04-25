from flask import Flask
from flask_restful import Resource, Api, abort
# from LEDController import LEDController
import logging


ROUTE_API = "/api"
ROUTE_LEDS = "/leds"
DEBUG = True


def abort_if_LED_invalid(led_pin: int):
    """Abort the request if invalid pin is chosen and give 404."""
    if False:  # TODO: update condition
        abort(404, message="Pin {pin} not available.".format(pin=led_pin))


class HelloWorld(Resource):
    """Demo 'Hello World' resource."""

    def get(self):
        logging.debug("GET: Hello, World!")
        return {"hello": "world"}


class LED(Resource):
    """LED Control resource."""

    def get(self, led_pin: int) -> dict:
        """GET pin state."""
        abort_if_LED_invalid(led_pin)
        state = "on"
        logging.debug("GET: pin {pin} = {state}".format(
            pin=led_pin, state=state))
        return {
            "pin": led_pin,
            "state": state  # TODO: update field with method call
        }

    def post(self, led_pin: int, command: str) -> None:
        """TODO: POST"""
        abort_if_LED_invalid(led_pin)
        logging.debug("POST: {command} pin {pin}".format(
            command=command, pin=led_pin))


def main():
    # Logging
    logger = logging.getLogger()
    if DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.CRITICAL)

    # Flask application
    app = Flask(__name__)
    api = Api(app)

    # Add resources (API endpoints)
    api.add_resource(HelloWorld, "/api")
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS + "/<int:led_pin>")

    # Run the app
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)


if __name__ == "__main__":
    main()
