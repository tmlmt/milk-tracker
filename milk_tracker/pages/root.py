from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from controllers.app import AppController
from nicegui import ui
from nicegui.events import ValueChangeEventArguments
from pages.header import display_header
from pydantic import ValidationError
from utils.time_utils import (
    get_current_date,
    get_current_time,
    time_between,
    timedelta_to_hrmin,
)


def page(mt: AppController) -> None:
    """Display Root page.

    Parameters
    ----------
    mt : AppController
        Milk Tracker instance

    """
    # Common CSS for all pages
    ui.add_sass(Path("css") / "main.sass")
    # Specific CSS
    ui.add_sass(Path("css") / "table.sass")

    mt.load_meals()

    def force_update_view() -> None:
        generate_latest_meals_table.refresh()
        generate_summary_table.refresh()
        figure_duration.update_figure(
            generate_graph(
                "duration_min",
                "Duration as a function of start time for the latest three dates",
                "Duration (min)",
            )
        )
        figure_time_since_previous_start.update_figure(
            generate_graph(
                "time_since_previous_start_hrs",
                "Time interval since previous START of meal",
                "Time interval (hrs)",
            )
        )
        figure_time_since_previous_end.update_figure(
            generate_graph(
                "time_since_previous_end_hrs",
                "Time interval since previous END of meal",
                "Time interval (hrs)",
            )
        )
        figure_summary_meals.update_figure(
            generate_summary_graph("meals", "Number of meals per day", "Quantity")
        )
        figure_summary_duration.update_figure(
            generate_summary_graph("duration", "Meal duration", "Duration (min)")
        )
        figure_summary_previous_end.update_figure(
            generate_summary_graph(
                "previous_end", "Time since previous end of meal", "Time interval (hrs)"
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

    display_header()

    ui.markdown("# Milk Tracker")

    ui.markdown("## Quick check")

    def confirm_vitamins_baby() -> None:
        if not mt.computed.has_baby_taken_vitamins_today:
            mt.confirm_vitamins_baby()
            checkmark_vitamins_baby.props("round color='secondary'").update()

    def confirm_vitamins_mother() -> None:
        if not mt.computed.has_mother_taken_vitamins_today:
            mt.confirm_vitamins_mother()
            checkmark_vitamins_mother.props("round color='secondary'").update()

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
            with ui.card_section().classes(
                "flex flex-row h-full w-full justify-center content-center"
            ):
                ui.label().bind_text_from(
                    mt.computed, "time_since_latest_end", backward=timedelta_to_hrmin
                ).classes("text-3xl")
                ui.icon("lock", color="grey").bind_visibility_from(
                    mt.computed, "is_ongoing_meal"
                ).classes("w-full self-center")
        with ui.card():
            ui.markdown("##### Previous start")
            ui.separator()
            with ui.card_section().classes(
                "flex flex-row h-full w-full justify-center content-center"
            ):
                ui.label().bind_text_from(
                    mt.computed, "time_since_latest_start", backward=timedelta_to_hrmin
                ).classes("text-3xl")
                ui.icon("lock", color="grey").bind_visibility_from(
                    mt.computed, "is_ongoing_meal"
                ).classes("w-full self-center")
        with ui.card():
            ui.markdown("##### Vitamin 👶")
            ui.separator()
            with ui.card_section().classes(
                "h-full w-full flex justify-center content-center"
            ):
                checkmark_vitamins_baby = ui.button(
                    icon="done", on_click=confirm_vitamins_baby
                ).props(
                    f"round color='{'secondary' if mt.computed.has_baby_taken_vitamins_today else 'grey'}'"  # noqa: E501
                )
        with ui.card():
            ui.markdown("##### Vitamins 👩‍🍼")
            ui.separator()
            with ui.card_section().classes(
                "h-full w-full flex justify-center content-center"
            ):
                checkmark_vitamins_mother = ui.button(
                    icon="done", on_click=confirm_vitamins_mother
                ).props(
                    f"round color='{'secondary' if mt.computed.has_mother_taken_vitamins_today else 'grey'}'"  # noqa: E501
                )

    ui.markdown("## New meal")

    def switch_focus_to_end_time() -> None:
        if len(new_start_time.value) == 5:  # noqa: PLR2004
            # Ref: https://github.com/zauberzeug/nicegui/discussions/2574
            ui.run_javascript(f"getElement({new_end_time.id}).$refs.qRef.focus()")

    def switch_focus_to_start_time() -> None:
        if len(new_end_time.value) == 0:
            ui.run_javascript(f"getElement({new_start_time.id}).$refs.qRef.focus()")

    with ui.row().classes("items-stretch"):
        with ui.column():
            ui.markdown("##### Date")
            with ui.input(value=get_current_date()).props(
                "mask='####-##-##' "
                ":rules='[v => /^[0-9]+-[0-1][0-9]-[0-3][0-9]$/.test(v) || \"Invalid date\"]' "  # noqa: E501
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
                    on_click=lambda: new_start_time.set_value(
                        get_current_time(include_sec=False)
                    ),
                ).bind_enabled_from(
                    mt.computed, "is_ongoing_meal", backward=lambda x: not x
                ).classes("h-full")
                with ui.input(
                    value=mt.get_input_default_value_newmeal_start_time(),
                    on_change=switch_focus_to_end_time,
                ).bind_enabled_from(
                    mt.computed, "is_ongoing_meal", backward=lambda x: not x
                ).props(
                    "mask='time' "
                    ":rules='[ (v, rules) => rules.time(v) || \"Invalid time\"]' "
                    "lazy-rules"
                ).classes("w-24") as new_start_time:
                    with ui.menu().props("no-parent-event") as menu_new_start_time:
                        with ui.time().props("format24h").bind_value(new_start_time):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu_new_start_time.close)
                    with new_start_time.add_slot("append"):
                        ui.icon("access_time").on(
                            "click", menu_new_start_time.open
                        ).classes("cursor-pointer")
        with ui.column():
            ui.markdown("##### End time")
            with ui.row().classes("items-stretch"):
                ui.button(
                    "Now",
                    on_click=lambda: new_end_time.set_value(
                        get_current_time(include_sec=False)
                    ),
                ).classes("h-full")
                with ui.input(on_change=switch_focus_to_start_time).props(
                    "mask='time' "
                    ':rules=\'[ (v, rules) => v == "" | rules.time(v) || "Invalid time"]\' '  # noqa: E501
                    "lazy-rules"
                ).classes("w-24") as new_end_time:
                    with ui.menu().props("no-parent-event") as menu_new_end_time:
                        with ui.time().props("format24h").bind_value(new_end_time):
                            with ui.row().classes("justify-end"):
                                ui.button("Close", on_click=menu_new_end_time.close)
                    with new_end_time.add_slot("append"):
                        ui.icon("access_time").on(
                            "click", menu_new_end_time.open
                        ).classes("cursor-pointer")
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
            generate_meal_round_list.refresh()
        else:
            mt.cancel_ongoing_meal()
            meal_rounds_container.clear()
            force_update_view()

    def handle_meal_round_action() -> None:
        if mt.computed.is_ongoing_meal_paused:
            mt.start_new_meal_round()
        else:
            mt.pause_current_meal_round()
        # Regenerate list of rounds
        generate_meal_round_list.refresh()

    @ui.refreshable
    def generate_meal_round_list() -> Optional[ui.list]:
        if not mt.computed.is_ongoing_meal:
            return None
        with ui.list().props("bordered dense") as meal_round_list:
            for round_number, round_details in enumerate(mt.ongoing_meal.rounds):  # type: ignore[union-attr]
                with ui.item().props(
                    f":active='{round_details.is_active}' active-class='bg-primary text-white'"  # noqa: E501
                ):
                    with ui.item_section().classes("w-24"):
                        ui.item_label(f"Round {round_number+1}")
                    with ui.item_section().classes("w-28"):
                        if round_details.is_active:
                            ui.item_label().bind_text_from(
                                mt.computed, "timer_meal_round"
                            )
                        else:
                            text = time_between(
                                round_details.end_datetime, round_details.start_datetime
                            )  # mypy[arg-type]: end_datetime is not none as the round is
                            #                    not active
                            if (
                                mt.computed.is_ongoing_meal_paused
                                and mt.ongoing_meal
                                and round_number == len(mt.ongoing_meal.rounds) - 1
                            ):
                                text += " (Paused)"
                            ui.item_label(text)

        return meal_round_list

    with ui.column():
        ui.markdown("##### Record meal")
        with ui.row().classes("items-stretch"):
            switch_lock_start_time = (
                ui.switch(
                    "Lock start time",
                    value=mt.computed.is_ongoing_meal,
                    on_change=toggle_newmeal_lock,
                )
                .props("icon='lock_clock' size='lg'")
                .bind_value_from(mt.computed, "is_ongoing_meal")
            )
            with ui.element().classes("content-center"):
                ui.button(on_click=handle_meal_round_action).bind_text_from(
                    mt.computed, "is_ongoing_meal_buttontxt"
                ).bind_enabled_from(mt.computed, "is_ongoing_meal")
        with ui.element() as meal_rounds_container:
            generate_meal_round_list()

    ui.markdown("## 10 last meals")

    @ui.refreshable
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

    generate_latest_meals_table()

    def delete_latest_meal() -> None:
        mt.delete_latest_meal()
        force_update_view()
        ui.notify("Latest meal removed from history", type="positive")

    ui.button("Delete last meal", on_click=delete_latest_meal, color="negative")

    ui.markdown("## Graphs")

    def generate_graph(
        field: Literal[
            "duration_min", "time_since_previous_start_hrs", "time_since_previous_end_hrs"
        ],
        title: str,
        yaxis_title: str,
    ) -> dict:
        # Get the three latest dates
        latest_dates = mt.meals.df["date"].drop_duplicates().nlargest(3)

        graph_data: List[Dict[str, Any]] = []
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
                "legend": {
                    "orientation": "h",
                    "xanchor": "center",
                    "x": 0.5,
                    "yanchor": "top",
                    "y": -0.3,
                },
            },
            "config": mt.config.PLOTLY_DEFAULT_CONFIG,
        }

    with ui.tabs() as tabs_graphs:
        ui.tab("duration", label="Duration")
        ui.tab("previous_start", label="Previous START")
        ui.tab("previous_end", label="Previous END")
    with ui.tab_panels(tabs_graphs, value="previous_end"):
        with ui.tab_panel("duration"):
            figure_duration = ui.plotly(
                generate_graph(
                    "duration_min",
                    "Duration as a function of start time for the latest three dates",
                    "Duration (min)",
                )
            ).classes("w-screen-and-padding")
        with ui.tab_panel("previous_start"):
            figure_time_since_previous_start = ui.plotly(
                generate_graph(
                    "time_since_previous_start_hrs",
                    "Time interval since previous START of meal",
                    "Time interval (hrs)",
                )
            ).classes("w-screen-and-padding")
        with ui.tab_panel("previous_end"):
            figure_time_since_previous_end = ui.plotly(
                generate_graph(
                    "time_since_previous_end_hrs",
                    "Time interval since previous END of meal",
                    "Time interval (hrs)",
                )
            ).classes("w-screen-and-padding")

    ui.markdown("## Statistics")

    @ui.refreshable
    def generate_summary_table() -> ui.table:
        mt.meals.compute_summary()
        return ui.table.from_pandas(mt.meals.df_summary_txt, pagination=0).props(  # type: ignore[arg-type]
            "table-class='sticky-header-column-table' virtual-scroll hide-pagination"
        )

    # Display the summary DataFrame
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
            graph_data[0].update(
                {"y": mt.meals.df_summary_raw["number_of_rows"].array.tolist()}
            )
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
                "xaxis": {"title": "Date", "tickformat": "%Y-%m-%d"},
                "yaxis": {
                    "title": yaxis_title,
                },
                "dragmode": "pan",
                "showlegend": False,
            },
            "config": mt.config.PLOTLY_DEFAULT_CONFIG,
        }

    with ui.tabs() as tabs_summary_graphs:
        ui.tab("meals", label="Meals")
        ui.tab("duration", label="Duration")
        ui.tab("previous_end", label="Previous END")
    with ui.tab_panels(tabs_summary_graphs, value="meals").classes("w-3xl"):
        with ui.tab_panel("meals"):
            figure_summary_meals = ui.plotly(
                generate_summary_graph("meals", "Number of meals per day", "Quantity")
            ).classes("w-screen-and-padding")
        with ui.tab_panel("duration"):
            figure_summary_duration = ui.plotly(
                generate_summary_graph("duration", "Meal duration", "Duration (min)")
            ).classes("w-screen-and-padding")
        with ui.tab_panel("previous_end"):
            figure_summary_previous_end = ui.plotly(
                generate_summary_graph(
                    "previous_end",
                    "Time since previous end of meal",
                    "Time interval (hrs)",
                )
            ).classes("w-screen-and-padding")
