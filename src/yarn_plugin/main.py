from fastapi import FastAPI

app = FastAPI(
    title="Yarn Plugin API",
    description="API for yarn and knitting pattern recommendations — MCP + GPT Actions compatible",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
