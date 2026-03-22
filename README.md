# Upemba IoT Diagnostics Backend 🔋🌍
[![CI Pipeline](https://github.com/bonheurNE07/upemba-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/bonheurNE07/upemba-backend/actions)
[![CD Pipeline](https://github.com/bonheurNE07/upemba-backend/actions/workflows/deploy.yml/badge.svg)](https://github.com/bonheurNE07/upemba-backend/actions)
[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django)
[![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A high-performance, edge-deployed IoT aggregation engine designed to securely ingest telemetry from ESP32 microcontrollers, perform real-time **Scikit-Learn Machine Learning** predictive maintenance, and alert technicians of critical hardware anomalies natively across local intranet ecosystems.

---

## ⚡ Architecture & Tech Stack

- **Core Web Framework**: Django 5.x + Django Rest Framework (DRF)
- **IoT Payload Ingestion**: Eclipse Mosquitto (MQTT) & Paho-MQTT Python Daemon
- **Artificial Intelligence**: `scikit-learn` Isolation Forest (Unsupervised Anomaly Detection)
- **Asynchronous Task Queue**: Celery & Redis
- **Database Engine**: PostgreSQL 16
- **Reverse Proxy**: Traefik (Optimized for Edge IP Routing)
- **Container Orchestration**: Docker & Docker Compose
- **Continuous Integration**: GitHub Actions (Linting, Pytest, Automatic Edge Deployment)

## 📡 Hardware Integration (ESP32 / Microcontrollers)
This backend expects IoT edge devices to transmit JSON payloads matching strict PostgreSQL mappings.

### Mosquitto Routing
Devices should publish payloads natively every **30 seconds** structurally avoiding database overflow.
`Topic`: `upemba/sensors/<DEVICE_MAC_OR_ID>/telemetry`

### Expected JSON Schema
```json
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
```

## 🧠 Machine Learning: Predictive Maintenance

Upemba executes predictive analytics natively using the `IsolationForest` algorithm. A persistent `celerybeat` process scrapes the historical database every minute, fetching exactly the last 100 observations per device to generate an `anomaly_score`.

- **NORMAL**: Hardware behaves inside established historical constraints.
- **WARNING**: Hardware trends deviate beyond classical variances.
- **CRITICAL**: Immediate voltage/vibration failure detected. Automatically spawns instant SMTP alert notifications to all users registered with the `TECHNICIAN` role.

---

## 🚀 Edge Deployment (Raspberry Pi CI/CD)

This repository is built for **100% Autonomous Local Delivery**. Whenever code is pushed to the `main` branch, the GitHub Actions cloud runner establishes a direct communication bridge to the localized Edge Node (Raspberry Pi). 

If the Ruff linters and Pytest cases pass 100%, the runner natively pulls the code onto the Raspberry Pi, safely injects the local `.envs` variables from the sandbox, and recompiles the Docker infrastructure over Traefik natively bridging `192.168.1.x` networks.

### Manual Fallback Deployment
If the global internet goes down, developers can mathematically bypass CI/CD by utilizing the `deploy.sh` script which directly establishes an SSH RSYNC tunnel natively from laptop to Pi:
```bash
./deploy.sh
```

## 📚 Deep Codebase Documentation
For engineering teams extending the codebase, hyper-detailed markdown manuals predicting architectural flows exist natively embedded exactly alongside the code in the respective folders:

- `backend/telemetry/documentation/`
- `backend/inventory/documentation/`
- `backend/users/documentation/`
- `config/documentation/`

Additionally, an enterprise-grade HTML Sphinx website can be instantly generated graphically by executing `make html` inside the `docs/` repository!
