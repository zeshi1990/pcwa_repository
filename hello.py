from flask import Flask, render_template, request, send_file
import mysql.connector
import pandas as pd

app = Flask(__name__)
cnx = mysql.connector.connect(user="root", password="root", database="ar_data")
cursor = cnx.cursor()

@app.route("/")
def index():
    return render_template("pcwa_download.html")
    # if request.method == 'GET':
    #     site_name = request.form['site']
    #     start_date = request.form['start_date']
    #     end_date = request.form['den_date']
    #     print site_name, start_date, end_date

@app.route("/download", methods=['Post'])
def download():
    site = request.form['site']
    start_date = str(request.form['start_date'])
    end_date = str(request.form['end_date'])
    query(site, start_date, end_date)
    send_file("tmp/tmp.csv")


def query(site, start_date, end_date):
    query_txt_site = "SELECT site_id, num_of_nodes FROM sites WHERE site_name = '" + site + "';"
    site_df = pd.read_sql_query(query_txt_site, cnx)

    site_id = site_df['site_id'][0]
    num_of_nodes = site_df['num_of_nodes'][0]

    final_ts = None
    ts_columns = ["datetime"]

    for node_id in range(1, num_of_nodes+1):
        query_txt_node_ts = ("SELECT level_1.datetime, motes.ground_dist - level_1.snowdepth FROM level_1 JOIN " +
            "motes ON level_1.site_id = motes.site_id AND level_1.node_id = motes.node_id WHERE " +
            "level_1.site_id = " + str(site_id) + " AND level_1.node_id = " + str(node_id) +
            " AND level_1.datetime > '" + start_date + "' AND level_1.datetime < '" + end_date +
            "' ORDER BY level_1.datetime;")
        # print query_txt_node_ts
        node_ts_df = pd.read_sql_query(query_txt_node_ts, cnx)
        if node_id == 1:
            final_ts = node_ts_df
        else:
            final_ts = final_ts.merge(node_ts_df, on="datetime")
        ts_columns.append("snowdepth_"+str(node_id))
    final_ts.columns = ts_columns
    final_ts.to_csv("tmp/tmp.csv")

if __name__ == "__main__":
    app.run(debug=True)