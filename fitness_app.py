import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# Function to encode local image to Base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Provide correct local path of the image
image_path = "834273.jpg"  # Ensure this file is in the same directory or provide a full path
base64_image = get_base64_of_image(image_path)

# Custom CSS for Background Image & Styling

# Custom CSS for improved UI
# Custom CSS for Background Image & Styling
page_bg_img = f'''
<style>
.stApp {{
    background: url("data:image/jpeg;base64,{base64_image}") no-repeat center center fixed;
    background-size: cover;
    color: white;
    font-family: 'Arial', sans-serif;
}}

.stApp::before {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6); /* Dark overlay for better contrast */
    z-index: -1;
}}

.stTitle, .stHeader, .stSubheader {{
    text-align: center;
    font-weight: bold;
    text-shadow: 3px 3px 10px rgba(255, 223, 0, 0.9);
}}

.stSidebar {{
    background-color: rgba(0, 0, 0, 0.8);
    padding: 20px;
    border-radius: 10px;
}}

.stButton>button {{
    background-color: #FFD700;
    color: black;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s ease-in-out;
}}

.stButton>button:hover {{
    background-color: #ffcc00;
    transform: scale(1.05);
}}

.stMetric {{
    font-size: 24px;
    font-weight: bold;
    color: #FFD700;
    text-shadow: 2px 2px 5px rgba(255, 215, 0, 0.7);
}}

input, select {{
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px;
    width: 100%;
}}

::placeholder {{
    color: white;
    opacity: 0.7;
}}

</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Load fitness dataset
dataset_path = "dataset-2.csv"
diet_chart_path = "diet_dataset_2.csv"
try:
    df = pd.read_csv(dataset_path)
    diet_df = pd.read_csv(diet_chart_path)
except FileNotFoundError:
    df = None  # Fallback if dataset isn't available
    diet_df = None

st.title("🏋 Personal Fitness Tracker")
st.subheader("Track your health & stay fit!")

# Sidebar for User Input
st.sidebar.header("🔹 Enter Your Details")
age = st.sidebar.number_input("Age:", min_value=18, max_value=80, step=1)
height = st.sidebar.number_input("Height (cm):", min_value=120, max_value=250, step=1)
weight = st.sidebar.number_input("Weight (kg):", min_value=45, max_value=300, step=1)
steps = st.sidebar.number_input("Daily Steps:", min_value=0, step=100)
workout = st.sidebar.number_input("Workout Minutes:", min_value=0, step=5)
sleep = st.sidebar.number_input("Sleep Hours:", min_value=0.0, step=0.5)

# BMI Calculator
def calculate_bmi(weight, height):
    if height > 0:
        return round(weight / ((height / 100) ** 2), 2)
    return None

# Calories Burned Calculator
def calculate_calories_burned(steps, workout, weight):
    return round((steps * 0.04) + (workout * 7), 2)

# Fitness Recommendation
def recommend_workout(steps, workout, sleep, bmi):
    step_advice = "Great job! Maintain your activity level." if steps >= 10000 else "Try to hit 10,000 steps daily."
    workout_advice = "You're working out enough!" if workout >= 30 else "Increase your workout time to at least 30 minutes."
    sleep_advice = "Your sleep is good!" if sleep >= 6 else "Try to get 7-8 hours of sleep."
    bmi_advice = f"Your BMI is '{bmi}', which is in the "
    if bmi < 18.5:
        bmi_advice += "Underweight category. Consider gaining some weight."
        color = "orange"
    elif 18.5 <= bmi < 25:
        bmi_advice += "Healthy Weight range. Keep up the good work!"
        color = "green"
    elif 25 <= bmi < 30:
        bmi_advice += "Overweight category. Consider adjusting your diet & exercise."
        color = "red"
    else:
        bmi_advice += "Obese category. Focus on fitness & a balanced diet."
        color = "red"
    return f"{step_advice} {workout_advice} {sleep_advice} {bmi_advice}", color

#  Diet Chart Generator
def generate_diet_chart(bmi):
    if diet_df is not None and 'BMI_Category' in diet_df.columns:
        category = 'Underweight' if bmi < 18.5 else 'Healthy Weight' if bmi < 25 else 'Overweight' if bmi < 30 else 'Obese'
        diet_info = diet_df[diet_df['BMI_Category'] == category]
        if not diet_info.empty:
            return diet_info.iloc[0].to_dict()  # Convert the row to a dictionary
    return "No diet data available."


# Educational Content Links
# Educational Content Links
def get_educational_links(bmi, sleep):
    links = {
        "Yoga for Everyone": "https://www.yogajournal.com/poses/yoga-for-beginners/"
    }

    if bmi < 18.5:
        links.update({
            "Gain Weight Tips": "https://www.healthline.com/nutrition/how-to-gain-weight",
            "Muscle Building": "https://www.bodybuilding.com/content/10-best-muscle-building-tips.html"
        })
    elif 18.5 <= bmi < 25:
        links.update({
            "General Fitness": "https://www.self.com/story/best-fitness-tips",
            "Healthy Lifestyle": "https://www.health.harvard.edu/staying-healthy"
        })
    else:
        links.update({
            "Weight Loss Tips": "https://www.medicalnewstoday.com/articles/weight-loss",
            "Fat Burning Exercises": "https://www.healthline.com/nutrition/best-exercise-weight-loss"
        })

    # Add Sleep Improvement Tips for users with < 6 hours of sleep
    if sleep < 6:
        links["Improve Your Sleep"] = "https://www.sleepfoundation.org/sleep-hygiene"

    return links
# Process User Data
bmi = calculate_bmi(weight, height)
calories_burned = calculate_calories_burned(steps, workout, weight)
edu_links = get_educational_links(bmi, sleep)

diet_chart = generate_diet_chart(bmi)
if st.sidebar.button("Get Recommendation"):
    st.subheader("📊 Your Fitness Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🔥 Calories Burned", value=f"{calories_burned} kcal")
    with col2:
        st.metric(label="⚖ Your BMI", value=f"{bmi}")
    
    result, color = recommend_workout(steps, workout, sleep, bmi)
    st.markdown(f'<div style="padding:10px; background-color:{color}; border-radius:10px;">{result}</div>', unsafe_allow_html=True)
    
    st.subheader("🥗 Recommended Diet Plan")
    if isinstance(diet_chart, dict):
        for key, value in diet_chart.items():
            st.write(f"**{key}:** {value}")
    else:
        st.write(diet_chart)
    
    st.subheader("📚 Educational Resources")
    for title, link in edu_links.items():
        st.write(f"📌 {title}: [{link}]({link})")
# Footer with your name
st.markdown(
    """
    <hr>
    <div style="text-align: center; font-size: 18px; color: white;">
        Developed by <b>Vikas Gupta</b>
    </div>
    """,
    unsafe_allow_html=True
)