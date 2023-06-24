from jinja2 import Template

# Define the template
template_str = """
# Made with tkinter_grid_helper
# GitHub : https://github.com/tzebre/tkinter_grid_helper
# By MATHIEU Theo theo.mathieu@insa-lyon.fr
import tkinter as tk
import customtkinter as ctk
import random

def create_widget(widget_type, parent):
    if widget_type == "Frame":
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
    elif widget_type == "CheckBox":
        widget = ctk.CTkCheckBox(master=parent)
    elif widget_type == "RadioButton":
        widget = ctk.CTkRadioButton(master=parent)
    elif widget_type == "Slider":
        widget = ctk.CTkSlider(master=parent)
    else:
        raise ValueError(f"Invalid widget type: {widget_type}")

    return widget
    

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.element = {{dict_element}}
        self.title("###")  # change title here
        self.desired_W, self.desired_H, x, y = self.set_window_size()
        self.placed = {}    
        self.geometry(f"{self.desired_W}x{self.desired_H}+{x}+{y}")
        self.resizable(False,False)
        self.create_place_element()
    
    def set_window_size(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight() 
    
        # Calculate the desired width and height based on 16:9 aspect ratio
        aspect_ratio = 16 / 9
    
        # Check if the screen width allows for the desired height based on aspect ratio
        if screen_width >= int(screen_height * aspect_ratio):
            desired_height = screen_height
            desired_width = int(screen_height * aspect_ratio)
        else:
            desired_width = screen_width
            desired_height = int(screen_width / aspect_ratio)
        
        desired_width = int(desired_width * 0.9)
        desired_height = int(desired_height * 0.9)
        x = (screen_width - desired_width) // 2
        y = (screen_height - desired_height) // 2
            
        return desired_width, desired_height, x, y
        
    def place_widget(self, widget, x, y, width, height):

        # Calculate the pixel positions based on percentages
        pixel_x = int(self.desired_W * (x / 100))
        pixel_y = int(self.desired_H * (y / 100))
        pixel_width = int(self.desired_W * (width / 100))
        pixel_height = int(self.desired_H * (height / 100))

        # Place the widget using the calculated pixel positions
        widget.configure(width=pixel_width, height=pixel_height, fg_color="red")
        widget.place(x=pixel_x, y=pixel_y)

        
    def create_place_element(self):
        for elem_widget in self.element:
            current = self.element[elem_widget]
            type = current.get("dropdownValue")
            widget = create_widget(type, self)
            self.placed[elem_widget] = widget
            self.place_widget(widget, current.get('startX'), current.get("startY"), current.get("width"), 
                current.get("height"))
            

app = Application()
app.mainloop()

"""
template = Template(template_str)


# Render the template
def render(dict_el):
    return template.render(dict_element=dict_el)


def save(dest, dict_el):
    with open(f"{dest}/my_template.py", 'w') as f:
        output = render(dict_el)
        f.write(output)


if __name__ == '__main__':
    test_dict = {
        'Test': {'startX': 24.0517, 'startY': 18.3644, 'width': 24.0517, 'height': 24.5337, 'dropdownValue': 'Label'},
        'rien': {'startX': 55.0444, 'startY': 34.2898, 'width': 17.9984, 'height': 21.8077, 'dropdownValue': 'Textbox'},
        'Bonjour': {'startX': 32.6069, 'startY': 69.5839, 'width': 14.8507, 'height': 18.6514,
                    'dropdownValue': 'Label'},
        'non': {'startX': 44.3099, 'startY': 36.2984, 'width': 12.5908, 'height': 17.5036, 'dropdownValue': 'Label'}}
    canva_dict = {'canvas_size': {'width': 1239, 'height': 697}}
    save("/Users/theomathieu/Downloads", test_dict)
