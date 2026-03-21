# GitHub Project: Upemba IoT Gateway 🌍📡

**Description:** An Industrial IoT (IIoT) ecosystem designed to monitor critical infrastructure (Solar Inverters, Water Pumps, Server Rooms) in the Upemba National Park. Uses edge telemetry (ESP32) and Machine Learning (Isolation Forest) for predictive maintenance to minimize downtime.

---

## 🛠 Senior Dev Observations & Suggestions
*Based on the initial scan of the Django backend:*
1. **Asset Identity & Telemetry are modeled well:** `Equipment`, `HealthStatus`, and `SensorReading` models correctly implement the required fields and UUIDs. The Model Directory Pattern is correctly applied.
2. **Maintenance Ledger is missing:** The file `maintenance.py` exists but needs the `MaintenanceLog` model implementation for human audit trails.
3. **Ingestion Strategy:** Since the ESP32 pushes to Mosquitto (MQTT), the Django backend shouldn't just rely on REST endpoints to get data. We need an MQTT consumer service (e.g., a background daemon or Celery worker) to ingest `SensorReading`s.
4. **Time-Series Optimization:** `SensorReading.timestamp` has `db_index=True`, which is good, but for high-frequency data, we should consider partitioning the PostgreSQL table by time (e.g., using `django-postgres-extra` or native Postgres partitioning) in the future.

---

## 📅 Milestones & Issues

### Milestone 1: Core Backend & Data Ingestion
**Goal:** Finalize the database schema, API logic, and connect the backend to the MQTT broker for live data ingestion.

- [ ] **Issue 1.1: Implement MaintenanceLog Model**
  - **Details:** In `inventory/models/maintenance.py`, create a `MaintenanceLog` model linked to `Equipment`. Include fields for `author` (User), `description`, `action_taken`, and `timestamp`.
- [ ] **Issue 1.2: Build REST API Interfaces (DRF)**
  - **Details:** Create serializers, views, and API routers for `Equipment`, `HealthStatus`, and `MaintenanceLog` to allow the Next.js frontend to securely access and mutate data.
- [ ] **Issue 1.3: MQTT Telemetry Ingestion Service**
  - **Details:** Create a long-running Django management command (or a separate worker) utilizing `paho-mqtt` to subscribe to the Mosquitto broker, parse the incoming JSON payload from the ESP32, and save it to the `SensorReading` model.

### Milestone 2: Machine Learning Integration
**Goal:** Implement the asynchronous anomaly detection pipeline using Celery and Scikit-Learn.

- [ ] **Issue 2.1: Implement Isolation Forest Model logic**
  - **Details:** Create a utility service in the `telemetry` app that loads a pre-trained `IsolationForest` model (or trains one dynamically on a rolling window) and returns an anomaly score given recent vibration, temp, and voltage features.
- [ ] **Issue 2.2: Celery Task for Predictive Maintenance**
  - **Details:** Create a Celery task that runs every X minutes (via Celery Beat). For each active `Equipment`, it retrieves the latest `SensorReadings`, processes them through the ML utility, and generates a new `HealthStatus` record if the anomaly score exceeds the threshold.
- [ ] **Issue 2.3: Alerting & Webhooks (Optional)**
  - **Details:** When a `HealthStatus` is flagged as `CRITICAL`, trigger an email/SMS alert to park rangers or push a WebSocket notification.

### Milestone 3: Submodule & Deployment Automation
**Goal:** Ensure the master gateway repository handles both backend and frontend, and testing is robust.

- [ ] **Issue 3.1: Unit & Integration Tests**
  - **Details:** Write `pytest` test cases verifying API endpoints and the Celery ML pipeline mock behavior.
- [ ] **Issue 3.2: Docker Compose Orchestration Refinement**
  - **Details:** Update the master `docker-compose.yml` to spin up Mosquitto, Django, Celery Worker, Celery Beat, Redis, Postgres, and the Next.js target simultaneously.
- [ ] **Issue 3.3: GitHub Actions CI Pipeline**
  - **Details:** Add a `.github/workflows/ci.yml` that runs `ruff` linting and `pytest` on every PR.
  
### Milestone 4: User Authentication & Role-Based Access
**Goal:** Implement strict access control for the dashboards and ensure alerts are routed correctly based on user roles.

- [ ] **Issue 4.1: User Integration & Role-Based Alerting**
  - **Details:** Implement user roles (e.g., `Technician`, `Admin`, `Ranger`) by extending the custom Django `User` model. Then, update the `AlertService` to dynamically query the database and route critical hardware telemetry alerts strictly to users assigned the `Technician` or `Admin` roles instead of hard-coded settings.