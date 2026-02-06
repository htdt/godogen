#!/usr/bin/env python3
"""
Token counter for markdown files across different LLM providers.
Supports OpenAI, Claude (Anthropic), and Gemini tokenization.
"""

import argparse
import sys
from pathlib import Path
from anthropic import Anthropic
from google import genai
import tiktoken


def count_openai_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens using OpenAI's tiktoken library."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("o200k_base")
    return len(encoding.encode(text))


def count_claude_tokens(text: str, model: str = "claude-sonnet-4-5") -> int:
    """Count tokens using Anthropic's tokenizer."""
    client = Anthropic()
    token_count = client.messages.count_tokens(
        model=model, messages=[{"role": "user", "content": text}]
    )
    return token_count.input_tokens


def count_gemini_tokens(text: str, model: str = "gemini-3-pro-preview") -> int:
    """Count tokens using Google's genai library."""
    client = genai.Client()
    response = client.models.count_tokens(model=model, contents=text)
    return response.total_tokens


def count_tokens_simple(text: str) -> int:
    """Simple approximation: ~4 characters per token (rough estimate)."""
    return len(text) // 4


def main():
    parser = argparse.ArgumentParser(
        description="Count tokens in a markdown file for different LLM providers"
    )
    parser.add_argument("file", type=Path, help="Path to the markdown file")
    parser.add_argument(
        "--openai-model",
        default="gpt-5.2",
        help="OpenAI model to use for tokenization (default: gpt-5.2)",
    )
    parser.add_argument(
        "--claude-model",
        default="claude-sonnet-4-5",
        help="Claude model to use for tokenization (default: claude-sonnet-4.5)",
    )
    parser.add_argument(
        "--gemini-model",
        default="gemini-3-pro-preview",
        help="Gemini model to use for tokenization (default: gemini-3-pro-preview)",
    )

    args = parser.parse_args()

    # Read the markdown file
    if not args.file.exists():
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)

    try:
        text = args.file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    # Count tokens for each provider
    print(f"Token counts for: {args.file}")
    print("=" * 60)

    openai_tokens = count_openai_tokens(text, args.openai_model)
    if openai_tokens >= 0:
        print(f"OpenAI ({args.openai_model}): {openai_tokens:,} tokens")

    claude_tokens = count_claude_tokens(text, args.claude_model)
    if claude_tokens >= 0:
        print(f"Claude ({args.claude_model}):  {claude_tokens:,} tokens")

    gemini_tokens = count_gemini_tokens(text, args.gemini_model)
    if gemini_tokens >= 0:
        print(f"Gemini ({args.gemini_model}):     {gemini_tokens:,} tokens")

    # Always show simple estimate
    simple_tokens = count_tokens_simple(text)
    print(f"\nSimple estimate:     {simple_tokens:,} tokens (~4 chars/token)")
    print(f"Character count:     {len(text):,} characters")
    print(f"Word count:          {len(text.split()):,} words")


if __name__ == "__main__":
    main()
