import tkinter as tk
from utils import (
    CreateToolTip,
    Dropdown,
    Input,
    FileSelector,
    Info,
    save_settings,
    load_settings,
)


class Settings(tk.Frame):
    def __init__(self, master, *args):
        super().__init__(master)
        self.speed_options = ["Fast", "Medium", "Slow"]
        self.yes_no_options = ["Yes", "No"]
        self.tooltips = {
            "Spotify Path": "The path to Spotify on your local computer.",
            "Speed": "How fast the script closes and reopens Spotify. Set this value lower if your computer is slow, or is experiencing high CPU usage.",
            "Pause When Locked": "Whether or not to stop the script from restarting Spotify while the Windows account is locked. This helps prevent Spotify restarting when using Spotify on phone and it reaches an ad.",
            "Push To Back": "Whether or not to push Spotify below the active window after restart.",
        }
        self.settings = load_settings()

        self.widget()

    def widget(self):
        Info(
            self,
            text="Updates to settings require the script to be restarted.",
            center=True,
        )._pack(pady=5)

        settings_frame = tk.Frame(self)
        settings_frame.grid_columnconfigure(1, weight=1)
        inputs = []  # may be better known as entries

        def on_change(_):
            if list(self.settings.values()) == [_entry.sv.get() for _entry in inputs]:
                save["state"] = "disabled"
            else:
                save["state"] = "normal"

        ## CREATE INPUT WIDGETS
        for i, (name, setting) in enumerate(self.settings.items()):
            ### CREATE LABEL WIDGET
            label = tk.Label(settings_frame, text=name)
            label.grid(row=i, column=0, padx=10)
            CreateToolTip(label, self.tooltips[name])

            ### CREATE ENTRY WIDGET
            if name == "Speed":
                entry = Dropdown(
                    settings_frame,
                    name,
                    self.speed_options,
                    self.speed_options.index(setting),
                )
            elif name == "Pause When Locked" or name == "Push To Back":
                entry = Dropdown(
                    settings_frame,
                    name,
                    self.yes_no_options,
                    self.yes_no_options.index(setting),
                )
            elif name == "Spotify Path":
                entry = FileSelector(settings_frame, name, setting, on_change=on_change)

            else:
                entry = Input(settings_frame, name=name, value=setting)
            CreateToolTip(entry, self.tooltips[name])
            entry.grid(
                row=i,
                column=1,
                padx=15,
                sticky=tk.W + tk.E,
                pady=2 if name == "Spotify Path" else 0,
            )
            inputs.append(entry)
            entry.on_change = on_change

        ### CREATE SAVE BUTTON WIDGET
        def on_click():
            settings = {}
            for input in inputs:
                value = input.sv.get()
                if value:
                    settings[input.name] = value
                else:
                    settings[input.name] = self.settings[input.name]

            self.settings = settings
            save_settings(settings)
            save["state"] = "disabled"
            self.master.focus()

        save = tk.Button(
            settings_frame,
            text="Save Settings",
            command=on_click,
            state="disabled",
        )
        save.grid(
            row=i + 1, column=0, columnspan=2, pady=10, padx=40, sticky=tk.W + tk.E
        )

        settings_frame.pack(fill="x")
