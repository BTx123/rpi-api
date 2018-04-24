# rpi-api

## Raspberry Pi API
| Method   | Route                    | Description                    |
|----------|--------------------------|--------------------------------|
| `GET`    | `/api/led/{{id}}`        | Get state of LED (HIGH or LOW) |
| `POST`   | `/api/led/{{id}}/on`     | Set LED to HIGH                |
| `POST`   | `/api/led/{{id}}/off`    | Set LED to LOW                 |
| `POST`   | `/api/led/{{id}}/toggle` | Toggle LED to opposite state   |
