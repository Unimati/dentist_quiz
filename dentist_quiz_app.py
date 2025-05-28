import streamlit as st

st.set_page_config(page_title="🦷 Dentist Personality Quiz", layout="centered")

st.title("🦷 Dentist Personality Quiz")

if 'step' not in st.session_state:
    st.session_state.step = 0

if 'answers' not in st.session_state:
    st.session_state.answers = {}

steps = [
    {
        'title': "Step 1: Patient Types",
        'questions': ["Total patients", "Children", "Adults", "Elderly"]
    },
    {
        'title': "Step 2: Case Types",
        'questions': ["Emergency cases", "Cosmetic cases", "Routine cases", "Surgical cases"]
    },
    {
        'title': "Step 3: Procedures",
        'questions': ["Cleanings", "Fillings", "Extractions", "Root canals", "Implants", "Whitening"]
    },
    {
        'title': "Step 4: Mood and Preferences",
        'questions': ["Fav procedure", "Least fav procedure", "Energy (1-10)"]
    }
]

step = st.session_state.step
st.subheader(steps[step]['title'])

for q in steps[step]['questions']:
    st.session_state.answers[q] = st.text_input(q, value=st.session_state.answers.get(q, ""))

if step == 3:
    mood = st.selectbox("Mood today:", ["Happy", "Stressed", "Tired", "Fulfilled", "Bored"], index=0)
    st.session_state.answers["Mood"] = mood

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if step > 0:
        if st.button("⬅ Back"):
            st.session_state.step -= 1

with col2:
    if step < len(steps) - 1:
        if st.button("Next ➡"):
            st.session_state.step += 1

with col3:
    if step == len(steps) - 1:
        if st.button("🔍 Analyze Me!"):
            st.subheader("Your Analysis")
            try:
                data = {k: int(v) if v.isdigit() else v for k, v in st.session_state.answers.items()}
                mood = data.get("Mood", "").lower()
                energy = int(data.get("Energy (1-10)", 5))
                num_patients = int(data.get("Total patients", 0))

                scores = {
                    'Pediatric Pro': int(data.get("Children", 0)) * 2,
                    'Restorative Expert': int(data.get("Fillings", 0)) * 2 + int(data.get("Root canals", 0)) * 2,
                    'Surgical Star': int(data.get("Extractions", 0)) * 2.5 + int(data.get("Implants", 0)) * 2.5 + int(data.get("Surgical cases", 0)) * 1.5,
                    'Cosmetic Aesthete': int(data.get("Whitening", 0)) * 3 + int(data.get("Cosmetic cases", 0)) * 2,
                    'Preventive Hero': int(data.get("Cleanings", 0)) * 2 + int(data.get("Routine cases", 0)) * 1.5,
                    'Emergency Responder': int(data.get("Emergency cases", 0)) * 2.5,
                    'Empath': 0,
                    'Burned-Out': 0,
                    'Balanced Clinician': 1
                }

                if num_patients <= 3 and mood in ['tired', 'bored', 'stressed']:
                    scores['Empath'] += 10
                if num_patients > 10 and (energy <= 3 or mood in ['tired', 'stressed']):
                    scores['Burned-Out'] += 15

                procedures = ["Cleanings", "Fillings", "Extractions", "Root canals", "Implants", "Whitening"]
                variety = len([int(data[p]) for p in procedures if int(data.get(p, 0)) > 0])
                if 3 <= variety <= 5:
                    scores['Balanced Clinician'] += 5

                best_fit = max(scores, key=scores.get)

                descriptions = {
                    'Pediatric Pro': "🧒 Pediatric Pro\nStrengths: Patient, nurturing, creative in handling young patients.\nWeaknesses: Can be exhausting; high energy required.\nFun Fact: Knows the name of every cartoon character.",
                    'Restorative Expert': "🛠️ Restorative Expert\nStrengths: Detail-oriented, excellent hand skills, problem solver.\nWeaknesses: Risk of repetitive strain, high precision fatigue.\nFun Fact: Probably owns magnifying loupes with LED lights.",
                    'Surgical Star': "🔪 Surgical Star\nStrengths: Decisive, confident, loves procedures.\nWeaknesses: Can feel rushed; more complex risk management.\nFun Fact: Feels at home with forceps and sutures.",
                    'Cosmetic Aesthete': "💎 Cosmetic Aesthete\nStrengths: Artistic, meticulous, focused on smile perfection.\nWeaknesses: Patient expectations can be very high.\nFun Fact: Has a favorite tooth shade (and it's B1).",
                    'Preventive Hero': "🛡️ Preventive Hero\nStrengths: Educator, promotes long-term oral health.\nWeaknesses: May get overlooked in glamour of specialties.\nFun Fact: Has a library of flossing techniques.",
                    'Emergency Responder': "🚨 Emergency Responder\nStrengths: Cool under pressure, fast thinker, triage skills.\nWeaknesses: High stress, unpredictable cases.\nFun Fact: Has seen it all — from cracked molars to swallowed crowns.",
                    'Empath': "🧠 The Empath\nStrengths: Emotionally in tune, compassionate, calming.\nWeaknesses: Risk of emotional exhaustion.\nFun Fact: Patients often share more than just oral health concerns.",
                    'Burned-Out': "🔥 Burned-Out\nStrengths: Highly productive, resilient, skilled.\nWeaknesses: At risk of fatigue, needs a break.\nFun Fact: Dreams of vacation while placing fillings.",
                    'Balanced Clinician': "⚖️ Balanced Clinician\nStrengths: Versatile, dependable, well-rounded.\nWeaknesses: May lack a signature specialty.\nFun Fact: Can shift from scaling to surgery with ease."
                }

                st.success(f"Your Dentist Type: {best_fit}")
                st.info(descriptions[best_fit])

            except ValueError:
                st.error("Please enter valid numbers in the form.")
