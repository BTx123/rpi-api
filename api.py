from flask import Flask
from flask_restful import Resource, Api, abort
from LEDController import LEDController
import logging


ROUTE_API = "/api"
ROUTE_LEDS = "/leds"
DEBUG = True

VALID_LEDS = [17]  # LED numbers should refer to GPIO number not RPi pin number
leds = {led: LEDController(led) for led in VALID_LEDS}


def abort_if_LED_invalid(led_pin: int):
    """Abort the request if invalid pin is chosen and give 404."""
    if led_pin not in VALID_LEDS:  # TODO: update condition
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
        state = leds[led_pin].get_state()
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
        # check for on, off, toggle
        if command == "on":
            leds[led_pin].on()
        elif command == "off":
            leds[led_pin].off()
        elif command == "toggle":
            leds[led_pin].toggle()
        else:
            abort(404, message="Command not available.")
        return {
            "pin": led_pin,
            "state": leds[led_pin].get_state()
        }


class LEDS(Resource):
    def get(self):
        return str(leds)


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

    # test
    api.add_resource(LED,  ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>/<string:command>", endpoint="turn on LED by pin")

    # Run the app
    #app.run(host="0.0.0.0", port=5000, debug=DEBUG)
    app.run(debug=DEBUG)


if __name__ == "__main__":
    main()
