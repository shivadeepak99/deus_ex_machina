from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from cognitive_core import cognitive_core_node
from agent_teams import dev_team_node, social_media_team_node
from config import VALID_TEAMS
from memory_manager import save_memory
from cli_formatter import print_info, print_heading, print_memory
VALID_TEAMS = ["dev_team", "social_media_team"]
# ... (VALID_TEAMS definition) ...

class AgentState(TypedDict):
    goal: str
    tasks: List[dict]
    history: List[str] # <-- The new short-term memory scratchpad
    result: str

def save_memory_node(state: dict):
    """A node that saves the result of a team's work to long-term memory."""
    goal = state.get("goal")
    result = state.get("result")
    if result and not result.startswith("ERROR"):
        memory_to_save = f"For the goal '{goal}', the result of one step was: {result}"
        save_memory(memory_to_save)
    # We must pass the history through to the next state
    return {"history": state.get("history", [])}
# The single source of truth for our valid teams



def router(state: AgentState):
    """ The router now decides whether to continue the loop or end. """
    print_info("\n" + "="*50)
    print_info("--- ROUTER: Analyzing state ---")
    tasks = state.get("tasks", [])
    if not tasks:
        print_info("Router -> All tasks complete. Ending workflow.")
        return END

    task_object = tasks[0]
    print(f"Router read task: '{task_object.get('task')}'")
    assigned_team = task_object.get("assigned_team")

    if assigned_team in VALID_TEAMS:
        print(f"Router -> Valid team found: '{assigned_team}'. Routing.")
        return assigned_team
    else:
        print(f"Router -> Invalid or no team specified: '{assigned_team}'. Ending.")
        return END


def build_graph():
    """Builds the agentic graph with the main execution loop."""
    workflow = StateGraph(AgentState)

    workflow.add_node("ceo", cognitive_core_node)
    workflow.add_node("dev_team", dev_team_node)
    workflow.add_node("social_media_team", social_media_team_node)
    workflow.add_node("save_memory", save_memory_node)

    workflow.set_entry_point("ceo")

    # This is the initial routing from the CEO's plan
    workflow.add_conditional_edges("ceo", router, {k: k for k in VALID_TEAMS} | {END: END})

    # After a team acts, save the result to memory
    workflow.add_edge("dev_team", "save_memory")
    workflow.add_edge("social_media_team", "save_memory")

    # --- THE FIX: After saving the memory, make another routing decision ---
    # This creates the main loop, sending the flow back to the router
    # to pick up the next task.
    workflow.add_conditional_edges("save_memory", router, {k: k for k in VALID_TEAMS} | {END: END})

    app = workflow.compile()
    print_heading("Agentic graph compiled successfully.")
    return app