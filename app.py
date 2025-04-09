from flask import Flask, jsonify
from flask_cors import CORS
import csv
from collections import defaultdict, Counter
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

def read_csv_group_by_month():
    # Format: {'YYYY-MM': Counter({'python': 3, 'java': 2, ...})}
    monthly_tag_counter = defaultdict(Counter)
    csv_path = 'Datafrom_stack.csv'

    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found at {csv_path}")
        return {}

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for i, row in enumerate(reader):
            try:
                tag = row['Tag'].strip()
                date_str = row['Published Date'].strip()
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%SZ")
                year_month = date_obj.strftime("%Y-%m")  # "2025-04"

                monthly_tag_counter[year_month][tag] += 1
            except Exception as e:
                print(f"❌ Error on row {i}: {e}")
                continue

    # Prepare output with top 6 tags per month
    output = []
    for month, tag_counter in sorted(monthly_tag_counter.items()):
        top_tags = tag_counter.most_common(6)
        output.append({
            "month": month,
            "top_tags": [{"tag": tag, "count": count} for tag, count in top_tags]
        })

    return output

@app.route('/data', methods=['GET'])
def get_top_tags_by_month():
    try:
        data = read_csv_group_by_month()
        return jsonify(data)
    except Exception as e:
        print(f"❌ Exception in /top-tags: {e}")
        return jsonify({"error": "Failed to process tags"}), 500

# Your other endpoints remain the same...
