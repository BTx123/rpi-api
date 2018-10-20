import unittest
from rpi import gpiozero_pseudo


class TestGPIOZeroPsuedo(unittest.TestCase):
    def setUp(self):
        self.pin = 10
        self.led = gpiozero_pseudo.LED(self.pin)

    def test_is_lit_false_by_default(self):
        self.assertFalse(self.led.is_lit)

    def test_pin_is_correct(self):
        self.assertEqual(self.pin, self.led.pin)

    def test_on(self):
        self.led.on()
        self.assertTrue(self.led.is_lit)

    def test_off(self):
        self.led.off()
        self.assertFalse(self.led.is_lit)

    def test_on_from_on(self):
        self.led.on()
        self.led.on()
        self.assertTrue(self.led.is_lit)

    def test_on_from_off(self):
        self.led.off()
        self.led.on()
        self.assertTrue(self.led.is_lit)

    def test_off_from_on(self):
        self.led.on()
        self.led.off()
        self.assertFalse(self.led.is_lit)

    def test_off_from_off(self):
        self.led.off()
        self.led.off()
        self.assertFalse(self.led.is_lit)

    def test_toggle_from_on(self):
        self.led.on()
        self.led.toggle()
        self.assertFalse(self.led.is_lit)

    def test_toggle_from_off(self):
        self.led.off()
        self.led.toggle()
        self.assertTrue(self.led.is_lit)


if __name__ == "__main__":
    unittest.main()
