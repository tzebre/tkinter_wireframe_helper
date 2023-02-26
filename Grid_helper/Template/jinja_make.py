from jinja2 import Template

# Define the template
template_str = """
import tkinter as tk
import customtkinter as ctk
import random

def create_widget(widget_type, parent):
    if widget_type == "Frame" or widget_type is None:
        widget = ctk.CTkFrame(master=parent)
    elif widget_type == "ScrollableFrame":
        widget = ctk.CTkScrollableFrame(master=parent)
    elif widget_type == "Textbox":
        widget = ctk.CTkTextbox(master=parent)
    elif widget_type == "Button":
        widget = ctk.CTkButton(master=parent)
    elif widget_type == "Label":
        widget = ctk.CTkLabel(master=parent)
    elif widget_type == "Entry":
        widget = ctk.CTkEntry(master=parent)
    elif widget_type == "OptionMenu":
        widget = ctk.CTkOptionMenu(master=parent)
    elif widget_type == "SegmentedButton":
        widget = ctk.CTkSegmentedButton(master=parent)
    elif widget_type == "Switch":
        widget = ctk.CTkSwitch(master=parent)
    elif widget_type == "Checkbox":
        widget = ctk.CTkCheckBox(master=parent)
    elif widget_type == "RadioButton":
        widget = ctk.CTkRadioButton(master=parent)
    elif widget_type == "Slider":
        widget = ctk.CTkSlider(master=parent)
    else:
        raise ValueError(f"Invalid widget type: {widget_type}")

    widget.grid(row=0, column=0)
    return widget

def random_color(hex_val):
    for i in range(3):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        rgb = [r, g, b]
        if hex_val:
            return f"#{r:02x}{g:02x}{b:02x}"
        else:
            return rgb

class Application(ctk.CTk):
    def __init__(self, debug):
        super().__init__()
        self.debug = debug
        self.title("###")  # change title here
        self.row = {{row_dict}}
        self.col = {{col_dict}}
        self.frame = {{frame_dict}}
        self.widget = {{widgets_list}}
        self.placed = {}
        self.geometry(
            "{}x{}+{}+{}".format(self.winfo_screenwidth(), self.winfo_screenheight(), int(0), int(0)))
        self.make_grid()
        if self.debug:
            self.color_grid()
        self.place_frame()

    def color_grid(self):
        color = ["silver", "grey"]
        for r in self.row:
            for c in self.col:
                if ((r + 1) + c) % 2 == 0:
                    val = 0
                else:
                    val = 1
                coloring = ctk.CTkButton(master=self, fg_color=color[val], text=f"r:{r},c:{c}", state = "disabled", text_color_disabled="black")
                coloring.grid(row=r, column=c, sticky="nsew")

    def make_grid(self):
        for r in self.row:
            print(r, self.row[r])
            self.grid_rowconfigure(r, weight=self.row[r])
        for c in self.col:
            self.grid_columnconfigure(c, weight=self.col[c])

    def place_frame(self):
        for i,frame in enumerate(self.frame):
            value = self.frame[frame]["coords"]
            if self.debug:
                parent = ctk.CTkFrame(master=self, fg_color=random_color(True))
            else:
                parent = ctk.CTkFrame(master=self, border_width=1, border_color="black")
            parent.grid(row=value[0], column=value[1],rowspan = value[2],columnspan=value[3], sticky="nsew")
            parent.grid_rowconfigure(0, weight=1)
            parent.grid_columnconfigure(0, weight=1)
            widget = create_widget(self.widget[i], parent)
            self.placed[frame] = {"parent": parent,"widget":widget, "coord":(value)}


app = Application({{debug}})
app.mainloop()

"""
template = Template(template_str)


# Render the template
def render(row_dict, col_dict, frame_dict, debug):
    widgets_list = []
    for f in frame_dict:
        widgets_list.append(frame_dict[f]["Type"])
    return template.render(row_dict=row_dict, col_dict=col_dict, frame_dict=frame_dict, debug=debug,
                           widgets_list=widgets_list)


def save(row_dict, col_dict, frame_dict, debug, dest):
    print(dest)
    print("save")
    with open(f"{dest}/my_template.py", 'w') as f:
        output = render(row_dict, col_dict, frame_dict, debug)
        f.write(output)
