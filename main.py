def plant_questionnaire():
    print("🌿 Welcome to PlantPal! Let's set up your growing preferences 🌿\n")

    plant_data = {}

    # 🌍 Location & Environment
    plant_data["Planting Location"] = input("Where do you want to plant? (Indoors / Outdoors): ").strip()

    if plant_data["Planting Location"].lower() == "indoors":
        plant_data["Natural Sunlight Access"] = input("Do you have access to natural sunlight? (Yes / No / Partial): ").strip()
    else:
        plant_data["Outdoor Exposure"] = input("Is the area exposed to wind or heavy rain? (Yes / No / Partial): ").strip()

    plant_data["Sunlight Hours"] = input("How many hours of sunlight does the space get daily? (0–2 / 3–5 / 6+ hours): ").strip()
    plant_data["Outlet Nearby"] = input("Do you have access to an outlet nearby for lights/pumps? (Yes / No): ").strip()

    # 💰 Budget & Kit Preferences
    plant_data["Budget"] = input("What is your budget for setup? (Under $30 / $30–$100 / $100+): ").strip()
    plant_data["Existing Kit"] = input("Do you already own a hydroponic or soil kit? (Yes – Hydro / Yes – Soil / No): ").strip()
    plant_data["Kit or DIY"] = input("Would you prefer a kit recommendation or DIY setup instructions? (Kit / DIY / Not sure): ").strip()
    plant_data["Electricity Preference"] = input("Do you want a system that works with or without electricity? (Doesn’t matter / Prefer no power required): ").strip()

    # 🌿 Growing Preferences
    plant_data["What to Grow"] = input("What do you want to grow? (Herbs / Leafy Greens / Small Veggies / Flowers / Not sure): ").strip()
    plant_data["Plant Count"] = input("How many plants would you like to grow at once? (1–3 / 4–6 / 7+): ").strip()
    plant_data["Harvest Speed"] = input("How soon would you like to harvest something? (Fastest possible / I’m patient / No preference): ").strip()
    plant_data["Low Maintenance"] = input("Do you prefer low-maintenance plants? (Yes / Doesn’t matter / I want a challenge): ").strip()

    # 🧪 Care & Maintenance
    plant_data["Weekly Care Time"] = input("How much time can you dedicate to plant care weekly? (Less than 30 min / 30–60 min / More than 1 hour): ").strip()
    plant_data["Care Reminders"] = input("Would you like reminders for care tasks? (Yes / No): ").strip()
    plant_data["Meal Suggestions"] = input("Do you want to receive meal suggestions based on what you grow? (Yes / No): ").strip()

    # ✅ Summary
    print("\n✅ Thanks! Here's a summary of your preferences:\n")
    for key, value in plant_data.items():
        print(f"{key}: {value}")

    return plant_data

# Run the questionnaire
if __name__ == "__main__":
    plant_questionnaire()