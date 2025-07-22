@echo off
echo Starting USD MCP Server with MCP Inspector...
echo.
cd /d "C:\Users\rudyc\projects\usd-ai"
npx @modelcontextprotocol/inspector "C:\Users\rudyc\projects\usd-ai\.venv\Scripts\python.exe" "C:\Users\rudyc\projects\usd-ai\usd-mcp\server\main.py"
pause