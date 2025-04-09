from flask import Flask, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

def read_and_process_csv():
    data = []

    try:
        with open('Datafrom_stack.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            # Check for expected headers
            expected_fields = {'date', 'level', 'technology'}
            if not expected_fields.issubset(set(reader.fieldnames)):
                print("CSV headers found:", reader.fieldnames)
                raise KeyError("CSV is missing one of the required fields: date, level, technology")

            for row in reader:
                try:
                    # Ensure the required fields are present in the row
                    if 'date' not in row or 'level' not in row or 'technology' not in row:
                        continue

                    # Extract and clean date
                    date_raw = row['date']
                    date_only = date_raw.split("T")[0] if "T" in date_raw else date_raw

                    # Append processed row
                    data.append({
                        "level": int(row['level']),
                        "technology": row['technology'],
                        "date": date_only
                    })
                except (ValueError, KeyError):
                    # Skip malformed rows
                    continue
    except FileNotFoundError:
        print("CSV file not found. Make sure 'Datafrom_stack.csv' is in the correct path.")
    except Exception as e:
        print(f"Error reading CSV: {e}")

    return data

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = read_and_process_csv()
        return jsonify(data)
    except Exception as e:
        print(f"Exception in /data: {e}")
        return jsonify({"error": "Failed to read data"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
