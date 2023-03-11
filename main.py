import flet_core.icons
from flet import *
import csv
import os


def main(page: Page):
    page.padding = 20
    page.title = "Jellop CSV Tool"
    page.auto_scroll = True
    # page.horizontal_alignment = "center"

    csv1_location = Text("", opacity=0)
    csv2_location = Text("", opacity=0)

    def picker1_dialogue(e: FilePickerResultEvent):
        if e.files and len(e.files):
            csv1_location.value = e.files[0].path
            csv1_location.update()

            results.controls.append(Text(f"> CSV 1 picked.\n   {e.files[0].path}", style=TextThemeStyle.BODY_MEDIUM))
            results.update()

    def picker2_dialogue(e: FilePickerResultEvent):
        if e.files and len(e.files):
            file_paths = []
            for idx, file in enumerate(e.files):
                file_paths.append(file.path)

            csv2_location.value = "\n".join(file_paths)
            csv2_location.update()

            results.controls.append(Text(f"> CSV 2 picked.\n   " + "\n   ".join(file_paths), style=TextThemeStyle.BODY_MEDIUM))
            results.update()

    my_picker1 = FilePicker(on_result=picker1_dialogue)
    page.overlay.append(my_picker1)
    page.update()

    my_picker2 = FilePicker(on_result=picker2_dialogue)
    page.overlay.append(my_picker2)
    page.update()

    def process_search(e):
        results.controls.append(pb)
        pb.opacity = 1
        results.update()

        if csv1_location.value == "" or csv2_location.value == "":
            results.controls.append(Text("> Please upload csv files.", style=TextThemeStyle.BODY_MEDIUM, color="red"))
            results.update()
            return

        list2 = []
        file_paths = csv2_location.value.split("\n")
        for file_path in file_paths:
            with open(file_path, encoding="ISO-8859-1") as f:
                list1 = []
                for idx, row in enumerate(f):
                    if idx != 0:
                        list1.append(row.split()[0])

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

        pb.value = 1
        pb.update()
        results.controls.append(
            Text("> File Saved in:\n   " + "\n   ".join(list2), style=TextThemeStyle.BODY_MEDIUM))
        results.update()
        return

    pb = ProgressBar(width=800, color="amber", bgcolor="#eeeeee", opacity=0)

    results = Column([
        Text("> Pick CSV 1 and CSV 2. Then click Process.", style=TextThemeStyle.BODY_LARGE)
    ])

    page.add(
        Column(
            [
                Container(
                    content=Column(
                        [
                            Row(
                                [
                                    Text("Jellop CSV Tool", style=TextThemeStyle.DISPLAY_MEDIUM)
                                ],
                                alignment=MainAxisAlignment.CENTER
                            ),
                            Divider(height=9, thickness=3),
                            Row(
                                [
                                    ElevatedButton(
                                        "Pick CSV 1",
                                        icon=flet_core.icons.UPLOAD_FILE,
                                        on_click=lambda _: my_picker1.pick_files(allow_multiple=False)
                                    ),
                                    ElevatedButton(
                                        "Pick CSV 2 (ID list)",
                                        icon=flet_core.icons.UPLOAD_FILE,
                                        on_click=lambda _: my_picker2.pick_files(allow_multiple=True)
                                    ),
                                    ElevatedButton(
                                        "Process",
                                        on_click=process_search
                                    ),
                                ],
                                alignment=MainAxisAlignment.SPACE_AROUND,
                                width=500,
                            ),
                            Container(
                                content=results,
                                bgcolor=colors.AMBER_50,
                                padding=30,
                                border_radius=10,
                                width=800,
                            ),
                        ],
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                ),
                Container(
                    content=Text("CG Engineering, Inc 2023"),
                    margin=margin.only(top=300),
                ),
                csv1_location,
                csv2_location
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.SPACE_AROUND,
        ),
    )


flet.app(target=main)
