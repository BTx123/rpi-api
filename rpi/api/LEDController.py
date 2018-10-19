"""
LEDController.py

Controller for LED on Raspberry Pi.

gpiozero
Basics Documentation: http://gpiozero.readthedocs.io/en/stable/recipes.html
LED Documentation: http://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=LED

Raspberry Pi
Pin Documentation: http://pi4j.com/pins/model-2b-rev1.html
"""

import logging
try:
    import gpiozero
except Exception as e:
    logging.log(logging.WARNING, "Falling back from gpiozero: {e}".format(e=e))
    import gpiozero_pseudo as gpiozero
    logging.log(logging.WARNING, "Now using pseudo gpiozero")


LOGGER = logging.getLogger("led_controller")


class LEDController:
    """Controller for LED on Raspberry Pi."""

    def __init__(self, pin: int):
        """
        Initialize LED Controller with a pin number corresponding to
        Raspberry Pi.

        Args:
            pin (int): LED pin to read and write states
        """
        self._pin = pin  # self._led.pin.number
        self._led = gpiozero.LED(self._pin)

    def get_state(self) -> bool:
        """
        Return the current state of the LED pin.
        True for on, False for off.
        """
        state = self._led.is_lit
        LOGGER.debug(
            "get_state: pin {pin} = {state}".format(pin=self._pin, state=state))
        return state

    def on(self) -> None:
        """Turn the LED on."""
        self._led.on()
        LOGGER.debug("on: {pin} = on".format(pin=self._pin))

    def off(self) -> None:
        """Turn the LED off."""
        self._led.off()
        LOGGER.debug("off: {pin} = off".format(pin=self._pin))

    def toggle(self) -> None:
        """Toggle the LED state."""
        self._led.toggle()
        LOGGER.debug("toggle: {pin} = {state}".format(
            pin=self._pin, state=self._led.is_lit))


def main():
    from time import sleep
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    LED = 17
    led = LEDController(LED)
    led.on()
    sleep(5)
    led.off()


if __name__ == '__main__':
    main()
