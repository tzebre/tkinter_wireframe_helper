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
selected = {"name": "", "height": 0, "width": 0, "type":"", "spec":{}}


def get_all_widget():
    all_widget = {}
    for w in all:
        all_widget[w] = get_position(w)
    return all_widget


def add_widget(widget):
    name = widget.name
    value = widget
    all[name] = value


def delete_widget(widget_name):
    del all[widget_name]


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
    # TODO verif conversion
    old_x, old_y, h, w = widget.get_relative('x', 'y', 'height', 'width')
    new_x = (old_x / 100) * width
    new_y = (old_y / 100) * height
    new_h = (h / 100) * height
    new_w = (w / 100) * width

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
    return render_template('index.html', all_widget=get_all_widget(), drop_values=widget_list, selected=selected)


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
    test = Widget(data["name"], data["coords"])
    add_widget(test)
    return jsonify(success=True)


@app.route('/resize', methods=['POST'])
def resize():
    data = request.json
    set_sizing(**data)
    return jsonify(success=True)


@app.route('/select_widget', methods=['POST'])
def select_widget():
    data = request.json
    selected["name"] = data["name"]
    coords = get_position(selected["name"])
    selected["height"] = int(coords["height"])
    selected["width"] = int(coords["width"])
    return jsonify(success=True)

@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    name = data["name"]
    delete_widget(name)
    global selected
    selected = {"name": "", "height": 0, "width": 0}
    return jsonify(success=True)

@app.route('/drop_choice', methods=['POST'])
def drop_choice():
    data = request.json
    type = data["type"]
    global selected
    selected["type"] = type
    return jsonify(success=True)

if __name__ == '__main__':
    app.run()
