import requests

def plant_questionnaire():
    st.title("🌿 Welcome to PlantPal!")
    st.subheader("Let's set up your growing preferences")

    plant_data = {}

    # Location & Environment
    plant_data["Planting Location"] = st.selectbox("Where do you want to plant?", ["Indoors", "Outdoors"])

    if plant_data["Planting Location"] == "Indoors":
        plant_data["Natural Sunlight Access"] = st.radio("Do you have access to natural sunlight?", ["Yes", "No", "Partial"])
    else:
        plant_data["Outdoor Exposure"] = st.radio("Is the area exposed to wind or heavy rain?", ["Yes", "No", "Partial"])

    plant_data["Sunlight Hours"] = st.selectbox("How many hours of sunlight does the space get daily?", ["0–2", "3–5", "6+ hours"])
    plant_data["Outlet Nearby"] = st.radio("Do you have access to an outlet nearby for lights/pumps?", ["Yes", "No"])

    # Budget & Kit Preferences
    plant_data["Budget"] = st.selectbox("What is your budget for setup?", ["Under $30", "$30–$100", "$100+"])
    plant_data["Existing Kit"] = st.selectbox("Do you already own a hydroponic or soil kit?", ["Yes – Hydro", "Yes – Soil", "No"])
    plant_data["Kit or DIY"] = st.selectbox("Would you prefer a kit recommendation or DIY setup instructions?", ["Kit", "DIY", "Not sure"])
    plant_data["Electricity Preference"] = st.selectbox("Do you want a system that works with or without electricity?", ["Doesn’t matter", "Prefer no power required"])

    # Growing Preferences
    plant_data["What to Grow"] = st.selectbox("What do you want to grow?", ["Herbs", "Leafy Greens", "Small Veggies", "Flowers", "Not sure"])
    plant_data["Plant Count"] = st.selectbox("How many plants would you like to grow at once?", ["1–3", "4–6", "7+"])
    plant_data["Harvest Speed"] = st.selectbox("How soon would you like to harvest something?", ["Fastest possible", "I’m patient", "No preference"])
    plant_data["Low Maintenance"] = st.selectbox("Do you prefer low-maintenance plants?", ["Yes", "Doesn’t matter", "I want a challenge"])

    # Care & Maintenance
    plant_data["Weekly Care Time"] = st.selectbox("How much time can you dedicate to plant care weekly?", ["Less than 30 min", "30–60 min", "More than 1 hour"])
    plant_data["Care Reminders"] = st.radio("Would you like reminders for care tasks?", ["Yes", "No"])
    plant_data["Meal Suggestions"] = st.radio("Do you want to receive meal suggestions based on what you grow?", ["Yes", "No"])

    # Submit button
    if st.button("Submit"):
        st.success("✅ Thanks! Here's a summary of your preferences:")
        for key, value in plant_data.items():
            st.write(f"**{key}**: {value}")

plant_questionnaire()

