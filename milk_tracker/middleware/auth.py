from typing import Awaitable, Callable

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import Client, app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Authorization
unrestricted_page_routes = {"/login"}


class AuthMiddleware(BaseHTTPMiddleware):
    """Restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(  # noqa: D102
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if (
            not app.storage.user.get("authenticated", False)
            and request.url.path in Client.page_routes.values()
            and request.url.path not in unrestricted_page_routes
        ):
            app.storage.user["referrer_path"] = (
                request.url.path
            )  # remember where the user wanted to go
            return RedirectResponse("/login")
        return await call_next(request)
