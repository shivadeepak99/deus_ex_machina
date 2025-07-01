from llm_intern import delegate_task
import json
import re
from config import VALID_TEAMS
from memory_manager import retrieve_memories  # <-- Import memory retrieval
from cli_formatter import print_ceo, print_raw, print_error, print_result


def cognitive_core_node(state: dict):
    """ The CEO node now uses memory to make better plans. """
    goal = state.get("goal")
    print_ceo(f"Processing Goal: {goal}")

    # --- LEVEL 3 UPGRADE: Retrieve relevant memories ---
    relevant_memories = retrieve_memories(goal, num_memories=3)
    memory_context = "\n".join(relevant_memories)
    print_ceo(f"Retrieved memories:\n{memory_context}")

    prompt = f"""
    As Evaiya, take the following high-level goal and break it down into a list of specific, actionable tasks.

    GOAL: "{goal}"

    First, consider these relevant memories from your past experiences:
    <MEMORIES>
    {memory_context}
    </MEMORIES>

    Use these memories to create a better, more informed plan.

    You MUST follow these rules for your response:
    1. Your response MUST include a single, valid JSON structure.
    2. For each task object, you MUST include a key named "assigned_team".
    3. The value for "assigned_team" MUST be one of these exact strings: {VALID_TEAMS}.
    """

    response_text = delegate_task(prompt)
    print_raw(response_text)
    # --- FINAL PARSER: Handles both JSON objects and arrays ---
    json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text)
    if not json_match:
        # Fallback for when there are no code block markers
        json_match = re.search(r'(\[[\s\S]*\]|\{[\s\S]*\})', response_text)

    if not json_match:
        print_error("CEO failed to find any JSON in Evaiya's response.")
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

        print_result(f"CEO successfully extracted tasks: {tasks}")
        return {"tasks": tasks}
    except json.JSONDecodeError as e:
        print(f"ERROR: CEO failed to parse the extracted JSON. String was: {json_string}\nError: {e}")
        return {"tasks": []}
