Machine Learning Anomaly Detection
==================================

The Upemba backend features a state-of-the-art native AI pipeline implementing **Scikit-Learn Isolation Forests** to perform predictive maintenance structurally.

The Isolation Forest Algorithm
------------------------------

The ``backend.telemetry.services.ml_service.AnomalyDetector`` class drives the analytical engine. The Isolation Forest algorithm isolates anomalous data points by randomly partitioning data sets. The fewer splits a data point requires to be isolated, the higher its anomaly score.

**Key Model Parameters:**
- ``n_estimators (100)``: Determines the total aggregate count of sub-trees generated globally to ensure stability.
- ``contamination (0.05)``: Structurally enforces that exactly 5% of historical background noise will be scrutinized as anomalous to ensure a tight predictive net.

Celery Task Orchestration
-------------------------

Predictions are never run exactly upon MQTT packet reception, as that would lock up the single-threaded listener. Instead, the backend relies on Celery (``celerybeat`` & ``celeryworker``).

1. The Background Task (``evaluate_equipment_health_task``) is triggered autonomously.
2. It iteratively fetches the **most recent 100 Sensor Readings** from PostgreSQL for every registered piece of equipment.
3. If less than 10 readings exist for an equipment piece, the model skips that device to prevent untrained predictive skewing.

Health Status Scoring Mechanism
-------------------------------

The resulting ``anomaly_score`` dictates the ``HealthStatus`` PostgreSQL record classification:

- **NORMAL (Score > 0)**: The machine is running precisely within established baseline tolerances.
- **WARNING (Score < 0 > -0.15)**: The machine is deviating significantly from standard telemetry paths, suggesting imminent degradation.
- **CRITICAL (Score < -0.15)**: The machine is actively in failure state.

Automatic Dispatch
------------------
If the result is graded ``CRITICAL``, the backend intentionally bypasses standard workflow and instantly triggers ``AlertService.trigger_critical_alert()``, dispatching an immediate email to Park Rangers/Technicians providing the exact node coordinates.
