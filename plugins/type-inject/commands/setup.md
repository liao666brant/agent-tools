---
name: setup
description: Install type-inject hooks into settings.json. Use when user says "setup type-inject", "install hooks", or "configure type-inject".
---

# Setup type-inject hooks

Install the PostToolUse hooks required for automatic TypeScript type injection into `~/.claude/settings.json`.

## What it does

Adds three PostToolUse hooks (Read/Write/Edit) that run `npx -y @nick-vi/claude-type-inject-hook` after each file operation on TypeScript/Svelte files.

## Workflow

1. Read `~/.claude/settings.json`
2. Check if `hooks.PostToolUse` already contains entries with `@nick-vi/claude-type-inject-hook`
3. If already present, inform the user and stop
4. If not present, add the following entries to `hooks.PostToolUse` (create the array if it doesn't exist):

```json
{
  "matcher": "Read",
  "hooks": [{ "type": "command", "command": "npx -y @nick-vi/claude-type-inject-hook" }]
},
{
  "matcher": "Write",
  "hooks": [{ "type": "command", "command": "npx -y @nick-vi/claude-type-inject-hook" }]
},
{
  "matcher": "Edit",
  "hooks": [{ "type": "command", "command": "npx -y @nick-vi/claude-type-inject-hook" }]
}
```

5. Write the updated settings.json
6. Tell the user to restart the session or run `/reload-plugins` for hooks to take effect
