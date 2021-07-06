from utils import get_data, get_search_index
from flask import Flask, render_template, request, send_file, Response

# flask function
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':
        query = request.form['search']
        print(query)
        indexes, timing = get_search_index(query)
        data = get_data(indexes)

    return render_template('search_page.html', timing=timing, query=query, data=data)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
