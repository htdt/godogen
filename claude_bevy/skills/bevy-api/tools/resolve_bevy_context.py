#!/usr/bin/env python3
"""Resolve the current Bevy lookup context for a target Cargo project."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = SKILL_ROOT / "docs"
RUSTDOC_ROOT = DOCS_ROOT / "rustdoc"
BEVY_REPO_ROOT = DOCS_ROOT / "bevy"
BEVY_WEBSITE_ROOT = DOCS_ROOT / "bevy-website"


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def find_cargo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent

    manifest_root = None
    for candidate in (current, *current.parents):
        if (candidate / "Cargo.toml").is_file():
            manifest_root = candidate
            break

    if manifest_root is None:
        raise FileNotFoundError(f"no Cargo.toml found from {start}")

    workspace_root = manifest_root
    for candidate in (manifest_root, *manifest_root.parents):
        manifest_path = candidate / "Cargo.toml"
        if not manifest_path.is_file():
            continue
        doc = load_toml(manifest_path)
        workspace = doc.get("workspace")
        if not isinstance(workspace, dict):
            continue
        if candidate == manifest_root:
            workspace_root = candidate
            continue
        members = workspace_members(candidate, doc)
        if manifest_root in members:
            workspace_root = candidate

    return workspace_root


def iter_dependency_tables(doc: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    tables: list[tuple[str, dict[str, Any]]] = []
    for key in ("dependencies", "dev-dependencies", "build-dependencies"):
        value = doc.get(key)
        if isinstance(value, dict):
            tables.append((key, value))

    targets = doc.get("target")
    if isinstance(targets, dict):
        for target_name, target_doc in targets.items():
            if not isinstance(target_doc, dict):
                continue
            for key in ("dependencies", "dev-dependencies", "build-dependencies"):
                value = target_doc.get(key)
                if isinstance(value, dict):
                    tables.append((f"target.{target_name}.{key}", value))

    return tables


def workspace_members(root: Path, manifest: dict[str, Any]) -> list[Path]:
    workspace = manifest.get("workspace")
    if not isinstance(workspace, dict):
        return []

    members = workspace.get("members")
    if not isinstance(members, list):
        return []

    excludes = {
        path.resolve()
        for item in workspace.get("exclude", [])
        if isinstance(item, str)
        for path in root.glob(item)
    }

    results: list[Path] = []
    seen: set[Path] = set()
    for item in members:
        if not isinstance(item, str):
            continue
        for match in root.glob(item):
            manifest_path = match / "Cargo.toml"
            if not manifest_path.is_file():
                continue
            resolved = match.resolve()
            if resolved in excludes or resolved in seen:
                continue
            results.append(resolved)
            seen.add(resolved)
    return results


def dep_version_text(dep: Any, workspace_deps: dict[str, Any] | None, name: str) -> str | None:
    if isinstance(dep, str):
        return dep
    if not isinstance(dep, dict):
        return None
    if isinstance(dep.get("version"), str):
        return dep["version"]
    if dep.get("workspace") is True and workspace_deps:
        return dep_version_text(workspace_deps.get(name), None, name)
    return None


def collect_manifest_versions(root: Path) -> list[str]:
    root_manifest = load_toml(root / "Cargo.toml")
    workspace = root_manifest.get("workspace")
    workspace_deps = workspace.get("dependencies") if isinstance(workspace, dict) else None
    if not isinstance(workspace_deps, dict):
        workspace_deps = None

    manifests = [root, *workspace_members(root, root_manifest)]
    versions: list[str] = []
    seen: set[str] = set()

    for manifest_root in manifests:
        doc = load_toml(manifest_root / "Cargo.toml")
        for table_name, table in iter_dependency_tables(doc):
            for dep_name, dep in table.items():
                if dep_name != "bevy" and not dep_name.startswith("bevy_"):
                    continue
                version = dep_version_text(dep, workspace_deps, dep_name)
                if not version:
                    continue
                if version not in seen:
                    versions.append(version)
                    seen.add(version)
    return versions


def collect_lock_versions(lockfile: Path) -> list[str]:
    if not lockfile.is_file():
        return []

    doc = load_toml(lockfile)
    packages = doc.get("package")
    if not isinstance(packages, list):
        return []

    versions: list[str] = []
    seen: set[str] = set()
    for package in packages:
        if not isinstance(package, dict):
            continue
        name = package.get("name")
        version = package.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            continue
        if name != "bevy" and not name.startswith("bevy_"):
            continue
        if version not in seen:
            versions.append(version)
            seen.add(version)
    return versions


def choose_current_version(manifest_versions: list[str], lock_versions: list[str]) -> str | None:
    if len(lock_versions) == 1:
        return lock_versions[0]
    if len(manifest_versions) == 1:
        return manifest_versions[0]
    return None


def rustdoc_root() -> str | None:
    candidates = [
        RUSTDOC_ROOT / "bevy/index.html",
        RUSTDOC_ROOT / "bevy_app/index.html",
        RUSTDOC_ROOT / "bevy_ecs/index.html",
        RUSTDOC_ROOT / "bevy_asset/index.html",
        RUSTDOC_ROOT / "bevy_ui/index.html",
    ]
    for path in candidates:
        if path.is_file():
            return str(RUSTDOC_ROOT.resolve())
    return None


def looks_like_bevy_repo(path: Path) -> bool:
    return (path / "Cargo.toml").is_file() and (path / "examples").is_dir()


def looks_like_bevy_website(path: Path) -> bool:
    return (path / "content").is_dir()


def existing_path(path: Path, predicate) -> str | None:
    resolved = path.resolve()
    if predicate(resolved):
        return str(resolved)
    return None


def build_result(project_root: Path) -> dict[str, Any]:
    lockfile = project_root / "Cargo.lock"
    manifest_versions = collect_manifest_versions(project_root)
    lock_versions = collect_lock_versions(lockfile)
    bevy_version = choose_current_version(manifest_versions, lock_versions)
    docs_root = rustdoc_root()
    bevy_repo = existing_path(BEVY_REPO_ROOT, looks_like_bevy_repo)
    bevy_website = existing_path(BEVY_WEBSITE_ROOT, looks_like_bevy_website)

    result = {
        "project_root": str(project_root),
        "bevy_version": bevy_version,
        "skill_root": str(SKILL_ROOT),
        "docs_root": str(DOCS_ROOT),
        "rustdoc_root": docs_root,
        "bevy_repo": bevy_repo,
        "bevy_website": bevy_website,
        "notes": [],
    }

    if not bevy_version:
        result["notes"].append(
            "Unable to resolve one current Bevy version from Cargo.toml or Cargo.lock."
        )

    if not docs_root:
        result["notes"].append(
            f"No rustdoc found at {RUSTDOC_ROOT}. Populate docs/rustdoc before relying on exact API surface."
        )

    if not bevy_repo:
        result["notes"].append(
            f"No bevy repo checkout found at {BEVY_REPO_ROOT}."
        )

    if not bevy_website:
        result["notes"].append(
            f"No bevy-website checkout found at {BEVY_WEBSITE_ROOT}."
        )

    return result


def print_text(result: dict[str, Any]) -> None:
    print(f"project_root={result['project_root']}")
    print(f"bevy_version={result['bevy_version'] or 'unresolved'}")
    print(f"skill_root={result['skill_root']}")
    print(f"docs_root={result['docs_root']}")
    print(f"rustdoc_root={result['rustdoc_root'] or 'missing'}")
    print(f"bevy_repo={result['bevy_repo'] or 'missing'}")
    print(f"bevy_website={result['bevy_website'] or 'missing'}")

    if result["notes"]:
        print("notes:")
        for note in result["notes"]:
            print(f"  - {note}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the resolved context as JSON.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    start = Path(args.path).expanduser()

    try:
        project_root = find_cargo_root(start)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    result = build_result(project_root)
    if args.json:
        json.dump(result, sys.stdout, indent=2)
        print()
    else:
        print_text(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
