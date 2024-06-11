from typing import Union

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from controllers.app import AppController
from fastapi.responses import RedirectResponse
from nicegui import app, ui

ph = PasswordHasher()


def page(mt: AppController) -> Union[None, RedirectResponse]:
    """Display Login page.

    Parameters
    ----------
    mt : AppController
        Milk Tracker instance

    """

    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if not mt.env["PASSWORD"]:
            ui.notify("Access deactivated", color="warning")
        else:
            try:
                ph.verify(mt.env["PASSWORD"], password_input.value)
                app.storage.user.update({"authenticated": True})
                ui.notify("Welcome back!", color="positive")
                ui.navigate.to(
                    app.storage.user.get("referrer_path", "/")
                )  # go back to where the user wanted to go
            except VerifyMismatchError:
                app.storage.user.update(
                    {"failed_attempts": app.storage.user.get("failed_attempts", 0) + 1}
                )
                if app.storage.user.get("failed_attempts", 0) >= mt.config.MAX_PASSWORD_ATTEMPTS:
                    login_form.clear()
                    with login_form:
                        access_denied_label()
                ui.notify(
                    f"Wrong password. Tries left: {3-app.storage.user.get('failed_attempts', 0)}",
                    color="negative",
                )

    def access_denied_label() -> ui.label:
        return ui.label("Too many failed login attempts. Access denied.").classes("text-red-600")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")
    with ui.card().classes("absolute-center"):
        if app.storage.user.get("failed_attempts", 0) >= mt.config.MAX_PASSWORD_ATTEMPTS:
            access_denied_label()
        else:
            with ui.element("div") as login_form:
                password_input = ui.input(
                    "Password", password=True, password_toggle_button=True
                ).on("keydown.enter", try_login)
                ui.button("Log in", on_click=try_login)
    return None
