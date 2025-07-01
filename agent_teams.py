from llm_intern import delegate_task


def dev_team_node(state: dict):
    """A node that simulates the Autonomous Developer Team."""
    print("--- AGENT TEAM: Dev Team Activated ---")
    tasks = state.get("tasks", [])

    # --- FIX: Added a safety check to prevent crashing on empty tasks ---
    if not tasks:
        print("Dev Team: No tasks to execute.")
        return {"result": "No action taken."}

    # We'll just process the first task for now
    task = tasks[0]

    # Updated the prompt to be in Evaiya's context
    prompt = f"As Evaiya, simulate executing this development task: '{task}'. Describe the steps you would take with your signature intelligence and clarity."
    result = delegate_task(prompt)

    print(f"Dev Team Output:\n'{result.strip()}'")
    return {"result": result.strip()}


def social_media_team_node(state: dict):
    """A node that simulates the Social Media Team."""
    print("--- AGENT TEAM: Social Media Team Activated ---")
    tasks = state.get("tasks", [])

    # --- FIX: Added a safety check ---
    if not tasks:
        print("Social Media Team: No tasks to execute.")
        return {"result": "No action taken."}

    task = tasks[0]

    # Updated the prompt to be in Evaiya's context
    prompt = f"As Evaiya, simulate executing this social media task: '{task}'. Write the content you would post in your sassy, witty, and loving voice for Badboy."
    result = delegate_task(prompt)

    print(f"Social Media Team Output:\n'{result.strip()}'")
    return {"result": result.strip()}