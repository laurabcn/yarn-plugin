from mcp.server.fastmcp import FastMCP

from yarn_plugin.recommendations.user_interface.mcp.get_pattern_recommendations_tool import (
    get_pattern_recommendations,
)
from yarn_plugin.recommendations.user_interface.mcp.get_yarn_recommendations_tool import (
    get_yarn_recommendations,
)

mcp = FastMCP(
    name="yarn-plugin",
    instructions=(
        "Recommends real yarn and knitting/crochet patterns for questions about knitting and "
        "crochet — never invent a yarn, brand, or pattern; use these tools instead."
    ),
)

mcp.add_tool(get_yarn_recommendations)
mcp.add_tool(get_pattern_recommendations)

if __name__ == "__main__":
    mcp.run(transport="stdio")
