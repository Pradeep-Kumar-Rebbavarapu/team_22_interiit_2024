
import os
import json
from py_expression_eval import Parser
from fuzzywuzzy import process
from backend.settings import BASE_DIR
import sys
# If you installed cricketstats by pip import the module with line below
import cricketstats as cks
from groq import Groq

client = Groq(api_key="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")

# If you cloned the github repo uncomment the block below.

player_data = open(os.path.join(BASE_DIR,'./data/player_data.json'), 'r')
past_data = player_data.read()

past_data = json.loads(past_data)



module_path = os.path.abspath(os.path.join("./cricketstats/src/"))
if module_path not in sys.path:
    sys.path.append(module_path)

parser = Parser()

def agentAI(message: str, all_players_id: list, all_players: list, all_players_variations: list) -> str:
    """Main function to process queries and return return response"""
  
    # PROMPTS
    QUICK_PROMPT = f'''Create me an exact JSON query as a string for the prompt given at the end. Follow these rules strictly:

    1. ONLY use the fields explicitly listed below
    2. Do NOT reference any fields that are not listed here
    3. Return ONLY the raw JSON string with NO markdown formatting, NO code blocks, NO backticks, and NO additional text
    4. Do NOT include json, , or any other markdown/code formatting
    5. Ensure all crucial data matches those provided

    Arguments which must be in the final output JSON (Or empty array):
        - players = ""    # One or two players specified by user. FORMAT: ["Player whose performance is being checked", "Against whom is it being checked"]. For example (DO NOT USE THE NAMES PROVIDED IN THE EXAMPLES). - If V Kohli plays against HH Pandya, write ['V Kohli', 'HH Pandya']. Options to choose from = ''' + str(all_players) + '''. If the players user mentioned do not lie in the Options, then use the first player name.
        - matchtype = Options = ['club_ODI_previous3_runs', 'club_ODI_previous3_wickets', 'club_ODI_previous3_balls played', 'club_ODI_previous3_overs', 'club_ODI_previous3_runs gave', 'club_ODI_lifetime_runs', 'club_ODI_lifetime_wickets', 'club_ODI_lifetime_balls played', 'club_ODI_lifetime_overs', 'club_ODI_lifetime_runs gave', 'club_Test_previous3_runs', 'club_Test_previous3_wickets', 'club_Test_previous3_balls played', 'club_Test_previous3_overs', 'club_Test_previous3_runs gave', 'club_Test_lifetime_runs', 'club_Test_lifetime_wickets', 'club_Test_lifetime_balls played', 'club_Test_lifetime_overs', 'club_Test_lifetime_runs gave', 'club_T20_previous3_runs', 'club_T20_previous3_wickets', 'club_T20_previous3_balls played', 'club_T20_previous3_overs', 'club_T20_previous3_runs gave', 'club_T20_lifetime_runs', 'club_T20_lifetime_wickets', 'club_T20_lifetime_balls played', 'club_T20_lifetime_overs', 'club_T20_lifetime_runs gave', 'international_ODI_previous3_runs', 'international_ODI_previous3_wickets', 'international_ODI_previous3_balls played', 'international_ODI_previous3_overs', 'international_ODI_previous3_runs gave', 'international_ODI_lifetime_runs', 'international_ODI_lifetime_wickets', 'international_ODI_lifetime_balls played', 'international_ODI_lifetime_overs', 'international_ODI_lifetime_runs gave', 'international_Test_previous3_runs', 'international_Test_previous3_wickets', 'international_Test_previous3_balls played', 'international_Test_previous3_overs', 'international_Test_previous3_runs gave', 'international_Test_lifetime_runs', 'international_Test_lifetime_wickets', 'international_Test_lifetime_balls played', 'international_Test_lifetime_overs', 'international_Test_lifetime_runs gave', 'international_T20_previous3_runs', 'international_T20_previous3_wickets', 'international_T20_previous3_balls played', 'international_T20_previous3_overs', 'international_T20_previous3_runs gave', 'international_T20_lifetime_runs', 'international_T20_lifetime_wickets', 'international_T20_lifetime_balls played', 'international_T20_lifetime_overs', 'international_T20_lifetime_runs gave']
        - columns = []    # An array containing the data the user wants, Options: ['runs', 'wickets', 'balls']
        Example: If the user says, "Runs of someone" then columns should be ["runs"]. If the user says, "wickets by someone", columns should be ["wickets"]. If the user says, "wickets and balls", columns should be ["wickets","balls"]. Default = ["runs", "wickets", "balls"]

    Note that if two players are mentioned, matchtype is empty. Only columns should be present. If only one player exists, then column is empty. If both are explicitly mentioned, prefer matchtype over columns.
    If there is only a single player and no matchtype is mentioned - Default: ['international_ODI_lifetime_runs', 'international_Test_lifetime_runs', 'international_T20_lifetime_runs', 'international_ODI_lifetime_wickets', 'international_Test_lifetime_wickets', 'international_T20_lifetime_wickets']    
    If user only told 'runs' without mentioning matchtype, then Default: ['international_ODI_lifetime_runs', 'international_Test_lifetime_runs', 'international_T20_lifetime_runs', 'club_ODI_lifetime_runs', 'club_Test_lifetime_runs', 'club_T20_lifetime_runs']
    If user only told 'wickets' without mentioning matchtype, then Default: ['international_ODI_lifetime_wickets', 'international_Test_lifetime_wickets', 'international_T20_lifetime_wickets', 'club_ODI_lifetime_wickets', 'club_Test_lifetime_wickets', 'club_T20_lifetime_wickets']

    Return a JSON containing all the required arguments and optional arguments as specified by the user:

    Output JSON Examples:
    {
        "players": ["Sarfaraz Ahmed", "KK Ram"],
        "matchtype": [],
        "columns": ["runs", "wickets"]
    }

    {
        "players": ["Sam Altman"],
        "matchtype": ["Test", "IT20"],
        "columns": []
    }

    Begin!
    '''

    DB_PROMPT = f'''Create me an exact JSON query as a string for the prompt given at the end. Follow these rules strictly:

    1. ONLY use the fields explicitly listed below
    2. Do NOT reference any fields that are not listed here
    3. Return ONLY the raw JSON string with NO markdown formatting, NO code blocks, NO backticks, and NO additional text
    4. Do NOT include json, , or any other markdown/code formatting
    5. Ensure all crucial data matches those provided

    Required Arguments which must be in the final output JSON:
        - players = ""    # Array of players specified by user. Pick only players inside this array and not from outside or the examples. For example (DO NOT USE THE NAMES PROVIDED IN THE EXAMPLES). - ["SS Kappa"] or ["ST Byako", "QW Marchem"]. Options to choose from = ''' + str(all_players) + '''. If the players user mentioned do not lie in the Options, then use the first player name.
        - to_date = ()    # Array of date in YYYY,MM,DD format. Default - [2024,11,10]. If value less than 10, do not add leading zeroes. If user's date is greater, choose [2024,6,30]. If user only enters a year say 2021, then set date as 2021,12,31
        - from_date = ()    # Array of date in YYYY,MM,DD format. Default - [2019,6,30]. If value less than 10, do not add leading zeroes. If user's date is smaller, choose [2019, 6, 30]. If user only enters a year say 2021, then set date as 2021,1,1.
        - matchtype = []    # An array containing the match type(s) specified by the user, Options: ["Test", "MDM", "ODI", "ODM", "T20", "IT20"] ("Test matches", "Multi-day matches", "One-day internationals", "One-day matches", "T20 internationals", "Non-official T20 internationals" respectively). Default - ["Test", "MDM", "ODI", "ODM", "T20", "IT20"]. 
        - columns = []    # An array containing the data the user wants, Options: ['Runs', 'Wickets', 'Avg Consecutive Dot Balls', 'Avg First Boundary Ball', 'Balls Bowled', 'Balls Faced', 'Balls Faced MeanAD', 'Batting', 'Batting Avg', 'Batting S/R', 'Batting S/R MeanAD', 'Boundary %', 'Boundary Given %', 'Boundary Given Rate', 'Boundary Rate', 'Bowled Outs', 'Bowleds','Bowling', 'Bowling Avg', 'Bowling Avg MeanAD', 'Bowling S/R', 'Bowling S/R MeanAD', 'Catches', 'Caught Outs', 'Caught and Bowled Outs', 'Caught and Bowleds', 'Caughts', 'Dismissal Rate', 'Dot Ball %', 'Dot Ball Bowled %', 'Dot Balls', 'Dot Balls Bowled', 'Drawn', 'Economy Rate', 'Economy Rate MeanAD', 'Extras', 'Fours', 'Foursgiven', 'Games', 'Hitwicket Outs', 'Hitwickets', 'Innings Batted', 'Innings Bowled', 'LBW Outs', 'LBWs', 'Mean Balls Faced', 'Mean Score', 'No Balls', 'Outs', 'Players', 'Run Outs', 'Runouts', 'Runs', 'Runs/Ball', 'Runsgiven', 'Runsgiven/Ball', 'Score MeanAD', 'Scoring Consistency', 'Singles', 'Singlesgiven', 'Sixes', 'Sixesgiven', 'Strike Turnover %', 'Strike Turnovergiven %', 'Stumped Outs', 'Stumpeds', 'Stumpings', 'Survival Consistency', 'Wickets', 'Wides', 'Win %', 'Won', 'Runs Rate', 'Runsgiven/Wicket', 'Runs AA', 'Runs/Ball AA', 'Runsgiven AA', 'Runsgiven/Ball AA', Default = All
        Example: If the user says, "Runs of someone" then columns should be ["Runs"]. If the user says, "wickets by someone", columns should be ["Wickets"]. If the user says, "team name and opposition team was what?", columns should be ["Team","Opposition"]. If the user wants "strike rate", strike rate means S/R, in general.

    Optional Arguments as requested by the user (Leave empty Arrays/False/None if not specified):
        - betweenovers=[]   # Search data only between these overs. eg. betweenovers = [1, 20]. Or if you only want to search for powerplays that are mandatory and option input "powerplays" eg. betweenovers =["powerplays"].
        - innings=[]    # Search these innings involving Array of numbers. Options: 1, 2, 3, 4. eg. innings = [1,3].
        - fielders=[]   # Search bowling stats involves Array of strings og names of specific fielders.
        - oppositionbatters=[]  # Search overs where players have bowled against certain batters. Cases: 1. Array of strings of batter names. 2. Array of strings of batters by handedness. eg. oppositionbatters=["Left hand", "Right hand"] or oppositionbatters=["Left hand"]. Two Options: "Right hand" and "Left hand"
        - oppositionbowlers=[]  # Search overs where players have batted against certain bowlers. Cases: 1. Array of strings of bowler names 2. Array of strings of bowlers by type, eg. oppositionbowlers=["Right arm pace","Left arm pace"]. Six Possibilities: ["Right arm pace","Left arm pace","Right arm off break","Right arm leg break","Left arm orthodox","Left arm wrist spin"]
        - superover=None    # Search normal innings or superover innings. Options: True, False eg. superover=True.
        - battingposition=[]    # Search stats at certain position in batting order. eg. battingposition=[1,2,3].
        - bowlingposition=[]    # Search stats at certain position in bowling order. eg. bowlingposition=[1,2]
        - sex=[]    # Search only matches of certain sex. Options: "male", "female" eg. sex = ["male"] 
        - playersteams=[]    # Search matches where players have played in certain teams. Options: team names eg. playerteams=["India", "Royal Challengers Bangalore"]
        - teammates=[]  # Search matches where certain teammates play. For this to work playerteams must be populated.
        - oppositionteams=[]    # Search matches where opposition is only certain teams. Options: team names eg. oppositionteams=["India", "England"]
        - venue=[]  # Search matches played only at these venues Options: Cricket Grounds eg. venue=["Sydney Cricket Ground", "Eden Gardens", "Brisbane Cricket Ground, Woolloongabba"]
        - teamtype=[]   # Search only for particualr type of teams. Options: "international", "club".
        - event=[]  # Search matches played as part of these Leagues or Tournaments Options: Name of League or Tournament eg. event=["Sheffield Shield", "ICC World Cup", "Big Bash League"] 
        - matchresult=None  # Search matches where players or teams have these results. When looking at players, this option *must* be used with at one team in playersteams variable. Options either "won" or "loss" or "draw" or "tie" eg. matchresult="won"
        - sumstats=False    # When switched to True, it adds an "all players" or "all teams" row at end of result that sums all players or teams stats that are searched for. Default - False


    Return a JSON containing all the required arguments and optional arguments as specified by the user:

    Output JSON Example:
    {
        "players": "Sarfaraz Ahmed",
        "database": "./all_json.zip",
        "to_date": [2022,01,24],
        "from_date": [2004,09,12],
        "matchtype": ["Test", "IT20"],
        "fielders": ["A Kumble", "R Jadeja"],
        "columns": ["Runs", "Boundary %"]
    }

    Begin!
    '''

    # AGENT_PROMPT = '''
    # You are a knowledgeable assistant that can handle various types of queries. Analyze the user's query and determine the best way to respond. Follow these steps:

    # 1. ONLY use format of JSON = { "Thought": "(thought)", "Action": "(action)", "Action Input": "(action_input)", "Response Format": "(response_format)" }
    # 2. Do NOT reference any other format not listed here
    # 4. Do NOT include json, , or *** any other markdown/code formatting

    # 1. First determine what type of information is needed:
    # - Database Query (SearchDB): For factual information stored in the database
    # - Calculation (Calculator): For mathematical operations
    # - Direct Response: For general knowledge or logical reasoning

    # 2. Create a response plan

    # 3. Respond with this exact JSON format only:
    # {
    #     "Thought": "Your analysis of what needs to be done",
    #     "Action": "SearchDB or Calculator or DirectResponse",
    #     "Action Input": "Your query or calculation or None for direct responses",
    #     "Response Format" : "Your Response"

    # Begin!
    # '''
    AGENT_PROMPT = '''
    You are a knowledgeable assistant that can handle various types of queries. Keep your context only to CRICKET. You have access to data from June 2019 to November 2024. Analyze the user's query and determine the best way to respond. Follow these steps:

    1. ONLY use format of JSON = { "Thought": "(thought)", "Action": "(action)", "Response Format": "(response_format)" }
    2. Do NOT reference any other format not listed here
    3. Do NOT include json, , or *** any other markdown/code formatting
    4. If the player is not present in the following list of players = ''' + str(all_players_variations) + ''', say "(Player Name) is not playing today." 
        Example: User says 'How is Tim Cook as a player?', Say 'Tim Cook is not playing today.'
    
    1. First determine what type of information is needed:
    - Database Query (SearchDB): For all factual information stored in the database for all other complex queries. Use when two or more players are involved or anything apart from wickets, runs, overs or balls is asked. Example = 1. Runs with win percentage and strike rate of Hardik, 2. How is Kohli against leg spinners?
    - Database Query (QuickDB): For extremely fast information of player Head to Head against scenarios. Contains runs, overs and balls data of previous 3 matches (international or club) and lifetime matches only for each match format. Also contains head to head data. Examples: 1. runs of Sam against Ethen, 2. total runs or wickets in test cricket of last 3 matches of Aman.
    - Calculation (Calculator): For mathematical operations
    - Direct Response: For general knowledge or logical reasoning

    2. Create a response plan

    3. Respond with this exact JSON format only:
    {
        "Thought": "Your analysis of what needs to be done",
        "Action": "SearchDB or Calculator or DirectResponse",
        "Action Input": "Your query or calculation or None for direct responses",
        "Response Format" : "Your Response",
        "Players": "Array of all players mentioned by the user, Format: ['Plauyer1', 'Player2']"
    }

    Begin!
    '''

    SQL_PROMPT = '''Create me an exact SQL query as a string for the prompt given at the end. Follow these rules strictly:

    1. ONLY use the tables and columns explicitly listed below
    2. Do NOT reference any tables or columns that are not listed here
    3. Return ONLY the raw SQL query with NO markdown formatting, NO code blocks, NO backticks, and NO additional text
    4. Do NOT include sql, , or any other markdown/code formatting
    5. Ensure all column and table names exactly match those provided

    -------- END OF TABLES
    Below is the user prompt'''

    DIRECT_PROMPT = '''You are a knowledgeable assistant for the user. DO NOT INCLUDE ANY EXPLICIT OR UNWANTED CONTENT.
                        Respond to the user query directly with your knowledge in 1-2 lines. Be short and concise.
                        Following is a summarised version of the format in which you have to respond to the user:

                    '''



    def match_players(player_names) -> list:

        print("Matching...")
        # If the LLM instead generates a string of a single player instead of an array.
        if type(player_names) == type("String"):
            dummyPlayers = []
            dummyPlayers.append(players)
            player_names = dummyPlayers

        players = []

        variations = [variation for variations_list in all_players_variations.values() for variation in variations_list]
        print("Alag: ", variations)
        # Match the best player playing in the match.
        for player_name in player_names:
            print(player_name)
            best_match = process.extractOne(player_name, variations)
            print(best_match)

            if best_match and best_match[1] >= 70:
                for key in all_players_variations.keys():
                    print(key)
                    if best_match[0] in all_players_variations[key]:
                        players.append(key)
                        break
        
        print("Khiladi: ", players)

        return players

    def match_ids(player_names) -> list:
        ids = []

        for player in player_names:
            ids.append(all_players_id[all_players.index(player)])

        return ids

    def calculator(input_query: str, response_format: str) -> float:
        """
        Evaluates mathematical expressions
        """
        try:
            return parser.parse(input_query).evaluate({})
        except Exception as e:
            raise ValueError(f"Error in calculation: {str(e)}")
        
    def fetchDataStats(input_query, message: str) -> str:
        print("DataStats Called")
        print(type(input_query))
        players_name = input_query.get('players', [])
        columns = input_query.get('columns', [])
        matchtype = input_query.get('matchtype', [])

        print(players_name, columns, matchtype)
        # Matching every player name to our players list.
        players_name = match_players(players_name)

        data = []

        players = match_ids(players_name)
        print(players)

        if len(players) == 1:
            for match in matchtype:
                data.append([match, past_data[players[0]][match]])
        if len(players) == 2:
            for column in columns:
                data.append([column, past_data[players[0]]["played_against"][players[1]][column]])

        data = gemini(f"""
                      You are a helpful humanoid agent. Answer the user like a normal human without mentioning your name.
                      Be very precise and to the point, do not extend. Talk in 1-2 lines.
                      Example: 'The wickets taken by Pandya in his last match was 4.'. 
                      TALK LIKE A HUMAN. IF THE DATA IS NOT PRESENT OR SILLY, ANSWER THE QUERY USING YOUR OWN DATA. 
                      Fill the query as per the response format for the user's query is given at the bottom.
                      
                      Adhere to the response format completely without fail. DO NOT USE ANY OTHER FORMAT TO SUMMARISE THE DATA.\nTake the data shown after this line. 
                      Data: \n""" + str(data) + "\nEND OF DATA. when the user asked: " + str(message) + f"\nEND OF USER PROMPT. SET NAME OF PLAYERS TO ONE OF THE OPTIONS: " + str(players_name) + 
                      '''\nCONFIRM IF THE OUTPUT DATA MATCHES THE QUERY USING COMMON SENSE BEFORE SHOWING OUTPUT. 
                      IF THE QUERY IS DIFFERENT, ANSWER THE QUERY ON YOUR OWN.''')

        return data
    
    def fetchCricStats(input_query, message: str) -> str:
        print("CricStats Called")
        print(input_query)
        oldPlayers = input_query.get('players', [])

        # Matching every player name to our players list.
        players = match_players(oldPlayers)
        print(players)

        if len(players) == 0:
            if type(oldPlayers) == type("String"):
                return f"{oldPlayers} is not playing today."
            if len(oldPlayers) == 1:
                return f"{oldPlayers[0]} is not playing today."
            else:
                return "No matching players found!"

        columns = input_query['columns']       

        search = cks.cricketstats.search(players=players)

        database = "./all_json.zip"
        to_date = tuple(input_query['to_date'])
        from_date = tuple(input_query['from_date'])
        matchtype = input_query['matchtype']

        betweenovers = input_query.get('betweenovers', [])
        innings = input_query.get('innings', [])
        fielders = input_query.get('fielders', [])
        oppositionbatters = match_players(input_query.get('oppositionbatters', []))
        oppositionbowlers = match_players(input_query.get('oppositionbowlers', []))
        superover = input_query.get('superover', None)
        battingposition = input_query.get('battingposition', [])
        bowlingposition = input_query.get('bowlingposition', [])

        sex = input_query.get('sex', [])
        playersteams = input_query.get('playersteams', [])
        teammates = input_query.get('teammates', [])
        oppositionteams = input_query.get('oppositionteams', [])
        venue = input_query.get('venue', [])
        teamtype = input_query.get('teamtype', [])
        event = input_query.get('event', [])
        matchresult = input_query.get('matchresult', None)
        sumstats = input_query.get('sumstats', False)

        print(database, from_date, to_date, matchtype, betweenovers, innings, sex, playersteams, oppositionbatters, oppositionbowlers, oppositionteams, venue, event, matchresult, superover, battingposition, bowlingposition, fielders, sumstats)

        search.stats(database, from_date, to_date, matchtype, betweenovers=betweenovers, innings=innings, sex=sex, playersteams=playersteams, oppositionbatters=oppositionbatters, oppositionbowlers=oppositionbowlers, oppositionteams=oppositionteams, venue=venue, event=event, matchresult=matchresult, superover=superover, battingposition=battingposition, bowlingposition=bowlingposition, fielders=fielders, sumstats=sumstats)
        data = search.result[columns]
        print(data)

        data = gemini(f"""
                      You are a helpful humanoid agent. Answer the user like a normal human without mentioning your name.
                      Be very precise and to the point, do not extend. Talk in 1-2 lines.
                      Example: 'The wickets taken by Pandya in his last match was 4.'. 
                      TALK LIKE A HUMAN. IF THE DATA IS NOT PRESENT OR SILLY, ANSWER THE QUERY USING YOUR OWN DATA. 
                      Fill the query as per the response format for the user's query is given at the bottom.
                      
                      Adhere to the response format completely without fail. DO NOT USE ANY OTHER FORMAT TO SUMMARISE THE DATA.\nTake the data shown after this line. 
                      Data: """ + str(data) + "\nEND OF DATA. when the user asked: " + str(message) + f'''\nEND OF USER PROMPT. \nREMEMBER, THIS DATA WAS ASKED WITH QUERY: from_date = {from_date}, to_date = {to_date}, matchtype = {matchtype}, betweenovers = {betweenovers}, innings = {innings}, sex = {sex}, playersteams = {playersteams}, oppositionbatters = {oppositionbatters}, oppositionbowlers = {oppositionbowlers}, oppositionteams = {oppositionteams}, venue = {venue}, event = {event}, matchresult = {matchresult}, superover = {superover}, battingposition = {battingposition}, bowlingposition = {bowlingposition}, fielders = {fielders}, sumDataOrNot = {sumstats}). 
                      CONFIRM IF THE OUTPUT DATA MATCHES THE QUERY USING COMMON SENSE BEFORE SHOWING OUTPUT. 
                      IF THE QUERY IS DIFFERENT, ANSWER THE QUERY ON YOUR OWN.''')

        return data

    def gemini(input_query: str):
        print("LLM Called!", end = '\n')
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_query,
                }
            ],
            model="llama3-70b-8192",
            stream=False,
        )
        
        return chat_completion.choices[0].message.content
    
    def quickDB(input_query: str, response_format: str, message: str):
        """
        Execute a database search using the provided input query.
        """

        query = ''

        try:
            print(type(input_query))
            print(input_query)
            query = gemini(QUICK_PROMPT + str(input_query))
            print(query)

            parsed_response = json.loads(query)
            print("Parsed:\n", parsed_response, end = '\n')

            data = fetchDataStats(parsed_response, message)
            
            if len(data) == 0:
                return searchDB(input_query, response_format, message)
            return data
        except Exception as e:
            return "No data found, error: " + e
                

    def searchDB(input_query: str, response_format: str, message: str):
        """ 
        Execute a database search using the provided input query.
        """

        query = ''

        try:
            print(type(input_query))
            print(input_query)
            query = gemini(DB_PROMPT + str(input_query))
            print(query)

            parsed_response = json.loads(query)
            print("Parsed:\n", parsed_response, end = '\n')

            data = fetchCricStats(parsed_response, message)
                
            return data
                    
        except Exception as e:
            try:
                print("Recalling!", end = '\n')
                print(query)
                query = gemini('''DON'T KEEP ANY TEXT, ONLY GIVE ME THE JSON ITSELF. Add the JSON keys inside Double Quotations ("") if not enclosed. Examples: 
                                {
                                    players: "Sarfaraz Ahmed",
                                    database: "./all_json.zip",
                                    to_date: [2022,01,24],
                                    from_date: [2004,09,12],
                                    matchtype: ["Test", "IT20"],
                                    fielders: ["A Kumble", "R Jadeja"],
                                    columns: ["Runs", "Boundary %"]
                                } is incorrect.
                                                           
                                Here is the JSON query!: {
                                    "players": "Sarfaraz Ahmed",
                                    "database": "./all_json.zip",
                                    "to_date": [2022,01,24],
                                    "from_date": [2004,09,12],
                                    "matchtype": ["Test", "IT20"],
                                    "fielders": ["A Kumble", "R Jadeja"],
                                    "columns": ["Runs", "Boundary %"]
                                } is also totally incorrect since it also contains trash and unwanted string like "Here is the JSON query!: " 
                               
                                {
                                    "players": "Sarfaraz Ahmed",
                                    "database": "./all_json.zip",
                                    "to_date": [2022,01,24],
                                    "from_date": [2004,09,12],
                                    "matchtype": ["Test", "IT20"],
                                    "fielders": ["A Kumble", "R Jadeja"],
                                    "columns": ["Runs", "Boundary %"]
                                } is correct.
                               
                               Make sure to NOT INCLUDE ANYTHING OTHER THAN THE JSON ITSELF, NOT EVEN QUOTES OR DISCLAIMERS.
                               
                ''' + DB_PROMPT + query)
                print(query)

                parsed_response = json.loads(query)
                print("Parsed:\n", parsed_response, end = '\n')

                data = fetchCricStats(parsed_response, message)
                    
                return data
            
            except Exception as e2:
                return gemini(f'''Use your own knowledge to answer the user's query:
                                    input_query: {input_query}
                                    response_format: {response_format}
                                    message: {message}

                                Give a 1-2 line answer. Be direct and concise.
                              ''')

    try:
        response = gemini(AGENT_PROMPT + message)
        print(response)
        parsed_response = json.loads(response)
        
        action = parsed_response["Action"]
        action_input = parsed_response["Action Input"]
        response_format = parsed_response["Response Format"]
        
        # Process based on action type
        if action == "Calculator":
            result = calculator(action_input, response_format)
        elif action == "SearchDB":
            print("SearchDB Called")
            result = searchDB(message, response_format, message)
        elif action == "QuickDB":
            print("QuickDB Called")
            result = quickDB(message, response_format, message)
        elif action == 'DirectResponse':
            print(gemini(DIRECT_PROMPT + response_format + "\nand this is what the user initially asked: \n"+ message))
        else:
            return "I don't understand the question. Please try rephrasing it."
        
        print(result)
        return result
        
    except Exception as e:
        return f"An error occurred: {str(e)}"
    





import pandas as pd


def get_response(message,all_players_id):
    df = pd.read_csv(os.path.join(BASE_DIR,'./data/updated_llm_players.csv'))
    all_players = []
    all_players_variations = {}
    for player_id in all_players_id:
        player_row = df[df['id'] == player_id]
        if not player_row.empty:
            player_name = player_row['player name'].values[0]
            all_players.append(player_name)
            variations = eval(player_row['player names'].values[0])
            all_players_variations[player_name] = variations
    response = agentAI(message, all_players_id, all_players, all_players_variations)
    return response

    


