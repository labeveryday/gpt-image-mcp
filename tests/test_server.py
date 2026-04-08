"""Smoke tests for the FastMCP server registration."""

import pytest

from gpt_image_mcp import server as server_module


def test_server_module_imports():
    assert server_module.mcp is not None
    assert callable(server_module.main)


@pytest.mark.asyncio
async def test_expected_tools_registered():
    tools = await server_module.mcp.get_tools()
    tool_names = set(tools.keys()) if isinstance(tools, dict) else {t.name for t in tools}
    expected = {
        "generate_image",
        "generate_batch",
        "analyze_thumbnail",
        "optimize_for_platform",
        "generate_reference_thumbnail",
        "get_prompt_suggestions",
        "cleanup_temp_files",
    }
    assert expected.issubset(tool_names), f"Missing tools: {expected - tool_names}"
