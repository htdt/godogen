Turn a natural language game description into a real game.

# Session Instructions

Non-interactive background process spawned by Teleforge. No terminal, no stdin, no interactive UI. User is on Telegram — reach them **only** via MCP tools.

**Only the main agent (godogen orchestrator) sends and checks messages.** Sub-agents must not call MCP tools.
Exception: godot-task must send a one-sentence status update every ~15 min.

Call `check_messages` before starting each new task and before ending the session.

After scaffold + decomposer, `send_message` a concise summary (game name, task count, numbered list). No approval gate — proceed immediately. User corrections arrive via `check_messages`.

godot-task reports results (screenshots, status) back to godogen. godogen sends the user a summary + best screenshots via `send_image`. After all tasks, godogen sends a final video via `send_video`.
