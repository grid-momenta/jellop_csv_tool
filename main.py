import flet_core.icons
from flet import *
import csv
from datetime import datetime
from pathlib import Path


def main(page: Page):
    csv1_location = Text("")
    csv2_location = Text("")
    result = Text("")

    def picker1_dialogue(e: FilePickerResultEvent):
        if e.files and len(e.files):
            csv1_location.value = e.files[0].path
            csv1_location.update()

    def picker2_dialogue(e: FilePickerResultEvent):
        if e.files and len(e.files):
            csv2_location.value = e.files[0].path
            csv2_location.update()

    my_picker1 = FilePicker(on_result=picker1_dialogue)
    page.overlay.append(my_picker1)
    page.update()

    my_picker2 = FilePicker(on_result=picker2_dialogue)
    page.overlay.append(my_picker2)
    page.update()

    def process_search(e):
        result.value = ""
        result.update()

        if csv1_location.value == "" or csv2_location.value == "":
            result.value = "Please upload 2 csv files."
            result.update()
            return

        list2 = []
        with open(csv2_location.value, encoding='utf-8') as f:
            for idx, row in enumerate(f):
                if idx != 0:
                    list2.append(row.split()[0])

        with open(csv1_location.value, encoding='utf-8') as f:
            csv_file = csv.reader(f, delimiter=",")
            headers = next(csv_file)
            rows = []

            for row in csv_file:
                if row[0] in list2:
                    rows.append(row)

            home = str(Path.home() / "Downloads")
            with open(f'{home}/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv', 'w') as c:
                write = csv.writer(c)
                write.writerow(headers)
                write.writerows(rows)

        result.value = f'File saved in {home}/{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv'
        result.update()

    page.add(
        Column([
            ElevatedButton("Pick CSV 1", icon=flet_core.icons.UPLOAD_FILE, on_click=lambda _: my_picker1.pick_files(allow_multiple=False)),
            csv1_location,
            ElevatedButton("Pick CSV 2", icon=flet_core.icons.UPLOAD_FILE, on_click=lambda _: my_picker2.pick_files(allow_multiple=False)),
            csv2_location,
            ElevatedButton("Process", on_click=process_search),
            result,
        ])
    )


flet.app(target=main)
