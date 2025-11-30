# color_module.py

def get_color_recommendation(skin_tone):
    """
    Returns a dictionary of Best and Avoid colors based on skin tone.
    """
    # Standardize input to handle "Light", "light", "LIGHT"
    skin_tone = skin_tone.capitalize() 

    rules = {
        "Light": {
            "Best": ["Navy Blue", "Emerald Green", "Maroon", "Pastel Pink", "Berry"],
            "Avoid": ["Pale Yellow", "Beige", "White (matches skin too much)"]
        },
        "Medium": {
            "Best": ["Olive Green", "Mustard", "Royal Blue", "Coral", "Teal"],
            "Avoid": ["Neon Colors", "Grey", "Mauve"]
        },
        "Dark": {
            "Best": ["White", "Cobalt Blue", "Bright Red", "Teal", "Gold", "Pastels"],
            "Avoid": ["Dark Brown", "Dull Grey", "Black (sometimes)"]
        }
    }
    
    # Default return if skin tone isn't recognized
    return rules.get(skin_tone, {
        "Best": ["Black", "White", "Navy"], 
        "Avoid": ["None"]
    })