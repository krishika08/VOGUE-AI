# main.py
import joblib
import warnings
from weather_module import get_weather
from color_module import get_color_recommendation

# Suppress warnings to keep the output clean
warnings.filterwarnings("ignore")

def load_resources():
    """Load the trained model and encoders."""
    try:
        print("⏳ Loading AI Brain...")
        model = joblib.load('model.pkl')
        le_weather = joblib.load('le_weather.pkl')
        le_event = joblib.load('le_event.pkl')
        le_skin = joblib.load('le_skin.pkl')
        le_outfit = joblib.load('le_outfit.pkl')
        print("✅ System Ready!")
        return model, le_weather, le_event, le_skin, le_outfit
    except FileNotFoundError:
        print("❌ Error: Model files not found. Please run 'train_model.py' first.")
        exit()

def get_outfit_prediction(model, le_weather, le_event, le_skin, le_outfit, weather, event, skin):
    """
    Encodes inputs, predicts using the ML model, and decodes the output.
    """
    try:
        # Transform inputs into numbers (using the saved encoders)
        # Note: We need to handle cases where the input might not match training data exactly
        w_encoded = le_weather.transform([weather])[0]
        e_encoded = le_event.transform([event])[0]
        s_encoded = le_skin.transform([skin])[0]

        # Predict
        prediction_idx = model.predict([[w_encoded, e_encoded, s_encoded]])
        
        # Convert number back to text
        outfit_name = le_outfit.inverse_transform(prediction_idx)[0]
        return outfit_name
    except ValueError as e:
        # Fallback if the specific combination/label wasn't seen in training
        return "Standard Smart Casual (Blue Jeans + White Shirt)"

def main():
    # 1. Load Resources
    model, le_weather, le_event, le_skin, le_outfit = load_resources()

    print("\n" + "="*50)
    print("👔 SMART CLOTHING RECOMMENDATION SYSTEM 👗")
    print("="*50)

    # 2. Collect User Input
    city = input("📍 Enter your City: ").strip()
    
    print("\nSelect Event: [Casual, Office, Party, Gym, Wedding]")
    event = input("🎉 Enter Event Type: ").strip().capitalize()
    
    print("\nSelect Skin Tone: [Light, Medium, Dark]")
    skin = input("🎨 Enter Skin Tone: ").strip().capitalize()

    # 3. Get Real-Time Weather
    print(f"\n🌍 Fetching weather for {city}...")
    weather_cat, temp = get_weather(city)
    print(f"   -> It is {temp}°C and '{weather_cat}'")

    # 4. Get Color Recommendations
    color_guide = get_color_recommendation(skin)

    # 5. Get ML Outfit Recommendation
    print("🧠 AI is thinking...")
    final_outfit = get_outfit_prediction(model, le_weather, le_event, le_skin, le_outfit, weather_cat, event, skin)

    # 6. Final Output Display
    print("\n" + "="*50)
    print("🌟 YOUR PERSONALIZED STYLE GUIDE 🌟")
    print("="*50)
    print(f"🌡️  Context:       {weather_cat} Weather ({temp}°C) | {event}")
    print(f"🧥  Outfit:        {final_outfit}")
    print("-" * 50)
    print(f"✅  Best Colors:   {', '.join(color_guide['Best'])}")
    print(f"❌  Avoid Colors:  {', '.join(color_guide['Avoid'])}")
    print("="*50 + "\n")

if __name__ == "__main__":
    main()