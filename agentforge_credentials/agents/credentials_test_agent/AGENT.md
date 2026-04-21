---
name: credentials-test-agent
namespace: project.credentials-test.credentials-test-agent
description: Test agent for credential vault resolution rig.
keywords: [credentials, vault, test]
model: sonnet
memory_profile: none
credentials:
  - key: test-rig-key
    scope: global
    required: true
runner: agentforge_credentials.agents.credentials_test_agent.runner:CredentialsRunner
---

# Credentials Test Agent

Deterministic test fixture that declares a single credential (`test-rig-key`) so the
credential vault resolution pipeline can be exercised end-to-end without an LLM.

Exists to verify `resolve_for_agent()` returns a populated `CredentialContext` when
the key is present in the vault, and returns it in the `missing` list when absent.
