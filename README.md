# agentforge-credentials-plugin

Credential vault resolution test rig for AgentForge (TAP-764).

Exercises the full EPIC-39 credential pipeline end-to-end:
`SecretStore` → `resolve_for_agent()` → `CredentialContext` — without an LLM or
external service.

## Structure

```
agentforge_credentials/
  __init__.py          # __version__
  plugin.json          # plugin manifest (namespace: project.credentials-test)
  plugin.py            # register(app) entry point
  routes.py            # GET /api/credentials-test/status
                       # POST /api/credentials-test/check
  agents/
    credentials_test_agent/
      AGENT.md         # declares credentials: [{key: test-rig-key}]
      runner.py        # CredentialsRunner.run() → "credentials:ok"
tests/
  test_runner.py       # unit tests for CredentialsRunner
backend/tests/
  test_credentials_smoke.py   # in AgentForge repo — SecretStore CRUD + resolver
```

## What it tests

- `SecretStore` CRUD: `create` / `get_value` / `update` / `delete`
- `list_audit()` records operations correctly
- Scope isolation: two keys with same name in different scopes are independent
- `resolve_for_agent()` returns a populated `CredentialContext` when the key is in the vault
- `resolve_for_agent()` returns the key in the `missing` list when absent (fail-fast path)

## Install

```bash
pip install -e /path/to/agentforge-credentials-plugin
```

The plugin self-registers via `agentforge.plugins` entry point. The smoke tests in
`backend/tests/test_credentials_smoke.py` are gated with
`@pytest.mark.skipif(not _plugin_installed(), ...)` so the AgentForge test suite
always passes whether or not the plugin is installed.

## Key API facts (from reading the source)

| API | Signature |
|---|---|
| `SecretStore.__init__` | `(db_path, master_key: bytes, key_version=1)` |
| `SecretStore.create` | `(key_name, value, scope="global", requester="") -> SecretMetadata` |
| `SecretStore.get_value` | `(key_name, scope="global", requester="") -> str | None` |
| `SecretStore.update` | `(key_name, value, scope="global", requester="") -> SecretMetadata | None` |
| `SecretStore.delete` | `(key_name, scope="global", requester="") -> bool` |
| `SecretStore.list_audit` | `(key_name=None, scope=None, operation=None, limit=100) -> list[AuditEntry]` |
| `resolve_for_agent` | `(config: AgentConfig, secret_store) -> tuple[CredentialContext, list[str]]` |
| `CredentialContext.resolved` | `dict[str, str]` — key → plaintext value |

`resolve_for_agent` is in `backend.core.credential_injector` (not `credential_resolver`).
