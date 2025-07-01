from graph import build_graph
from cli_formatter import print_heading


def main():
    app = build_graph()

    goal = "Develop a simple python script to fetch the weather and then post a tweet about it."

    # --- LEVEL 6 UPGRADE: Initialize the state with an empty history ---
    inputs = {"goal": goal, "history": []}

    print_heading("--- Running Agentic Workflow ---")
    final_state = app.invoke(inputs, {"recursion_limit": 15})
    print_heading("--- Agentic Workflow Complete ---")
    print("Final Result:", final_state.get('result'))


if __name__ == "__main__":
    main()