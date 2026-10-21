"""Regress the OCI analysis failure with the actual shared transport principal."""
from __future__ import annotations

import copy
import json
import tomllib
from pathlib import Path

import pytest

from tradingcodex_service.application.agents import (
    AGENT_SPECS, _project_agent_toml, _project_head_manager_prompt,
)
from tradingcodex_service.application.analysis_runs import begin_analysis_run
from tradingcodex_service.application.artifact_bindings import verify_authenticated_artifact_binding
from tradingcodex_service.application.research import find_workspace_research_artifact_read_only
from tradingcodex_service.application.runtime import ensure_workspace_manifest
from tradingcodex_service.mcp_runtime import call_mcp_tool, handle_mcp_rpc

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def handoff(tmp_path: Path) -> tuple[Path, dict]:
    ensure_workspace_manifest(tmp_path)
    begin_analysis_run(tmp_path, "Analyze the supplied public filing.", run_id="analysis-inherited", apply_investor_context=False)
    snapshot = call_mcp_tool(tmp_path, "record_source_snapshot", {
        "provider": "Issuer filing", "source_category": "issuer_release",
        "source_locator": "https://example.test/filing", "coverage_note": "Test fixture, not investment evidence.",
        "payload": {"excerpt": "Revenue was 100."},
    }, transport_principal="head-manager")
    return tmp_path, {
        "artifact_id": "handoff-fundamental", "artifact_type": "evidence_pack",
        "title": "Recorded specialist handoff", "universe": "public_equity",
        "markdown": "# Research handoff\n\nThe fundamental specialist reported revenue of 100. Source: https://example.test/filing. Recorded by Head Manager; no independent specialist authentication.\n",
        "summary": "Sourced child findings recorded by the coordinator.",
        "status": {"handoff": "accepted", "evidence_readiness": "factual", "action_readiness": "research-only", "confidence": "medium", "confidence_basis": "Supplied source excerpt.", "missing_evidence": [], "blocked_actions": ["orders", "approval"]},
        "lineage": {"workflow_run_id": "analysis-inherited", "knowledge_cutoff": snapshot["recorded_at"], "source_snapshot_ids": [snapshot["snapshot_id"]], "input_artifact_ids": [], "dataset_ids": [], "calculation_run_ids": []},
        "requirements": [],
    }


def test_shared_transport_records_sources_handoff_and_synthesis(handoff, monkeypatch):
    root, payload = handoff
    monkeypatch.setenv("TRADINGCODEX_MCP_PRINCIPAL", "head-manager")
    rpc = handle_mcp_rpc(root, {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "create_research_artifact", "arguments": payload}})
    assert rpc["result"]["isError"] is False, rpc
    stored = find_workspace_research_artifact_read_only(root, "handoff-fundamental")
    assert stored["producer_role"] == "head-manager"
    assert verify_authenticated_artifact_binding(root, stored)["receipt_hash"]
    synthesis = copy.deepcopy(payload)
    synthesis.pop("artifact_id")
    synthesis["artifact_type"] = "synthesis_report"
    synthesis["lineage"]["input_artifact_ids"] = ["handoff-fundamental"]
    call_mcp_tool(root, "create_research_artifact", synthesis, transport_principal="head-manager")
    final = find_workspace_research_artifact_read_only(root, "synthesis-analysis-inherited")
    assert verify_authenticated_artifact_binding(root, final)["receipt_hash"]
    assert final["input_artifact_ids"] == ["handoff-fundamental"]


@pytest.mark.parametrize("readiness", ["portfolio-review", "draft-eligible", "blocked"])
def test_coordinator_evidence_cannot_gain_action_readiness(handoff, readiness):
    root, payload = handoff
    payload["status"]["action_readiness"] = readiness
    payload["status"]["evidence_readiness"] = "decision-grade"
    with pytest.raises(PermissionError, match="research-only"):
        call_mcp_tool(root, "create_research_artifact", payload, transport_principal="head-manager")


def test_coordinator_handoff_requires_recorded_sources(handoff):
    root, payload = handoff
    payload["lineage"]["source_snapshot_ids"] = []
    with pytest.raises(ValueError, match="source_snapshot_ids"):
        call_mcp_tool(root, "create_research_artifact", payload, transport_principal="head-manager")


def test_inherited_connection_cannot_claim_specialist_or_approval(handoff):
    root, payload = handoff
    payload["principal_id"] = "fundamental-analyst"
    with pytest.raises(PermissionError, match="does not match"):
        call_mcp_tool(root, "create_research_artifact", payload, transport_principal="head-manager")
    with pytest.raises(PermissionError, match="not allowed"):
        call_mcp_tool(root, "request_order_approval", {}, transport_principal="head-manager")


def test_parent_handoff_does_not_satisfy_independent_review(handoff):
    root, payload = handoff
    call_mcp_tool(root, "create_research_artifact", payload, transport_principal="head-manager")
    synthesis = copy.deepcopy(payload)
    synthesis.pop("artifact_id")
    synthesis["artifact_type"] = "synthesis_report"
    synthesis["status"]["evidence_readiness"] = "decision-grade"
    synthesis["status"]["action_readiness"] = "draft-eligible"
    synthesis["lineage"]["input_artifact_ids"] = ["handoff-fundamental"]
    with pytest.raises(ValueError, match="portfolio-manager and risk-manager"):
        call_mcp_tool(root, "create_research_artifact", synthesis, transport_principal="head-manager")


def test_projection_uses_supported_child_instructions_and_is_idempotent(tmp_path):
    base = ROOT / "workspace_templates/modules/codex-base/files/.codex"
    prompts = tmp_path / ".codex/prompts/base_instructions"
    prompts.mkdir(parents=True)
    for name in ("fixed-role.md", "head-manager.md"):
        (prompts / name).write_text((base / "prompts/base_instructions" / name).read_text(encoding="utf-8"), encoding="utf-8")
    config = tmp_path / ".codex/config.toml"
    config.write_text('[permissions.trading-research]\nextends = ":workspace"\n', encoding="utf-8")
    _project_head_manager_prompt(tmp_path)
    first_root = config.read_bytes()
    _project_head_manager_prompt(tmp_path)
    assert config.read_bytes() == first_root
    assert "developer_instructions" in tomllib.loads(config.read_text(encoding="utf-8"))
    roles = ROOT / "workspace_templates/modules/fixed-subagents/files/.codex/agents"
    target = tmp_path / ".codex/agents"
    target.mkdir()
    for template in roles.glob("*.toml"):
        path = target / template.name
        path.write_bytes(template.read_bytes())
        _project_agent_toml(tmp_path, template.stem, [])
        first = path.read_bytes()
        _project_agent_toml(tmp_path, template.stem, [])
        assert path.read_bytes() == first
        role = tomllib.loads(path.read_text(encoding="utf-8"))
        assert "mcp_servers" not in role
        assert "model_instructions_file" not in role
        assert "Your assigned specialist role" in role["developer_instructions"]
        assert role["name"] == template.stem
    assert "record_source_snapshot" in AGENT_SPECS["head-manager"].mcp_allowlist
