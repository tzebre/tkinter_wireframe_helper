from flask import Flask, render_template, request, jsonify, g
from jinja_maker import save

app = Flask(__name__)

possible_args = {
    "Button": ["corner_radius", "border_width", "border_spacing", "fg_color", "hover_color", "border_color",
               "text_color", "text_color_disabled", "text", "font", "textvariable", "image", "state", "hover",
               "command", "compound", "anchor"],
    "CheckBox": ["checkbox_width", "checkbox_height", "corner_radius", "border_width" "fg_color",
                 "hover_color", "border_color",
                 "text_color", "text_color_disabled", "text", "font", "textvariable", "state", "hover",
                 "command", "variable", "onvalue", "offvalue"],
    "ComboBox": ["corner_radius", "border_width", "fg_color", "border_color", "button_color", "button_hover_color",
                 "dropdown_fg_color", "dropdown_hover_color", "dropdown_text_color", "test_color",
                 "test_color_disabled", "font", "dropdown_font", "values", "hover", "state", "command", "variable",
                 "justify"],

}
widget_list = [
    "Frame",
    "ComboBox",
    "ScrollableFrame",
    "Textbox",
    "Button",
    "Label",
    "Entry",
    "OptionMenu",
    "SegmentedButton",
    "Switch",
    "CheckBox",
    "RadioButton",
    "Slider"
]

x = 0
y = 0
height = 100
width = 100
all = {}


def add_widget(widget):
    name = widget.name
    value = widget
    all[name] = value


def delete_widget(widget):
    del all[widget.name]


def get_size():
    return x, y, height, width


def set_sizing(**kwargs):
    global x, y, height, width
    for arg in kwargs:
        if arg == "x":
            x = kwargs[arg]
        elif arg == "y":
            y = kwargs[arg]
        elif arg == "height":
            height = kwargs[arg]
        elif arg == "width":
            width = kwargs[arg]
        else:
            print("error")


def get_position(name):
    widget = all[name]
    print(x, y, height)
    old_x, old_y, h, w = widget.get_relative('x', 'y', 'height', 'width')
    new_x = x + ((old_x * width) / 100)
    new_y = y + ((old_y * height) / 100)
    new_h = (h * height) / 100
    new_w = (w * width) / 100

    return {"x": new_x, "y": new_y, "height": new_h, "width": new_w}


class Widget():
    def __init__(self, name, coordinate, widget_type=None):
        self.name = name
        self.coordinate = coordinate
        self.type = widget_type

    def get_name(self):
        return self.name

    def get_relative(self, *args):
        if args:
            to_return = []
            for request_arg in args:
                try:
                    to_return.append(self.coordinate[request_arg])
                except:
                    print(
                        f"Warning: Exception occurred for argument :{request_arg}."
                        f" Valid argument are: x, y, height, width")
            return to_return
        else:
            return self.coordinate


@app.route('/')
def index():
    return render_template('index.html', drop_values=widget_list)


@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json  # Assuming the data sent is in JSON format
    # Process the rectangles data as needed
    # Save the rectangles in a dictionary or perform any other necessary actions
    save("/Users/theomathieu/Downloads", data)
    return jsonify(success=True)


@app.route('/new_widget', methods=['POST'])
def new_widget():
    data = request.json
    test = Widget(len(all), data)
    add_widget(test)
    print("position_all", get_position(len(all) - 1))
    print("position_wid", test.get_relative())
    print("relative", test.get_name(), test.get_relative("x", "y"))
    return jsonify(success=True)


@app.route('/resize', methods=['POST'])
def resize():
    data = request.json
    set_sizing(**data)
    print(get_size())
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
