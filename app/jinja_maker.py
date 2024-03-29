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
        self.title("###")  # change title here
        self.desired_W, self.desired_H, x, y = self.set_window_size()
        self.placed = {}    
        self.element_dict = {{element_dict}}
        self.geometry(f"{self.desired_W}x{self.desired_H}+{x}+{y}")
        self.resizable(False,False)
        self.create_widget()
    
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
        
    def place_widget(self, widget, x, y, width, height, **kwargs):
        # Calculate the pixel positions based on percentages
        pixel_x = int(self.desired_W * (x / 100))
        pixel_y = int(self.desired_H * (y / 100))
        pixel_width = int(self.desired_W * (width / 100))
        pixel_height = int(self.desired_H * (height / 100))

        # Place the widget using the calculated pixel positions
        widget.configure(width=pixel_width, height=pixel_height)
        
        widget.place(x=pixel_x, y=pixel_y)

    #create and place widget
    def create_widget(self):
    {% for element_name in element_dict %}
        # element : {{element_name}}
        current = self.element_dict['{{element_name}}'] 
        type = '{{element_dict[element_name]["type"]}}'
        widget = create_widget(type, self)
        self.placed['{{element_name}}'] = widget
        self.place_widget(widget, 
        {%- for arg_name in element_dict[element_name] -%}
            {%- if arg_name != "type" and arg_name != "widget" -%}
                {{arg_name}} = {{element_dict[element_name][arg_name]}},
            {%- endif -%}
        {%- endfor -%}
        )    
    {% endfor %}


app = Application()
app.mainloop()

"""
template = Template(template_str)


# Render the template
def render(dict_el):
    return template.render(element_dict=dict_el)


def save(dest, dict_el):
    with open(f"{dest}/my_template.py", 'w') as f:
        output = render(dict_el)
        f.write(output)


if __name__ == '__main__':
    test_dict = {
        'A': {'type': 'Entry', 'width': 20.8517, 'height': 23.4987, 'y': 18.0157, 'x': 33.627},
        'B': {'type': 'Slider', 'width': 23.4949, 'height': 20.1044, 'y': 57.1802, 'x': 51.6887},
        'C': {'type': 'Slider', 'width': 18.649, 'height': 8.87728, 'y': 26.3708, 'x': 74.8899}}

    save("/Users/theomathieu/Downloads", test_dict)
