import requests
import google.generativeai as genai


# === API KEYS ===
FDC_API_KEY = 'naE6pWAijzsfCTZdtNq7CbUfIzwkji9Bbx4pGBxk'
GEMINI_API_KEY = 'AIzaSyAMnUDeFclBZewM99VOiauW32VWpIfWB14'
FDC_SEARCH_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

# === CONFIGURE GEMINI ===
genai.configure(api_key=GEMINI_API_KEY)

def get_input(prompt, options=None):
   while True:
       print(f"\n{prompt}")
       if options:
           for i, option in enumerate(options, 1):
               print(f"{i}. {option}")
           choice = input("Enter the number of your choice: ").strip()
           if choice.isdigit() and 1 <= int(choice) <= len(options):
               return options[int(choice) - 1]
           else:
               print(" Invalid choice. Try again.")
       else:
           return input("Your answer: ").strip()

def get_food_nutrition(food_name):
   try:
       search_params = {
           'query': food_name,
           'api_key': FDC_API_KEY,
           'dataType': 'Foundation,SR Legacy',
           'pageSize': 1
       }
       search_resp = requests.get(FDC_SEARCH_URL, params=search_params)
       if search_resp.status_code != 200:
           return {"Error": f"USDA API search error: {search_resp.status_code}"}


       foods = search_resp.json().get('foods', [])
       if not foods:
           return {"Error": f"No results found for '{food_name}'"}


       food_id = foods[0]['fdcId']
       print(f"🔍 Using FDC ID {food_id} from dataType: {foods[0].get('dataType')}")


       detail_url = f"https://api.nal.usda.gov/fdc/v1/food/{food_id}"
       detail_resp = requests.get(detail_url, params={'api_key': FDC_API_KEY})
       if detail_resp.status_code != 200:
           return {"Error": f"USDA API detail error: {detail_resp.status_code}"}


       food = detail_resp.json()
       nutrients = food.get('foodNutrients', [])
       nutrient_values = {}
       for n in nutrients:
           try:
               nid = n['nutrient']['id']
               amt = n.get('amount')
               if nid in [1008, 1003, 1004, 1079] and amt is not None:
                   nutrient_values[nid] = amt
           except:
               continue


       return {
           "Description": food.get('description', 'N/A'),
           "Calories": nutrient_values.get(1008, 'N/A'),
           "Protein": nutrient_values.get(1003, 'N/A'),
           "Fat": nutrient_values.get(1004, 'N/A'),
           "Fiber": nutrient_values.get(1079, 'N/A'),
       }
   except Exception as e:
       return {"Error": str(e)}


def generate_meal_idea(plant_name, nutrients):
   try:
       model = genai.GenerativeModel("gemini-1.5-flash")
       prompt = f"""
       I'm growing {plant_name}. Here are its USDA nutrients: {nutrients}.
       Suggest one simple, healthy meal idea that uses this plant as the main ingredient.
       Keep the description under 50 words and highlight the nutrient benefit.
       """
       response = model.generate_content(prompt)
       return response.text.strip()
   except Exception as e:
       return f"Error generating meal idea: {str(e)}"


kit_recommendations = {
   "Hydro": {
       "Under $30": "https://www.amazon.com/example-hydro-30",
       "$30–$100": "https://www.amazon.com/example-hydro-100",
       "$100+": "https://www.amazon.com/example-hydro-100plus",
   },
   "Soil": {
       "Under $30": "https://www.amazon.com/example-soil-30",
       "$30–$100": "https://www.amazon.com/example-soil-100",
       "$100+": "https://www.amazon.com/example-soil-100plus",
   }
}


def get_plant_suggestions(plant_type, preferences=None):
    """
    Use Gemini to suggest a list of plants based on user preferences and plant type.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            if plant_type == "Herbs":
                prompt = """
                Suggest a list of 5 popular culinary herbs that are easy to grow at home. List only the herb names, separated by commas. Do not include any extra text.
                """
                if preferences:
                    prompt = f"Suggest a list of 5 culinary herbs that match these preferences: {preferences}. List only the herb names, separated by commas. Do not include any extra text."
            elif plant_type == "Leafy Greens":
                prompt = """
                Suggest a list of 5 popular leafy greens that are easy to grow at home. List only the plant names, separated by commas. Do not include any extra text.
                """
                if preferences:
                    prompt = f"Suggest a list of 5 leafy greens that match these preferences: {preferences}. List only the plant names, separated by commas. Do not include any extra text."
            elif plant_type == "Small Veggies":
                prompt = """
                Suggest a list of 5 popular small vegetables that are easy to grow at home. List only the vegetable names, separated by commas. Do not include any extra text.
                """
                if preferences:
                    prompt = f"Suggest a list of 5 small vegetables that match these preferences: {preferences}. List only the vegetable names, separated by commas. Do not include any extra text."
            else:  # "Not sure"
                prompt = """
                Suggest a list of 5 popular edible plants that are easy to grow at home. List only the plant names, separated by commas. Do not include any extra text.
                """
                if preferences:
                    prompt = f"Suggest a list of 5 edible plants that match these preferences: {preferences}. List only the plant names, separated by commas. Do not include any extra text."
            
            response = model.generate_content(prompt)
            plants = [p.strip() for p in response.text.split(',') if p.strip()]
            
            if plants:  # If we got valid suggestions, return them
                return plants
            else:
                print(f"Attempt {attempt + 1}: No valid plants returned, retrying...")
                
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error getting plant suggestions: {e}")
            if attempt < max_retries - 1:
                print("Retrying...")
            else:
                print("Failed to get plant suggestions after all attempts.")
                return []
    
    return []


def plant_questionnaire():
   print("🌿 Welcome to GrowPal CLI!\nLet's set up your growing preferences.")
   plant_data = {}


   plant_data["Planting Location"] = get_input("Where do you want to plant?", ["Indoors", "Outdoors"])
   if plant_data["Planting Location"] == "Indoors":
       plant_data["Natural Sunlight Access"] = get_input("Do you have access to natural sunlight?", ["Yes", "No", "Partial"])
   else:
       plant_data["Outdoor Exposure"] = get_input("Is the area exposed to wind or heavy rain?", ["Yes", "No", "Partial"])


   plant_data["Sunlight Hours"] = get_input("How many hours of sunlight does the space get daily?", ["0–2", "3–5", "6+ hours"])
   plant_data["Outlet Nearby"] = get_input("Do you have access to an outlet nearby for lights/pumps?", ["Yes", "No"])
   plant_data["Existing Kit"] = get_input("Do you already own a hydroponic or soil kit?", ["Yes – Hydro", "Yes – Soil", "No"])


   if plant_data["Existing Kit"] == "No":
       plant_data["wants_suggestion"] = get_input("Do you want a kit recommendation?", ["Yes", "No"])
       if plant_data["wants_suggestion"] == "Yes":
           plant_data["Preferred Method"] = get_input("Which setup are you most interested in?", ["Hydro", "Soil"])
           plant_data["Budget"] = get_input("What is your budget for setup?", ["Under $30", "$30–$100", "$100+"])


   plant_data["What to Grow"] = get_input("What do you want to grow?", ["Herbs", "Leafy Greens", "Small Veggies", "Not sure"])
   plant_data["Plant Count"] = get_input("How many plants would you like to grow at once?", ["1–3", "4–6", "7+"])
   plant_data["Harvest Speed"] = get_input("How soon would you like to harvest something?", ["Fastest possible", "I'm patient", "No preference"])
   plant_data["Low Maintenance"] = get_input("Do you prefer low-maintenance plants?", ["Yes", "Doesn't matter", "I want a challenge"])
   plant_data["Weekly Care Time"] = get_input("How much time can you dedicate to plant care weekly?", ["Less than 30 min", "30–60 min", "More than 1 hour"])
   plant_data["Care Reminders"] = get_input("Would you like reminders for care tasks?", ["Yes", "No"])
   plant_data["Meal Suggestions"] = get_input("Do you want to receive meal suggestions based on what you grow?", ["Yes", "No"])


   # === Summary ===
   print("\n🌱 Here's a summary of your preferences:")
   for key, value in plant_data.items():
       print(f"- {key}: {value}")


   # === Kit Recommendation ===
   if plant_data.get("wants_suggestion") == "Yes":
       kit_type = plant_data.get("Preferred Method")
       budget = plant_data.get("Budget")
       link = kit_recommendations.get(kit_type, {}).get(budget)
       if link:
           print(f"\n🛠️ Based on your preferences, here's a recommended {kit_type.lower()} kit within your budget:")
           print(link)
       else:
           print("\n Sorry, no kit recommendation available for that combo yet.")


   # === Nutrition Info ===
   # Get plant suggestions based on type and preferences
   preference_options = ["Flavor", "Cuisine", "Easy to grow", "No preference/Blank"]
   preference_prompt = f"Do you have any preferences for {plant_data['What to Grow'].lower()}? (e.g., flavor, cuisine, easy to grow)"
   preference_choice = get_input(preference_prompt + "\n(Select an option or choose 'No preference/Blank')", preference_options)
   preferences = "" if preference_choice == "No preference/Blank" else preference_choice
   plant_list = get_plant_suggestions(plant_data["What to Grow"], preferences)
   print(f"\n🌿 Gemini suggests these {plant_data['What to Grow'].lower()} for you: {', '.join(plant_list)}")
   print("\nFetching nutrition info for each plant...")
   chart_data = []
   for plant in plant_list:
       info = get_food_nutrition(plant)
       if "Error" not in info:
           chart_data.append([plant, info.get("Calories", "N/A"), info.get("Protein", "N/A"), info.get("Fat", "N/A"), info.get("Fiber", "N/A")])
   
   # Print chart
   print(f"\n📊 USDA Nutrition Chart for {plant_data['What to Grow']} (per 100g):")
   print(f"{'Plant':<15}{'Calories':<10}{'Protein':<10}{'Fat':<10}{'Fiber':<10}")
   print("-"*55)
   for row in chart_data:
       print(f"{row[0]:<15}{row[1]:<10}{row[2]:<10}{row[3]:<10}{row[4]:<10}")
   
   # Meal suggestions for all plant types
   if plant_data["Meal Suggestions"] == "Yes":
       print("\n🍽️ Generating meal ideas using Gemini...")
       for plant in plant_list:
           info = get_food_nutrition(plant)
           if "Error" not in info:
               meal = generate_meal_idea(plant, info)
               print(f"\n✨ Meal Suggestion for {plant}:")
               print(meal)


if __name__ == "__main__":
   plant_questionnaire()



