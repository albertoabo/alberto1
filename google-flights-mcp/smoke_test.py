"""Launch the server from .mcp.json over stdio, list its tools and run one search.

    uv run --with mcp python smoke_test.py [FROM] [TO] [YYYY-MM-DD]
"""
import asyncio
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    cfg = json.loads((Path(__file__).parent / ".mcp.json").read_text())["mcpServers"]["google-flights"]
    origin, dest = sys.argv[1:3] if len(sys.argv) >= 3 else ("JFK", "LAX")
    day = sys.argv[3] if len(sys.argv) > 3 else (date.today() + timedelta(days=30)).isoformat()
    params = StdioServerParameters(command=cfg["command"], args=cfg["args"])
    async with stdio_client(params) as (r, w), ClientSession(r, w) as s:
        await s.initialize()
        print("tools:", [t.name for t in (await s.list_tools()).tools])
        res = await s.call_tool("search_flights", {"from_airport": origin, "to_airport": dest, "date": day})
        print(res.content[0].text[:2000])


asyncio.run(main())
