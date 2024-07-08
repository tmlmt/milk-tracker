from controllers.app import AppController
from nicegui import events, ui
from pages.header import display_header
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

    table = ui.table.from_pandas(mt.memories.df).classes("w-[30rem]")
    table.add_slot(
        "header",
        r"""
        <q-tr :props="props">
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
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
            <q-td auto-width >
                <q-btn size="sm" color="warning" round dense icon="delete"
                    @click="() => $parent.$emit('delete', props.row)"
                />
            </q-td>
        </q-tr>
    """,
    )

    def add_row() -> None:
        table.rows.append({"date": get_current_date(), "description": "New guy"})
        ui.notify("Added new row")
        table.update()

    def edit_entry(e: events.GenericEventArguments) -> None:
        for row in table.rows:
            if row["date"] == e.args["date"]:
                row.update(e.args)
        ui.notify(f"Updated rows to: {table.rows}")
        table.update()

    def delete(e: events.GenericEventArguments) -> None:
        table.rows[:] = [row for row in table.rows if row["id"] != e.args["id"]]
        ui.notify(f'Deleted row with ID {e.args["id"]}')
        table.update()

    with table.add_slot("bottom-row"):
        with table.cell().props("colspan=3"):
            ui.button("Add row", icon="add", color="accent", on_click=add_row).classes(
                "w-full"
            )

    table.on("edit_entry", edit_entry)
    table.on("delete", delete)
