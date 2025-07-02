from pydantic import BaseModel

class QuestionnaireInput(BaseModel):
    planting_location: str
    sunlight_access: str
    sunlight_hours: str
    outlet_nearby: str
    budget: str
    existing_kit: str
    kit_or_diy: str
    electricity_preference: str
    what_to_grow: str
    plant_count: str
    harvest_speed: str
    low_maintenance: str
    weekly_care_time: str
    care_reminders: str
    meal_suggestions: str 