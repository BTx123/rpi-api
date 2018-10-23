# Raspberry Pi API
The Raspberry Pi API creates a server to control General-Purpose Input/Output (GPIO) pins on the Pi over a local netowrk. The script utilizes [`flask_restful`](http://flask-restful.readthedocs.io/en/latest/index.html) to serve content and [`gpiozero`](https://gpiozero.readthedocs.io/en/stable/) to control the onboard GPIO pins. Currently, the API restricts the use of GPIO pins to predefined ones, but could certainly be extended to allow any GPIO pin to be added and used. See below for setup instructions and API routes.

## TODO
* Add/Remove pins to valid list of pins via RESTful API, other routes TBD
* Implement UI with simulation

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
A Raspberry Pi (we used a Raspberry Pi 3 Model B) to act as a server with the following:
* Linux distribution of your choice - we chose the minimal [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/), but it should also work with the Desktop version
* [Python 3](https://www.python.org/) (developed using Python 3.6) and [pip](https://packaging.python.org/tutorials/installing-packages/) to run the scripts and easily install packages.
* Python packages (listed under [Built With](#built-with) below, which you can install by running `python3 -m pip install -r requirements.txt`.

Optionally, you may want to:
* [Setup SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/) to edit and test scripts directly on the Pi.
* Use [Angry IP Scanner](http://angryip.org/) to find a Pi's IP address on the *same* network without needing to connect the Pi to external displays and input devices.

### Running on a Raspberry Pi Server
1. To get a local copy of the repository, run `git clone https://github.com/BTx123/rpi-api.git`.
2. Start the server on http://0.0.0.0:5000 with `python3 rpi/api.py`, allowing local network clients to send API requests. If any errors appear, see [Prerequisites](#prerequisites) above.
3. After confirming that your server is running, navigate to a browser, [Postman](https://www.getpostman.com/), or any REST client to make [API requests](#api-routes). `{{server_IP_address}}` should be replaced by the IP address of your Pi. Examples below:
    * `GET http://{{server_IP_address}}:5000/api/led/17` - send a `GET` request to the server on port 5000 to read the state of GPIO pin 17
    * `POST http://{{server_IP_address}}:5000/api/led/17/toggle` - send a `POST` request to toggle the state of GPIO pin 17
4. Sending a request should toggle pins between HIGH and LOW states, thus turning connected LEDs, or whatever is connected to the GPIO pins, on and off.

### Setting up a Simple Circuit
Below is a sample circuit, consisting of a resistor in series with a LED.
<img src="https://github.com/BTx123/rpi-api/blob/master/circuit-diagram.png" alt="Whoops, image is missing!" width="50%">

## API Routes
Available routes are listed in the table below. [Link](https://www.getpostman.com/collections/e0f69c3b0b4844c131a5) to Postman Collection.

Note: `{{id}}` should be replaced with the *GPIO* pin number, not the *Raspberry Pi* pin number. Raspberry Pi's [GPIO usage guide](https://www.raspberrypi.org/documentation/usage/gpio/) has more information regarding GPIO pin numbering.

| Method | Route                     | Description             |
|--------|---------------------------|-------------------------|
| `GET`  | `/api/leds`               | Get state of all LEDs   |
| `GET`  | `/api/leds/{{id}}`        | Get state of single LED |
| `POST` | `/api/leds/on`            | Set all LEDs to HIGH    |
| `POST` | `/api/leds/off`           | Set all LEDs to LOW     |
| `POST` | `/api/leds/toggle`        | Toggle all LEDs         |
| `POST` | `/api/leds/{{id}}/on`     | Set single LED to HIGH  |
| `POST` | `/api/leds/{{id}}/off`    | Set single LED to LOW   |
| `POST` | `/api/leds/{{id}}/toggle` | Toggle single LED       |

## Built With
* [Raspberry Pi 3 Model B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [Python 3.6](https://www.python.org/)
* [gpiozero](https://gpiozero.readthedocs.io/en/stable/): simple GPIO interfacing with Raspberry Pi
* [flask_restful](http://flask-restful.readthedocs.io/en/latest/index.html): quickly build a Flask API
* [Postman](https://www.getpostman.com/)

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/BTx123/rpi-api/blob/master/LICENSE.md) file for details

## Contributors
* [Ruth Nguyen](https://github.com/ruthienguyen)
* [Brian Tom](https://github.com/BTx123)
