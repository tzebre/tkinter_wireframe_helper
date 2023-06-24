from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
rectangles = {}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_rectangle', methods=['POST'])
def save_rectangle():
    rectangle = request.get_json()
    # Perform any necessary validation or processing here
    return jsonify(success=True)


if __name__ == '__main__':
    app.run()
