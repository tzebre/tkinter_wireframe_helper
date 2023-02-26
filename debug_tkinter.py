import tkinter as tk
import customtkinter as ctk
import random
from jija_make import save


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


class Customframe(tk.Frame):
    def __init__(self, master, row=None, col=None, debug=False, **kwargs):
        super().__init__(master)
        self.big_frm_dict = {}
        self.debug = debug
        self.row = row
        self.col = col
        self.dict_args = kwargs
        self.btn_color = None
        self.color = ["silver", "grey"]
        self.selected = {"row": None, "column": None, "rownspan": None, "columnspan": None}
        self.grid_config()

    def grid_config(self):
        for i, r in enumerate(self.row):
            self.grid_rowconfigure(i, weight=r)
        for i, c in enumerate(self.col):
            self.grid_columnconfigure(i, weight=c)
        if self.debug:
            self.all_btn = {}
            for r_i, r in enumerate(self.row):
                self.all_btn[r_i] = {}
                for c_i, c in enumerate(self.col):
                    if ((r_i + 1) + c_i) % 2 == 0:
                        val = 0
                    else:
                        val = 1
                    self.all_btn[r_i][c_i] = {"widget": None, "selected": None}
                    self.all_btn[r_i][c_i]["widget"] = ctk.CTkButton(master=self, fg_color=self.color[val],
                                                                     border_width=2, border_color="firebrick",
                                                                     text=f"r:{r_i}, rw:{r}, c:{c_i}, cw:{c}, {val}",
                                                                     command=lambda r=r_i, c=c_i: self.click(r, c))
                    self.all_btn[r_i][c_i]["widget"].grid(row=r_i, column=c_i, sticky="nsew")

    def click(self, r, c):
        if self.all_btn[r][c]["selected"]:
            if ((r + 1) + c) % 2 == 0:
                val = 0
            else:
                val = 1
            self.all_btn[r][c]["widget"].configure(fg_color=self.color[val])
            self.all_btn[r][c]["selected"] = False
        else:
            self.all_btn[r][c]["widget"].configure(fg_color="darkgreen")
            self.all_btn[r][c]["selected"] = True

    def big_frame(self, row, column, rowspan, columnspan, name):
        self.big_frm_dict[name] = ctk.CTkButton(master=self, fg_color=random_color(True), text=name, state="disabled")
        self.big_frm_dict[name].grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew")


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.frame_to_save = {}
        self.title("Debug")
        self.scale_value = {"row": {}, "col": {}}
        self.config()
        self.attributes("-topmost", True)
        self.saved = {}
        self.custom_frame = {}

    def config(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.row_entry = ctk.CTkEntry(master=self, placeholder_text="Number of row")
        self.col_entry = ctk.CTkEntry(master=self, placeholder_text="Number of colmun")
        self.row_entry.grid(row=0, column=0)
        self.col_entry.grid(row=0, column=1)
        self.ok_btn = ctk.CTkButton(master=self, text="Validate", command=self.place_slider)
        self.ok_btn.grid(row=1, column=0)
        self.exp_code = ctk.CTkButton(master=self, text="export code", command=self.export_code)
        self.exp_code.grid(row=1, column=1)

    def export_code(self):
        row = self.scale_value["row"]
        col = self.scale_value["col"]
        frame = self.frame_to_save
        save(row, col, frame, True)

    def display(self):
        self.row = list(self.scale_value["row"].values())
        self.col = list(self.scale_value["col"].values())

    def scale_mvd(self, value, c, r):
        self.delete_all_group()
        if c == 0:
            self.scale_value["row"][r] = int(value)
        else:
            self.scale_value["col"][r] = int(value)
        self.display()
        self.custom.row = self.row
        self.custom.col = self.col
        self.custom.grid_config()

    def place_slider(self):
        ok = False
        nb_col = 0
        nb_row = 0
        try:
            nb_row = int(self.row_entry.get())
            ok = True
        except ValueError as v:
            print(f"Please enter a valid integer for row: {v}")
            ok = False
        try:
            nb_col = int(self.col_entry.get())
            ok = True
        except ValueError as v:
            print(f"Please enter a valid integer for col: {v}")
            ok = False
        if ok:
            self.scale_value = {"row": {}, "col": {}}
            try:
                self.slider_frame_row.destroy
                self.slider_frame_col.destroy
            except AttributeError:
                print("slider already destroyed")
            self.slider_frame_row = ctk.CTkFrame(master=self)
            self.slider_frame_row.grid_columnconfigure(0, weight=1)
            self.slider_frame_row.grid(row=2, column=0, sticky="nsew")
            self.slider_frame_col = ctk.CTkFrame(master=self)
            self.slider_frame_col.grid_columnconfigure(0, weight=1)
            self.slider_frame_col.grid(row=2, column=1, sticky="nsew")
            frame = [self.slider_frame_row, self.slider_frame_col]
            for i, w in enumerate([nb_row, nb_col]):
                for line in range(w):
                    if i == 0:
                        self.scale_value["row"][line] = 1
                    else:
                        self.scale_value["col"][line] = 1
                    self.display()
                    frame[i].grid_rowconfigure(line, weight=1)
                    slider = tk.Scale(master=frame[i], from_=1, to=10, orient="horizontal", bd=0, sliderrelief=tk.FLAT,
                                      troughcolor='gray92', activebackground="#1F6AA5",
                                      command=lambda value, c=i, r=line: self.scale_mvd(value, c, r))
                    slider.grid(row=line, column=0, sticky="nsew", padx=3)
            self.add_group()
            self.create_toplevel()

    def create_toplevel(self):
        try:
            self.top_level.destroy()
            self.delete_all_group()
        except:
            pass
        self.top_level = tk.Toplevel(self)
        self.top_level.lower(belowThis=self)
        self.top_level.geometry(
            "{}x{}+{}+{}".format(self.winfo_screenwidth(), self.winfo_screenheight(), int(0), int(0)))
        self.top_level.lower(belowThis=self)
        self.top_level.grid_columnconfigure(0, weight=1)
        self.top_level.grid_rowconfigure(0, weight=1)
        self.custom = Customframe(self.top_level, self.row, self.col, True)
        self.custom.grid(row=0, column=0, sticky="nsew")

    def add_group(self):
        row = 3 + len(self.saved)
        display_btn = ctk.CTkButton(master=self, text="save", command=lambda r=row: self.saving_group(r))
        display_btn.grid(row=row, column=0)
        display_Label = ctk.CTkEntry(master=self, placeholder_text="Name of group")
        display_Label.grid(row=row, column=1)
        self.saved[row] = {"btn": display_btn, "entry": display_Label}

    def saving_group(self, row):
        self.saved[row]["btn"].configure(text="delete", command=lambda r=row: self.delete(r))
        self.saved[row]["entry"].configure(state="disabled")
        group_name = self.saved[row]["entry"].get()
        self.get_selected_btn(group_name)
        self.group_frame(group_name)
        self.add_group()

    def delete(self, row):
        group_name = self.saved[row]["entry"].get()
        self.custom.big_frm_dict[group_name].destroy()
        self.custom.big_frm_dict.pop(group_name)
        self.frame_to_save.pop(group_name)
        for case in self.custom_frame[group_name]["coords"]:
            self.custom.all_btn[case[0]][case[1]]["widget"].configure(state="normal")
            self.custom.all_btn[case[0]][case[1]]["selected"] = True
            self.custom.click(case[0], case[1])
        self.custom_frame.pop(group_name)
        self.saved[row]["btn"].destroy()
        self.saved[row]["entry"].destroy()
        self.saved.pop(row)
        self.place_group()

    def place_group(self):
        new_saved = {}
        for i, r in enumerate(self.saved.values()):
            txt = r["btn"].cget("text")
            entry_txt = r["entry"].get()
            if txt == "delete":
                str_var = tk.StringVar()
                str_var.set(entry_txt)
                display_btn = ctk.CTkButton(master=self, text=txt, command=lambda row=i + 3: self.delete(row))
                display_Label = ctk.CTkEntry(master=self, textvariable=str_var, state="disabled")
            else:
                display_btn = ctk.CTkButton(master=self, text=txt, command=lambda row=i + 3: self.saving_group(row))
                display_Label = ctk.CTkEntry(master=self, placeholder_text=entry_txt)
            display_btn.grid(row=i + 3, column=0)
            display_Label.grid(row=i + 3, column=1)
            new_saved[i + 3] = {"btn": display_btn, "entry": display_Label}
            r["btn"].destroy()
            r["entry"].destroy()
        self.saved = new_saved

    def get_selected_btn(self, group_name):
        color = random_color(True)
        for row in self.custom.all_btn:
            for col in self.custom.all_btn[row]:
                if self.custom.all_btn[row][col]["selected"]:
                    self.custom.all_btn[row][col]["selected"] = False
                    if group_name not in self.custom_frame:
                        self.custom_frame[group_name] = {"coords": [(row, col)], "frame": None}
                    else:
                        self.custom_frame[group_name]["coords"].append((row, col))
                    self.custom.all_btn[row][col]["widget"].configure(state="disabled", fg_color=color)

    def delete_all_group(self):
        self.custom_frame = {}
        self.frame_to_save = {}
        for r in self.saved.values():
            r["btn"].destroy()
            r["entry"].destroy()
        self.saved = {}
        self.add_group()

    def group_frame(self, group_name):
        coords = self.custom_frame[group_name]["coords"]
        row_list = []
        col_list = []
        for c in coords:
            row_list.append(c[0])
            col_list.append(c[1])
        row_list = list(set(row_list))
        col_list = list(set(col_list))
        row = min(row_list)
        col = min(col_list)
        rowspan = (max(row_list) - row) + 1
        columnspan = (max(col_list) - col) + 1
        self.frame_to_save[group_name] = (row, col, rowspan, columnspan)
        self.custom.big_frame(row, col, rowspan, columnspan, group_name)


app = Application()
app.mainloop()
