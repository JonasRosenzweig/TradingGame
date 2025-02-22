import json
import os


class SaveManager:
    SAVE_FILE = "saves.json"
    MAX_SAVES = 3

    @staticmethod
    def load_saves():
        if not os.path.exists(SaveManager.SAVE_FILE):
            # Create default empty saves
            default_saves = {
                f"save_{i + 1}": {"name": None, "data": None}
                for i in range(SaveManager.MAX_SAVES)
            }
            SaveManager.save_data(default_saves)
            return default_saves

        with open(SaveManager.SAVE_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save_data(data):
        with open(SaveManager.SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def create_new_save(slot, player_name):
        saves = SaveManager.load_saves()
        saves[f"save_{slot}"] = {
            "name": player_name,
            "data": {
                "money": 100,  # Changed from 1000 to 100
                # Add other initial game state here
            }
        }
        SaveManager.save_data(saves)