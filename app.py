from flask import Flask, jsonify
from flask_cors import CORS
import csv
from collections import defaultdict, Counter
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

def read_csv_and_aggregate_top_tags():
    csv_path = 'Datafrom_stack.csv'
    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at {csv_path}")
        return {}

    year_tag_map = defaultdict(list)

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        print("📌 CSV Headers:", reader.fieldnames)

        for i, row in enumerate(reader):
            try:
                tag = row['Tag'].strip()
                pub_date = row['Published Date'].strip()
                year = datetime.strptime(pub_date, "%Y-%m-%d %H:%M:%SZ").year
                year_tag_map[year].append(tag)
            except Exception as e:
                print(f"❌ Error in row {i}: {e}")
                continue

    # Top 6 tags per year
    result = {}
    for year, tags in year_tag_map.items():
        top_tags = Counter(tags).most_common(6)
        result[str(year)] = [{"tag": tag, "count": count} for tag, count in top_tags]

    return result

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = read_csv_and_aggregate_top_tags()
        return jsonify(data)
    except Exception as e:
        print(f"❌ Exception in /data: {e}")
        return jsonify({"error": "Failed to process data"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
