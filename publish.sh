#!/usr/bin/env bash
# Publish Godogen runtime files into a target game repo.
#
# Usage:
#   ./publish.sh --engine godot|bevy --agent claude|codex --out <target_dir> [--force]
#   ./publish.sh --engine godot|bevy --agent claude|codex <target_dir> [--force]
#
# The Stop hook is best-effort: when `tg-push` and TG_* env vars are present at runtime
# it pushes the latest screenshots/result/{N}/video.mp4 to Telegram, otherwise it no-ops.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
HELPERS="$REPO_ROOT/scripts/publish"

ENGINE=""
AGENT=""
OUT=""
FORCE=0

usage() {
    sed -n '1,9p' "$0" >&2
}

resolve_path() {
    python3 -c 'import pathlib,sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$1"
}

link_bevy_docs() {
    local target_docs_dir="$1"
    local source_docs_dir="$REPO_ROOT/bevy/skills/bevy-help/docs"
    local name

    mkdir -p "$target_docs_dir"
    if [ -f "$source_docs_dir/.gitignore" ]; then
        cp "$source_docs_dir/.gitignore" "$target_docs_dir/.gitignore"
    fi

    for name in rustdoc bevy bevy-website; do
        local source_link="$source_docs_dir/$name"
        local target_link="$target_docs_dir/$name"
        local source_target

        if [ ! -L "$source_link" ]; then
            echo "error: $source_link is not configured." >&2
            echo "Run ./setup_bevy_docs.sh <shared_bevy_docs_dir> in this source repo before publishing." >&2
            exit 1
        fi

        source_target="$(resolve_path "$source_link")"
        if [ ! -d "$source_target" ]; then
            echo "error: $source_link points to missing docs at $source_target." >&2
            echo "Run ./setup_bevy_docs.sh <shared_bevy_docs_dir> again with a valid Bevy docs folder before publishing." >&2
            exit 1
        fi

        rm -rf "$target_link"
        ln -s "$source_target" "$target_link"
    done
}

while [ $# -gt 0 ]; do
    case "$1" in
        --engine) ENGINE="${2:-}"; shift 2 ;;
        --agent)  AGENT="${2:-}";  shift 2 ;;
        --out)    OUT="${2:-}";    shift 2 ;;
        --force)  FORCE=1;         shift   ;;
        -h|--help) usage; exit 0 ;;
        -*) echo "error: unknown option $1" >&2; usage; exit 1 ;;
        *)
            if [ -n "$OUT" ]; then
                echo "error: target specified more than once" >&2
                exit 1
            fi
            OUT="$1"
            shift
            ;;
    esac
done

case "$ENGINE" in
    godot|bevy) ;;
    *) echo "error: --engine must be godot or bevy" >&2; usage; exit 1 ;;
esac

case "$AGENT" in
    claude)
        MANIFEST="CLAUDE.md"
        SKILLS_DIR_REL=".claude/skills"
        HOOK_CONFIG_DIR=".claude"
        AGENT_NAME="Claude"
        GODOGEN_COMMAND="/godogen"
        GODOT_API_COMMAND="/godot-api"
        BEVY_HELP_COMMAND="/bevy-help"
        ;;
    codex)
        MANIFEST="AGENTS.md"
        SKILLS_DIR_REL=".agents/skills"
        HOOK_CONFIG_DIR=".codex"
        AGENT_NAME="Codex"
        GODOGEN_COMMAND="\$godogen"
        GODOT_API_COMMAND="\$godot-api"
        BEVY_HELP_COMMAND="\$bevy-help"
        ;;
    *) echo "error: --agent must be claude or codex" >&2; usage; exit 1 ;;
esac

if [ -z "$OUT" ]; then
    echo "error: --out <target_dir> is required" >&2
    usage
    exit 1
fi

TARGET="$(cd "$OUT" 2>/dev/null && pwd || (mkdir -p "$OUT" && cd "$OUT" && pwd))"

if [ "$FORCE" -eq 1 ] && [ -d "$TARGET" ]; then
    echo "Force: cleaning $TARGET"
    rm -rf "${TARGET:?}"
    mkdir -p "$TARGET"
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/skills/godogen"
rsync -a --delete --exclude='__pycache__/' "$REPO_ROOT/shared/skills/godogen/" "$TMP/skills/godogen/"
rsync -a --exclude='__pycache__/' "$REPO_ROOT/$ENGINE/skills/godogen/" "$TMP/skills/godogen/"

if [ "$ENGINE" = "godot" ]; then
    rsync -a --delete --exclude='doc_source/' --exclude='__pycache__/' \
        "$REPO_ROOT/godot/skills/godot-api" "$TMP/skills/"
else
    rsync -a --delete --exclude='docs/' --exclude='__pycache__/' \
        "$REPO_ROOT/bevy/skills/bevy-help" "$TMP/skills/"
fi

python3 "$HELPERS/render_dir.py" "$TMP" \
    "AGENT_ID=$AGENT" \
    "AGENT_NAME=$AGENT_NAME" \
    "SKILLS_DIR=$SKILLS_DIR_REL" \
    "GODOGEN_SKILL_DIR=$SKILLS_DIR_REL/godogen" \
    "GODOT_API_SKILL_DIR=$SKILLS_DIR_REL/godot-api" \
    "BEVY_HELP_SKILL_DIR=$SKILLS_DIR_REL/bevy-help" \
    "HOOK_CONFIG_DIR=$HOOK_CONFIG_DIR" \
    "ENGINE_NAME=${ENGINE^}" \
    "GODOGEN_COMMAND=$GODOGEN_COMMAND" \
    "GODOT_API_COMMAND=$GODOT_API_COMMAND" \
    "BEVY_HELP_COMMAND=$BEVY_HELP_COMMAND"

if [ "$AGENT" = "codex" ]; then
    python3 "$HELPERS/generate_codex_metadata.py" "$TMP/skills"
elif [ "$ENGINE" = "godot" ]; then
    python3 "$HELPERS/inject_claude_lookup_frontmatter.py" "$TMP/skills/godot-api/SKILL.md"
else
    python3 "$HELPERS/inject_claude_lookup_frontmatter.py" "$TMP/skills/bevy-help/SKILL.md"
fi

echo "Publishing $ENGINE/$AGENT to: $TARGET"

mkdir -p "$TARGET/$SKILLS_DIR_REL"
rsync -a --delete "$TMP/skills/" "$TARGET/$SKILLS_DIR_REL/"

if [ "$ENGINE" = "bevy" ]; then
    link_bevy_docs "$TARGET/$SKILLS_DIR_REL/bevy-help/docs"
    echo "Linked bevy-help docs from source repo"
fi

mkdir -p "$TMP/game"
cp "$REPO_ROOT/$ENGINE/game-engine.md" "$TMP/game/game-engine.md"
python3 "$HELPERS/render_dir.py" "$TMP/game" \
    "AGENT_NAME=$AGENT_NAME" \
    "GODOGEN_COMMAND=$GODOGEN_COMMAND"
cp "$TMP/game/game-engine.md" "$TARGET/$MANIFEST"
echo "Created $MANIFEST"

mkdir -p "$TARGET/$HOOK_CONFIG_DIR/hooks"
rsync -a "$REPO_ROOT/shared/hooks/stop_post_task_gate.py" \
    "$TARGET/$HOOK_CONFIG_DIR/hooks/"
rsync -a "$REPO_ROOT/$ENGINE/hooks/" "$TARGET/$HOOK_CONFIG_DIR/hooks/"
python3 "$HELPERS/render_dir.py" "$TARGET/$HOOK_CONFIG_DIR/hooks" \
    "AGENT_ID=$AGENT" \
    "AGENT_NAME=$AGENT_NAME" \
    "HOOK_CONFIG_DIR=$HOOK_CONFIG_DIR" \
    "ENGINE_NAME=${ENGINE^}"
chmod +x "$TARGET/$HOOK_CONFIG_DIR/hooks/stop_post_task_gate.py" "$TARGET/$HOOK_CONFIG_DIR/hooks/capture_result.sh"

if [ "$AGENT" = "codex" ]; then
    cp "$REPO_ROOT/shared/hooks/hooks.json" "$TARGET/$HOOK_CONFIG_DIR/hooks.json"
    python3 "$HELPERS/render_dir.py" "$TARGET/$HOOK_CONFIG_DIR" \
        "AGENT_ID=$AGENT" \
        "AGENT_NAME=$AGENT_NAME" \
        "HOOK_CONFIG_DIR=$HOOK_CONFIG_DIR" \
        "ENGINE_NAME=${ENGINE^}"
    python3 "$HELPERS/ensure_codex_hooks_feature.py" "$TARGET/$HOOK_CONFIG_DIR/config.toml"
    echo "Installed Codex stop hook"
else
    python3 "$HELPERS/merge_claude_stop_hook.py" "$TARGET/$HOOK_CONFIG_DIR/settings.json"
    echo "Installed Claude Code stop hook"
fi

if [ ! -f "$TARGET/.gitignore" ]; then
    {
        if [ "$AGENT" = "claude" ]; then
            printf '.claude\nCLAUDE.md\n'
        else
            printf '.agents\nAGENTS.md\n.codex\n'
        fi
        if [ "$ENGINE" = "godot" ]; then
            printf 'assets\nscreenshots\n.godot\n*.import\nbin/\nobj/\n'
        else
            printf '/target\n/screenshots\n.bevy-help.log\n'
        fi
    } > "$TARGET/.gitignore"
    echo "Created .gitignore"
fi

git -C "$TARGET" init -q 2>/dev/null || true

echo "Done. skills: $(find "$TARGET/$SKILLS_DIR_REL" -mindepth 1 -maxdepth 1 -type d | wc -l)"
