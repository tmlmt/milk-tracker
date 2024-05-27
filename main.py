from nicegui import ui
from textwrap import dedent
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import os
from lib.time_utils import timedelta_to_hrmin, is_time_format
from lib.pandas_utils import prepend_series_to_df, append_series_to_df

# Configuration
ASSETS_DIR = "assets"
FILE_NAME = "journal.xlsx"
PLOTLY_DEFAULT_CONFIG = {"staticPlot": True}
load_dotenv()

df = pd.read_excel(os.path.join(ASSETS_DIR, FILE_NAME))

# -- Clean dataset
# When there's no end_time, make it equal to start time
df.loc[df["end_time"] == "?", "end_time"] = df["start_time"]
# Turn date and time columns to datetime
df["date"] = pd.to_datetime(df["date"])


def compute_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Combine 'Date' and 'Time' into a single datetime column
    # Convert to string first and combine, to circumvent errors in converting excel format to datetime
    df["start_datetime"] = df.apply(
        lambda row: pd.to_datetime(str(row["date"].date()) + " " + str(row["start_time"])),
        axis=1,
    )
    df["end_datetime"] = df.apply(
        lambda row: pd.to_datetime(str(row["date"].date()) + " " + str(row["end_time"])),
        axis=1,
    )

    df.loc[df["end_datetime"] < df["start_datetime"], "end_datetime"] += pd.Timedelta(days=1)

    # Calculate duration
    df["duration"] = df["end_datetime"] - df["start_datetime"]
    df["duration_hrmin"] = df["duration"].apply(timedelta_to_hrmin)
    df["duration_hrs"] = round(df["duration"].dt.total_seconds() / 3600, 2)

    # Calculate other things of interest
    df["previous_end_datetime"] = df["end_datetime"].shift(1)
    df["time_since_previous_start"] = df["start_datetime"].diff()
    df["time_since_previous_start_hrmin"] = df["time_since_previous_start"].apply(
        timedelta_to_hrmin
    )
    df["time_since_previous_start_hrs"] = round(
        df["time_since_previous_start"].dt.total_seconds() / 3600, 2
    )

    df["time_since_previous_end"] = df["start_datetime"] - df["previous_end_datetime"]
    df["time_since_previous_end_hrmin"] = df["time_since_previous_end"].apply(timedelta_to_hrmin)
    df["time_since_previous_end_hrs"] = round(
        df["time_since_previous_end"].dt.total_seconds() / 3600, 2
    )

    return df


df = compute_columns(df)


def get_time_since_latest_end() -> pd.Timestamp:
    return pd.Timestamp.now() - df.iloc[-1]["end_datetime"]


def get_time_since_latest_start() -> pd.Timestamp:
    return pd.Timestamp.now() - df.iloc[-1]["start_datetime"]


def get_latest_meal_info() -> str:
    return dedent(f"""\
    - Date: {df.iloc[-1]["date"].date()}
    - Start time: {df.iloc[-1]["start_time"]}
    - End time: {df.iloc[-1]["end_time"]}
    - Duration: {df.iloc[-1]["duration_hrmin"]}
    """)


def get_current_time(include_sec=True) -> str:
    return f"{datetime.now():%X}" if include_sec else f"{datetime.now():%H:%M}"


def get_current_date() -> str:
    return datetime.now().date().strftime("%Y-%m-%d")


# Dynamic labels and markdown
time_since_latest_end = get_time_since_latest_end()
time_since_latest_start = get_time_since_latest_start()
latest_meal_info = get_latest_meal_info()
current_time = f"{datetime.now():%X}"


def continuous_update() -> None:
    global current_time, time_since_latest_end, time_since_latest_start
    current_time = get_current_time()
    if current_time[-2:] == "00":
        time_since_latest_end = get_time_since_latest_end()
        time_since_latest_start = get_time_since_latest_start()


def force_update(df) -> None:
    global latest_meal_info, table_latest_meals
    continuous_update()
    latest_meal_info = get_latest_meal_info()
    table_latest_meals_container.clear()
    with table_latest_meals_container:
        generate_latest_meals_table(df)
    table_summary_container.clear()
    with table_summary_container:
        generate_summary_table(df)
    figure_duration.update_figure(
        generate_graph(
            df,
            "duration_hrs",
            "Duration as a Function of Start Time for the Latest Three Dates",
            "Duration (hrs)",
        )
    )
    figure_time_since_previous_start.update_figure(
        generate_graph(
            df,
            "time_since_previous_start_hrs",
            "Time interval since previous start of meal",
            "Time interval (hrs)",
        )
    )
    figure_time_since_previous_end.update_figure(
        generate_graph(
            df,
            "time_since_previous_end_hrs",
            "Time interval since previous end of meal",
            "Time interval (hrs)",
        )
    )


ui.timer(1.0, continuous_update)

# Add new entry


def add_entry(df, date, start_time, end_time):
    # Validation
    if not end_time or not date or not start_time:
        ui.notify("All fields must be filled in", type="negative")
        return False
    if not is_time_format(start_time) or not is_time_format(end_time):
        ui.notify("Times must be given in HH:MM format", type="negative")
        return False
    # Creating the new entry
    new_entry = pd.DataFrame(
        [
            {
                "date": pd.to_datetime(date),
                "start_time": str(pd.to_datetime(start_time).time()),
                "end_time": str(pd.to_datetime(end_time).time()),
            }
        ]
    )
    # To compute all columns, we also need the previous meal
    new_entry = compute_columns(
        prepend_series_to_df(df.iloc[-1][["date", "start_time", "end_time"]], new_entry)
    ).iloc[-1]
    # Merging and saving to file
    df = append_series_to_df(new_entry, df)
    save_to_file(df, os.path.join(ASSETS_DIR, FILE_NAME))
    # Clearing inputs
    new_end_time.set_value("")
    new_start_time.set_value(get_current_time(include_sec=False))
    new_date.set_value(get_current_date())
    # Updating UI
    force_update(df)
    # Success message
    ui.notify("Meal added to history", type="positive")


def save_to_file(df, file_path):
    df[["date", "start_time", "end_time"]].to_excel(file_path, index=False)


ui.markdown("# Milk Tracker")

ui.markdown("## Quick check")

with ui.row().classes("items-stretch"):
    with ui.card():
        ui.markdown("##### Latest meal")
        ui.separator()
        ui.markdown().bind_content_from(globals(), "latest_meal_info")
    with ui.card():
        ui.markdown("##### Time since latest end")
        ui.separator()
        with ui.card_section().classes("h-full content-center"):
            ui.label().bind_text_from(
                globals(), "time_since_latest_end", backward=timedelta_to_hrmin
            ).classes("text-3xl")
    with ui.card():
        ui.markdown("##### Time since latest start")
        ui.separator()
        with ui.card_section().classes("h-full content-center"):
            ui.label().bind_text_from(
                globals(), "time_since_latest_start", backward=timedelta_to_hrmin
            ).classes("text-3xl")
    with ui.card():
        ui.markdown("##### Current time")
        ui.separator()
        with ui.card_section().classes("h-full content-center"):
            ui.label().bind_text_from(globals(), "current_time").classes("text-3xl")

ui.markdown("## New meal")

with ui.row().classes("items-stretch"):
    with ui.column():
        ui.markdown("##### Date")
        with ui.input(value=get_current_date()) as new_date:
            with new_date.add_slot("append"):
                ui.icon("edit_calendar").on("click", lambda: menu_new_date.open()).classes(
                    "cursor-pointer"
                )
            with ui.menu().props("auto-close") as menu_new_date:
                ui.date().bind_value(new_date)
    with ui.column():
        ui.markdown("##### Start time")
        with ui.row().classes("items-stretch"):
            ui.button(
                "Now",
                on_click=lambda: new_start_time.set_value(get_current_time(include_sec=False)),
            ).classes("h-full")
            with ui.input(value=get_current_time(include_sec=False)) as new_start_time:
                with new_start_time.add_slot("append"):
                    ui.icon("access_time").on("click", lambda: menu_new_start_time.open()).classes(
                        "cursor-pointer"
                    )
                with ui.menu() as menu_new_start_time:
                    with ui.time().props("format24h").bind_value(new_start_time):
                        with ui.row().classes("justify-end"):
                            ui.button("Close", on_click=menu_new_start_time.close)
    with ui.column():
        ui.markdown("##### End time")
        with ui.row().classes("items-stretch"):
            ui.button(
                "Now", on_click=lambda: new_end_time.set_value(get_current_time(include_sec=False))
            ).classes("h-full")
            with ui.input() as new_end_time:
                with new_end_time.add_slot("append"):
                    ui.icon("access_time").on("click", lambda: menu_new_end_time.open()).classes(
                        "cursor-pointer"
                    )
                with ui.menu() as menu_new_end_time:
                    with ui.time().props("format24h").bind_value(new_end_time):
                        with ui.row().classes("justify-end"):
                            ui.button("Close", on_click=menu_new_end_time.close)
    with ui.column():
        ui.button(
            "Add",
            on_click=lambda: add_entry(
                df, new_date.value, new_start_time.value, new_end_time.value
            ),
        ).classes("h-full w-20")

ui.markdown("## 10 last meals")


def generate_latest_meals_table(df):
    return ui.table.from_pandas(
        df.tail(10)[
            [
                "date",
                "start_time",
                "end_time",
                "duration_hrmin",
                "time_since_previous_start_hrmin",
                "time_since_previous_end_hrmin",
            ]
        ].rename(
            {
                "date": "Date",
                "start_time": "Start time",
                "end_time": "End time",
                "duration_hrmin": "Duration",
                "time_since_previous_start_hrmin": "Time since previous start",
                "time_since_previous_end_hrmin": "Time since previous end",
            }
        )
    )


with ui.element() as table_latest_meals_container:
    generate_latest_meals_table(df)

ui.markdown("## Graphs")


def generate_graph(df, field: str, title: str, yaxis_title: str) -> dict:
    # Get the three latest dates
    latest_dates = df["date"].drop_duplicates().nlargest(3)

    data = []
    for i, date in enumerate(latest_dates):
        date_data = df[df["date"] == date]
        data.append(
            {
                "type": "scatter",
                "name": str(date.date()),
                "mode": "markers+lines",
                "x": [
                    "2024-05-08 " + t for t in date_data["start_time"].astype(str).values.tolist()
                ],
                "y": date_data[field].values.tolist(),
            }
        )

    fig = {
        "data": data,
        "layout": {
            "title": title,
            "xaxis": {"title": "Start Time", "tickformat": "%Hh%M"},
            "yaxis": {"title": yaxis_title},
        },
    }

    return fig

    "Duration as a Function of Start Time for the Latest Three Dates"


figure_duration = ui.plotly(
    generate_graph(
        df,
        "duration_hrs",
        "Duration as a Function of Start Time for the Latest Three Dates",
        "Duration (hrs)",
    )
)
figure_time_since_previous_start = ui.plotly(
    generate_graph(
        df,
        "time_since_previous_start_hrs",
        "Time interval since previous start of meal",
        "Time interval (hrs)",
    )
)
figure_time_since_previous_end = ui.plotly(
    generate_graph(
        df,
        "time_since_previous_end_hrs",
        "Time interval since previous end of meal",
        "Time interval (hrs)",
    )
)

ui.markdown("## Statistics")


def generate_summary_table(df: pd.DataFrame) -> ui.table:
    summary_df: pd.DataFrame = (
        df.groupby("date")
        .agg(
            number_of_rows=pd.NamedAgg(column="date", aggfunc="count"),
            average=pd.NamedAgg(column="duration", aggfunc="mean"),
            min=pd.NamedAgg(column="duration", aggfunc="min"),
            max=pd.NamedAgg(column="duration", aggfunc="max"),
            sum=pd.NamedAgg(column="duration", aggfunc="sum"),
        )
        .reset_index()
    )

    summary_df[["average", "min", "max", "sum"]] = summary_df[
        ["average", "min", "max", "sum"]
    ].apply(
        lambda x: x.apply(timedelta_to_hrmin),
    )

    # Rename the columns for clarity
    summary_df.rename(
        columns={
            "date": "Date",
            "number_of_rows": "Number of meals",
            "average": "Average duration",
            "min": "Minimum duration",
            "max": "Maximum duration",
            "sum": "Cumulative duration",
        },
        inplace=True,
    )

    return ui.table.from_pandas(summary_df)


# Display the summary DataFrame
with ui.element() as table_summary_container:
    generate_summary_table(df)

# Common parameters for ui.run
run_params = {"port": 6520, "show": False, "title": "Milk Tracker"}

# Run in HTTPS if a certificate is given in the .env file
if all(s in os.environ for s in ["SSL_KEYFILE", "SSL_CERTFILE"]):
    run_params.update(
        {"ssl_certfile": os.environ["SSL_CERTFILE"], "ssl_keyfile": os.environ["SSL_KEYFILE"]}
    )

ui.run(**run_params)
