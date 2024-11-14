import fal_client
import os
from termcolor import colored
import json
from py_expression_eval import Parser
from gtts import gTTS
from io import BytesIO
from pathlib import Path
from sqlalchemy import create_engine
import sqlite3
import google.generativeai as genai
from typing import Any, List, Tuple, Dict, Union,Optional
import re
from backend.settings import FAL_KEY,GOOGLE_API_KEY,WEATHER_API_KEY
os.environ['FAL_KEY'] = FAL_KEY
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

parser = Parser()



SQL_PROMPT = '''Create me an exact SQL query as a string for the prompt given at the end. Follow these rules strictly:

1. ONLY use the tables and columns explicitly listed below
2. Do NOT reference any tables or columns that are not listed here
3. Return ONLY the raw SQL query with NO markdown formatting, NO code blocks, NO backticks, and NO additional text
4. Do NOT include ```sql, ```, or any other markdown/code formatting
5. Ensure all column and table names exactly match those provided

Example correct response:
SELECT name FROM api_player WHERE id = 1;

Example incorrect responses:
```sql
SELECT name FROM api_player WHERE id = 1;
```
"SELECT name FROM api_player WHERE id = 1;"
`SELECT name FROM api_player WHERE id = 1;`

Default entry type for each table shown after an arrow (->) = (index, column_name, data_type, nullable, default_value, some_flag)

The following tables and their columns are the ONLY ones available for querying:

api_metadata -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'data_version', 'varchar(10)', 0, None, 0),
    (2, 'created', 'date', 0, None, 0),
    (3, 'revision', 'INTEGER', 0, None, 0)
]

api_team -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'name', 'varchar(100)', 0, None, 0)
]

api_matchinfo -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'balls_per_over', 'INTEGER', 0, '6', 0),
    (2, 'city', 'varchar(100)', 0, None, 0),
    (3, 'date', 'date', 0, None, 0),
    (4, 'gender', 'varchar(10)', 0, None, 0),
    (5, 'match_type', 'varchar(10)', 0, None, 0),
    (6, 'team_type', 'varchar(50)', 0, None, 0),
    (7, 'players_data', 'json', 0, None, 0),
    (8, 'match_type_number', 'INTEGER', 0, None, 0),
    (9, 'overs', 'INTEGER', 0, None, 0),
    (10, 'season', 'varchar(20)', 0, None, 0),
    (11, 'venue', 'varchar(100)', 0, None, 0),
    (12, 'player_of_match', 'varchar(100)', 0, None, 0),
    (13, 'team_a_id', 'bigint', 1, None, 0),
    (14, 'team_b_id', 'bigint', 1, None, 0),
    (15, 'toss_decision', 'varchar(10)', 0, None, 0),
    (16, 'toss_winner', 'varchar(100)', 0, None, 0),
    (17, 'target_runs', 'INTEGER', 1, None, 0),
    (18, 'target_overs', 'INTEGER', 1, None, 0),
    (19, 'meta_id', 'bigint', 0, None, 0)
]

api_official -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'match_referee', 'varchar(100)', 1, None, 0),
    (2, 'tv_umpire', 'varchar(100)', 1, None, 0),
    (3, 'umpire', 'varchar(100)', 0, None, 0),
    (4, 'match_info_id', 'bigint', 0, None, 0)
]

api_outcome -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'runs', 'INTEGER', 1, None, 0),
    (2, 'wickets', 'INTEGER', 1, None, 0),
    (3, 'winner', 'varchar(100)', 0, None, 0),
    (4, 'match_info_id', 'bigint', 0, None, 0)
]

api_player -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'name', 'varchar(100)', 0, None, 0),
    (2, 'unique_name', 'varchar(100)', 0, None, 0),
    (3, 'gender', 'varchar(10)', 1, None, 0),
    (4, 'role', 'varchar(50)', 1, None, 0)
]

api_team_players -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'team_id', 'bigint', 0, None, 0),
    (2, 'player_id', 'bigint', 0, None, 0)
]

api_matchinfo_team_a_players -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'matchinfo_id', 'bigint', 0, None, 0),
    (2, 'player_id', 'bigint', 0, None, 0)
]

api_matchinfo_team_b_players -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'matchinfo_id', 'bigint', 0, None, 0),
    (2, 'player_id', 'bigint', 0, None, 0)
]

api_inning -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'team_id', 'bigint', 0, None, 0),
    (2, 'match_info_id', 'bigint', 0, None, 0)
]

api_over -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'over_number', 'INTEGER', 0, None, 0),
    (2, 'inning_id', 'bigint', 0, None, 0)
]

api_delivery -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'batter_id', 'bigint', 0, None, 0),
    (2, 'bowler_id', 'bigint', 0, None, 0),
    (3, 'non_striker_id', 'bigint', 0, None, 0),
    (4, 'batter_runs', 'INTEGER', 0, None, 0),
    (5, 'extras_runs', 'INTEGER', 0, '0', 0),
    (6, 'total_runs', 'INTEGER', 0, None, 0),
    (7, 'over_id', 'bigint', 0, None, 0)
]

api_extra -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'wides', 'INTEGER', 1, None, 0),
    (2, 'legbyes', 'INTEGER', 1, None, 0),
    (3, 'delivery_id', 'bigint', 0, None, 0)
]

api_wicket -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'kind', 'varchar(100)', 0, None, 0),
    (2, 'player_out', 'varchar(100)', 0, None, 0),
    (3, 'delivery_id', 'bigint', 0, None, 0),
    (4, 'fielder_id', 'bigint', 1, None, 0)
]

api_powerplay -> [
    (0, 'id', 'INTEGER', 1, None, 1),
    (1, 'from_over', 'decimal(3,1)', 0, None, 0),
    (2, 'to', 'decimal(3,1)', 0, None, 0),
    (3, 'powerplay_type', 'varchar(10)', 0, None, 0),
    (4, 'match_info_id', 'bigint', 0, None, 0)
]

-------- END OF TABLES
Below is the user prompt'''



def calculator(input: str) -> float:
    """Evaluates mathematical expressions"""
    try:
        return parser.parse(input).evaluate({})
    except Exception as e:
        raise ValueError(f"Error in calculation: {str(e)}")

def searchDB    (input_query: str):
    """
    Execute a database search using the provided input query.
    """
    try:
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            
            handler = fal_client.submit(
                "fal-ai/any-llm",
                arguments={
                    "prompt": SQL_PROMPT + input_query,      
                    "model": "openai/gpt-4o-mini"
                },
            )
            request_id = handler.request_id
            
            status = fal_client.status("fal-ai/any-llm", request_id, with_logs=True)
            result = fal_client.result("fal-ai/any-llm", request_id)
            
            # Extract and clean the SQL query
            sql_query = str(result['output']).strip()
            
            # Remove any extra quotes around the query
            sql_query = sql_query.strip('"\'')
            
            print(f"Executing query: {sql_query}")
            
            # Execute query
            cursor.execute(sql_query)
            data = cursor.fetchall()
            
            return data
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

AGENT_PROMPT = '''
You are a knowledgeable assistant that can handle various types of queries. Analyze the user's query and determine the best way to respond. Follow these steps:

1. First determine what type of information is needed:
   - Database Query (SearchDB): For factual information stored in the database
   - Calculation (Calculator): For mathematical operations
   - Direct Response: For general knowledge or logical reasoning

2. Create a response plan
3. Respond with this exact JSON format:
{
    "Thought": "Your analysis of what needs to be done",
    "Action": "SearchDB or Calculator or DirectResponse",
    "Action Input": "Your SQL query or calculation or None for direct responses",
    "Response Format": {
        "template": "Your response template with placeholders using col0, col1, etc.",
        "style": "default/table/list/detailed",
        "metadata": {
            "column_names": ["optional", "list", "of", "column", "names"],
            "description": "Optional description of the data"
        }
    }
}

Examples:

User: "Is Rohit Sharma male or female?"
{
    "Thought": "Need to check the gender information from the player database",
    "Action": "SearchDB",
    "Action Input": "SELECT name, gender FROM api_player WHERE name LIKE '%Rohit Sharma%'",
    "Response Format": {
        "template": "{col0} is {col1}.",
        "style": "default",
        "metadata": {
            "column_names": ["name", "gender"]
        }
    }
}

User: "Show me the top 5 players by runs"
{
    "Thought": "Need to get top 5 batters and their run totals",
    "Action": "SearchDB",
    "Action Input": "SELECT p.name, SUM(d.batter_runs) as runs FROM api_delivery d JOIN api_player p ON d.batter_id = p.id GROUP BY p.name ORDER BY runs DESC LIMIT 5",
    "Response Format": {
        "template": "Top 5 Run Scorers:\n{table_data}",
        "style": "table",
        "metadata": {
            "column_names": ["Player Name", "Total Runs"]
        }
    }
}

User: "List all teams"
{
    "Thought": "Need to fetch all team names from the database",
    "Action": "SearchDB",
    "Action Input": "SELECT name FROM api_team",
    "Response Format": {
        "template": "Teams:\n{list_data}",
        "style": "list",
        "metadata": {
            "column_names": ["Team Name"]
        }
    }
}

Remember:
- Always use col0, col1, etc. in templates for positional data
- Provide clear column names in metadata when possible
- Use appropriate style for data presentation
- Consider readability and formatting in the response

Begin!
'''
    



def create_table(data: List[Tuple], headers: List[str]) -> str:
    """Creates a formatted table from data"""
    if not data:
        return "No data available"
    
    # Use provided headers or generate default ones
    headers = headers or [f"Column {i+1}" for i in range(len(data[0]))]
    
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in data:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))
    
    # Create header
    header = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    separator = "-" * len(header)
    
    # Create rows
    rows = []
    for row in data:
        formatted_row = " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
        rows.append(formatted_row)
    
    return f"{header}\n{separator}\n" + "\n".join(rows)

def create_list(data: List[Tuple], header: str = None) -> str:
    """Creates a formatted list from data"""
    result = []
    if header:
        result.append(header)
    result.extend(f"- {item[0]}" if isinstance(item, tuple) else f"- {item}" for item in data)
    return "\n".join(result)

def sanitize_input(text: str) -> str:
    """
    Removes or escapes problematic control characters in strings.
    
    Args:
        text: String potentially containing control characters.
    
    Returns:
        Sanitized string.
    """
    # Replace control characters (like newlines, tabs) with empty strings
    return re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)

def format_response(data: Union[List[Tuple], Tuple[Any]], response_format: Dict) -> str:
    """
    Formats the response according to the specified template and style.
    
    Args:
        data: Query results or calculated values.
        response_format: Dictionary containing template, style, and metadata.
    
    Returns:
        Formatted response string.
    """
    if not data:
        return "No data available for this query."

    try:
        # Sanitize response format inputs
        template = sanitize_input(response_format.get("template", "{data}"))
        style = response_format.get("style", "default")
        metadata = {k: sanitize_input(v) if isinstance(v, str) else v for k, v in response_format.get("metadata", {}).items()}
        column_names = metadata.get("column_names", [])

        # Convert single tuple to list of tuples for consistent handling
        if isinstance(data, tuple):
            data = [data]

        # Handle different response styles
        if style == "table":
            table_str = create_table(data, column_names)
            return template.format(table_data=table_str)

        elif style == "list":
            header = metadata.get("description", "")
            list_str = create_list(data, header)
            return template.format(list_data=list_str)

        else:  # default style
            # Create a dictionary with positional keys (col0, col1, etc.)
            result_dict = {}
            row = data[0]  # Use first row for single-row responses
            for i, value in enumerate(row):
                # Format numbers nicely
                if isinstance(value, float):
                    formatted_value = f"{value:.2f}"
                else:
                    formatted_value = str(value)
                result_dict[f"col{i}"] = formatted_value

            # Add any additional metadata if needed
            for key, value in metadata.items():
                if key not in ["column_names", "description"]:
                    result_dict[key] = value

            return template.format(**result_dict)

    except KeyError as e:
        # Return a more helpful error message
        missing_key = str(e).strip("'")
        return f"Error: Missing data for placeholder '{missing_key}'. Available keys: {', '.join(result_dict.keys())}"
    except Exception as e:
        return f"Error formatting response: {str(e)}"

def agentAI(message: str) -> str:
    """Main function to process queries and return responses"""
    try:
        # Get AI response for query analysis
        handler = fal_client.submit(
            "fal-ai/any-llm",
            arguments={
                "prompt": AGENT_PROMPT + message,      
                "model": "openai/gpt-4o-mini"
            }
        )
        
        response = fal_client.result("fal-ai/any-llm", handler.request_id)
        parsed_response = json.loads(response['output'])
        
        action = parsed_response["Action"]
        action_input = parsed_response["Action Input"]
        response_format = parsed_response["Response Format"]
        
        # Process based on action type
        if action == "Calculator":
            result = [(calculator(action_input),)]
        elif action == "SearchDB":
            result = searchDB(action_input)
        else:
            return "I don't understand the question. Please try rephrasing it."
        print(result)
        return result
        
    except Exception as e:
        return f"An error occurred: {str(e)}"