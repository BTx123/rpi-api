"""
api.py

Make a RESTful API on a Raspberry Pi.
"""


from flask import Flask
from flask_restful import Resource, Api, abort
import logging
from mysqlDatabase import DatabaseConnection
from mysql_ssh import DatabaseConnectionSSH


try:
    import gpiozero
except Exception as e:
    logging.log(logging.WARNING, "Falling back from gpiozero: {e}".format(e=e))
    import gpiozero_pseudo as gpiozero
    logging.log(logging.WARNING, "Now using pseudo gpiozero")


# Logging and debugging
LOGGER = logging.getLogger(__name__)
DEBUG = True

#MYSQL Connection
sshConnection = DatabaseConnectionSSH({"host": "127.0.0.1", "port": "3306", "user": "root", "password":"Calplug2016","database": "rpi_api"}, {'ssh_address': 'cpmqtt1.calit2.uci.edu', 'remote_bind_address':('cpmqtt1.calit2.uci.edu', 3306), 'local_bind_address':('127.0.0.1', 3306), 'ssh_username': 'calplug', 'ssh_password':'Calplug2016'})

# Routing API   host/api/led/17
ROUTE_API = "/api"
ROUTE_LEDS = "/leds"

# LED numbers should refer to GPIO number not RPi pin number
leds = dict()


def abort_if_LED_invalid(led_pin: int) -> None:
    """Abort the request if invalid pin is chosen and give 404."""

    if led_pin not in leds.keys():
        abort(404, message="Pin {pin} not available.".format(pin=led_pin))


def get_led(led_pin: int) -> dict:
    """Return led pin with current state."""

    return {
        "led_pin": led_pin,
        "state": leds[led_pin].is_lit
    }


class HelloWorld(Resource):
    """Demo 'Hello World' resource."""

    def get(self):
        LOGGER.debug("GET: Hello, World!")
        return {"hello": "world"}


class LEDS(Resource):
    """Resource for multiple LEDs."""

    def get(self) -> dict:
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

    def put(self) -> dict:
        """Handle exception if led already exist"""
        LOGGER.debug("PUT: invalid")
        abort(404, message="Pin should be specific.")

    def delete(self) -> dict:
        """DELETE command to delete all pins"""
        LOGGER.debug("DELETE: all pins")
        leds.clear()
        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }


class LED(Resource):
    """Resource for single LED."""

    def get(self, led_pin: int) -> dict:
        """GET single pin state."""
        abort_if_LED_invalid(led_pin)
        LOGGER.debug("GET: Pin {pin}".format(pin=led_pin))
        return get_led(led_pin)

    def post(self, led_pin: int, command: str) -> dict:
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
            # Event is not valid
            abort(404, message="Command not available.")
        try:
            sshConnection.execute((get_led(led_pin)))
        except:
            LOGGER.debug("Error inserting value into table")
        return get_led(led_pin)

    def put(self, led_pin: int) -> dict:
        """PUT command to create new LED"""
        LOGGER.debug("PUT: Pin {pin}".format(pin=led_pin))
        if led_pin in leds.keys():
            try:
                sshConnection.execute((get_led(led_pin)))
            except:
                LOGGER.debug("Error inserting value into table")

            return {
                "message": "Pin {pin} already exists.".format(pin=led_pin),
                "pins": [get_led(led_pin) for led_pin in leds]
            }
        leds[led_pin] = gpiozero.LED(led_pin)
        try:
            sshConnection.execute((get_led(led_pin)))
        except:
            LOGGER.debug("Error inserting value into table")

        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }

    def delete(self, led_pin: int) -> dict:
        """DELETE command to delete an existing LED"""
        abort_if_LED_invalid(led_pin)
        LOGGER.debug("DELETE: Pin {pin}".format(pin=led_pin))
        del leds[led_pin]
        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }


def main():
    # Logging
    logger_names = logging.Logger.manager.loggerDict.keys()
    for name in logger_names:
        logger = logging.getLogger(name)
        if DEBUG:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.CRITICAL)

    # Flask application
    app = Flask(__name__)
    api = Api(app)

    # Add resources (API endpoints)
    # GET /api
    api.add_resource(HelloWorld, "/api", endpoint="hello_world")
    # GET /api/leds
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS, endpoint="all_leds")
    # GET /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>", endpoint="led_by_pin")

    # POST /api/leds/{{command}}
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS +
                     "/<string:command>", endpoint="command_all_leds")
    # POST /api/leds/{{led_pin}}/{{command}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>/<string:command>",
                     endpoint="command_led_by_pin")

    # PUT /api/leds
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS,
                     endpoint="put_led_illegal")
    # PUT /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>", endpoint="put_led")

    # DELETE /api/leds
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS,
                     endpoint="delete_all_led")
    # DELETE /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>", endpoint="delete_led")

    # Run the app on local network: 127.0.0.1:5000
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)


if __name__ == "__main__":
    main()
