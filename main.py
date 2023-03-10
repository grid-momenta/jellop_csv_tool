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
            file_paths = ["CSV file list for filtering:"]
            for idx, file in enumerate(e.files):
                file_paths.append(file.path)

            csv2_location.value = "\n".join(file_paths)
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

        list2 = ["File saved in:"]
        file_paths = csv2_location.value.split("\n")
        for file_path in file_paths[1:]:
            with open(file_path, encoding="ISO-8859-1") as f:
                list1 = []
                for idx, row in enumerate(f):
                    if idx != 0:
                        list1.append(row.split()[0])
                # list2.append({file_path: list1})

                with open(csv1_location.value, encoding="ISO-8859-1") as f:
                    csv_file = csv.reader(f, delimiter=",")
                    rows = []

                    one_d_dict = {}
                    for value in list1:
                        one_d_dict[value] = True

                    for row in csv_file:
                        if row[0] in one_d_dict:
                            names = row[5].split(" ")
                            fn = names[0] if len(names) else ""
                            ln = names[1] if len(names) > 1 else ""
                            rows.append([row[1], row[2], row[3], row[4], fn, ln])

                    file_location = os.path.dirname(file_path)
                    dir_name = os.path.join(file_location, "FB_upload")
                    if not os.path.exists(dir_name):
                        os.makedirs(dir_name)

                    _, tail = os.path.split(file_path)

                    save_file = f"{dir_name}/FB_upload_{tail}"

                    with open(save_file, 'w', newline='', encoding='utf-8') as c:
                        write = csv.writer(c)
                        write.writerow(["email", "country", "st", "ct", "fn", "ln"])
                        write.writerows(rows)

                    list2.append(save_file)

        result.value = "\n".join(list2)
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
                    on_click=lambda _: my_picker2.pick_files(allow_multiple=True)
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
