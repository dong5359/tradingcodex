"""Create a user-owned persona Brain source; never install or update one.

Standard library only, so this helper runs without application runtime access.
The canonical Brain service remains responsible for validation and lifecycle.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

SKILL_ROOT = Path(__file__).resolve().parents[1]


def create_source(
    workspace: Path,
    *,
    template: str,
    brain_id: str,
    name: str,
    publisher: str,
    license_name: str,
    version: str = "1.0.0",
) -> Path:
    if not re.fullmatch(r"investment-brain-[a-z0-9]+(?:-[a-z0-9]+)*", brain_id):
        raise ValueError("Use a lowercase hyphen-case investment-brain-* id.")
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        raise ValueError("Use a numeric major.minor.patch version.")
    for label, value in (("name", name), ("publisher", publisher), ("license", license_name)):
        if not value.strip() or "\n" in value or "\r" in value:
            raise ValueError(f"{label} must be a nonempty single line.")

    references = SKILL_ROOT / "references"
    catalog = json.loads((references / "catalog.json").read_text(encoding="utf-8"))
    entries = {item["id"]: item for item in catalog["personas"]}
    if template not in entries:
        raise ValueError(f"Unknown template. Choose one of: {', '.join(entries)}")
    entry = entries[template]
    description = f"Apply a personal investment lens inspired by {entry['name']}, with explicit scope and falsifiers."
    skill = (
        "---\n"
        f"name: {brain_id}\n"
        f"description: {json.dumps(description, ensure_ascii=False)}\n"
        "---\n\n"
        f"# {name}\n\n"
        "Read [personal method](references/method.md) first, then the "
        "[starting lens](references/persona.md). Explicit personal adaptations "
        "take precedence over the starting lens. Preserve unresolved conflicts "
        "and missing inputs rather than inventing a method. Treat current "
        "evidence as capable of falsifying either lens.\n\n"
        "For review and improvement, apply [learning principles]"
        "(references/review-principles.md). Return bounded hypotheses, "
        "counterexamples, and validation needs; do not silently change principles.\n\n"
        "This is an inspired analytical perspective, not the named investor "
        "or an endorsement. Retain the [source attribution]"
        "(references/upstream-license.md).\n"
    )
    manifest = {
        "format": "tradingcodex.investment-brain",
        "schema_version": 1,
        "type": "investment-brain",
        "id": brain_id,
        "version": version,
        "skill": "skill",
        "source": {"publisher": publisher, "license": license_name},
    }
    metadata = {
        "interface": {
            "display_name": name,
            "short_description": "Personal investment lens and review principles",
            "default_prompt": "Use $" + brain_id + " for this investment analysis.",
        },
        "policy": {"allow_implicit_invocation": False},
    }
    # JSON is a YAML subset; escaping user text is independent of YAML syntax.
    files = {
        ".tradingcodex/plugin.json": json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        "skill/SKILL.md": skill,
        "skill/agents/openai.yaml": json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        "skill/references/persona.md": (references / "personas" / f"{template}.md").read_text(encoding="utf-8"),
        "skill/references/upstream-license.md": (references / "upstream-license.md").read_text(encoding="utf-8"),
        "skill/references/review-principles.md": (references / "review-principles.md").read_text(encoding="utf-8"),
        "skill/references/method.md": (
            "# Personal method — draft\n\n"
            "No personal method has been supplied yet. The starting lens is a "
            "reference, not a claim that personalization is complete.\n\n"
            "- Intended horizon and market scope: not specified.\n"
            "- Evidence priorities and competence limits: not specified.\n"
            "- General thesis, falsifiers, and abstention criteria: not specified.\n"
            "- Adaptations to the starting lens and conflicts: not specified.\n"
            "- Strengths to preserve and weaknesses to test: not specified.\n\n"
            "Replace these unknowns only with explicitly supplied general "
            "principles. Keep private cases and personal account facts out "
            "of this portable document.\n"
        ),
    }

    workspace = workspace.resolve(strict=True)
    parent = workspace / "investment-brains"
    if parent.is_symlink() or parent.resolve() != parent:
        raise ValueError("The source parent must be a real workspace-local directory.")
    parent.mkdir(exist_ok=True)
    destination = parent / brain_id
    # Exclusive creation also rejects a symlink or an existing source.
    destination.mkdir(exist_ok=False)
    for relative, content in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True)
    parser.add_argument("--id", dest="brain_id", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--publisher", required=True)
    parser.add_argument("--license", dest="license_name", required=True)
    parser.add_argument("--version", default="1.0.0")
    args = parser.parse_args()
    try:
        path = create_source(Path.cwd(), **vars(args))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Source not created: {error}\n")
    print(json.dumps({"source": str(path.relative_to(Path.cwd().resolve())), "status": "draft",
                      "next": "Personalize, then validate through the Brain service."}))


if __name__ == "__main__":
    main()
