from flask import Flask, render_template, request, jsonify
from jinja_maker import save

app = Flask(__name__)
rectangles = {}


@app.route('/')
def index():
    widget_list = [
        "Frame",
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
    return render_template('index.html', drop_values = widget_list)


@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json  # Assuming the data sent is in JSON format
    print(data)  # Assuming the rectangles are stored in a 'rectangles' key
    # Process the rectangles data as needed
    # Save the rectangles in a dictionary or perform any other necessary actions
    save("/Users/theomathieu/Downloads", data)
    return jsonify(success=True)


@app.route('/get_dropdown_values')
def get_dropdown_values():
    widget_list = [
        "Frame",
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
    return widget_list


if __name__ == '__main__':
    app.run()
