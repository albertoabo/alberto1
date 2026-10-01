# google-flights-mcp

Google Flights search for Claude, via the open-source
[jonzarecki/fast-flights-mcp](https://github.com/jonzarecki/fast-flights-mcp) server
(built on [fast-flights](https://pypi.org/project/fast-flights/)). No API key needed.

## Requirements

- [uv](https://docs.astral.sh/uv/) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## Claude Code

`.mcp.json` in this repo registers the server as `google-flights`. Open Claude Code in this
folder and approve the project MCP server when prompted (or check with `/mcp`).

To make it available in every project instead:

```bash
claude mcp add --scope user google-flights -- uvx \
  --with 'fast-flights>=2.2,<3' --with 'fastmcp>=2.9,<2.13' --with 'primp<0.15' \
  --from git+https://github.com/jonzarecki/fast-flights-mcp@2f41853c4ae29f3bc6e92b286bc0c2093e7fabb1 \
  fast-flights-mcp
```

## Claude Desktop

Copy the `mcpServers` block from `.mcp.json` into `claude_desktop_config.json`
(macOS: `~/Library/Application Support/Claude/`, Windows: `%APPDATA%\Claude\`) and restart.
If Desktop can't find `uvx`, use its absolute path (`which uvx`).

## Tools

- `search_flights` — one-way or round-trip search (airports, date, return date, cabin, passengers, stops…)
- `call_tool_bulk` / `call_tools_bulk` — batch several searches in one call

## Why the version pins

Upstream hasn't kept up with its dependencies; unpinned it fails to start:

| Pin | Reason |
| --- | --- |
| `fast-flights<3` | 3.x removed `FlightData` / `get_flights` |
| `fastmcp<2.13` | newer releases reject the `dependencies=` argument the server passes |
| `primp<0.15` | newer releases dropped the `chrome_126` impersonation fast-flights 2.x uses |

The upstream commit is pinned too, so a future upstream change can't break this silently.

## Smoke test

```bash
uv run --with mcp python smoke_test.py JFK LAX 2026-11-15
```

The first run downloads dependencies (about 30s), so an MCP client may time out on its very first start; retry once.
