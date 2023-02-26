from jinja2 import Template

# Define the template
template_str = """
import tkinter as tk
import customtkinter as ctk
import random

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
        for frame in self.frame:
            value = self.frame[frame]
            if self.debug:
                widget = ctk.CTkFrame(master=self, fg_color=random_color(True))
            else:
                widget = ctk.CTkFrame(master=self, border_width=1, border_color="black")
            widget.grid(row=value[0], column=value[1],rowspan = value[2],columnspan=value[3], sticky="nsew")
            self.placed[frame] = {"widget":widget, "coord":(value)}


app = Application({{debug}})
app.mainloop()

"""
template = Template(template_str)


# Render the template
def render(row_dict, col_dict, frame_dict, debug):
    return template.render(row_dict=row_dict, col_dict=col_dict, frame_dict=frame_dict, debug=debug)

def save(row_dict, col_dict, frame_dict, debug):
    with open('my_template.py', 'w') as f:
        output = render(row_dict, col_dict, frame_dict, debug)
        f.write(output)
