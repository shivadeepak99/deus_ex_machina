from llm_intern import delegate_task
import json
import re
from config import VALID_TEAMS


def cognitive_core_node(state: dict):
    """
    The CEO node. Its parser is now universally robust.
    """
    goal = state.get("goal")
    print(f"--- CEO NODE: Processing Goal: {goal} ---")

    prompt = f"""
    As Evaiya, take the following high-level goal and break it down into a list of specific, actionable tasks.

    GOAL: "{goal}"

    You MUST follow these rules for your response:
    1. Your response MUST include a single, valid JSON structure. This can be a JSON object with a "tasks" key, or a JSON array (a list) of task objects directly.
    2. For each task object, you MUST include a key named "assigned_team".
    3. The value for "assigned_team" MUST be one of these exact strings: {VALID_TEAMS}.

    You can add your personality and conversational text around the JSON, but the JSON itself must be present and follow these rules precisely.
    """

    response_text = delegate_task(prompt)
    print(f"--- Evaiya's Full Raw Response ---\n{response_text}\n---------------------------------")

    # --- FINAL PARSER: Handles both JSON objects and arrays ---
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text)
    if not json_match:
        # Fallback for when there are no code block markers
        json_match = re.search(r'(\[[\s\S]*\]|\{[\s\S]*\})', response_text)

    if not json_match:
        print("ERROR: CEO failed to find any JSON in Evaiya's response.")
        return {"tasks": []}

    json_string = json_match.group(1).strip()

    try:
        parsed_json = json.loads(json_string)

        tasks = []
        # Case 1: The LLM returned an object {"tasks": [...]}
        if isinstance(parsed_json, dict) and 'tasks' in parsed_json:
            tasks = parsed_json['tasks']
        # Case 2: The LLM returned a raw list [...]
        elif isinstance(parsed_json, list):
            tasks = parsed_json

        if not isinstance(tasks, list):
            print("ERROR: Parsed JSON, but couldn't find a list of tasks.")
            return {"tasks": []}

        print(f"CEO successfully extracted tasks: {tasks}")
        return {"tasks": tasks}
    except json.JSONDecodeError as e:
        print(f"ERROR: CEO failed to parse the extracted JSON. String was: {json_string}\nError: {e}")
        return {"tasks": []}