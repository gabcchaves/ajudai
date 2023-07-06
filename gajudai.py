import PySimpleGUI as sg

# Layout.
layout = [
    [sg.Menu([
        ["File", [
            {"Open": {"image_filename": "res/plus-icon.svg"}},
            "Save",
            "Exit"
        ]]
    ])],
    [sg.Text("Content")],
]

window = sg.Window("Window Title", layout, size=(800, 600))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "Exit":
        break

window.close()
