import tkinter as tk
import customtkinter as ctk
import random
from jinja_make import save

_DEBUG_ = False



def random_color(hex_val):
    """

    Args:
        hex_val: Bool true if return hex code color if false rgb code color

    Returns:
        string : Hex color code or rgb code
    """
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
    """
        A class that creates a custom frame with selectable grid cells.

        Args:
            master (Tk): The parent window of the frame.
            row (list): A list of relative weights for each row.
            col (list): A list of relative weights for each column.
            **kwargs: Additional keyword arguments.

        Attributes:
            big_frm_dict (dict): A dictionary to store big frames.
            all_btn (dict): A dictionary to store all buttons.
            debug (bool): A flag to indicate whether to display debug information.
            row (list): A list of relative weights for each row.
            col (list): A list of relative weights for each column.
            dict_args (dict): A dictionary to store additional keyword arguments.
            btn_color (None): The color of the button.
            color (list): A list of alternating colors for the button.
            selected (dict): A dictionary to store the selected cell.

        Methods:
            grid_config(): Configures the grid layout of the custom frame.
            click(r, c): A callback function for the button click event.
            big_frame(row, column, rowspan, columnspan, name): Creates a big frame.

        """

    def __init__(self, master, row=None, col=None, **kwargs):
        super().__init__(master)
        self.big_frm_dict = {}
        self.all_btn = {}
        self.debug = True
        self.row = row
        self.col = col
        self.dict_args = kwargs
        self.btn_color = None
        self.color = ["silver", "grey"]
        self.selected = {"row": None, "column": None, "rownspan": None, "columnspan": None}
        self.grid_config()

    def grid_config(self):
        """
        Configure the grid with value in self.row and self.col.
        If debug = True fill each case of grid with button and store all button in self.all_btn
        """
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
                                                                     command=lambda r_lbd=r_i, c_lbd=c_i: self.click(
                                                                         r_lbd, c_lbd))
                    self.all_btn[r_i][c_i]["widget"].grid(row=r_i, column=c_i, sticky="nsew")

    def click(self, r, c):
        """
        If click on a button this method is called
        button became disabled
        Args :
            r (int) : row of the button
            c (int) : col of the button
        """
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
        """
        Create biger button fi groupe is saved

        Args :
            row : starting row
            column : starting column
            rowspan : nb of row to expend
            columnspan : nb of col to expend
            nam : name of the group
        """
        frame = ctk.CTkFrame(master=self, fg_color=random_color(True), border_width=2, border_color="firebrick")
        frame.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        self.big_frm_dict[name] = {"frame": frame, "widget": None}
        combobox = ctk.CTkOptionMenu(master=frame,
                                     values=["Frame", "ScrollableFrame", "Textbox", "Button", "Label", "Entry",
                                             "OptionMenu",
                                             "SegmentedButton", "Switch", "Checkbox", "RadioButton", "Slider"],
                                     command=lambda event, name=name: self.get_combovalue(event, name))
        combobox.grid(row=0, column=0)

    def get_combovalue(self, event, name):
        self.big_frm_dict[name]["widget"] = event
        Application.change_type(event, name)


class Application(ctk.CTk):
    frame_to_save = {}

    def __init__(self):
        """
        Init a new instance of class Application
        Attributes:
            self.top_level: tk.Toplevel where the grid frame is displayed
            self.custom: Customframe displayed in self.top_level
            self.slider_frame_row: Frame containing slider for row weight
            self.slider_frame_col: Frame containing slider for col weight
            self.row_entry: Entry for row number
            self.col_entry: Entry for col number.
            self.ok_btn: Button to make the grid with x row and y col all with weight 1
            self.exp_code: Button to create a code template
            self.row: Number of row
            self.col: Number of col
            self.frame_to_save: Dictionary with frame name as key and parameters as value
            self.scale_value: Dictionary with scale value for row and column
            self.saved: Dictionary with button and entry value for each scale
            self.custom_frame: Dictionary with keys for group name, coords of all grid button in this frame
        """
        super().__init__()
        self.top_level = None
        self.custom = None
        self.slider_frame_row = None
        self.slider_frame_col = None
        self.row_entry = None
        self.col_entry = None
        self.ok_btn = None
        self.exp_code = None
        self.row = None
        self.col = None
        self.title("Debug")
        self.scale_value = {"row": {}, "col": {}}
        self.config()
        self.attributes("-topmost", True)
        self.saved = {}
        self.custom_frame = {}

    def config(self):
        """
        Method to make the grid and place button in window
        """
        for column_nb in range(2):
            self.grid_columnconfigure(column_nb, weight=1)
        for row_nb in range(4):
            self.grid_rowconfigure(row_nb, weight=1)
        self.row_entry = ctk.CTkEntry(master=self, placeholder_text="Number of row")
        self.col_entry = ctk.CTkEntry(master=self, placeholder_text="Number of column")
        self.row_entry.grid(row=0, column=0)
        self.col_entry.grid(row=0, column=1)
        self.ok_btn = ctk.CTkButton(master=self, text="Validate", command=self.place_slider)
        self.ok_btn.grid(row=1, column=0)
        self.exp_code = ctk.CTkButton(master=self, text="export code", command=self.export_code)
        self.exp_code.grid(row=1, column=1)

    def export_code(self):
        """
        Method to prepare args and call template creation
        """
        row = self.scale_value["row"]
        col = self.scale_value["col"]
        frame = Application.frame_to_save
        save(row, col, frame, _DEBUG_)

    def get_slider_value(self):
        """
        Get list of slider value
        """
        self.row = list(self.scale_value["row"].values())
        self.col = list(self.scale_value["col"].values())

    def scale_mvd(self, value, c, r):
        """
        Method to save scale value when they change
        Args:
            value (int): The new value of the scale moved.
            c (int): The column index of the scale moved.
            r (int): The row index of the scale moved.

        Returns:
            None.

        Raises:
            None.
        """
        self.delete_all_group()
        if c == 0:
            self.scale_value["row"][r] = int(value)
        else:
            self.scale_value["col"][r] = int(value)
        self.get_slider_value()
        self.custom.row = self.row
        self.custom.col = self.col
        self.custom.grid_config()

    def place_slider(self):
        try:
            nb_row = int(self.row_entry.get())
        except ValueError as v:
            print(f"Please enter a valid integer for row number. {v}")
            # TODO Error window
            return
        try:
            nb_col = int(self.col_entry.get())
        except ValueError as v:
            print(f"Please enter a valid integer for column number. {v}")
            # TODO Error window
            return
        self.scale_value = {"row": {}, "col": {}}
        self.slider_frame_row = ctk.CTkFrame(master=self)
        self.slider_frame_row.grid_columnconfigure(0, weight=1)
        self.slider_frame_row.grid(row=2, column=0, sticky="nsew")
        self.slider_frame_col = ctk.CTkFrame(master=self)
        self.slider_frame_col.grid_columnconfigure(0, weight=1)
        self.slider_frame_col.grid(row=2, column=1, sticky="nsew")
        frame = [self.slider_frame_row, self.slider_frame_col]
        for i, what in enumerate([nb_row, nb_col]):
            for line in range(what):
                if i == 0:
                    self.scale_value["row"][line] = 1
                else:
                    self.scale_value["col"][line] = 1
                frame[i].grid_rowconfigure(line, weight=1)
                slider = tk.Scale(master=frame[i], from_=1, to=10, orient="horizontal", bd=0, sliderrelief=tk.FLAT,
                                  troughcolor='gray92', activebackground="#1F6AA5",
                                  command=lambda value, c=i, r=line: self.scale_mvd(value, c, r))
                slider.grid(row=line, column=0, sticky="nsew", padx=3)
        self.get_slider_value()
        self.add_group()
        self.create_toplevel()

    def create_toplevel(self):
        """
        Create a top level full size window and put a Custom frame inside
        """
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
        self.custom = Customframe(self.top_level, self.row, self.col)
        self.custom.grid(row=0, column=0, sticky="nsew")

    def add_group(self):
        """
        Add a button and entry for define a new group
        """
        row = 3 + len(self.saved)
        display_btn = ctk.CTkButton(master=self, text="save", command=lambda r=row: self.saving_group(r))
        display_btn.grid(row=row, column=0)
        display_label = ctk.CTkEntry(master=self, placeholder_text="Name of group")
        display_label.grid(row=row, column=1)
        self.saved[row] = {"btn": display_btn, "entry": display_label}

    def saving_group(self, row):
        """
        Save a new group

        Args :
            row : Row to save
        """
        self.saved[row]["btn"].configure(text="delete", command=lambda r=row: self.delete(r))
        self.saved[row]["entry"].configure(state="disabled")
        group_name = self.saved[row]["entry"].get()
        self.get_selected_btn(group_name)
        self.group_frame(group_name)
        self.add_group()

    def delete(self, row):
        """
        Delete a group if clic on delete
        Args:
            row : Row of the group to delete
        """
        group_name = self.saved[row]["entry"].get()
        self.custom.big_frm_dict[group_name]["frame"].destroy()
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
        """
        replace all row of group saving
        """
        new_saved = {}
        for i, r in enumerate(self.saved.values()):
            txt = r["btn"].cget("text")
            entry_txt = r["entry"].get()
            if txt == "delete":
                str_var = tk.StringVar()
                str_var.set(entry_txt)
                display_btn = ctk.CTkButton(master=self, text=txt, command=lambda row=i + 3: self.delete(row))
                display_label = ctk.CTkEntry(master=self, textvariable=str_var, state="disabled")
            else:
                display_btn = ctk.CTkButton(master=self, text=txt, command=lambda row=i + 3: self.saving_group(row))
                display_label = ctk.CTkEntry(master=self, placeholder_text=entry_txt)
            display_btn.grid(row=i + 3, column=0)
            display_label.grid(row=i + 3, column=1)
            new_saved[i + 3] = {"btn": display_btn, "entry": display_label}
            r["btn"].destroy()
            r["entry"].destroy()
        self.saved = new_saved

    def get_selected_btn(self, group_name):
        """
        Put in self.custom_frame a dictionary with keys = name of group value = coords
        """
        color = random_color(True)
        for row in self.custom.all_btn:
            for col in self.custom.all_btn[row]:
                if self.custom.all_btn[row][col]["selected"]:
                    self.custom.all_btn[row][col]["selected"] = False
                    if group_name not in self.custom_frame:
                        self.custom_frame[group_name] = {"coords": [(row, col)], "frame": None}
                    else:
                        self.custom_frame[group_name]["coords"].append((row, col))

    def delete_all_group(self):
        """
        Delete all vlues saved related to customframe
        """
        self.custom_frame = {}
        Application.frame_to_save = {}
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
        Application.frame_to_save[group_name] = {"coords": (row, col, rowspan, columnspan), "Type": None}
        self.custom.big_frame(row, col, rowspan, columnspan, group_name)

    @classmethod
    def change_type(cls, type, name):
        Application.frame_to_save[name]["Type"] = type
        print(Application.frame_to_save[name]["Type"])


app = Application()
app.mainloop()
