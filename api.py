from flask import Flask
from flask_restful import Resource, Api, abort
from LEDController import LEDController
import logging


PATH_TO_API = "/api/leds"
DEBUG = True

#create a todo list ie list of the id and states of each pin, call the state and id in LED Controller, make a class for each pin, and then call it 
leds = {17: 'state,id' }

led = LEDController(17) 

def abort_if_LED_invalid(led_pin: int):
    """Abort the request if invalid pin is chosen and give 404."""
    if led_pin not in leds:  # TODO: update condition
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
        state = led.get_state()
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
    api.add_resource(LED, PATH_TO_API + "/<int:led_pin>")


    #test 
    api.add_resource(LED, PATH_TO_API + "/<int:led_pin>/on", endpoint="turn on LED by pin")
    api.add_resource(LED, PATH_TO_API + "/<int:led_pin>/off", endpoint ="turn off LED by pin")
    api.add_resource(LED, PATH_TO_API + "/<int:led_pin>/toggle", endpoint = "toggle LED by pin")

    # Run the app
    app.run(debug=DEBUG)



if __name__ == "__main__":
    main()
