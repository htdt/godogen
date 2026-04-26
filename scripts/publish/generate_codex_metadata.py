"""Write each skill's agents/openai.yaml from its SKILL.md frontmatter."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def parse_frontmatter(path: Path) -> dict[str, str | bool]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    lines = text[4:end].splitlines()
    data: dict[str, str | bool] = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        if not line.strip() or ":" not in line:
            idx += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "|":
            idx += 1
            block: list[str] = []
            while idx < len(lines):
                candidate = lines[idx]
                if candidate and not candidate.startswith(" ") and ":" in candidate:
                    break
                block.append(candidate[2:] if candidate.startswith("  ") else candidate)
                idx += 1
            data[key] = "\n".join(block).strip()
            continue
        if value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip('"').strip("'")
        idx += 1
    return data


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_]+", name) if part)


def write_openai_yaml(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return

    meta = parse_frontmatter(skill_file)
    name = str(meta.get("name") or skill_dir.name)
    description = " ".join(str(meta.get("description") or "").split())
    if len(description) > 120:
        description = description[:117].rstrip() + "..."
    display_name = str(meta.get("display_name") or title_from_name(name))
    short_description = str(meta.get("short_description") or description or display_name)
    default_prompt = str(
        meta.get("default_prompt") or f"Use ${name} when this skill is relevant."
    )

    lines = [
        "interface:",
        f"  display_name: {json.dumps(display_name)}",
        f"  short_description: {json.dumps(short_description)}",
        f"  default_prompt: {json.dumps(default_prompt)}",
    ]
    if "allow_implicit_invocation" in meta:
        flag = "true" if bool(meta["allow_implicit_invocation"]) else "false"
        lines.extend(["", "policy:", f"  allow_implicit_invocation: {flag}"])

    agents_dir = skill_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (agents_dir / "openai.yaml").write_text("\n".join(lines) + "\n")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: generate_codex_metadata.py <skills_root>", file=sys.stderr)
        return 2

    skills_root = Path(argv[1])
    for skill_dir in sorted(p for p in skills_root.iterdir() if p.is_dir()):
        write_openai_yaml(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
