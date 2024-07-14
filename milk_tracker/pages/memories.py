from controllers.app import AppController
from nicegui import events, ui
from pages.header import display_header
from pydantic import ValidationError
from schemas.memory import Memory
from utils.time_utils import get_current_date


def page(mt: AppController) -> None:
    """Display Memories page.

    Parameters
    ----------
    mt : AppController
        Milk Tracker instance

    """
    display_header()
    ui.markdown("# Milk Tracker")
    ui.markdown("## Memories")
    mt.load_memories()

    table = ui.table.from_pandas(mt.memories.df).classes("w-full")
    for column in table.columns:
        column.update({"align": "left", "sortable": True})
        if column["field"] in ["date", "age"]:
            column.update({"headerClasses": "w-36"})

    table.add_slot(
        "header",
        r"""
        <q-tr :props="props">
            <q-th key="date" :props="props">
                Date
            </q-th>
            <q-th key="age" :props="props">
                Age
            </q-th>
            <q-th key="description" :props="props">
                Description
            </q-th>
            <q-th auto-width />
        </q-tr>
    """,
    )
    table.add_slot(
        "body",
        r"""
        <q-tr :props="props">
            <q-td key="date" :props="props">
                {{ props.row.date }}
                <q-popup-edit v-model="props.row.date" v-slot="scope"
                    @update:model-value="() => $parent.$emit('edit_entry', props.row)"
                >
                    <q-input v-model="scope.value"
                        dense autofocus counter
                        @keyup.enter="scope.set"
                    />
                </q-popup-edit>
            </q-td>
            <q-td key="age" :props="props">
                {{ props.row.age }}
            </q-td>
            <q-td key="description" :props="props">
                {{ props.row.description }}
                <q-popup-edit v-model="props.row.description" v-slot="scope"
                    @update:model-value="() => $parent.$emit('edit_entry', props.row)"
                >
                    <q-input v-model.number="scope.value" type="text"
                        dense autofocus counter
                        @keyup.enter="scope.set"
                    />
                </q-popup-edit>
            </q-td>
            <q-td auto-width>
                <q-btn size="sm" color="warning" round dense icon="delete"
                    @click="() => $parent.$emit('delete', props.row)"
                />
            </q-td>
        </q-tr>
    """,
    )

    # Reusable Dialog Element
    with ui.dialog() as dialog, ui.card():
        ui.label("Are you sure?")
        with ui.row():
            ui.button("Yes", on_click=lambda: dialog.submit("Yes"))
            ui.button("No", on_click=lambda: dialog.submit("No"))

    def add_row() -> None:
        try:
            new_entry = Memory(
                date=new_memory_date.value, description=new_memory_description.value
            )
        except ValidationError:
            ui.notify("Check that your input is correct", type="negative")
            return
        mt.memories.add(new_entry)
        mt.memories.save_to_file()
        table.rows[:] = mt.memories.table_rows
        table.update()
        new_memory_date.value = get_current_date()
        new_memory_description.value = "-"
        ui.notify("Memory added", type="positive")

    def edit_entry(e: events.GenericEventArguments) -> None:
        try:
            edited_memory = Memory(date=e.args["date"], description=e.args["description"])
        except ValidationError:
            ui.notify("Check that your input is correct", type="negative")
            return
        mt.memories.edit(e.args["index"], edited_memory)
        mt.memories.save_to_file()
        table.rows[:] = mt.memories.table_rows
        table.update()
        ui.notify("Memory edited", type="positive")

    async def delete(e: events.GenericEventArguments) -> None:
        result = await dialog
        if result == "Yes":
            mt.memories.remove(e.args["index"])
            mt.memories.save_to_file()
            table.rows[:] = mt.memories.table_rows
            ui.notify(
                f'Deleted Memory with DATE {e.args["date"]} and INDEX {e.args["index"]}',
                type="positive",
            )
            table.update()

    with table.add_slot("top-row"):
        with table.row():
            with table.cell():
                with ui.input(value=get_current_date()).props(
                    "mask='####-##-##' "
                    ":rules='[v => /^[0-9]+-[0-1][0-9]-[0-3][0-9]$/.test(v) || \"Invalid date\"]' "  # noqa: E501
                    "lazy-rules"
                ).classes("w-36") as new_memory_date:
                    with ui.menu().props("auto-close no-parent-event") as menu_new_date:
                        ui.date().bind_value(new_memory_date)
                    with new_memory_date.add_slot("append"):
                        ui.icon("edit_calendar").on("click", menu_new_date.open).classes(
                            "cursor-pointer"
                        )
            with table.cell().classes("!bg-gray-100"):
                ui.label("-")
            with table.cell():
                new_memory_description = ui.input().props(
                    ":rules='[v => v.length > 0 || \"Empty description\"]'"
                )
            with table.cell():
                pass
        with table.row():
            with table.cell().props("colspan=4"):
                ui.button("Add row", icon="add", on_click=add_row).classes("w-full")

    table.on("edit_entry", edit_entry)
    table.on("delete", delete)
