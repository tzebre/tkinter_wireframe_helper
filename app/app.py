from flask import Flask, render_template, request, jsonify
from jinja_maker import save

app = Flask(__name__)
rectangles = {}

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


@app.route('/')
def index():
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
    return render_template('index.html', drop_values=widget_list)


@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json  # Assuming the data sent is in JSON format
    print(data)  # Assuming the rectangles are stored in a 'rectangles' key
    # Process the rectangles data as needed
    # Save the rectangles in a dictionary or perform any other necessary actions
    save("/Users/theomathieu/Downloads", data)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
