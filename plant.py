import requests
import google.generativeai as genai


# === API KEYS ===
FDC_API_KEY = 'naE6pWAijzsfCTZdtNq7CbUfIzwkji9Bbx4pGBxk'
GEMINI_API_KEY = 'AIzaSyCSDjHY4dyHY5IC3wr2atPwTIGQ9xq4FXI'
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


   plant_data["What to Grow"] = get_input("What do you want to grow?", ["Herbs", "Leafy Greens", "Small Veggies", "Flowers", "Not sure"])
   plant_data["Plant Count"] = get_input("How many plants would you like to grow at once?", ["1–3", "4–6", "7+"])
   plant_data["Harvest Speed"] = get_input("How soon would you like to harvest something?", ["Fastest possible", "I’m patient", "No preference"])
   plant_data["Low Maintenance"] = get_input("Do you prefer low-maintenance plants?", ["Yes", "Doesn’t matter", "I want a challenge"])
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
   food_map = {
       "Herbs": "parsley",
       "Leafy Greens": "spinach",
       "Small Veggies": "tomato",
       "Flowers": "zucchini blossom",
       "Not sure": "lettuce"
   }
   food_query = food_map.get(plant_data["What to Grow"], plant_data["What to Grow"].lower())


   print(f"\n🔍 Looking up nutrition data for: {food_query}...")
   food_info = get_food_nutrition(food_query)
   if "Error" in food_info:
       print(f"Could not fetch nutrition data: {food_info['Error']}")
   else:
       print("\n📊 USDA Nutrition Facts:")
       for key, value in food_info.items():
           print(f"- {key}: {value}")


       if plant_data["Meal Suggestions"] == "Yes":
           print("\n🍽️ Generating a meal idea using Gemini...")
           meal = generate_meal_idea(food_query, food_info)
           print("\n✨ Meal Suggestion from Gemini:")
           print(meal)


if __name__ == "__main__":
   plant_questionnaire()



