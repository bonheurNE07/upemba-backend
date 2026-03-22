# Centralized Settings Documentation

This configuration repository houses the absolute environment overrides dictating how the Upemba backend morphs depending on the execution sphere (Local vs Production vs Edge).

## The Environment Architecture
- `config/settings/base.py`: The universal truth. This file loads `django-environ`, registers all Third-Party plugins (Celery, Allauth, DRF), and connects to Mosquitto.
- `config/settings/local.py`: The development sandbox. It forcefully overrides caching schemas to execute dummy caches and injects aggressive debug toolbars (like `django-debug-toolbar`) for engineering velocity.
- `config/settings/production.py`: The physical hardened layer. It natively binds Anymail SMTP hooks, activates strict PostgreSQL connection constraints, and explicitly governs Traefik web interactions.

## Edge Deployment Toggles (Traefik Overrides)
File: `config/settings/production.py`

When deploying strictly to the Local Area Network (IoT Edge), strict Internet HTTPS checks must be decoupled:
1. `SECURE_SSL_REDIRECT` maps structurally to the `.envs` override. If toggled off, Django natively strips the `__Secure-` prefix from Session and CSRF Cookies.
2. `CSRF_TRUSTED_ORIGINS` mathematically accepts bare IP addresses natively to prevent `403 Forbidden` API timeouts during local field inspections by technicians.
