# dataset_generator.py
import pandas as pd
import random

# 1. Define our categories
weather_conditions = ['Hot', 'Moderate', 'Cold', 'Rainy']
event_types = ['Casual', 'Office', 'Party', 'Gym', 'Wedding']
skin_tones = ['Light', 'Medium', 'Dark']

# 2. Define the "Logic Rules" used to generate the data
# Dictionary Format: (Weather, Event) -> List of valid outfits
outfit_rules = {
    # HOT WEATHER
    ('Hot', 'Casual'): ['T-shirt + Shorts', 'Cotton Polo + Chinos', 'Linen Shirt + Jeans', 'Graphic Tee + Cargo Shorts'],
    ('Hot', 'Office'): ['Linen Shirt + Trousers', 'Cotton Formal Shirt + Chinos', 'Half-Sleeve Formal Shirt'],
    ('Hot', 'Party'): ['Printed Half-Sleeve Shirt + Jeans', 'Polo T-shirt + Trousers', 'Linen Blazer + T-shirt'],
    ('Hot', 'Gym'): ['Sleeveless Tank + Shorts', 'Dri-Fit Tee + Shorts'],
    ('Hot', 'Wedding'): ['Light Cotton Kurta', 'Linen Suit', 'Pastel Waistcoat Set'],

    # MODERATE WEATHER
    ('Moderate', 'Casual'): ['T-shirt + Jeans', 'Checkered Shirt + Chinos', 'Henley + Jeans', 'Denim Shirt + Khakis'],
    ('Moderate', 'Office'): ['Formal Shirt + Trousers', 'Business Casual Blazer + Chinos'],
    ('Moderate', 'Party'): ['Casual Blazer + Jeans', 'Party Wear Shirt + Chinos', 'Solid Shirt + Trousers'],
    ('Moderate', 'Gym'): ['T-shirt + Track Pants', 'Polyester Tee + Joggers'],
    ('Moderate', 'Wedding'): ['Traditional Kurta Pajama', 'Waistcoat Set', 'Bandhgala Suit'],

    # COLD WEATHER
    ('Cold', 'Casual'): ['Hoodie + Jeans', 'Sweatshirt + Joggers', 'Denim Jacket + Jeans', 'Puffer Jacket + Chinos'],
    ('Cold', 'Office'): ['Formal Shirt + Sweater', 'Suit with Tie', 'Turtleneck + Trousers'],
    ('Cold', 'Party'): ['Leather Jacket + Jeans', 'Velvet Blazer + Trousers', 'Overcoat + Boots'],
    ('Cold', 'Gym'): ['Full Sleeve Dri-Fit + Track Pants', 'Hoodie + Joggers'],
    ('Cold', 'Wedding'): ['Sherwani + Shawl', '3-Piece Suit', 'Velvet Bandhgala'],
    
    # RAINY WEATHER
    ('Rainy', 'Casual'): ['Waterproof Jacket + Shorts', 'Dark T-shirt + Nylon Pants'],
    ('Rainy', 'Office'): ['Dark Shirt + Trousers + Raincoat'],
    ('Rainy', 'Party'): ['Short Sleeve Shirt + Dark Jeans'], # Avoid floor length/light colors
    ('Rainy', 'Gym'): ['Synthetic T-shirt + Shorts'],
    ('Rainy', 'Wedding'): ['Dark Suit (Avoid Velvets)', 'Short Kurta + Trousers']
}

data = []

# 3. Generate 5000 random samples
print("Generating synthetic data...")
for _ in range(5000):
    weather = random.choice(weather_conditions)
    event = random.choice(event_types)
    skin = random.choice(skin_tones)
    
    # Select the correct outfit list based on weather and event
    possible_outfits = outfit_rules.get((weather, event))
    
    # Pick one random outfit from that valid list
    outfit = random.choice(possible_outfits)
    
    data.append([weather, event, skin, outfit])

# 4. Save to CSV
df = pd.DataFrame(data, columns=['Weather', 'Event', 'Skin_Tone', 'Outfit'])
df.to_csv('clothing_data.csv', index=False)

print("✅ SUCCESS: 'clothing_data.csv' has been created with 5000 rows!")
print(df.head()) # Show first 5 rows