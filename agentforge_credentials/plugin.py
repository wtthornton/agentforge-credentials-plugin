"""AgentForge plugin entry point for agentforge-credentials-plugin.

`register(app)` is called by `PluginRegistry.register_plugin()`:
1. Mounts the credentials-test router onto the host FastAPI app.
2. Loads the credentials-test-agent into the host's AgentLoader (if present).
"""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI

logger = logging.getLogger(__name__)

_AGENTS_DIR = Path(__file__).parent / "agents"
_NAMESPACE = "project.credentials-test"


def register(app: FastAPI) -> None:
    from agentforge_credentials.routes import router

    app.include_router(router)

    agent_loader = getattr(app.state, "agent_loader", None)
    if agent_loader is None:
        logger.debug(
            "credentials-test plugin: no agent_loader on app.state — skipping agent load"
        )
        return

    try:
        newly_loaded = agent_loader.load_external(_AGENTS_DIR, _NAMESPACE)
        logger.info(
            "credentials-test plugin: loaded %d agent(s) from %s",
            len(newly_loaded),
            _AGENTS_DIR,
        )
    except Exception:
        logger.exception("credentials-test plugin: agent load failed")
