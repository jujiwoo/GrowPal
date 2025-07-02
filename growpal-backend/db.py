import sqlite3
from models import QuestionnaireInput

conn = sqlite3.connect("growpal.db")
cursor = conn.cursor()

# Run once to create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS questionnaire_responses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    planting_location TEXT,
    sunlight_access TEXT,
    sunlight_hours TEXT,
    outlet_nearby TEXT,
    budget TEXT,
    existing_kit TEXT,
    kit_or_diy TEXT,
    electricity_preference TEXT,
    what_to_grow TEXT,
    plant_count TEXT,
    harvest_speed TEXT,
    low_maintenance TEXT,
    weekly_care_time TEXT,
    care_reminders TEXT,
    meal_suggestions TEXT
)
""")
conn.commit()

def save_response(data: QuestionnaireInput):
    cursor.execute("""
        INSERT INTO questionnaire_responses (
            planting_location, sunlight_access, sunlight_hours, outlet_nearby,
            budget, existing_kit, kit_or_diy, electricity_preference,
            what_to_grow, plant_count, harvest_speed, low_maintenance,
            weekly_care_time, care_reminders, meal_suggestions
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(data.dict().values()))
    conn.commit()
