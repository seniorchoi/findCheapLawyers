from flask import Flask, render_template, request
import os
import csv
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # Load environment variables from .env


def load_lawyers():
    lawyers = []
    with open('lawyers100.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lawyers.append({
                'name': row['Name'],
                'lawFirm': row['Law Firm'],
                'keyPractices': row['Key Practice Areas'],
                'imageURL': row['Image URL'],
                'phoneNumber': row['Phone Number'],
                'email': row['Email'],
                'city': row['city'],
                'Latitude': float(row['Latitude']) if row['Latitude'] else 0.0,
                'Longitude': float(row['Longitude']) if row['Longitude'] else 0.0,
            })
    return lawyers

@app.route('/')
def home():
    city = request.args.get('city', '').strip()
    specialization = request.args.get('specialization', '').strip()

    lawyers = load_lawyers()
    filtered_lawyers = lawyers

    # Filter by city
    if city:
        filtered_lawyers = [lawyer for lawyer in filtered_lawyers if lawyer['city'].lower() == city.lower()]

    # Filter by specialization (Key Practice Areas)
    if specialization:
        filtered_lawyers = [lawyer for lawyer in filtered_lawyers if specialization.lower() in lawyer['keyPractices'].lower()]

    google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

    return render_template(
        'index.html',
        lawyers=filtered_lawyers,
        city=city,
        specialization=specialization,
        google_maps_api_key=google_maps_api_key  # Passing the API key
    )

if __name__ == '__main__':
    app.run(debug=True)
