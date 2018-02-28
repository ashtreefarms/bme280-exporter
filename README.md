# bme280_exporter

Python Prometheus exporter for the Bosch BME280 sensor 

## Requirements

This driver requires that you have previously installed the
[Adafruit_Python_BME280](https://github.com/adafruit/Adafruit_Python_BME280) package.

## Installation

```bash
pip install bme280_exporter
```

## Usage

```bash
$ bme280_exporter -h
usage: bme280_exporter [-h] [-v] [-p PORT] [-a ADDRESS] [-l LABELS]
                       [-i INTERVAL] [-f FILTER] [-ho HO] [-po PO] [-to TO]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -p PORT, --port PORT  exporter port (default: 9500
  -a ADDRESS, --address ADDRESS
                        BME280 I2C address (default: 0x77)
  -l LABELS, --labels LABELS
                        JSON object of Prometheus labels to apply
  -i INTERVAL, --interval INTERVAL
                        measurement sample interval (default: 2)
  -f FILTER, --filter FILTER
                        filter value to apply (0-4, default: 0)
  -ho HO                humidity oversampling value (1-5, default: 4)
  -po PO                pressure oversampling value (1-5, default: 4)
  -to TO                temperature oversampling value (1-5, default: 4)
```

## Docker

```bash
docker pull ashtreefarms/bme280-exporter-rpi
docker run -p 9500:9500 --device /dev/i2c-1 ashtreefarms/bme280-exporter-rpi
```

# MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.