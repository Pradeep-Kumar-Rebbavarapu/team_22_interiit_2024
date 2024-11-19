import streamlit as st
import datetime as datetime
import json

file_path = "/Users/bhavyashah/Desktop/Model_UI_Integration/player_data.json"
with open(file_path, 'r') as file:
    player_data = json.load(file)

player_list = list(player_data.keys())

st.title("Team Selection")
st.subheader("Options")
col1, col2, col3 = st.columns(3)

with col1:
    match_date = st.date_input(
        label="Match Date",
        value=datetime.datetime(2020, 1, 1),
        min_value=datetime.datetime(2000, 1, 1),
        max_value=datetime.datetime(2025, 12, 31),
        format="YYYY-MM-DD",
        help="Select the start date for filtering the data."
    )

with col2:
    st.subheader("Team 1 Selection")

    if "team1_selected_players" not in st.session_state:
        st.session_state.team1_selected_players = []

    for i in range(11):
        if len(st.session_state.team1_selected_players) < 11:
            available_players = [
                pid for pid in player_list if pid not in st.session_state.team1_selected_players
            ]
            selected_player = st.selectbox(
                label=f"Player {i + 1}",
                options=available_players,
                key=f"team1_player_{i}"
            )

            # Add selected player to the list if it's not already in the team
            if selected_player not in st.session_state.team1_selected_players:
                st.session_state.team1_selected_players.append(selected_player)
            else:
                st.session_state.team1_selected_players[i] = selected_player
        else:
            st.selectbox(
                label=f"Player {i + 1}",
                options=st.session_state.team1_selected_players,
                key=f"team1_player_{i}",
                disabled=True
            )

    st.write("### Team 1 Players:")
    st.write([player for player in st.session_state.team1_selected_players])

    if len(st.session_state.team1_selected_players) == 11:
        st.success("Team 1 is complete!")

with col3:
    st.subheader("Team 2 Selection")

    if "team2_selected_players" not in st.session_state:
        st.session_state.team2_selected_players = []

    available_for_team2 = [
        pid for pid in player_list if pid not in st.session_state.team1_selected_players
    ]

    for i in range(11):
        if len(st.session_state.team2_selected_players) < 11:
            available_players_team2 = [
                pid for pid in available_for_team2 if pid not in st.session_state.team2_selected_players
            ]
            selected_player_team2 = st.selectbox(
                label=f"Player {i + 1}",
                options=available_players_team2,
                key=f"team2_player_{i}"
            )

            # Add selected player to the list if it's not already in the team
            if selected_player_team2 not in st.session_state.team2_selected_players:
                st.session_state.team2_selected_players.append(selected_player_team2)
            else:
                st.session_state.team2_selected_players[i] = selected_player_team2
        else:
            st.selectbox(
                label=f"Player {i + 1}",
                options=st.session_state.team2_selected_players,
                key=f"team2_player_{i}",
                disabled=True
            )

    st.write("### Team 2 Players:")
    st.write([player for player in st.session_state.team2_selected_players])

    if len(st.session_state.team2_selected_players) == 11:
        st.success("Team 2 is complete!")
