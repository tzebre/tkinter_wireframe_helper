from flask import Flask, render_template, request, jsonify, g
from jinja_maker import save

app = Flask(__name__)

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
selected = {"name": "", "x": 0, "y": 0, "height": 0, "width": 0, "type": "", "spec": {}}


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


def get_final():
    full_dict = {}
    for widget in all:
        wid_class = all[widget]
        coord = wid_class.coordinate
        full_dict[widget] = {'type': wid_class.type, 'width': coord["width"], 'height': coord["height"],
                             'y': coord["y"], 'x': coord["x"]}
    return full_dict


def get_position(name):
    widget = all[name]
    old_x, old_y, h, w = widget.get_relative('x', 'y', 'height', 'width')
    new_x = (old_x / 100) * width
    new_y = (old_y / 100) * height
    new_h = (h / 100) * height
    new_w = (w / 100) * width

    return {"x": new_x, "y": new_y, "height": new_h, "width": new_w}


class Widget:
    def __init__(self, name, coordinate, widget_type="Frame"):
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


@app.route('/save_all')
def save_all():
    final_widgets = get_final()
    # TODO ask for a path to save the template
    save("/Users/theomathieu/Downloads", final_widgets)  # CHANGE PATH
    return render_template('index.html', all_widget=get_all_widget(), drop_values=widget_list, selected=selected)


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
    selected["x"] = int(coords["x"])
    selected["y"] = int(coords["y"])
    selected["type"] = all[selected["name"]].type
    return jsonify(success=True)


@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    name = data["name"]
    delete_widget(name)
    global selected
    selected = {"name": "", "x": 0, "y": 0, "height": 0, "width": 0, "type": "", "spec": {}}
    return jsonify(success=True)


@app.route('/drop_choice', methods=['POST'])
def drop_choice():
    data = request.json
    type = data["type"]
    global selected
    selected["type"] = type
    all[selected["name"]].type = type
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
