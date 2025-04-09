from flask import Flask, jsonify
from flask_cors import CORS
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)

def read_and_process_csv():
    data = []
    with open('stackoverflow_data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert datetime to only date part (yyyy-mm-dd)
            date_only = row['date'].split("T")[0] if "T" in row['date'] else row['date']
            data.append({
                "level": int(row['level']),
                "technology": row['technology'],
                "date": date_only
            })
    return data

@app.route('/data', methods=['GET'])
def get_data():
    data = read_and_process_csv()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
