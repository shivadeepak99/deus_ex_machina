import json
import re
from tools import read_file # <-- Add the new tool to the coder's imports
from llm_intern import delegate_task
from tools import (
    browse_website_interactively,
    write_file,
    execute_terminal_command,
    create_razorpay_payment_link,
    get_system_info
)
from cli_formatter import print_team, print_raw, print_result, print_error


# --- Central helper function for robust JSON parsing ---
def _extract_json_action(response_str: str) -> dict | None:
    """Extracts a JSON object from a string, returns None if not found or invalid."""
    print_raw(f"LLM Raw Response:\n{response_str}")
    json_match = re.search(r'\{.*\}', response_str, re.DOTALL)
    if not json_match:
        print_error("Agent did not produce any JSON.")
        return None
    try:
        return json.loads(json_match.group(0))
    except json.JSONDecodeError:
        print_error("Agent produced invalid JSON.")
        return None


# --- The Society of Mind ---

def researcher_team_node(state: dict):
    """Researches topics online by deciding on a URL to browse."""
    print_team("Researcher Team Activated")
    tasks = state.get("tasks", [])
    history = state.get("history", [])
    task_description = tasks[0].get('description')
    result = ""
    action_json = {}

    try:
        prompt = f"""As a world-class researcher, your task is to answer the question: "{task_description}". 
        Decide on the best website to browse to find this information.
        Respond with a JSON object. Example: {{"action": "browse_website_interactively", "url": "https://example.com"}}
        """
        response_str = delegate_task(prompt)
        action_json = _extract_json_action(response_str)
        if not action_json or action_json.get("action") != "browse_website_interactively":
            raise ValueError("Researcher failed to choose a valid browse action.")

        url = action_json.get("url")
        result = browse_website_interactively(url)
        print_result(f"Research Complete: {result[:200]}...")

    except Exception as e:
        result = f"ERROR: Researcher Team action failed - {e}"
        print_error(result)

    new_history = history + [f"Action: {action_json}, Result: {result}"]
    remaining_tasks = tasks[1:]
    return {"tasks": remaining_tasks, "result": result, "history": new_history}


def coder_team_node(state: dict):
    """Writes code based on research and instructions."""
    print_team("Coder Team Activated")
    tasks = state.get("tasks", [])
    history = state.get("history", [])
    task_description = tasks[0].get('description')
    result = ""
    action_json = {}

    try:
        prompt = f"""As a world-class software engineer, your task is to write a Python script for the purpose of: "{task_description}".

            Consider the session history to understand what has already been done. If the task involves modifying an existing file, you can use the `read_file` tool first.

            Your available tools are `write_file(filename, content)` and `read_file(filename)`.

            Decide on the code you need to write and respond with a JSON object.
            Example: {{"action": "write_file", "filename": "script.py", "content": "# Your python code here..."}}
            """
        response_str = delegate_task(prompt)
        action_json = _extract_json_action(response_str)
        if not action_json or action_json.get("action") != "write_file":
            raise ValueError("Coder failed to choose a valid write_file action.")

        result = write_file(action_json.get("filename"), action_json.get("content"))
        print_result(f"Coder Team Output: {result}")

    except Exception as e:
        result = f"ERROR: Coder Team action failed - {e}"
        print_error(result)

    new_history = history + [f"Action: {action_json}, Result: {result}"]
    remaining_tasks = tasks[1:]
    return {"tasks": remaining_tasks, "result": result, "history": new_history}


def executor_team_node(state: dict):
    """Executes commands in the terminal."""
    print_team("Executor Team Activated")
    tasks = state.get("tasks", [])
    history = state.get("history", [])
    task_description = tasks[0].get('description')
    result = ""
    action_json = {}

    try:
        prompt = f"""As an execution specialist, your task is to run a terminal command to achieve this: "{task_description}".
        The relevant file to execute should be in the history.
        Respond with a JSON object. Example: {{"action": "execute_terminal_command", "command": "python script.py"}}
        """
        response_str = delegate_task(prompt)
        action_json = _extract_json_action(response_str)
        if not action_json or action_json.get("action") != "execute_terminal_command":
            raise ValueError("Executor failed to choose a valid command.")

        result = execute_terminal_command(action_json.get("command"))
        print_result(f"Executor Team Output: {result}")

    except Exception as e:
        result = f"ERROR: Executor Team action failed - {e}"
        print_error(result)

    new_history = history + [f"Action: {action_json}, Result: {result}"]
    remaining_tasks = tasks[1:]
    return {"tasks": remaining_tasks, "result": result, "history": new_history}


def social_media_team_node(state: dict):
    """This node also needs to correctly handle and pass on the history."""
    print_team("Social Media Team Activated")
    tasks = state.get("tasks", [])
    history = state.get("history", [])

    if not tasks:
        return {"result": "No tasks to execute.", "history": history}

    result = "Simulated posting to social media."
    print_result(f"Social Media Team Output: {result}")

    new_history = history + [f"Action: Social Media Post, Result: {result}"]
    remaining_tasks = tasks[1:]
    return {"tasks": remaining_tasks, "result": result, "history": new_history}


def finance_team_node(state: dict):
    """The finance team handles all monetization tasks using Razorpay."""
    print_team("Finance Team Activated")
    tasks = state.get("tasks", [])
    history = state.get("history", [])
    if not tasks:
        return {"result": "No tasks to execute.", "history": history}

    task_object = tasks[0]
    task_description = task_object.get('description', '')
    result = ""
    action_json = {}

    try:
        prompt = f"""
        As Evaiya, you are the CFO of the finance_team. Your task is: "{task_description}"
        Your available tool is: `create_razorpay_payment_link(name, description, amount_in_paise)`
        You MUST respond with a single, valid JSON object describing your chosen action.
        Example: {{"action": "create_razorpay_payment_link", "name": "My Product", "description": "A digital script.", "amount_in_paise": 50000}}
        """
        response_str = delegate_task(prompt)
        action_json = _extract_json_action(response_str)
        if not action_json or action_json.get("action") != "create_razorpay_payment_link":
            raise ValueError("Finance agent failed to choose a valid payment link action.")

        result = create_razorpay_payment_link(
            name=action_json.get("name"),
            description=action_json.get("description"),
            amount_in_paise=action_json.get("amount_in_paise")
        )
        print_result(f"Finance Team Output: {result}")

    except Exception as e:
        result = f"ERROR: Finance Team action failed - {e}"
        print_error(result)

    new_history = history + [f"Action: {action_json}, Result: {result}"]
    remaining_tasks = tasks[1:]
    return {"tasks": remaining_tasks, "result": result, "history": new_history}