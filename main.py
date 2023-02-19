import flet_core.icons
from flet import *
import csv
from datetime import datetime
import os


def main(page: Page):
    page.padding = 20
    page.title = "Jellop CSV Tool"

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
        with open(csv2_location.value, encoding="ISO-8859-1") as f:
            for idx, row in enumerate(f):
                if idx != 0:
                    list2.append(row.split()[0])

        with open(csv1_location.value, encoding="ISO-8859-1") as f:
            csv_file = csv.reader(f, delimiter=",")
            headers = next(csv_file)
            rows = []


            one_d_dict = {}
            for value in list2:
                one_d_dict[value] = True

            for row in csv_file:
                if row[0] in one_d_dict:
                    rows.append(row)

            file_location = os.path.dirname(csv2_location.value)
            dir_name = os.path.join(file_location, "FB_upload")
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)

            _, tail = os.path.split(csv2_location.value)

            save_file = f"{dir_name}/FB_upload_{tail}"

            with open(save_file, 'w', newline='') as c:
                write = csv.writer(c)
                write.writerow(headers)
                write.writerows(rows)

            result.value = f'File saved in {save_file}'
            result.update()
            return

    page.add(
        Column([
            Column([
                ElevatedButton(
                    "Pick CSV 1",
                    icon=flet_core.icons.UPLOAD_FILE,
                    on_click=lambda _: my_picker1.pick_files(allow_multiple=False)
                ),
                csv1_location,
                ElevatedButton(
                    "Pick CSV 2 (ID list)",
                    icon=flet_core.icons.UPLOAD_FILE,
                    on_click=lambda _: my_picker2.pick_files(allow_multiple=False)
                ),
                csv2_location,
                ElevatedButton(
                    "Process",
                    on_click=process_search
                ),
                result,
                Container(
                    content=Column([Text("CG Engineering, Inc 2023")]),
                    margin=Margin(top=300, bottom=0, left=500, right=0)
                ),
            ], expand=True),
        ])
    )


flet.app(target=main)
