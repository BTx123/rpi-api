from flask import Flask
from flask_restful import Resource, Api, abort
from LEDController import LEDController
import logging


ROUTE_API = "/api"
ROUTE_LEDS = "/leds"
LOGGER = logging.getLogger("api")
DEBUG = True

# LED numbers should refer to GPIO number not RPi pin number
VALID_LEDS = [17, 27, 22]
leds = {led: LEDController(led) for led in VALID_LEDS}


def abort_if_LED_invalid(led_pin: int):
    """Abort the request if invalid pin is chosen and give 404."""
    if led_pin not in VALID_LEDS:
        abort(404, message="Pin {pin} not available.".format(pin=led_pin))


def get_led(led_pin: int) -> dict:
    """Return led pin with current state."""
    return {
        "led_pin": led_pin,
        "state": leds[led_pin].get_state()
    }


class HelloWorld(Resource):
    """Demo 'Hello World' resource."""

    def get(self):
        LOGGER.debug("GET: Hello, World!")
        return {"hello": "world"}


class LEDS(Resource):
    """Resource for multiple LEDs."""

    def get(self):
        """GET multiple LED states."""
        LOGGER.debug("GET: all pins".format())

        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }

    def post(self, command: str) -> dict:
        """POST commands to all LEDs: on, off, or toggle."""
        LOGGER.debug("POST: {command} all pins".format(command=command))

        # Check for on, off, toggle
        if command == "on":
            for led in leds.values():
                led.on()
        elif command == "off":
            for led in leds.values():
                led.off()
        elif command == "toggle":
            for led in leds.values():
                led.toggle()

        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }


class LED(Resource):
    """Resource for single LED."""

    def get(self, led_pin: int) -> dict:
        """GET single pin state."""
        abort_if_LED_invalid(led_pin)
        LOGGER.debug("GET: pin {pin}".format(pin=led_pin))
        return get_led(led_pin)

    def post(self, led_pin: int, command: str) -> None:
        """POST command to single pin: on, off, or toggle."""
        abort_if_LED_invalid(led_pin)
        LOGGER.debug("POST: {command} pin {pin}".format(
            command=command, pin=led_pin))

        # Check for on, off, toggle
        if command == "on":
            leds[led_pin].on()
        elif command == "off":
            leds[led_pin].off()
        elif command == "toggle":
            leds[led_pin].toggle()
        else:
            abort(404, message="Command not available.")

        return get_led(led_pin)


def main():
    # Logging
    api_logger = logging.getLogger("api")
    controller_logger = logging.getLogger("led_controller")
    pseudo_logger = logging.getLogger("gpiozero_pseudo")
    loggers = [api_logger, controller_logger, pseudo_logger]
    if DEBUG:
        for logger in loggers:
            logger.setLevel(logging.DEBUG)
    else:
        for logger in loggers:
            logger.setLevel(logging.CRITICAL)

    # Flask application
    app = Flask(__name__)
    api = Api(app)

    # Add resources (API endpoints)
    # GET /api
    api.add_resource(HelloWorld, "/api", endpoint="hello_world")
    # GET /api/leds
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS, endpoint="all_leds")
    # POST /api/leds/{{command}}
    api.add_resource(LEDS,  ROUTE_API + ROUTE_LEDS +
                     "/<string:command>", endpoint="command_all_leds")
    # GET /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>", endpoint="led_by_pin")
    # POST /api/leds/{{led_pin}}//{{command}}
    api.add_resource(LED,  ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>/<string:command>", endpoint="command_led_by_pin")

    # Run the app on local network
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)


if __name__ == "__main__":
    main()
