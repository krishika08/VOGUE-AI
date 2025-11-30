# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# 1. Load Data
df = pd.read_csv('clothing_data.csv')

# 2. Preprocessing
le_weather = LabelEncoder()
le_event = LabelEncoder()
le_skin = LabelEncoder()
le_outfit = LabelEncoder()

df['Weather_n'] = le_weather.fit_transform(df['Weather'])
df['Event_n'] = le_event.fit_transform(df['Event'])
df['Skin_n'] = le_skin.fit_transform(df['Skin_Tone'])
df['Outfit_n'] = le_outfit.fit_transform(df['Outfit'])

X = df[['Weather_n', 'Event_n', 'Skin_n']]
y = df['Outfit_n']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- THE FIX IS HERE ---
# max_depth=3 makes the tree simpler and the graph readable
model = DecisionTreeClassifier(max_depth=3, random_state=42) 
model.fit(X_train, y_train)

# 4. Save everything
joblib.dump(model, 'model.pkl')
joblib.dump(le_weather, 'le_weather.pkl')
joblib.dump(le_event, 'le_event.pkl')
joblib.dump(le_skin, 'le_skin.pkl')
joblib.dump(le_outfit, 'le_outfit.pkl')

print("✅ Model Retrained with cleaner logic (Depth 3)!")