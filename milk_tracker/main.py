from pathlib import Path

from controllers.app import AppController
from middleware.auth import AuthMiddleware
from nicegui import app, ui
from pages import login, root

# Milk Tracker overall controller
mt = AppController(config_file=Path("config.yaml"))

# Authorization
app.add_middleware(AuthMiddleware)


@ui.page("/login")
def login_page() -> None:  # noqa: D103
    login.page(mt)


@ui.page("/")
def main_page() -> None:  # noqa: D103
    root.page(mt)


ui.run(
    port=int(mt.env["APP_PORT"]),
    show=False,
    title=mt.config.TITLE,
    storage_secret=mt.env["STORAGE_SECRET"],
)
