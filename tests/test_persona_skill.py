from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

from tradingcodex_cli.generator import bootstrap_workspace
from tradingcodex_service.application.agents import EXPECTED_SUBAGENTS, build_projection_state
from tradingcodex_service.application.analysis_runs import begin_analysis_run
from tradingcodex_service.application.investment_brains import (
    install_investment_brain,
    rollback_investment_brain,
    set_investment_brain_status,
    update_investment_brain,
    validate_investment_brain_bundle,
)

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "workspace_templates/modules/repo-skills/files/.agents/skills/tcx-persona"
CATALOG = json.loads((SKILL / "references/catalog.json").read_text(encoding="utf-8"))
spec = importlib.util.spec_from_file_location("persona_scaffold", SKILL / "scripts/create_persona.py")
scaffold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scaffold)


def _create(workspace: Path, template: str = "warren-buffett") -> Path:
    return scaffold.create_source(
        workspace, template=template, brain_id="investment-brain-my-quality",
        name="My Quality", publisher="Workspace owner", license_name="MIT",
    )


@pytest.mark.parametrize("entry", CATALOG["personas"], ids=lambda entry: entry["id"])
def test_every_persona_creates_valid_attributed_brain(tmp_path: Path, entry: dict) -> None:
    source = _create(tmp_path, entry["id"])
    bundle = validate_investment_brain_bundle(source)
    assert bundle.manifest["id"] == "investment-brain-my-quality"
    assert bundle.manifest["version"] == "1.0.0"
    assert entry["name"] in (source / "skill/references/persona.md").read_text(encoding="utf-8")
    attribution = (source / "skill/references/upstream-license.md").read_text(encoding="utf-8")
    assert CATALOG["revision"] in attribution
    assert "Copyright (c) 2026 monarchjuno" in attribution
    assert "Permission is hereby granted" in attribution
    assert "not specified" in (source / "skill/references/method.md").read_text(encoding="utf-8")
    assert not (tmp_path / ".tradingcodex").exists()


def test_scaffold_rejects_overwrite_and_invalid_inputs_without_changes(tmp_path: Path) -> None:
    source = _create(tmp_path)
    before = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
    with pytest.raises(FileExistsError):
        _create(tmp_path)
    after = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
    assert before == after
    for kwargs in (
        {"brain_id": "../escape"},
        {"template": "../warren-buffett"},
        {"version": "1.0"},
        {"publisher": ""},
    ):
        arguments = dict(template="warren-buffett", brain_id="investment-brain-invalid",
                         name="Personal", publisher="Me", license_name="MIT")
        arguments.update(kwargs)
        with pytest.raises(ValueError):
            scaffold.create_source(tmp_path, **arguments)
    assert not (tmp_path / "investment-brains/investment-brain-invalid").exists()


def test_generated_persona_is_root_only_and_helper_works_offline(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    bootstrap_workspace(workspace)
    state = build_projection_state(workspace)
    assert len(EXPECTED_SUBAGENTS) == 9
    assert state["skills"]["tcx-persona"]["implicit_invocation"] is True
    assert state["skills"]["tcx-persona"]["owner_roles"] == ["head-manager"]
    assert "tcx-persona" in state["agents"]["head-manager"]["projected_skills"]
    for role in EXPECTED_SUBAGENTS:
        assert "tcx-persona" not in state["agents"][role]["effective_skills"]
    generated = workspace / ".agents/skills/tcx-persona"
    assert list(generated.rglob("SKILL.md")) == [generated / "SKILL.md"]
    assert len(list((generated / "references/personas").glob("*.md"))) == 13
    # An ordinary interpreter can scaffold without importing the service.
    result = subprocess.run(
        [sys.executable, "-I", str(generated / "scripts/create_persona.py"),
         "--template", "peter-lynch", "--id", "investment-brain-my-lynch",
         "--name", "My Lynch", "--publisher", "Me", "--license", "MIT"],
        cwd=workspace, capture_output=True, text=True, check=True,
    )
    receipt = json.loads(result.stdout)
    assert receipt["status"] == "draft"
    validate_investment_brain_bundle(workspace / receipt["source"])
    assert not (workspace / ".agents/skills/investment-brain-my-lynch").exists()


def test_personal_revision_preserves_run_version_and_can_roll_back(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    bootstrap_workspace(workspace)
    source = _create(workspace)
    brain_id = "investment-brain-my-quality"
    method = source / "skill/references/method.md"
    method.write_text("# Personal method\n\nRequire durable cash flows and abstain when leverage is unclear.\n", encoding="utf-8")
    baseline = install_investment_brain(workspace, local_source=source, active=False, actor="test")
    with pytest.raises(ValueError, match="not active"):
        begin_analysis_run(workspace, "$" + brain_id, run_id="inactive-persona")
    set_investment_brain_status(workspace, brain_id, "active", actor="test")
    before = begin_analysis_run(workspace, "$" + brain_id, run_id="persona-before")
    alias = begin_analysis_run(workspace, "$tcx-persona Use Warren Buffett.", run_id="persona-alias")
    assert alias["investment_brain_binding"]["brain_id"] == ""
    with pytest.raises(ValueError, match="exactly one"):
        begin_analysis_run(workspace, "$" + brain_id + " $investment-brain-second", run_id="persona-multiple")
    method.write_text("# Personal method\n\nRequire durable cash flows, examine cyclicality, and abstain when leverage is unclear.\n", encoding="utf-8")
    manifest_path = source / ".tradingcodex/plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = "1.0.1"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    changed = update_investment_brain(workspace, brain_id, local_source=source, actor="test")
    after = begin_analysis_run(workspace, "$" + brain_id, run_id="persona-after")
    assert before["investment_brain_binding"]["version"] == "1.0.0"
    assert after["investment_brain_binding"]["version"] == "1.0.1"
    assert changed["content_digest"] != baseline["content_digest"]
    frozen = json.loads((workspace / ".tradingcodex/mainagent/runs/persona-before/run.json").read_text(encoding="utf-8"))
    assert frozen["investment_brain_binding"] == before["investment_brain_binding"]
    rollback_investment_brain(workspace, brain_id, version="1.0.0", actor="test")
    restored = begin_analysis_run(workspace, "$" + brain_id, run_id="persona-restored")
    assert restored["investment_brain_binding"]["content_digest"] == baseline["content_digest"]
