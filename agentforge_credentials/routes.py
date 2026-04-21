"""Credentials test plugin HTTP routes."""

from __future__ import annotations

from fastapi import APIRouter, Request

from agentforge_credentials import __version__

router = APIRouter(prefix="/api/credentials-test", tags=["credentials-test"])


@router.get("/status")
async def status() -> dict:
    return {"status": "ok", "plugin": "credentials-test", "version": __version__}


@router.post("/check")
async def check_credentials(request: Request) -> dict:
    loader = getattr(request.app.state, "agent_loader", None)
    secret_store = getattr(request.app.state, "secret_store", None)
    if loader is None or secret_store is None:
        return {"resolved": False, "reason": "missing dependencies"}

    config = loader.resolve("project.credentials-test.credentials-test-agent")
    if config is None:
        return {"resolved": False, "reason": "agent not found"}

    from backend.core.credential_injector import resolve_for_agent

    context, missing = await resolve_for_agent(config, secret_store)
    return {
        "resolved": len(missing) == 0,
        "missing": missing,
        "resolved_keys": list(context.resolved.keys()),
    }
