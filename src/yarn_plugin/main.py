from fastapi import FastAPI

from yarn_plugin.recommendations.user_interface.http.get_yarn_recommendations_controller import (
    router as recommendations_router,
)

app = FastAPI(
    title="Yarn Plugin API",
    description="API for yarn and knitting pattern recommendations — MCP + GPT Actions compatible",
    version="0.1.0",
)

app.include_router(recommendations_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
