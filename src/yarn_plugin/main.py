from fastapi import FastAPI

from yarn_plugin.recommendations.user_interface.http.get_yarn_recommendations_controller import (
    router as recommendations_router,
)
from yarn_plugin.user_access.user_interface.http.accept_invitation_controller import (
    router as accept_invitation_router,
)
from yarn_plugin.user_access.user_interface.http.create_invitation_controller import (
    router as create_invitation_router,
)
from yarn_plugin.user_access.user_interface.http.list_invitations_controller import (
    router as list_invitations_router,
)
from yarn_plugin.user_access.user_interface.http.login_controller import router as login_router
from yarn_plugin.user_access.user_interface.http.validate_invitation_controller import (
    router as validate_invitation_router,
)

app = FastAPI(
    title="Yarn Plugin API",
    description="API for yarn and knitting pattern recommendations — MCP + GPT Actions compatible",
    version="0.1.0",
)

app.include_router(recommendations_router)
app.include_router(create_invitation_router)
app.include_router(list_invitations_router)
app.include_router(validate_invitation_router)
app.include_router(accept_invitation_router)
app.include_router(login_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}