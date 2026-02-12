#!/usr/bin/env python3
"""
Godot API XML → Markdown Converter

Converts Godot API XML class documentation to compact, LLM-friendly markdown.

Getting XML Documentation from Godot Source:
--------------------------------------------
Godot's API docs are stored as XML files in doc/classes/ directory (~400 files).
Use sparse checkout to fetch only the docs without the entire codebase:

    mkdir -p md_source && cd md_source
    git clone --depth 1 --filter=blob:none --sparse https://github.com/godotengine/godot.git
    cd godot && git sparse-checkout set doc/classes

Usage:
------
    # Generate unified API reference (128 classes, ~64k tokens)
    python godot_api_converter.py -i md_source/godot/doc/classes -o md_ready/godot_api.md \\
        --unified-classes --method-desc first

    # See all options
    python godot_api_converter.py --help
"""

import xml.etree.ElementTree as ET
import re
import argparse
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from class_list import CLASS_SCENE, CLASS_SCRIPT, PRIORITY_CLASSES, CLASS_UNIFIED


class DescriptionMode(Enum):
    """Mode for including descriptions."""

    NONE = "none"
    FIRST_SENTENCE = "first"
    BRIEF = "brief"
    FULL = "full"


@dataclass
class ConversionConfig:
    """Configuration for markdown conversion."""

    class_description: DescriptionMode = DescriptionMode.FIRST_SENTENCE
    method_descriptions: DescriptionMode = DescriptionMode.NONE
    property_descriptions: DescriptionMode = DescriptionMode.NONE
    signal_descriptions: DescriptionMode = DescriptionMode.NONE
    constant_descriptions: DescriptionMode = DescriptionMode.NONE
    max_enum_values: int = 10  # Maximum enum values to show per enum
    # Compact mode options (enabled by default)
    no_virtual: bool = True  # Skip virtual/override methods
    compact_format: bool = True  # Use inline props, short headers, no separators
    simple_signals: bool = True  # Omit params for parameterless signals


def convert_bbcode(text: str) -> str:
    """Convert Godot BBCode to plain text/minimal markdown."""
    if not text:
        return ""

    # Convert code tags
    text = re.sub(r"\[code\](.*?)\[/code\]", r"`\1`", text)

    # Convert formatting
    text = re.sub(r"\[b\](.*?)\[/b\]", r"**\1**", text)
    text = re.sub(r"\[i\](.*?)\[/i\]", r"*\1*", text)

    # Convert references
    text = re.sub(r"\[(method|member|signal|param|constant|enum)\s+([^\]]+)\]", r"`\2`", text)
    text = re.sub(r"\[([A-Z][a-zA-Z0-9_]+)\]", r"\1", text)  # [ClassName] → ClassName

    # Remove URLs
    text = re.sub(r"\[url[^\]]*\].*?\[/url\]", "", text)
    # Remove codeblocks
    text = re.sub(r"\[codeblock\].*?\[/codeblock\]", "", text, flags=re.DOTALL)
    text = re.sub(r"\[codeblocks\].*?\[/codeblocks\]", "", text, flags=re.DOTALL)

    # Clean up whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def first_sentence(text: str) -> str:
    """Extract first sentence only."""
    text = convert_bbcode(text)
    if not text:
        return ""

    match = re.match(r"^[^.!?]*[.!?]", text)
    if match:
        return match.group(0).strip()

    return text[:100].strip()


def get_description(text: str | None, mode: DescriptionMode) -> str:
    """Get description text based on mode."""
    if mode == DescriptionMode.NONE or not text:
        return ""
    elif mode == DescriptionMode.FIRST_SENTENCE:
        return first_sentence(text)
    else:  # FULL
        return convert_bbcode(text)


def format_param(param_elem) -> str:
    """Format a parameter element as 'name: Type'."""
    name = param_elem.get("name", "")
    ptype = param_elem.get("type", "")
    default = param_elem.get("default")

    result = f"{name}: {ptype}"
    if default is not None:
        result += f" = {default}"

    return result


def escape_table_cell(text: str) -> str:
    """Escape pipe characters for markdown tables."""
    if not text:
        return ""
    return text.replace("|", "\\|")


def should_skip_class(name: str) -> bool:
    """Check if a class should be skipped (editor-only, internal, etc.)."""
    skip_prefixes = ["Editor", "_"]
    skip_suffixes = ["Plugin", "Server"]
    skip_exact = ["@GlobalScope", "@GDScript"]

    if name in skip_exact:
        return True

    for prefix in skip_prefixes:
        if name.startswith(prefix):
            return True

    for suffix in skip_suffixes:
        if name.endswith(suffix) and name != "AudioServer":
            return True

    return False


def parse_class(xml_path: Path, config: ConversionConfig) -> str | None:
    """Parse a single XML class file and return markdown string."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing {xml_path}: {e}")
        return None

    name = root.get("name")
    if not name:
        return None

    if should_skip_class(name):
        return None

    inherits = root.get("inherits", "")

    class_desc = ""
    if config.class_description != DescriptionMode.NONE:
        brief_elem = root.find("brief_description")
        full_desc_elem = root.find("description")

        if config.class_description == DescriptionMode.FIRST_SENTENCE:
            if brief_elem is not None and brief_elem.text:
                class_desc = first_sentence(brief_elem.text)
        elif config.class_description == DescriptionMode.BRIEF:
            if brief_elem is not None and brief_elem.text:
                class_desc = convert_bbcode(brief_elem.text)
        elif config.class_description == DescriptionMode.FULL:
            if full_desc_elem is not None and full_desc_elem.text:
                class_desc = convert_bbcode(full_desc_elem.text)

    if config.compact_format and inherits:
        lines = [f"## {name} <- {inherits}"]
    else:
        lines = [f"## {name}"]
        if inherits:
            lines.append(f"Inherits: {inherits}")

    lines.append("")

    if class_desc:
        lines.append(class_desc)
        lines.append("")

    # Properties/Members
    members = root.find("members")
    if members is not None and len(members):
        if config.compact_format:
            lines.append("**Props:**")
            for m in members:
                mname = m.get("name", "")
                mtype = m.get("type", "")
                default = m.get("default", "")
                enum = m.get("enum")

                if enum:
                    mtype = f"{mtype} ({enum})"

                # Inline format: name: Type = default (omit empty default)
                if default:
                    lines.append(f"- {mname}: {mtype} = {default}")
                else:
                    lines.append(f"- {mname}: {mtype}")
        else:
            lines.append("### Properties")
            lines.append("| Name | Type | Default |")
            lines.append("|------|------|---------|")

            for m in members:
                mname = m.get("name", "")
                mtype = m.get("type", "")
                default = m.get("default", "")
                enum = m.get("enum")

                if enum:
                    mtype = f"{mtype} ({enum})"

                default = escape_table_cell(default)
                lines.append(f"| {mname} | {mtype} | {default} |")

        # Add property descriptions if enabled
        if config.property_descriptions != DescriptionMode.NONE:
            lines.append("")
            for m in members:
                mname = m.get("name", "")
                desc = get_description(m.text, config.property_descriptions)
                if desc:
                    lines.append(f"- **{mname}**: {desc}")

        lines.append("")

    # Methods
    methods = root.find("methods")
    if methods is not None:
        method_lines = []
        for m in methods:
            mname = m.get("name", "")
            qualifiers = m.get("qualifiers", "")

            # Skip virtual methods if configured
            is_virtual = "virtual" in qualifiers
            if config.no_virtual and is_virtual:
                continue

            # Get return type
            ret = m.find("return")
            ret_type = ret.get("type") if ret is not None else "void"

            # Get parameters
            params = []
            for p in m.findall("param"):
                params.append(format_param(p))

            # Get description
            desc_elem = m.find("description")
            desc = get_description(
                desc_elem.text if desc_elem is not None else None, config.method_descriptions
            )

            virtual_marker = "" if config.compact_format else ("🔷 " if is_virtual else "")
            ret_str = f" -> {ret_type}" if ret_type and ret_type != "void" else ""
            desc_str = f" - {desc}" if desc else ""

            method_lines.append(
                f"- {virtual_marker}{mname}({', '.join(params)}){ret_str}{desc_str}"
            )

        if method_lines:
            if config.compact_format:
                lines.append("**Methods:**")
            else:
                lines.append("### Methods")
            lines.extend(method_lines)
            lines.append("")

    # Signals
    signals = root.find("signals")
    if signals is not None and len(signals):
        if config.compact_format:
            lines.append("**Signals:**")
        else:
            lines.append("### Signals")

        for s in signals:
            sname = s.get("name", "")

            # Get parameters
            params = []
            for p in s.findall("param"):
                pname = p.get("name", "")
                ptype = p.get("type", "")
                params.append(f"{pname}: {ptype}")

            # Get description
            desc_elem = s.find("description")
            desc = get_description(
                desc_elem.text if desc_elem is not None else None, config.signal_descriptions
            )

            # Build signal line - simplified format for parameterless signals
            if config.simple_signals and not params:
                param_str = ""
            else:
                param_str = f"({', '.join(params)})" if params else ""
            desc_str = f" - {desc}" if desc else ""

            lines.append(f"- {sname}{param_str}{desc_str}")

        lines.append("")

    # Constants/Enums
    constants = root.find("constants")
    if constants is not None and len(constants):
        # Group by enum name
        enums: dict[str, list[tuple[str, str, str | None]]] = {}

        for c in constants:
            enum_name = c.get("enum", "Constants")
            cname = c.get("name", "")
            cvalue = c.get("value", "")
            cdesc_raw = c.text  # Store raw text

            if enum_name not in enums:
                enums[enum_name] = []
            enums[enum_name].append((cname, cvalue, cdesc_raw))

        if enums:
            if config.compact_format:
                lines.append("**Enums:**")
            else:
                lines.append("### Enums")

            for enum_name, values in enums.items():
                # Format: **EnumName:** CONST1=0, CONST2=1, ...
                value_strs = [f"{n}={v}" for n, v, _ in values[: config.max_enum_values]]
                if len(values) > config.max_enum_values:
                    value_strs.append("...")

                lines.append(f"**{enum_name}:** {', '.join(value_strs)}")

                # Add descriptions if enabled
                if config.constant_descriptions != DescriptionMode.NONE:
                    for cname, cvalue, cdesc_raw in values:
                        cdesc = get_description(cdesc_raw, config.constant_descriptions)
                        if cdesc:
                            lines.append(f"  - {cname}: {cdesc}")

            lines.append("")

    return "\n".join(lines)


def parse_index_entry(xml_path: Path) -> tuple[str, str, str] | None:
    """Parse XML for index entry: (name, inherits, brief_description)."""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError:
        return None

    name = root.get("name")
    if not name or should_skip_class(name):
        return None

    inherits = root.get("inherits", "")
    brief_elem = root.find("brief_description")
    brief = first_sentence(brief_elem.text) if brief_elem is not None and brief_elem.text else ""

    return (name, inherits, brief)


def convert_directory_split(
    input_dir: Path,
    split_dir: Path,
    config: ConversionConfig,
    classes_filter: list[str] | None = None,
) -> None:
    """Convert XML files to per-class markdown files + a prioritized index."""

    split_dir.mkdir(parents=True, exist_ok=True)

    xml_files = sorted(input_dir.glob("*.xml"))
    if classes_filter:
        classes_set = set(classes_filter)
        xml_files = [f for f in xml_files if f.stem in classes_set]

    # Build index entries and write per-class files
    unified_set = set(CLASS_UNIFIED)
    common_entries: list[tuple[str, str, str]] = []
    other_entries: list[tuple[str, str, str]] = []
    converted_count = 0
    skipped_count = 0

    for xml_file in xml_files:
        # Parse index entry
        entry = parse_index_entry(xml_file)
        if entry is None:
            skipped_count += 1
            continue

        name, inherits, brief = entry

        # Parse full class content — always use full description in per-class files
        detail_config = ConversionConfig(
            class_description=DescriptionMode.FULL,
            method_descriptions=config.method_descriptions,
            property_descriptions=config.property_descriptions,
            signal_descriptions=config.signal_descriptions,
            constant_descriptions=config.constant_descriptions,
            max_enum_values=config.max_enum_values,
            no_virtual=config.no_virtual,
            compact_format=config.compact_format,
            simple_signals=config.simple_signals,
        )
        result = parse_class(xml_file, detail_config)
        if result is None:
            skipped_count += 1
            continue

        # Write per-class file
        (split_dir / f"{name}.md").write_text(result + "\n")
        converted_count += 1

        # Sort into common vs other for the index
        if name in unified_set:
            common_entries.append((name, inherits, brief))
        else:
            other_entries.append((name, inherits, brief))

    # Write two separate index files
    def write_index(path: Path, title: str, entries: list[tuple[str, str, str]]) -> None:
        lines = [f"# {title}", ""]
        for name, inherits, brief in sorted(entries):
            parent = f" <- {inherits}" if inherits else ""
            desc = f" — {brief}" if brief else ""
            lines.append(f"- {name}{parent}{desc}")
        lines.append("")
        path.write_text("\n".join(lines))

    write_index(split_dir / "_common.md", f"Common Classes ({len(common_entries)})", common_entries)
    write_index(split_dir / "_other.md", f"Other Classes ({len(other_entries)})", other_entries)

    print(f"Converted {converted_count} classes, skipped {skipped_count}")
    print(f"Common index: {split_dir / '_common.md'} ({len(common_entries)} classes)")
    print(f"Other index: {split_dir / '_other.md'} ({len(other_entries)} classes)")
    print(f"Output directory: {split_dir}")


def convert_directory(
    input_dir: Path,
    output_file: Path,
    config: ConversionConfig,
    classes_filter: list[str] | None = None,
) -> None:
    """Convert all XML files in directory to a single markdown file."""

    xml_files = sorted(input_dir.glob("*.xml"))

    # Filter classes if specified
    if classes_filter:
        classes_set = set(classes_filter)
        xml_files = [f for f in xml_files if f.stem in classes_set]

    if config.compact_format:
        output_parts = [
            "# Godot API Reference",
            "",
        ]
    else:
        output_parts = [
            "# Godot API Reference",
            "",
            "Compact API reference for LLM context.",
            "",
            "---",
            "",
        ]

    converted_count = 0
    skipped_count = 0

    for xml_file in xml_files:
        result = parse_class(xml_file, config)
        if result:
            output_parts.append(result)
            if not config.compact_format:
                output_parts.append("---")
            output_parts.append("")
            converted_count += 1
        else:
            skipped_count += 1

    # Write output
    output_file.write_text("\n".join(output_parts))

    print(f"Converted {converted_count} classes, skipped {skipped_count}")
    print(f"Output written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Godot XML class documentation to compact markdown"
    )
    parser.add_argument(
        "-i",
        "--input_dir",
        type=Path,
        default=Path("./doc_source/godot/doc/classes"),
        help="Directory containing XML class files",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("godot_api.md"),
        help="Output markdown file (default: godot_api.md)",
    )
    output_group.add_argument(
        "--split-dir",
        type=Path,
        help="Output per-class .md files + _index.md to this directory",
    )
    parser.add_argument(
        "--class-desc",
        choices=["none", "first", "brief", "full"],
        default="brief",
        help="Class description mode: none, first (sentence), brief (full brief_description), or full (full description) (default: first)",
    )
    parser.add_argument(
        "--method-desc",
        choices=["none", "first", "full"],
        default="none",
        help="Method description mode: none, first (sentence), or full (default: none)",
    )
    parser.add_argument(
        "--property-desc",
        choices=["none", "first", "full"],
        default="none",
        help="Property description mode: none, first (sentence), or full (default: none)",
    )
    parser.add_argument(
        "--signal-desc",
        choices=["none", "first", "full"],
        default="none",
        help="Signal description mode: none, first (sentence), or full (default: first)",
    )
    parser.add_argument(
        "--constant-desc",
        choices=["none", "first", "full"],
        default="none",
        help="Constant/enum description mode: none, first (sentence), or full (default: none)",
    )
    parser.add_argument(
        "--priority-only",
        action="store_true",
        help="Only convert priority classes (commonly used for game dev)",
    )
    parser.add_argument(
        "--scene-classes",
        action="store_true",
        help="Use CLASS_SCENE list from class_list.py (optimized for scene generation)",
    )
    parser.add_argument(
        "--script-classes",
        action="store_true",
        help="Use CLASS_SCRIPT list from class_list.py (optimized for script generation)",
    )
    parser.add_argument(
        "--unified-classes",
        action="store_true",
        help="Use CLASS_UNIFIED list (covers 99%% scene / 95%% script use cases)",
    )
    parser.add_argument("--classes", nargs="+", help="Specific class names to convert")
    parser.add_argument(
        "--max-enum-values",
        type=int,
        default=10,
        help="Maximum enum values to show per enum (default: 10)",
    )
    parser.add_argument(
        "--include-virtual",
        action="store_true",
        help="Include virtual/override methods (excluded by default)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Use verbose format: tables, full headers, separators (compact by default)",
    )
    parser.add_argument(
        "--full-signals",
        action="store_true",
        help="Show empty parentheses for parameterless signals",
    )

    args = parser.parse_args()

    if not args.input_dir.is_dir():
        print(f"Error: {args.input_dir} is not a directory")
        return 1

    config = ConversionConfig(
        class_description=DescriptionMode(args.class_desc),
        method_descriptions=DescriptionMode(args.method_desc),
        property_descriptions=DescriptionMode(args.property_desc),
        signal_descriptions=DescriptionMode(args.signal_desc),
        constant_descriptions=DescriptionMode(args.constant_desc),
        max_enum_values=args.max_enum_values,
        no_virtual=not args.include_virtual,
        compact_format=not args.verbose,
        simple_signals=not args.full_signals,
    )

    # Determine class filter
    classes_filter = None
    if args.classes:
        classes_filter = args.classes
    elif args.unified_classes:
        classes_filter = CLASS_UNIFIED
    elif args.scene_classes:
        classes_filter = CLASS_SCENE
    elif args.script_classes:
        classes_filter = CLASS_SCRIPT
    elif args.priority_only:
        classes_filter = PRIORITY_CLASSES

    if args.split_dir:
        convert_directory_split(args.input_dir, args.split_dir, config, classes_filter)
    else:
        convert_directory(args.input_dir, args.output, config, classes_filter)

    return 0


if __name__ == "__main__":
    exit(main())
