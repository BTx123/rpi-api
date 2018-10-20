"""
gpiozero_psuedo.py

Placeholder gpiozero library for testing without Raspberry Pi.
"""

import logging


LOGGER = logging.getLogger(__name__)


class LED:
    """Pseudo-LED for testing without Raspberry Pi."""

    @staticmethod
    def _bool_to_str(b: bool) -> str:
        return "on" if b else "off"

    def __init__(self, pin, is_lit=False):
        self.pin = pin
        self.is_lit = is_lit

    def on(self):
        self.is_lit = True
        LOGGER.debug("LED {pin} turned on".format(pin=self.pin))

    def off(self):
        self.is_lit = False
        LOGGER.debug("LED {pin} turned off".format(pin=self.pin))

    def toggle(self):
        self.is_lit = not self.is_lit
        LOGGER.debug("LED {pin} toggled to {state}".format(
            pin=self.pin, state=LED._bool_to_str(self.is_lit)))
