from nicegui import ui


def display_header() -> ui.element:
    """Display header."""
    with ui.element().classes("absolute top-0 right-0 mt-11 mr-4") as div:
        with ui.button(icon="menu"):
            with ui.menu() as menu:
                ui.menu_item("Meals", lambda: ui.navigate.to("/"))
                ui.menu_item("Memories", lambda: ui.navigate.to("/memories"))
                ui.separator()
                ui.menu_item("Close", menu.close)
    return div
