# API Router URL Documentation

This document explains the global URL traversal routing engines exposing the Django Rest Framework securely to external endpoints.

## The Global Router
File: `config/api_router.py`

The Upemba backend natively relies on the `DefaultRouter` class from DRF to procedurally generate all ViewSet URLs without hardcoding string variables.

**Mappings:**
- `router.register("users", UserViewSet)` maps `/api/users/` exclusively to query the authentication structures.
- `router.register("inventory/equipment", EquipmentViewSet)` securely bridges the physical asset pipeline to the Next.js React frontend architectures.

## The App URL Inclusions
File: `config/urls.py`

This file is the root tree.
1. `/api/` maps directly sequentially to the DRF router logic.
2. `/api/schema/` automatically calculates the Swagger API metadata logic, utilizing `drf-spectacular` internally.
3. `/api/docs/` visibly renders the Swagger API definitions natively in the browser so engineers can inspect JSON inputs flawlessly.
