import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="IPL Pro Dashboard", layout="wide")

# ---------------- USER STORAGE ----------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "1234"}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

# ---------------- LOGIN + SIGNUP ----------------
if not st.session_state.logged_in:

    st.title("🏏 IPL Dashboard")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    # LOGIN
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            if new_user in st.session_state.users:
                st.warning("User already exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created! Please login.")

    st.stop()

# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.image("logos/ipl_logo.jpg", width=200)

with col2:
    st.markdown("<h1 style='color:#ff4b2b;'>IPL Analytics Dashboard</h1>", unsafe_allow_html=True)

with col3:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

st.write(f"👋 Welcome, {st.session_state.current_user}")

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio("📌 Navigation", [
    "🏠 Home",
    "📊 Prediction",
    "📈 Stats",
    "👤 Player Stats"
])

# ---------------- HOME ----------------
if page == "🏠 Home":
    st.markdown("## Welcome to IPL Analytics Dashboard 🏏")

    st.write("""
This IPL Analytics Dashboard predicts match outcomes using machine learning 
and provides insights into team and player performance.

Explore predictions, analyze stats, and visualize data using an interactive dashboard.
""")

# ---------------- PREDICTION ----------------
elif page == "📊 Prediction":

    model = pickle.load(open('outputs/model.pkl','rb'))
    columns = pickle.load(open('outputs/columns.pkl','rb'))

    teams = [
        'Mumbai Indians','Chennai Super Kings','Royal Challengers Bangalore',
        'Kolkata Knight Riders','Delhi Capitals','Sunrisers Hyderabad',
        'Rajasthan Royals','Punjab Kings'
    ]

    logos = {
        'Mumbai Indians': "logos/mi.jpg",
        'Chennai Super Kings': "logos/csk.jpg",
        'Royal Challengers Bangalore': "logos/rcb.jpg",
        'Kolkata Knight Riders': "logos/kkr.jpg",
        'Delhi Capitals': "logos/dc.jpg",
        'Sunrisers Hyderabad': "logos/srh.jpg",
        'Rajasthan Royals': "logos/rr.jpg",
        'Punjab Kings': "logos/pbks.jpg"
    }

    c1, c2 = st.columns(2)

    with c1:
        t1 = st.selectbox("Team 1", teams)
        st.image(logos[t1], width=140)

    with c2:
        t2 = st.selectbox("Team 2", teams)
        st.image(logos[t2], width=140)

    toss = st.selectbox("Toss Winner", [t1, t2])

    if st.button("🚀 Predict Winner"):

        with st.spinner("Analyzing match..."):
            time.sleep(1)

        df = pd.DataFrame({'team1':[t1],'team2':[t2],'toss_winner':[toss]})
        df = pd.get_dummies(df)
        df = df.reindex(columns=columns, fill_value=0)

        pred = model.predict(df)[0]
        proba = model.predict_proba(df)[0]

        st.success(f"🏆 Winner: {pred}")
        st.image(logos[pred], width=150)

        team_probs = {t:p for t,p in zip(model.classes_,proba) if t in [t1,t2]}
        names = list(team_probs.keys())
        values = list(team_probs.values())

        colA, colB = st.columns(2)

        with colA:
            fig, ax = plt.subplots(figsize=(4,3))
            ax.bar(names, values)
            st.pyplot(fig)

        with colB:
            fig2, ax2 = plt.subplots(figsize=(4,3))
            ax2.pie(values, labels=names, autopct='%1.1f%%')
            st.pyplot(fig2)

# ---------------- STATS ----------------
elif page == "📈 Stats":

    st.markdown("## 📊 Team Stats")

    teams = ["MI","CSK","RCB","KKR"]
    wins = [120,110,95,100]

    fig, ax = plt.subplots(figsize=(5,3))
    ax.bar(teams, wins)
    st.pyplot(fig)

# ---------------- PLAYER STATS ----------------
elif page == "👤 Player Stats":

    st.markdown("## 👤 Player Performance")

    data = {
        "Player": ["Virat Kohli", "Rohit Sharma", "MS Dhoni", "David Warner", "KL Rahul"],
        "Runs": [7263, 6211, 5082, 6100, 5800],
        "Strike Rate": [130.4, 134.2, 139.5, 137.8, 135.6],
    }

    df = pd.DataFrame(data)
    st.dataframe(df)

