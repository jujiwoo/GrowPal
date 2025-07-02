import unittest
from unittest.mock import patch, MagicMock
import plant

class TestGrowPalCLI(unittest.TestCase):
    def test_grow_type_display(self):
        # Test fallback logic for grow_type_display
        for value, expected in [
            ("Herbs", "Herbs"),
            ("Not sure", "plants"),
            ("", "plants"),
            (None, "plants")
        ]:
            grow_type = value
            grow_type_display = grow_type if grow_type and grow_type != "Not sure" else "plants"
            self.assertEqual(grow_type_display, expected)

    @patch('builtins.input', side_effect=["2"])
    def test_get_input_options_valid(self, mock_input):
        result = plant.get_input("Pick one", ["A", "B", "C"])
        self.assertEqual(result, "B")

    @patch('builtins.input', side_effect=["C", "1"])
    @patch('os.system')
    @patch('plant.print_banner')
    def test_get_input_clear_hotkey(self, mock_banner, mock_system, mock_input):
        result = plant.get_input("Pick one", ["A", "B"])
        self.assertEqual(result, "A")
        mock_system.assert_called_with('clear')
        mock_banner.assert_called()

    @patch('builtins.input', side_effect=["X"])
    def test_get_input_exit_hotkey(self, mock_input):
        with self.assertRaises(SystemExit):
            plant.get_input("Pick one", ["A", "B"])

    @patch('builtins.input', side_effect=["R"])
    def test_get_input_restart_hotkey(self, mock_input):
        with self.assertRaises(plant.RestartException):
            plant.get_input("Pick one", ["A", "B"])

    @patch('requests.get')
    def test_get_food_nutrition_success(self, mock_get):
        # Mock search response
        mock_search = MagicMock()
        mock_search.status_code = 200
        mock_search.json.return_value = {
            'foods': [{
                'fdcId': 123,
                'dataType': 'Foundation'
            }]
        }
        # Mock detail response
        mock_detail = MagicMock()
        mock_detail.status_code = 200
        mock_detail.json.return_value = {
            'description': 'Spinach',
            'foodNutrients': [
                {'nutrient': {'id': 1008}, 'amount': 23},
                {'nutrient': {'id': 1003}, 'amount': 2.9},
                {'nutrient': {'id': 1004}, 'amount': 0.4},
                {'nutrient': {'id': 1079}, 'amount': 2.2}
            ]
        }
        mock_get.side_effect = [mock_search, mock_detail]
        result = plant.get_food_nutrition("spinach")
        self.assertEqual(result["Description"], "Spinach")
        self.assertEqual(result["Calories"], 23)
        self.assertEqual(result["Protein"], 2.9)
        self.assertEqual(result["Fat"], 0.4)
        self.assertEqual(result["Fiber"], 2.2)

    @patch('requests.get')
    def test_get_food_nutrition_no_results(self, mock_get):
        mock_search = MagicMock()
        mock_search.status_code = 200
        mock_search.json.return_value = {'foods': []}
        mock_get.return_value = mock_search
        result = plant.get_food_nutrition("unknown")
        self.assertIn("Error", result)

    @patch('google.generativeai.GenerativeModel')
    def test_generate_meal_idea_success(self, mock_model):
        mock_instance = MagicMock()
        mock_instance.generate_content.return_value.text = "A healthy salad."
        mock_model.return_value = mock_instance
        result = plant.generate_meal_idea("spinach", {"Calories": 23})
        self.assertIn("salad", result)

    @patch('google.generativeai.GenerativeModel')
    def test_generate_meal_idea_error(self, mock_model):
        mock_model.side_effect = Exception("API error")
        result = plant.generate_meal_idea("spinach", {"Calories": 23})
        self.assertIn("Error generating meal idea", result)

if __name__ == "__main__":
    unittest.main() 