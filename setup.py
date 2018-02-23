#!/usr/bin/env python

import os
from setuptools import find_packages, setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name="bme280_exporter",
    version="0.0.1-alpha",
    author="Jake Krog",
    author_email="jake.krog@gmail.com",
    description="Prometheus exporter for the Bosch BME280 sensor",
    long_description=README,
    license="MIT",
    keywords=["raspberry pi", "rpi", "prometheus", "BME280", "i2c", "temperature", "humidity", "pressure"],
    url="https://github.com/ashtreefarms/bme280_exporter",
    download_url="https://github.com/ashtreefarms/bme280_exporter/tarball/0.0.1-alpha",
    packages=find_packages(),
    install_requires=["Adafruit_BME280", "prometheus_client"],
    entry_points={
        'console_scripts': [
            'bme280_exporter = bme280_exporter.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console"
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring"
    ]
)