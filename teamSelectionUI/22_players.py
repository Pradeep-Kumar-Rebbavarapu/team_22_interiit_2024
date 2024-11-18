import streamlit as st
import datetime as datetime
import json

# Load player data from JSON file
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

# Column 2: Team 1 Selection
with col2:
    st.subheader("Team 1 Selection")

    # Initialize the list for Team 1 if it doesn't exist
    if "team1_selected_players" not in st.session_state:
        st.session_state.team1_selected_players = []

    # Loop through each player slot (1-11)
    for i in range(11):
        # Only allow selecting players if there are less than 11 in the team
        if len(st.session_state.team1_selected_players) < 11:
            # Filter players that have not been selected yet
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
                # If player is already selected in a different slot, update that slot
                st.session_state.team1_selected_players[i] = selected_player
        else:
            # Once 11 players are selected, prevent further additions and make dropdown read-only
            st.selectbox(
                label=f"Player {i + 1}",
                options=st.session_state.team1_selected_players,
                key=f"team1_player_{i}",
                disabled=True
            )

    # Display selected players for Team 1
    st.write("### Team 1 Players:")
    st.write([player for player in st.session_state.team1_selected_players])

    # Display success message if 11 players have been selected
    if len(st.session_state.team1_selected_players) == 11:
        st.success("Team 1 is complete!")

# Column 3: Team 2 Selection
with col3:
    st.subheader("Team 2 Selection")

    # Initialize the list for Team 2 if it doesn't exist
    if "team2_selected_players" not in st.session_state:
        st.session_state.team2_selected_players = []

    # Dynamically filter players not in Team 1
    available_for_team2 = [
        pid for pid in player_list if pid not in st.session_state.team1_selected_players
    ]

    # Loop through each player slot (1-11)
    for i in range(11):
        # Only allow selecting players if there are less than 11 in the team
        if len(st.session_state.team2_selected_players) < 11:
            # Filter players that have not been selected yet
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
                # If player is already selected in a different slot, update that slot
                st.session_state.team2_selected_players[i] = selected_player_team2
        else:
            # Once 11 players are selected, prevent further additions and make dropdown read-only
            st.selectbox(
                label=f"Player {i + 1}",
                options=st.session_state.team2_selected_players,
                key=f"team2_player_{i}",
                disabled=True
            )

    # Display selected players for Team 2
    st.write("### Team 2 Players:")
    st.write([player for player in st.session_state.team2_selected_players])

    # Display success message if 11 players have been selected
    if len(st.session_state.team2_selected_players) == 11:
        st.success("Team 2 is complete!")