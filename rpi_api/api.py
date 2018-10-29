from flask import Flask  # flask package
from flask_restful import Resource, Api, abort
import logging


try:
    import gpiozero
except Exception as e:
    logging.log(logging.WARNING, "Falling back from gpiozero: {e}".format(e=e))
    import gpiozero_pseudo as gpiozero
    logging.log(logging.WARNING, "Now using pseudo gpiozero")


# Logging and debugging
LOGGER = logging.getLogger(__name__)
DEBUG = True

# Routing API   host/api/led/17
ROUTE_API = "/api"
ROUTE_LEDS = "/leds"

# LED numbers should refer to GPIO number not RPi pin number
VALID_LEDS = [17, 27, 22] # the ID  for the LED
leds = {led: gpiozero.LED(led) for led in VALID_LEDS}
#led: gpiozero.LED(led)     17: LED(17)


def abort_if_LED_invalid(led_pin: int) -> None:  # send the error to the suer
    """Abort the request if invalid pin is chosen and give 404."""

    if led_pin not in VALID_LEDS:
        abort(404, message="Pin {pin} not available.".format(pin=led_pin))


def get_led(led_pin: int) -> dict: # return the dict: pin:state
    """Return led pin with current state."""

    return {
        "led_pin": led_pin,
        "state": leds[led_pin].is_lit
    }


class HelloWorld(Resource): # test the thing is working
    """Demo 'Hello World' resource."""

    def get(self):
        LOGGER.debug("GET: Hello, World!")
        return {"hello": "world"}


class LEDS(Resource): # give the multiple LEDs
    """Resource for multiple LEDs."""

    def get(self) -> dict:
        """GET multiple LED states."""
        LOGGER.debug("GET: all pins".format())

        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }

    def post(self, command: str) -> dict: # makes it on or off
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
        '''Handle exception if led already exist'''
        abort(404, message="Pin should be specific.")
    
class LED(Resource): # signle assess to the LED
    """Resource for single LED."""

    def get(self, led_pin: int) -> dict:
        """GET single pin state."""
        abort_if_LED_invalid(led_pin)
        LOGGER.debug("GET: pin {pin}".format(pin=led_pin))
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
            abort(404, message="Command not available.") # tell us that the event is not valid

        return get_led(led_pin)
    
    def put(self, led_pin: int) -> dict:
        """PUT command to create new LED"""
        VALID_LEDS.append(led_pin)
        leds[led_pin] = gpiozero.LED(led_pin)

        return {
            "pins": [get_led(led_pin) for led_pin in leds]
        }

    def delete(self, led_pin: int) -> dict:
        """DELETE command to delete an existing LED"""
        abort_if_LED_invalid(led_pin) # Check if the LED inside the list

        VALID_LEDS.remove(led_pin)
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
    # make a flask applicaiton, just make a server
    app = Flask(__name__)
    api = Api(app)

    # Add resources (API endpoints)
    # GET /api
    api.add_resource(HelloWorld, "/api", endpoint="hello_world")
    # GET /api/leds
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS, endpoint="all_leds")
    # POST /api/leds/{{command}}
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS +
                     "/<string:command>", endpoint="command_all_leds")
    # GET /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>", endpoint="led_by_pin")
    # POST /api/leds/{{led_pin}}/{{command}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                     "/<int:led_pin>/<string:command>",
                     endpoint="command_led_by_pin")

    # PUT /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                    "/<int:led_pin>", endpoint = "put_led")

    # PUT /api/leds
    api.add_resource(LEDS, ROUTE_API + ROUTE_LEDS, 
                    endpoint = "put_led_illegal")
    
    # DELETE /api/leds/{{led_pin}}
    api.add_resource(LED, ROUTE_API + ROUTE_LEDS +
                    "/<int:led_pin>", endpoint = "delete_led")

    # Run the app on local network: 127.0.0.1:5000
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)


if __name__ == "__main__":
    main()
