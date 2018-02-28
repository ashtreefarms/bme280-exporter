import logging
from prometheus_client import Counter, Gauge

_LOG_MESSAGE_FORMAT = "   ".join(["temp: {temp:.2f} C",
                                  "humidity: {humidity:.2f}%",
                                  "pressure: {pressure:.2f} hPa"])
_METRICS = {
    # Gauges
    'humidity': ('bme280_humidity_percent', "Current BME280 humidity"),
    'pressure': ('bme280_pressure_pa', "Current BME280 atmospheric pressure"),
    'temp': ('bme280_temperature_celsius', "Current BME280 temperature"),
    
    # Counters
    'io_reads': ('bme280_io_reads_total', "Total number of BME280 I/O reads"),
    'io_errors': ('bme280_io_errors_total', "Total number of BME280 I/O errors")
}

logger = logging.getLogger(__name__)


def _gauge(metric, labels=None):
    """Initialize and return a Gauge object"""
    if labels is None:
        labels = {}
    label_keys = list(labels.keys())
    label_values = [labels[k] for k in label_keys]
    gauge = Gauge(*metric, label_keys)
    if len(label_values):
        gauge = gauge.labels(*label_values)
    return gauge


def _counter(metric, labels=None):
    """Initialize and return a Counter object"""
    if labels is None:
        labels = {}
    label_keys = list(labels.keys())
    label_values = [labels[k] for k in label_keys]
    counter = Counter(*metric, label_keys)
    if len(label_values):
        counter = counter.labels(*label_values)
    return counter


class BME280Exporter(object):
    """Collects and exports metrics for a single BME280 sensor"""
    def __init__(self, bme280, labels=None, metrics=_METRICS, log_format=_LOG_MESSAGE_FORMAT):
        self.bme280 = bme280
        self.temp = None
        self.humidity = None
        self.pressure = None
        self.log_format = log_format
        self.humidity_gauge = _gauge(metrics['humidity'], labels)
        self.pressure_gauge = _gauge(metrics['pressure'], labels)
        self.temp_gauge = _gauge(metrics['temp'], labels)
        self.ioread_counter = _counter(metrics['io_reads'], labels)
        self.ioerror_counter = _counter(metrics['io_errors'], labels)
    
    def measure(self):
        """Read BME280 measurements"""
        self.ioread_counter.inc()
        try:
            self.temp = self.bme280.read_temperature()
            self.humidity = self.bme280.read_humidity()
            self.pressure = self.bme280.read_pressure()
        except IOError:
            logger.error('IOError when reading BME280 measurements')
            self.ioerror_counter.inc()
        logger.info(self.log_format.format(temp=self.temp,
                                           humidity=self.humidity,
                                           pressure=(self.pressure / 100)))
    
    def export(self):
        """Export BME280 metrics to Prometheus"""
        self.humidity_gauge.set(self.humidity)
        self.pressure_gauge.set(self.pressure)
        self.temp_gauge.set(self.temp)
