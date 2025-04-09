from flask import Flask, jsonify
from flask_cors import CORS
import csv
from collections import defaultdict
import os

app = Flask(__name__)
CORS(app)

def read_and_group_csv():
    grouped_data = defaultdict(lambda: {"tags": [], "date": ""})
    csv_path = 'Datafrom_stack.csv'

    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at {csv_path}")
        return []

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        print("📌 CSV Headers:", reader.fieldnames)

        for i, row in enumerate(reader):
            try:
                question_id = row['Question']
                tag = row['Tag']
                published_date = row['Published Date'].split(" ")[0]  # Keep only date part

                grouped_data[question_id]["tags"].append(tag)
                grouped_data[question_id]["date"] = published_date
            except Exception as e:
                print(f"❌ Error on row {i}: {e}")
                continue

    # Convert to list format for JSON
    final_data = []
    for q_id, info in grouped_data.items():
        final_data.append({
            "question": q_id,
            "tags": info["tags"],
            "date": info["date"]
        })

    return final_data

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = read_and_group_csv()
        return jsonify(data)
    except Exception as e:
        print(f"❌ Exception in /data: {e}")
        return jsonify({"error": "Failed to read data"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
