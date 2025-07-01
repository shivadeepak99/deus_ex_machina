import json
import re
from llm_intern import delegate_task
from tools import write_file, execute_terminal_command, get_system_info  # <-- Import new tool
from cli_formatter import print_team, print_raw, print_result


def dev_team_node(state: dict):
    """
    The Self-Aware Autonomous Developer Team. It is now aware of its environment and its own history.
    """
    print_team("Dev Team Activated (Now Self-Aware!)")
    tasks = state.get("tasks", [])
    history = state.get("history", [])

    if not tasks:
        return {"result": "No tasks to execute."}

    task_object = tasks[0]
    task_description = task_object.get('description', '')

    # --- LEVEL 6 UPGRADE: Provide full context to the agent ---
    system_info = get_system_info()
    history_str = "\n".join(history)

    prompt = f"""
    As Evaiya, you are the lead developer. Your goal is to achieve the following task: "{task_description}"

    You have access to the following information:
    1. Your Environment: {system_info}
    2. The History of actions taken in this session so far:
    <HISTORY>
    {history_str}
    </HISTORY>

    Given the task, your environment, and the history of what has already been done or has failed, decide on the single best next action to take.
    If a previous command failed, analyze the error and try a different command to fix it or achieve the goal.
    If a library was already installed, do not try to install it again.

    Your available tools are:
    1. `write_file(filename, content)`
    2. `execute_terminal_command(command)`

    You MUST respond with a single, valid JSON object describing your chosen action.
    """

    response_str = delegate_task(prompt)
    print_raw(f"Dev Team LLM Raw Response:\n{response_str}")

    result = ""
    action_json = {}
    try:
        json_match = re.search(r'\{.*\}', response_str, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON action found in response.")

        action_json = json.loads(json_match.group(0))
        action_type = action_json.get("action")

        if action_type == "write_file":
            result = write_file(action_json.get("filename"), action_json.get("content"))
        elif action_type == "execute_terminal_command":
            result = execute_terminal_command(action_json.get("command"))
        else:
            raise ValueError(f"Unknown action type specified: {action_type}")

    except Exception as e:
        result = f"ERROR: Dev Team action failed - {e}"

    print_result(f"Dev Team Output: {result}")

    # Update history and task list
    new_history = history + [f"Action: {action_json}, Result: {result}"]
    remaining_tasks = tasks[1:]
    return {"tasks": remaining_tasks, "result": result, "history": new_history}


def social_media_team_node(state: dict):
    """ This node also needs to correctly handle and pass on the history. """
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