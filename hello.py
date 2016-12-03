from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("pcwa_download")
    # if request.method == 'GET':
    #     site_name = request.form['site']
    #     start_date = request.form['start_date']
    #     end_date = request.form['den_date']
    #     print site_name, start_date, end_date

@app.route("/download", methods=['POST'])
def download():
    return request.form['site']


if __name__ == "__main__":
    app.run(debug=True)