from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
rectangles = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/save_all', methods=['POST'])
def save_all():
    data = request.json  # Assuming the data sent is in JSON format
    rectangles = data['rectangles']  # Assuming the rectangles are stored in a 'rectangles' key
    # Process the rectangles data as needed
    # Save the rectangles in a dictionary or perform any other necessary actions
    print(rectangles)
    return jsonify(success=True)

@app.route('/get_dropdown_values')
def get_dropdown_values():
    values = ['Value 1', 'Value 2', 'Value 3']
    return values

if __name__ == '__main__':
    app.run()
