# Upemba IoT Gateway - Project Context

## 1. Core Mission
An Industrial IoT (IIoT) ecosystem designed to monitor critical infrastructure (Solar Inverters, Water Pumps, Server Rooms) in remote environments such as the Upemba National Park. The system uses real-time telemetry and Machine Learning (Isolation Forest) to predict hardware failure before it occurs, thereby minimizing downtime in off-grid conservation areas. This is a B-Tech Final Year Project.

## 2. Technical Architecture
The project follows a Decoupled Micro-service Architecture managed via Docker Compose on a Raspberry Pi (Ubuntu Server 24).

- **Edge Layer (ESP32):** C++ firmware utilizing `PubSubClient` and `ArduinoJson v7`. Collects 3-axis vibration (ADXL335), voltage (ZMPT101B), and temperature (DS18B20). Data is pushed via MQTT.
- **Message Broker (Mosquitto):** Handles high-frequency asynchronous data ingestion.
- **Backend (Django 5.x + DRF):** 
  - *Inventory App*: Manages the "Digital Twin" of physical assets and manual Maintenance Logs.
  - *Telemetry App*: Manages time-series sensor data and ML-generated health statuses.
- **Task Queue (Celery + Redis):** Offloads heavy Machine Learning computations (Anomaly Detection) from the main request/response cycle.
- **Database (PostgreSQL 15):** Relational storage with indexing on time-series fields for rapid dashboard rendering.
- **Frontend (Next.js):** Professional dashboard for real-time visualization and asset management.

## 3. Database Domain Model
- **Asset Identity:** UUID-based identification to support future multi-gateway synchronization.
- **Telemetry Stream:** High-frequency relational storage of Temperature, Voltage, and Vibration ($X, Y, Z$).
- **Maintenance Ledger:** Audit trail of human interventions and corrective actions.
- **AI Intelligence:** Storage of Anomaly Scores and predictive status flags.

## 4. Development Standards
- **Tooling:** `uv` (Package Management), `just` (Command Runner), Docker (Containerization).
- **Pattern:** Model Directory Pattern (splitting `models.py` into specialized packages).
- **Git Strategy:** Git Submodules to manage Backend and Frontend repositories independently within a Master Gateway repository.

## 5. Edge Layer Implementation Details (ESP32)
The ESP32 acts as the edge node collecting telemetry and pushing it to the local broker.
- **Networking:** Connects to local Intranet Wi-Fi (`WIFI_SSID`), with auto-reconnect fallback.
- **MQTT:** Maintains a persistent connection to Mosquitto (`MQTT_BROKER`) via `PubSubClient`, retrying every 5 seconds on disconnect.
- **Telemetry Payload:** JSON structured telemetry using `ArduinoJson v7`.
  - Encapsulates `device_id` and nested `data` (temp, volt, vib: {x, y, z}).
- **Reporting:** Polling and publishing occur synchronously at a fixed interval (`REPORT_INTERVAL`), with local serial fallback for debugging.
