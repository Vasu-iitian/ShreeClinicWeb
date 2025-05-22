from flask import Flask, render_template, request, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/clinic-460409-5ef2696ab4bb.json", scope)
client = gspread.authorize(creds)
sheet = client.open("PrescriptionData").sheet1  # Make sure this spreadsheet exists and is shared

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # No change to template

@app.route('/submit', methods=['POST'])
def submit():
    try:
        now = datetime.now()
        row = [
            now.strftime("%d-%m-%Y"),
            now.strftime("%H:%M:%S"),
            request.form.get("name"),
            request.form.get("age"),
            request.form.get("sex"),
            request.form.get("weight"),
            request.form.get("mobile"),
            request.form.get("case"),
            request.form.get("diagnosis"),
            request.form.get("prescription"),
            request.form.get("opd"),
        ]

        print("📤 Submitting row to Google Sheet:", row)
        sheet.append_row(row)
        print("✅ Row submitted successfully.")
        return redirect('/')
    except Exception as e:
        print("❌ Internal Server Error:", e)
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
