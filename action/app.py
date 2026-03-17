import streamlit as st
import pandas as pd
import os
import time
from streamlit_autorefresh import st_autorefresh
from PIL import Image

# ------------------ LOGIN + TEAM SELECTION ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.markdown("<h1 style='text-align:center;color:gold;'>🔐 IPL Auction Login</h1>", unsafe_allow_html=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    teams_list = ["SRH", "CSK", "MI", "RCB"]
    selected_team = st.selectbox("Select your team", teams_list)

    if st.button("Login", use_container_width=True):
        if user != "" and pwd != "":
            st.session_state.logged_in = True
            st.session_state.username = user
            st.session_state.user_team = selected_team
            st.success(f"Welcome {user}! You will bid for {selected_team} 🎉")
            st.rerun()
        else:
            st.error("Enter username & password")

if not st.session_state.logged_in:
    login()
    st.stop()

# ------------------ PLAYER IMAGES ------------------
player_images = {
    # Senior Players
    "MS Dhoni": r"C:\Users\Shanmukha Priya\Downloads\dhoni.PNG",
    "Rohit Sharma": r"C:\Users\Shanmukha Priya\Downloads\rohit.PNG",
    "Virat Kohli": r"C:\Users\Shanmukha Priya\Downloads\kohli.PNG",
    "Hardik Pandya": r"C:\Users\Shanmukha Priya\Downloads\hardik.PNG",
    "Ravindra Jadeja": r"C:\Users\Shanmukha Priya\Downloads\jadeja.PNG",
    "KL Rahul": r"C:\Users\Shanmukha Priya\Downloads\rahul.PNG",
    "Jasprit Bumrah": r"C:\Users\Shanmukha Priya\Downloads\bumrah.PNG",
    "Mohammed Shami": r"C:\Users\Shanmukha Priya\Downloads\shami.PNG",
    "Bhuvneshwar Kumar": r"C:\Users\Shanmukha Priya\Downloads\bhuvi.PNG",
    "Suryakumar Yadav": r"C:\Users\Shanmukha Priya\Downloads\sky.PNG",
    # Young Players
    "Yashasvi Jaiswal": r"C:\Users\Shanmukha Priya\Downloads\jaiswal.PNG",
    "Shubman Gill": r"C:\Users\Shanmukha Priya\Downloads\gill.PNG",
    "Rinku Singh": r"C:\Users\Shanmukha Priya\Downloads\rinku.PNG",
    "Tilak Varma": r"C:\Users\Shanmukha Priya\Downloads\tilak.PNG",
    "Ruturaj Gaikwad": r"C:\Users\Shanmukha Priya\Downloads\ruturaj.PNG",
    "Ishan Kishan": r"C:\Users\Shanmukha Priya\Downloads\ishan.PNG",
    "Abhishek Sharma": r"C:\Users\Shanmukha Priya\Downloads\abhi.PNG",
    "Sai Sudharsan": r"C:\Users\Shanmukha Priya\Downloads\sai.PNG",
    "Arshdeep Singh": r"C:\Users\Shanmukha Priya\Downloads\arshdeep.PNG",
    "Umran Malik": r"C:\Users\Shanmukha Priya\Downloads\umran.PNG",
    "Prithvi Shaw": r"C:\Users\Shanmukha Priya\Downloads\parth.PNG",
    "Nitish Kumar Reddy": r"C:\Users\Shanmukha Priya\Downloads\nitsh.PNG"
}

# ------------------ TEAM LOGOS ------------------
team_logos = {
    "SRH": r"C:\Users\Shanmukha Priya\Downloads\srh.png",
    "CSK": r"C:\Users\Shanmukha Priya\Downloads\csk.png",
    "MI": r"C:\Users\Shanmukha Priya\Downloads\mi.png",
    "RCB": r"C:\Users\Shanmukha Priya\Downloads\rcb.png"
}

# ------------------ TEAMS ------------------
if "teams" not in st.session_state:
    st.session_state.teams = {
        "SRH": {"name":"Sunrisers Hyderabad","purse":2000,"players":[],"color":"#ff4b00"},
        "CSK": {"name":"Chennai Super Kings","purse":2000,"players":[],"color":"#fddb00"},
        "MI": {"name":"Mumbai Indians","purse":2000,"players":[],"color":"#0056a6"},
        "RCB": {"name":"Royal Challengers Bengaluru","purse":2000,"players":[],"color":"#d50032"}
    }


# ------------------ FUNCTIONS ------------------
def update_budget(team, price):
    st.session_state.teams[team]["purse"] -= price

def add_player(team, player):
    st.session_state.teams[team]["players"].append(player)

# ------------------ PAGE CONFIG ------------------
st.set_page_config(layout="wide")

# ------------------ UI STYLE ------------------
st.markdown("""
<style>
.stApp{background: linear-gradient(120deg,#020617,#0f172a,#1e293b);color:white;}
.title{text-align:center;font-size:50px;color:gold;font-weight:bold;text-shadow:0 0 20px gold;}
.player-card{background:#1e293b;padding:30px;border-radius:20px;text-align:center;box-shadow:0 0 25px gold;animation: spotlight 2s infinite alternate;position:relative;}
.player-card:before{content:"";position:absolute;top:-20px;left:50%;transform:translateX(-50%);width:220px;height:20px;background:radial-gradient(circle, gold 10%, transparent 70%);filter:blur(10px);}
@keyframes spotlight{0%{box-shadow:0 0 10px gold;}100%{box-shadow:0 0 40px orange;}}
div.stButton > button{height:55px;font-size:18px;border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='title'>🏏 IPL AUCTION LIVE</h1>", unsafe_allow_html=True)
st.write(f"👤 Logged in as: {st.session_state.username} | Team: {st.session_state.user_team}")

# ------------------ AUTO REFRESH ------------------
st_autorefresh(interval=1000, key="auction")

# ------------------ LOAD PLAYERS ------------------
players = pd.read_csv("players.csv")

# ------------------ SESSION STATE ------------------
if "index" not in st.session_state:
    st.session_state.index = 0
if "price" not in st.session_state:
    st.session_state.price = players.iloc[0]["base_price"]
if "winner" not in st.session_state:
    st.session_state.winner = None
if "sold" not in st.session_state:
    st.session_state.sold = False
if "timer_start" not in st.session_state:
    st.session_state.timer_start = time.time()
if "history" not in st.session_state:
    st.session_state.history = []

player = players.iloc[st.session_state.index] if st.session_state.index < len(players) else None

# ------------------ TEAMS PANEL ------------------
st.write("## 🏏 Teams")
teams_data = st.session_state.teams
team_cols = st.columns(4)
for i, team in enumerate(teams_data):
    with team_cols[i]:
        logo = team_logos.get(team, "")
        if logo and os.path.isfile(logo):
            st.image(logo, width=80)
        st.markdown(f"### {teams_data[team]['name']}")
        purse = teams_data[team]["purse"]
        percent = purse / 2000
        st.write(f"💰 ₹{purse}")
        st.progress(percent)
        st.write("Players:", len(teams_data[team]["players"]))

# ------------------ PLAYER + BIDDING + LIVE BIDS ------------------
left, center, right = st.columns([2,6,2])

# Team Bidding Buttons
with left:
    st.write("## 🏏 Teams Bidding")
    for team in st.session_state.teams:
        if team == st.session_state.user_team:
            if st.button(f"Raise Paddle {team}", key=f"bid_{team}", use_container_width=True):
                bid = st.session_state.price + 20
                if st.session_state.teams[team]["purse"] >= bid:
                    st.session_state.price = bid
                    st.session_state.winner = team
                    st.session_state.timer_start = time.time()
                    st.session_state.history.append(f"🏏 {st.session_state.teams[team]['name']} bids ₹{bid}")
        else:
            st.button(f"Raise Paddle {team}", key=f"disabled_{team}", disabled=True, use_container_width=True)

# Player Card
with center:
    st.markdown("<div class='player-card'>", unsafe_allow_html=True)
    if player is not None:
        st.subheader(player["name"])
        img_path = player_images.get(player["name"], "")
        if img_path and os.path.isfile(img_path):
            img = Image.open(img_path)
            st.image(img, width=250)

        st.markdown(f"### 💰 Current Price: ₹{st.session_state.price}")

        total_time = 10
        elapsed = int(time.time() - st.session_state.timer_start)
        time_left = total_time - elapsed

        if not st.session_state.sold and time_left > 0:
            progress = int((time_left / total_time) * 360)
            st.markdown(f"""
            <div style="display:flex;justify-content:center">
            <div style="
            width:140px;height:140px;border-radius:50%;
            background:conic-gradient(gold {progress}deg,#1e293b 0deg);
            display:flex;align-items:center;justify-content:center;
            font-size:32px;font-weight:bold;color:white;">
            {time_left}
            </div>
            </div>
            """, unsafe_allow_html=True)
        elif not st.session_state.sold:
            if st.session_state.winner:
                winner = st.session_state.winner
                price = st.session_state.price
                add_player(winner, player["name"])
                update_budget(winner, price)
                st.session_state.history.append(f"{player['name']} SOLD to {st.session_state.teams[winner]['name']} ₹{price}")
                st.markdown(f"<div style='text-align:center;font-size:40px;color:gold;'>🔨 SOLD to {st.session_state.teams[winner]['name']} for ₹{price}</div>", unsafe_allow_html=True)
            else:
                st.warning("❌ No bids received")
            st.session_state.sold = True
            st.session_state.sold_time = time.time()

        if st.session_state.sold:
            st.markdown("### ⏸ Next player loading...")
            if time.time() - st.session_state.sold_time > 5:
                st.session_state.index += 1
                if st.session_state.index < len(players):
                    st.session_state.price = players.iloc[st.session_state.index]["base_price"]
                    st.session_state.winner = None
                    st.session_state.sold = False
                    st.session_state.timer_start = time.time()
                    st.rerun()
                else:
                    st.success("🏆 Auction Finished!")

    st.markdown("</div>", unsafe_allow_html=True)

# Live Bids Panel
with right:
    st.subheader("📊 Live Bids")
    if len(st.session_state.history) == 0:
        st.info("No bids yet. Start bidding!")
    else:
        for bid_text in st.session_state.history[::-1]:
            if "SOLD" in bid_text:
                st.markdown(f"<div style='color:gold;font-weight:bold'>{bid_text}</div>", unsafe_allow_html=True)
            else:
                st.write(bid_text)

# ------------------ FINAL SQUADS ------------------
st.write("---")
with st.expander("🏆 Final Squads"):
    for t in st.session_state.teams:
        st.write("###", st.session_state.teams[t]["name"])
        for p in st.session_state.teams[t]["players"]:
            st.write("•", p)

# ------------------ LEADERBOARD ------------------
st.write("---")
st.subheader("📊 Leaderboard")
leaderboard = []
for t in st.session_state.teams:
    team_data = st.session_state.teams[t]
    leaderboard.append({
        "Team": team_data["name"],
        "Players": len(team_data["players"]),
        "Remaining Purse": team_data["purse"]
    })
df = pd.DataFrame(leaderboard)
df = df.sort_values(by=["Players", "Remaining Purse"], ascending=[False, False]).reset_index(drop=True)
df.index = df.index + 1
st.dataframe(df, use_container_width=True)