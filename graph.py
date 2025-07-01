from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from cognitive_core import cognitive_core_node
from agent_teams import dev_team_node, social_media_team_node
from config import VALID_TEAMS  # <-- IMPORT FROM OUR NEW CONFIG FILE


class AgentState(TypedDict):
    goal: str
    tasks: List[dict]
    result: str


def router(state: AgentState):
    """ This router is now simple and unbreakable. """
    print("--- ROUTER: Analyzing task ---")
    tasks = state.get("tasks", [])
    if not tasks:
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
    """Builds the agentic graph."""
    workflow = StateGraph(AgentState)

    workflow.add_node("ceo", cognitive_core_node)
    workflow.add_node("dev_team", dev_team_node)
    workflow.add_node("social_media_team", social_media_team_node)

    workflow.set_entry_point("ceo")

    # This line now uses the imported VALID_TEAMS
    workflow.add_conditional_edges("ceo", router, {k: k for k in VALID_TEAMS} | {END: END})

    workflow.add_edge("dev_team", END)
    workflow.add_edge("social_media_team", END)

    app = workflow.compile()
    print("Agentic graph compiled successfully.")
    return app