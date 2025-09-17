import requests
import csv
from datetime import datetime

# 📝 Fill these in
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
AUTH_CODE = "YOUR_AUTH_CODE"  # From the redirect URL after OAuth

# 1️⃣ Exchange AUTH_CODE for ACCESS_TOKEN
token_url = "https://www.strava.com/oauth/token"
payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": AUTH_CODE,
    "grant_type": "authorization_code"
}

print("Getting access token...")
token_res = requests.post(token_url, data=payload)
token_data = token_res.json()

if 'access_token' not in token_data:
    print("Error getting token:", token_data)
    exit()

access_token = token_data["access_token"]
print("✅ Access token received!")

# 2️⃣ Fetch your recent activities
activities_url = "https://www.strava.com/api/v3/athlete/activities"
headers = {"Authorization": f"Bearer {access_token}"}
params = {"per_page": 50, "page": 1}

print("Downloading activities...")
res = requests.get(activities_url, headers=headers, params=params)
activities = res.json()

if isinstance(activities, dict) and activities.get('errors'):
    print("Error fetching activities:", activities)
    exit()

# 3️⃣ Save selected fields to CSV
with open("strava_activities.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Date", "Name", "Distance_km", "Moving_Time_min", "Avg_Pace_min_per_km", "Avg_HR"])

    for act in activities:
        distance_km = act["distance"] / 1000
        moving_min = act["moving_time"] / 60
        avg_pace = (act["moving_time"] / 60) / distance_km if distance_km > 0 else 0
        avg_hr = act.get("average_heartrate", "")
        date = datetime.strptime(act["start_date"], "%Y-%m-%dT%H:%M:%SZ").date()
        writer.writerow([date, act["name"], round(distance_km, 2), round(moving_min, 1), round(avg_pace, 2), avg_hr])

print("✅ Saved to strava_activities.csv")
