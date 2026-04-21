"""Deterministic runner for credentials-test-agent."""

from __future__ import annotations


class CredentialsRunner:
    def run(self, input_text: str) -> str:
        return "credentials:ok"
