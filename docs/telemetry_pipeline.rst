MQTT Telemetry Ingestion Pipeline
=================================

The Telemetry Pipeline is the high-velocity data ingestion framework operating within Django to securely pull raw JSON structures from Mosquitto and anchor them into PostgreSQL.

The `mqtt_listener` Architecture
--------------------------------

Unlike standard HTTP REST APIs that require an active connection request, the Upemba backend utilizes Python's ``paho-mqtt`` client running structurally as a detached background daemon loop.

This daemon is officially triggered using:

.. code-block:: bash

    python manage.py mqtt_listener

In production (e.g., on the Raspberry Pi), this loop is wrapped natively inside an isolated Docker container (``backend_production_mqtt_listener``) assuring that it operates flawlessly independent of the Web Server HTTP threads.

Data Mapping & Auto-Association
-------------------------------

When the listener detects a valid payload matching ``upemba/sensors/+/telemetry``, it intercepts the JSON.

1. **Equipment Registration**: It queries the PostgreSQL ``Equipment`` database using the provided ``device_id``. 
   - If the equipment does not physically exist in the records, the backend autonomously instantiates it (e.g., mapping it as an ``INVERTER`` automatically). 

2. **Database Write**: It creates a new ``SensorReading`` record containing the ``temperature``, ``voltage``, ``vib_x``, ``vib_y``, and ``vib_z`` values.

3. **Django Admin Visibility**: These values are physically registered into ``backend/telemetry/admin.py``, surfacing in the graphical ``http://<SERVER_IP>/admin`` dashboard the millisecond the packet processes.
