from Adafruit_BME280 import *
import argparse
from bme280_exporter import BME280Exporter
import json
import logging
import prometheus_client
from time import sleep

_DEFAULT_FILTER = 0
_DEFAULT_I2C_ADDRESS = 0x77
_DEFAULT_LOG_FORMAT = '%(asctime)s - %(message)s'
_DEFAULT_OVERSAMPLING = 4
_DEFAULT_PORT = 9500
_DEFAULT_SAMPLE_INTERVAL = 2

logger = logging.getLogger('bme280_exporter')


def init_arg_parser():
    """Initialize, configure, and return an instance of ArgumentParser"""
    p = argparse.ArgumentParser()
    p.add_argument("-v", "--verbose", action='store_true',
                   help="increase output verbosity")
    p.add_argument("-p", "--port", type=int, default=_DEFAULT_PORT,
                   help="exporter port (default: {}"
                        .format(_DEFAULT_PORT))
    p.add_argument("-a", "--address", type=lambda x: int(x, 0),
                   default=_DEFAULT_I2C_ADDRESS,
                   help="BME280 I2C address (default: 0x{:02x})"
                        .format(_DEFAULT_I2C_ADDRESS))
    p.add_argument("-l", "--labels", type=json.loads,
                   help="JSON object of Prometheus labels to apply")
    p.add_argument("-i", "--interval",
                   type=int, default=_DEFAULT_SAMPLE_INTERVAL,
                   help="measurement sample interval (default: {})"
                        .format(_DEFAULT_SAMPLE_INTERVAL))
    p.add_argument("-f", "--filter", type=int, default=_DEFAULT_FILTER,
                   help="filter value to apply (0-4, default: {})"
                        .format(_DEFAULT_FILTER))
    p.add_argument("-ho", type=int, default=_DEFAULT_OVERSAMPLING,
                   help="humidity oversampling value (1-5, default: {})"
                        .format(_DEFAULT_OVERSAMPLING))
    p.add_argument("-po", type=int, default=_DEFAULT_OVERSAMPLING,
                   help="pressure oversampling value (1-5, default: {})"
                        .format(_DEFAULT_OVERSAMPLING))
    p.add_argument("-to", type=int, default=_DEFAULT_OVERSAMPLING,
                   help="temperature oversampling value (1-5, default: {})"
                        .format(_DEFAULT_OVERSAMPLING))
    return p


def configure_logger(args):
    """Configure the module logger"""
    f = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger.setLevel(log_level)
    logger.addHandler(ch)


def main():
    """Run the exporter"""
    parser = init_arg_parser()
    args = parser.parse_args()

    configure_logger(args)
    logger.info("initializing BME280 at 0x{a:02x} filter: {f} oversampling(h: {h}, p: {p}, t: {t})"
                .format(a=args.address,
                        f=args.filter,
                        h=args.ho,
                        p=args.po,
                        t=args.to))

    bme280 = BME280(address=args.address,
                    filter=args.filter,
                    h_mode=args.ho,
                    p_mode=args.po,
                    t_mode=args.to)

    logger.info("initializing exporter with labels {}".format(args.labels))
    exporter = BME280Exporter(bme280, labels=args.labels)
    
    logger.info('starting exporter on port {}'.format(args.port))
    prometheus_client.start_http_server(args.port)

    logger.info("starting sampling with {:.1f}s interval".format(args.interval))
    while True:
        exporter.measure()
        exporter.export()
        sleep(args.interval)


if __name__ == "__main__":
    main()
