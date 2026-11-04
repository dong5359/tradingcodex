from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

import pytest
import yaml
from markdown_it import MarkdownIt

from tradingcodex_cli.generator import bootstrap_workspace
from tradingcodex_service.application.agents import AGENT_SPECS, SKILL_SPECS


@pytest.fixture(autouse=True)
def isolated_generation_runtime(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRADINGCODEX_PYTHON", sys.executable)
    monkeypatch.setenv("TRADINGCODEX_TEST_SCRATCH_ROOT", str(tmp_path / "scratch-root"))


def test_expectations_bundle_is_discoverable_and_portable(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)

    assert "tcx-expectations" in AGENT_SPECS["head-manager"].builtin_skills
    assert SKILL_SPECS["tcx-expectations"].user_visible is True
    config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
    assert any(
        item["path"] == "../.agents/skills/tcx-expectations/SKILL.md"
        and item["enabled"] is True
        for item in config["skills"]["config"]
    )

    bundle = root / ".agents/skills/tcx-expectations"
    for relative in (
        "SKILL.md", "agents/openai.yaml", "agents/expectations-analyst.md",
        "references/scenario-design.md", "references/evidence-collection.md",
        "references/behavioral-cases.md",
    ):
        assert (bundle / relative).is_file(), relative
    metadata = yaml.safe_load((bundle / "agents/openai.yaml").read_text(encoding="utf-8"))
    assert metadata["policy"]["allow_implicit_invocation"] is True

    # Validate actual generated links, including cross-bundle valuation routing.
    documents = list(bundle.rglob("*.md")) + [
        root / ".agents/skills/tcx-workflow/SKILL.md",
        root / ".tradingcodex/subagents/skills/valuation-analyst/tcx-valuation/SKILL.md",
    ]
    for document in documents:
        text = document.read_text(encoding="utf-8")
        assert not re.search(r"[A-Za-z]:[\\/]Users[\\/]", text)
        links = (
            child.attrGet("href")
            for token in MarkdownIt().parse(text)
            for child in (token.children or [])
            if child.type == "link_open"
        )
        for link in links:
            if re.match(r"https?://|#", link):
                continue
            target = (document.parent / link.split("#", 1)[0]).resolve()
            assert target.is_relative_to(root.resolve()), (document, link)
            assert target.exists(), (document, link)

    # This specialty must not create a privileged or falsely authenticated role.
    assert "expectations-analyst" not in AGENT_SPECS
    assert not (root / ".codex/agents/expectations-analyst.toml").exists()


def test_update_keeps_expectations_resources_and_user_owned_content(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)
    personal = root / "VALUATION_GUIDELINES.md"
    personal.write_text("User-owned preferences must survive an update.\n", encoding="utf-8")
    bootstrap_workspace(root, update=True)

    assert personal.read_text(encoding="utf-8") == "User-owned preferences must survive an update.\n"
    bundle = root / ".agents/skills/tcx-expectations"
    assert (bundle / "agents/expectations-analyst.md").is_file()
    assert (bundle / "references/scenario-design.md").is_file()
