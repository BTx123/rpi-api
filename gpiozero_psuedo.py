class LED:
    """Pseudo-LED for testing without Raspberry Pi."""

    def __init__(self, led_pin, is_lit=False):
        self._led_pin = led_pin
        self._is_lit = is_lit

    def is_lit(self) -> bool:
        return self._is_lit

    def on(self):
        self._is_lit = True
        print("LED {pin} turned on".format(pin=self._led_pin))

    def off(self):
        self._is_lit = False
        print("LED {pin} turned off".format(pin=self._led_pin))

    def toggle(self):
        self._is_lit = not self._is_lit
        print("LED {pin} toggled to {state}".format(
            pin=self._led_pin, state=LED._bool_to_str(self._is_lit)))

    @staticmethod
    def _bool_to_str(b: bool) -> str:
        return "on" if b else "off"
