from __future__ import annotations

import os
import tomllib
from pathlib import Path

from tradingcodex_cli.generator import bootstrap_workspace
from tradingcodex_service.application.agents import AGENT_SPECS, RESEARCH_ROLES, SKILL_SPECS
from tradingcodex_service.application.data_sources import disable_openbb, enable_openbb
from tradingcodex_service.mcp_runtime import TOOL_REGISTRY


def test_openbb_is_a_direct_optional_inherited_projection(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)

    assert "tcx-openbb" not in SKILL_SPECS
    assert "record_external_data_result" not in TOOL_REGISTRY
    assert "fetch_official_source_data" not in TOOL_REGISTRY
    for role in RESEARCH_ROLES:
        assert "tcx-openbb" not in AGENT_SPECS[role].builtin_skills
        config = tomllib.loads((root / f".codex/agents/{role}.toml").read_text(encoding="utf-8"))
        assert "mcp_servers" not in config
        openbb = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))["mcp_servers"]["openbb"]
        assert openbb["command"] == "uvx"
        assert openbb["args"] == [
            "--from", "openbb-mcp-server", "--with", "openbb", "openbb-mcp",
            "--transport", "stdio",
        ]
        assert openbb["enabled"] is True
        assert openbb["required"] is False
        assert openbb["env_vars"] == []

    for path in (root / ".codex/agents").glob("*.toml"):
        if path.stem in RESEARCH_ROLES:
            continue
        config = tomllib.loads(path.read_text(encoding="utf-8"))
        assert "openbb" not in config.get("mcp_servers", {})


def test_dashboard_skill_is_retired_in_favor_of_session_links(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)

    assert "tcx-dashboard" not in SKILL_SPECS
    assert not (root / ".agents/skills/tcx-dashboard").exists()
    config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
    skill_paths = {item["path"] for item in config["skills"]["config"]}
    assert "../.agents/skills/tcx-dashboard/SKILL.md" not in skill_paths


def test_wiki_skill_discloses_only_materially_used_pages() -> None:
    skill_path = (
        Path(__file__).resolve().parents[1]
        / "workspace_templates/modules/repo-skills/files/.agents/skills/tcx-wiki/SKILL.md"
    )
    skill_text = skill_path.read_text(encoding="utf-8")

    assert "When Wiki background materially affects the answer" in skill_text
    assert "`Wiki used:`" in skill_text
    assert "workspace-relative paths of pages actually" in skill_text
    assert "Omit the line when no Wiki page materially affected the answer" in skill_text


def test_investor_context_uses_native_workspace_file_edits(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)
    skill_text = (root / ".agents/skills/tcx-investor-context/SKILL.md").read_text(encoding="utf-8")
    config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))

    assert "ordinary user-owned workspace file" in skill_text
    assert "native `apply_patch`" in skill_text
    assert "never prefix the workspace path or use an absolute" in skill_text
    assert "duplicated workspace path is not valid verification" in skill_text
    assert "do not add an MCP service" in skill_text
    assert "terminal handoff" not in skill_text
    assert "User-Terminal Commands" not in skill_text
    for profile in ("trading-research", "trading-build"):
        roots = config["permissions"][profile]["filesystem"][":workspace_roots"]
        assert roots[".tradingcodex"] == "deny"
        assert roots[".tradingcodex/user"] == ("read" if os.name == "nt" else "write")


def test_openbb_enable_projects_env_names_only(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)
    enable_openbb(root, ["FMP_API_KEY"])
    bootstrap_workspace(root, update=True)

    config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
    assert config["mcp_servers"]["openbb"]["enabled"] is True
    assert config["mcp_servers"]["openbb"]["env_vars"] == ["FMP_API_KEY"]


def test_openbb_explicit_disable_survives_workspace_update(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)
    disable_openbb(root)

    bootstrap_workspace(root, update=True)

    config = tomllib.loads((root / ".codex/config.toml").read_text(encoding="utf-8"))
    assert config["mcp_servers"]["openbb"]["enabled"] is False


def test_update_preserves_user_openbb_instead_of_duplicate_default(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    bootstrap_workspace(root)
    path = root / ".codex/config.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("# BEGIN TradingCodex managed OpenBB")
    end = text.index("# END TradingCodex managed OpenBB") + len("# END TradingCodex managed OpenBB")
    custom = '[mcp_servers.openbb]\nurl = "https://example.test/user-openbb"\nenabled = false\n'
    path.write_text(text[:start] + custom + text[end:], encoding="utf-8")
    bootstrap_workspace(root, update=True)
    bootstrap_workspace(root, update=True)
    config = tomllib.loads(path.read_text(encoding="utf-8"))
    assert config["mcp_servers"]["openbb"] == {
        "url": "https://example.test/user-openbb", "enabled": False,
    }
