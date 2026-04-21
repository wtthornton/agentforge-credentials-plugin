"""Unit tests for CredentialsRunner."""

from __future__ import annotations

from agentforge_credentials.agents.credentials_test_agent.runner import (
    CredentialsRunner,
)


def test_runner_returns_ok() -> None:
    runner = CredentialsRunner()
    assert runner.run("anything") == "credentials:ok"


def test_runner_ignores_input() -> None:
    runner = CredentialsRunner()
    assert runner.run("") == "credentials:ok"
    assert runner.run("some text") == "credentials:ok"
