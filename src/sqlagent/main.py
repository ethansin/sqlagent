import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv
from jinja2 import Template

from tools.get_table_tool import get_tables_tool
from tools.get_columns_tool import get_columns_tool
from tools.make_query_tool import make_query_tool
from tools.write_script_tool import write_script_tool
from tools.execute_script_tool import execute_script_tool

load_dotenv()

api_key = os.getenv("OPENAI_KEY")

def parse_tool_selection(message: str) -> dict:
    """Extract the tool selection JSON payload from the agent's message."""
    try:
        return json.loads(message)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in payload: {e}") from e

def tool_selector(tool_values: dict, database: str) -> str:
    """Select the appropriate tool based on the tool values provided."""
    if tool_values['tool_name'] == "get_tables":
        return get_tables_tool(database)
    elif tool_values['tool_name'] == "get_columns":
        return get_columns_tool(database, tool_values['input'])
    elif tool_values['tool_name'] == "make_query":
        return make_query_tool(database, tool_values['input'])
    elif tool_values['tool_name'] == "write_script":
        return write_script_tool(tool_values['input'])
    elif tool_values['tool_name'] == "execute_script":
        return execute_script_tool()
    elif tool_values['tool_name'] == "DONE":
        return "DONE"
    else: 
        return "Invalid tool selected. Please check your formatting or the name of the tool you used to verify it matches one in the list of tools."

def agent_loop(initial_message: str, database: str, request: str, model: str = "gpt-5-nano-2025-08-07") -> None:


    with open("src/sqlagent/templates/issue_command.md", "r") as f:
        issue_command_prompt = {
            "role": "system",
            "content": f.read()
        }

    with open("src/sqlagent/templates/explanation.md", "r") as f:
        explanation_template = Template(f.read())
        explanation_prompt_content = explanation_template.render(
            request=request
        )
        explanation_prompt = {
            "role": "system",
            "content": explanation_prompt_content
        }

    client = OpenAI(api_key=api_key)

    messages = [{
        "role": "system",
        "content": initial_message
    }]

    task_status = "IN_PROGRESS"

    first_turn = True

    while task_status != "DONE":

        if first_turn:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
        else:
            response = client.chat.completions.create(
                model=model,
                messages=messages + [explanation_prompt]
            )

        agent_explanation = response.choices[0].message.content
        print(agent_explanation)
        messages.append({
            "role": "assistant",
            "content": agent_explanation
        })

        
        response = client.chat.completions.create(
            model=model,
            messages=messages + [issue_command_prompt]
        )

        agent_turn = response.choices[0].message.content
        print(agent_turn)

        tool_code = parse_tool_selection(agent_turn)
        tool_output = tool_selector(tool_code, database)
        print(tool_output[:200])
        if tool_output == "DONE":
            task_status = "DONE"
        messages.append({
            "role": "system",
            "content": "#TOOL OUTPUT\n" + tool_selector(tool_code, database)
        })
        
    # messages.append({
    #     "role": "user",
    #     "content": "Thanks for working on this. Can you provide the final answer with any relevant data I might need to see?"
    # })

    # final_response = client.chat.completions.create(
    #     model=model,
    #     messages=messages
    # )

    # print(final_response.choices[0].message.content)

    return messages


def sqlagent(request: str, database: str) -> None:

    with open("src/sqlagent/templates/initial.md", "r") as f:
        initial_message_template = Template(f.read())
    
    initial_message = initial_message_template.render(
        database=database,
        request=request
        )
    
    message_log = agent_loop(initial_message, database, request=request, model="gpt-5-nano-2025-08-07")

    with open("bin/sqlagent_message_log.txt", "w") as f:
        for message in message_log:
            f.write(f"{message['role'].upper()}:\n{message['content']}\n\n")

sqlagent("please find the number of rows where the number of slot tags is mismatched with the number of tokens","243hw2.db")
