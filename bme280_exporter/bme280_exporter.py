from Adafruit_BME280 import *
import logging
from prometheus_client import Counter, Gauge

METRICS = {
    # Gauges
    'humidity': ('bme280_humidity_percent', "Current BME280 humidity"),
    'pressure': ('bme280_pressure_pa', "Current BME280 atmospheric pressure"),
    'temp': ('bme280_temperature_celsius', "Current BME280 temperature"),
    
    # Counters
    'io_reads': ('bme280_io_reads_total', "Total number of BME280 I/O reads"),
    'io_errors': ('bme280_io_errors_total', "Total number of BME280 I/O errors")
}

logger = logging.getLogger(__name__)


class BME280Exporter:
    @staticmethod
    def gauge(info, labels=None):
        if labels is None:
            labels = {}
        label_keys = list(labels.keys())
        label_values = [labels[k] for k in label_keys]
        gauge = Gauge(info[0], info[1], label_keys)
        if len(label_values):
            gauge = gauge.labels(*label_values)
        return gauge
            
    @staticmethod
    def counter(info, labels=None):
        if labels is None:
            labels = {}
        label_keys = list(labels.keys())
        label_values = [labels[k] for k in label_keys]
        counter = Counter(info[0], info[1], label_keys)
        if len(label_values):
            counter = counter.labels(*label_values)
        return counter
    
    def __init__(self, address, metrics=METRICS, labels=None):
        self.temp = None
        self.humidity = None
        self.pressure = None
        self.humidity_gauge = BME280Exporter.gauge(metrics['humidity'], labels)
        self.pressure_gauge = BME280Exporter.gauge(metrics['pressure'], labels)
        self.temp_gauge = BME280Exporter.gauge(metrics['temp'], labels)
        self.ioread_counter = BME280Exporter.counter(metrics['io_reads'], labels)
        self.ioerror_counter = BME280Exporter.counter(metrics['io_errors'], labels)
        self.bme280 = BME280(address=address,
                             t_mode=BME280_OSAMPLE_8,
                             p_mode=BME280_OSAMPLE_8,
                             h_mode=BME280_OSAMPLE_8)
    
    def measure(self):
        self.ioread_counter.inc()
        try:
            self.temp = self.bme280.read_temperature()
            self.humidity = self.bme280.read_humidity()
            self.pressure = self.bme280.read_pressure()
        except IOError:
            logger.error('IOError when reading BME280 measurements')
            self.ioerror_counter.inc()
        logger.info("   ".join([
            "temp: {:.2f} C".format(self.temp),
            "humidity: {:.2f}%".format(self.humidity),
            "pressure: {:.2f} hPa".format(self.pressure / 100)
        ]))
    
    def export(self):
        self.humidity_gauge.set(self.humidity)
        self.pressure_gauge.set(self.pressure)
        self.temp_gauge.set(self.temp)
