Hardware & Edge Node Integration
================================

This document covers how peripheral IoT nodes (like the ESP32) physically interface with the Upemba Backend architecture over the local intranet.

Device Specifications
-------------------

The Upemba backend natively supports any edge device capable of publishing to an MQTT broker. Our primary reference microcontrollers are the ESP32 and ESP8266.

Base Configurations required on the Edge Device:
- **Broker IP**: ``192.168.1.72`` (or the designated Raspberry Pi IP Address)
- **Broker Port**: ``1883``
- **Transmission Interval**: ``30,000 ms`` (30 seconds is strictly recommended for production deployments to avoid overloading the PostgreSQL database while providing sufficient data points for Machine Learning aggregation).

MQTT Routing (Topic Structure)
------------------------------

The Django backend enforces a wildcard subscription payload map. When programming an ESP32, it **must** transmit to the following topic format:

.. code-block:: text

    upemba/sensors/<DEVICE_MAC_OR_ID>/telemetry

Because the Python listener subscribes to ``upemba/sensors/+/telemetry``, the ``+`` wildcard dynamically ingests array streams from thousands of devices autonomously.

JSON Payload Schema
-------------------

The ESP32 firmware should serialize the sensor output exactly matching this JSON object struct:

.. code-block:: json

    {
        "device_id": "EQUIP-INV-001",
        "data": {
            "temp": 27.81,
            "volt": 8.94,
            "vib": {
                "x": -0.39,
                "y": -0.32,
                "z": 0.63
            }
        }
    }

If the parser detects malformed JSON or entirely missing keys, the payload will be instantly dropped and logged as a warning.
