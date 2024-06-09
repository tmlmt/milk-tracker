from pathlib import Path
from typing import Any, Dict, List, Literal, Union

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from controllers.app import AppController
from fastapi.responses import RedirectResponse
from middleware.auth import AuthMiddleware
from nicegui import app, ui
from nicegui.events import ValueChangeEventArguments
from pydantic import ValidationError
from utils.time_utils import get_current_date, get_current_time, timedelta_to_hrmin

# Configuration
CONFIG_FILE = Path("config.yaml")

# Milk Tracker overall controller
mt = AppController(CONFIG_FILE)

# Authorization
app.add_middleware(AuthMiddleware)
ph = PasswordHasher()

# Declaration
current_time = None
time_since_latest_end = None
time_since_latest_start = None
latest_meal_info = None


@ui.page("/login")
def login() -> Union[None, RedirectResponse]:  # noqa: D103
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


@ui.page("/")
def main_page() -> None:  # noqa: D103
    # Common CSS for all pages
    ui.add_sass(Path("css") / "main.sass")
    # Specific CSS
    ui.add_sass(Path("css") / "table.sass")

    mt.load_data()

    def force_update_view() -> None:
        table_latest_meals_container.clear()
        with table_latest_meals_container:
            generate_latest_meals_table()
        table_summary_container.clear()
        with table_summary_container:
            generate_summary_table()
        figure_duration.update_figure(
            generate_graph(
                "duration_min",
                "Duration as a Function of Start Time for the Latest Three Dates",
                "Duration (min)",
            )
        )
        figure_time_since_previous_start.update_figure(
            generate_graph(
                "time_since_previous_start_hrs",
                "Time interval since previous start of meal",
                "Time interval (hrs)",
            )
        )
        figure_time_since_previous_end.update_figure(
            generate_graph(
                "time_since_previous_end_hrs",
                "Time interval since previous end of meal",
                "Time interval (hrs)",
            )
        )

    ui.timer(1.0, mt.do_continuous_update)

    # Add new entry

    def add_finished_meal(date: str, start_time: str, end_time: str) -> bool:
        # Validation
        try:
            mt.add_finished_meal(date=date, start_time=start_time, end_time=end_time)
        except ValidationError:
            ui.notify("Invalid meal data: check all fields")
            return False
        # Clearing inputs
        new_end_time.set_value("")
        new_start_time.set_value(get_current_time(include_sec=False))
        switch_lock_start_time.set_value(False)
        new_date.set_value(get_current_date())
        # Updating UI
        force_update_view()
        # Success message
        ui.notify("Meal added to history", type="positive")
        return True

    ui.markdown("# Milk Tracker")

    ui.markdown("## Quick check")

    with ui.row().classes("items-stretch"):
        with ui.card():
            ui.markdown("##### Latest meal")
            ui.separator()
            ui.markdown().bind_content_from(mt.computed, "latest_meal_info")
        with ui.card():
            ui.markdown("##### Current time")
            ui.separator()
            with ui.card_section().classes("h-full content-center"):
                ui.label().bind_text_from(mt.computed, "current_time").classes("text-3xl")
        with ui.card():
            ui.markdown("##### Previous end")
            ui.separator()
            with ui.card_section().classes("h-full content-center"):
                ui.label().bind_text_from(
                    mt.computed, "time_since_latest_end", backward=timedelta_to_hrmin
                ).classes("text-3xl")
        with ui.card():
            ui.markdown("##### Previous start")
            ui.separator()
            with ui.card_section().classes("h-full content-center px-2"):
                ui.label().bind_text_from(
                    mt.computed, "time_since_latest_start", backward=timedelta_to_hrmin
                ).classes("text-3xl")

    ui.markdown("## New meal")

    with ui.row().classes("items-stretch"):
        with ui.column():
            ui.markdown("##### Date")
            with ui.input(value=get_current_date()).props(
                "mask='####-##-##' "
                ":rules='[v => /^[0-9]+-[0-1][0-9]-[0-3][0-9]$/.test(v) || \"Invalid date\"]' "
                "lazy-rules"
            ).classes("w-36") as new_date:
                with ui.menu().props("auto-close no-parent-event") as menu_new_date:
                    ui.date().bind_value(new_date)
                with new_date.add_slot("append"):
                    ui.icon("edit_calendar").on("click", menu_new_date.open).classes(
                        "cursor-pointer"
                    )
        with ui.column():
            ui.markdown("##### Start time")
            with ui.row().classes("items-stretch"):
                ui.button(
                    "Now",
                    on_click=lambda: new_start_time.set_value(get_current_time(include_sec=False)),
                ).bind_enabled_from(
                    mt.computed, "is_ongoing_meal", backward=lambda x: not x
                ).classes("h-full")
                with ui.input(
                    value=mt.get_input_default_value_newmeal_start_time()
                ).bind_enabled_from(mt.computed, "is_ongoing_meal", backward=lambda x: not x).props(
                    "mask='time' :rules='[ (val, rules) => rules.time(val) || \"Invalid time\"]' "
                    "lazy-rules"
                ).classes("w-24") as new_start_time:
                    with ui.menu().props("no-parent-event") as menu_new_start_time:
                        with ui.time().props("format24h").bind_value(new_start_time):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu_new_start_time.close)
                    with new_start_time.add_slot("append"):
                        ui.icon("access_time").on("click", menu_new_start_time.open).classes(
                            "cursor-pointer"
                        )
        with ui.column():
            ui.markdown("##### End time")
            with ui.row().classes("items-stretch"):
                ui.button(
                    "Now",
                    on_click=lambda: new_end_time.set_value(get_current_time(include_sec=False)),
                ).classes("h-full")
                with ui.input().props(
                    "mask='time' :rules='[ (val, rules) => rules.time(val) || \"Invalid time\"]' "
                    "lazy-rules"
                ).classes("w-24") as new_end_time:
                    with ui.menu().props("no-parent-event") as menu_new_end_time:
                        with ui.time().props("format24h").bind_value(new_end_time):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu_new_end_time.close)
                    with new_end_time.add_slot("append"):
                        ui.icon("access_time").on("click", menu_new_end_time.open).classes(
                            "cursor-pointer"
                        )
        with ui.column().classes("justify-end"):
            ui.button(
                "Add",
                on_click=lambda: add_finished_meal(
                    new_date.value, new_start_time.value, new_end_time.value
                ),
            ).classes("h-20 w-20")

    def toggle_newmeal_lock(e: ValueChangeEventArguments) -> None:
        if e.value:
            # Try to fix start time before trying to start new meal
            if not new_start_time.value or len(new_start_time.value) != 5:  # noqa: PLR2004
                new_start_time.set_value(get_current_time(include_sec=False))
            try:
                mt.start_new_meal(date=new_date.value, start_time=new_start_time.value)
            except ValidationError:
                ui.notify("Please check date and start time before locking the meal")
                return
            force_update_view()
        else:
            mt.cancel_ongoing_meal()
            force_update_view()

    with ui.column():
        ui.markdown("##### Record meal")
        switch_lock_start_time = (
            ui.switch(
                "Lock start time",
                value=mt.computed.is_ongoing_meal,
                on_change=toggle_newmeal_lock,
            )
            .props("icon='lock_clock' size='lg'")
            .bind_value_from(mt.computed, "is_ongoing_meal")
        )

    ui.markdown("## 10 last meals")

    def generate_latest_meals_table() -> ui.table:
        return ui.table.from_pandas(
            mt.meals.df.tail(10)[
                [
                    "date",
                    "start_time",
                    "end_time",
                    "duration_hrmin",
                    "time_since_previous_start_hrmin",
                    "time_since_previous_end_hrmin",
                ]
            ]
            .rename(
                columns={
                    "date": "Date",
                    "start_time": "Start time",
                    "end_time": "End time",
                    "duration_hrmin": "Duration",
                    "time_since_previous_start_hrmin": "Time since previous start",
                    "time_since_previous_end_hrmin": "Time since previous end",
                }
            )
            .iloc[::-1],
            pagination=0,
        ).props("table-class='sticky-header-column-table' virtual-scroll hide-pagination")

    with ui.element() as table_latest_meals_container:
        generate_latest_meals_table()

    def delete_latest_meal() -> None:
        mt.delete_latest_meal()
        force_update_view()
        ui.notify("Latest meal removed from history", type="positive")

    ui.button("Delete last meal", on_click=delete_latest_meal, color="negative")

    ui.markdown("## Graphs")

    def generate_graph(field: str, title: str, yaxis_title: str) -> dict:
        # Get the three latest dates
        latest_dates = mt.meals.df["date"].drop_duplicates().nlargest(3)

        graph_data = []
        for date in latest_dates:
            date_data = mt.meals.df[mt.meals.df["date"] == date]
            date_data = date_data[
                (date_data[field] != "")
                & (date_data[field].notna())
                & (date_data[field].astype(float) != 0)
            ]

            graph_data.append(
                {
                    "type": "scatter",
                    "name": str(date.date()),
                    "mode": "markers+lines",
                    "x": [
                        "2024-05-08 " + t
                        for t in date_data["start_time"].astype(str).array.tolist()
                    ],
                    "y": date_data[field].array.tolist(),
                }
            )

        max_y = max(mt.meals.df[mt.meals.df["date"].isin(latest_dates)][field])

        return {
            "data": graph_data,
            "layout": {
                "title": title,
                "xaxis": {"title": "Start Time", "tickformat": "%Hh%M"},
                "yaxis": {
                    "title": yaxis_title,
                    "range": [-max_y * 0.05, max_y * 1.05],
                },
                "dragmode": False,
            },
            "config": mt.config.PLOTLY_DEFAULT_CONFIG,
        }

    with ui.tabs() as tabs_graphs:
        ui.tab("duration", label="Duration")
        ui.tab("latest_start", label="Time since latest START")
        ui.tab("latest_end", label="Time since latest END")
    with ui.tab_panels(tabs_graphs, value="latest_end").classes("w-3xl"):
        with ui.tab_panel("duration"):
            figure_duration = ui.plotly(
                generate_graph(
                    "duration_min",
                    "Duration as a Function of Start Time for the Latest Three Dates",
                    "Duration (min)",
                )
            )
        with ui.tab_panel("latest_start"):
            figure_time_since_previous_start = ui.plotly(
                generate_graph(
                    "time_since_previous_start_hrs",
                    "Time interval since previous start of meal",
                    "Time interval (hrs)",
                )
            )
        with ui.tab_panel("latest_end"):
            figure_time_since_previous_end = ui.plotly(
                generate_graph(
                    "time_since_previous_end_hrs",
                    "Time interval since previous end of meal",
                    "Time interval (hrs)",
                )
            )

    ui.markdown("## Statistics")

    def generate_summary_table() -> ui.table:
        mt.meals.compute_summary()
        return ui.table.from_pandas(mt.meals.df_summary_txt, pagination=0).props(  # type: ignore[arg-type]
            "table-class='sticky-header-column-table' virtual-scroll hide-pagination"
        )

    # Display the summary DataFrame
    with ui.element() as table_summary_container:
        generate_summary_table()

    def generate_summary_graph(
        field: Literal["meals", "duration", "previous_end"], title: str, yaxis_title: str
    ) -> dict:
        if mt.meals.df_summary_raw is None:
            msg = "Summary DataFrame not available"
            raise Exception(msg)  # noqa: TRY002

        graph_data: List[Dict[str, Any]] = [
            {
                "type": "scatter",
                "name": "Data",
                "mode": "markers+lines",
                "color": "#5898D4",
                "x": mt.meals.df_summary_raw["date"].astype(str).array.tolist(),
            }
        ]

        if field == "meals":
            graph_data[0].update({"y": mt.meals.df_summary_raw["number_of_rows"].array.tolist()})
        else:
            graph_data[0].update(
                {
                    "y": mt.meals.df_summary_raw[f"avg_{field}"].array.tolist(),
                    "error_y": {
                        "type": "data",
                        "symmetric": False,
                        "array": (
                            mt.meals.df_summary_raw[f"max_{field}"]
                            - mt.meals.df_summary_raw[f"avg_{field}"]
                        ).array.tolist(),
                        "arrayminus": (
                            mt.meals.df_summary_raw[f"avg_{field}"]
                            - mt.meals.df_summary_raw[f"min_{field}"]
                        ).array.tolist(),
                        "color": "#7D1128",
                        "thickness": 1,
                        "width": 3,
                        "opacity": 1,
                    },
                }
            )

        return {
            "data": graph_data,
            "layout": {
                "title": title,
                "xaxis": {"title": "Date"},
                "yaxis": {
                    "title": yaxis_title,
                },
                "dragmode": "pan",
                "selectdirection": "h",
            },
            "config": mt.config.PLOTLY_DEFAULT_CONFIG,
        }

    with ui.tabs() as tabs_summary_graphs:
        ui.tab("meals", label="Meals")
        ui.tab("duration", label="Duration")
        ui.tab("previous_end", label="Time since previous END")
    with ui.tab_panels(tabs_summary_graphs, value="meals").classes("w-3xl"):
        with ui.tab_panel("meals"):
            ui.plotly(
                generate_summary_graph("meals", "Number of meals per day", "Quantity")
            ).classes("w-screen-and-padding")
        with ui.tab_panel("duration"):
            ui.plotly(
                generate_summary_graph("duration", "Meal duration", "Duration (min)")
            ).classes("w-screen-and-padding")
        with ui.tab_panel("previous_end"):
            ui.plotly(
                generate_summary_graph(
                    "previous_end", "Time since previous end of meal", "Time interval (hrs)"
                )
            ).classes("w-screen-and-padding")


ui.run(
    port=int(mt.env["APP_PORT"]),
    show=False,
    title=mt.config.TITLE,
    storage_secret=mt.env["STORAGE_SECRET"],
)
