Continuous Deployment Architecture
==================================

The Upemba Backend repository natively supports two mutually independent deployment pathways for edge routing to local infrastructure (e.g., Raspberry Pi servers).

Option A: Automated CI/CD (GitHub Self-Hosted Runner)
-----------------------------------------------------

This is the primary enterprise deployment strategy, ensuring code is delivered 100% autonomously every time a developer merges code into the ``main`` branch on GitHub.

1. A **GitHub Actions Self-Hosted Runner** is permanently installed into the Raspberry Pi as an active systemd background daemon (``sudo ./svc.sh start``).
2. The code passes the rigorous CI checks (Pytest, Ruff, Node24 configurations).
3. GitHub automatically pings the Raspberry Pi, transferring control to the local hardware.
4. The Raspberry Pi systematically clones the latest code strictly into the ``~/actions-runner/_work/...`` sandbox.
5. The pipeline gracefully forces the Pi to copy its secured Local Area Network environment variables (``cp -r ~/upemba-backend/.envs ./``) into the active shell.
6. The entire Docker cluster natively regenerates (``docker compose ... up -d --build``) and routes out the Traefik proxies.

Option B: Manual Fallback Shell Execution (Local RSYNC)
-------------------------------------------------------

If the global GitHub infrastructure goes offline, or if the developer wishes to bypass the CI pipeline locally without an internet connection natively from their terminal, we execute the exact fallback protocol explicitly designed via ``deploy.sh``.

.. code-block:: bash

    chmod +x deploy.sh
    ./deploy.sh

**Mechanism of Action:**
1. The script establishes a direct local area SSH Bridge from the developer laptop direct to the Pi (e.g., ``192.168.1.72``).
2. It utilizes ``rsync`` mathematically to delta-compare the entire codebase, uploading exclusively files that changed (reducing network load directly).
3. The script forces the hardware backend API to execute raw Docker Compose shutdown and rebuild instructions manually without ever pinging the open internet.

Bypassing Strict Internet HTTPS (Traefik)
-----------------------------------------
Because the pipeline is geared for a Raspberry Pi local IP natively lacking a top-level domain, the default Let's Encrypt certificates are bypassed physically in ``compose/production/traefik/traefik.yml``, forcing Traefik to permit ``http://192.168.1.72/`` connections directly without throwing 404 security checks.
