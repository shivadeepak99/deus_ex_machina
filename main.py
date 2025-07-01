from graph import build_graph


def main():
    """
    The entry point for our Deus Ex Machina.
    This builds the agentic graph and runs it with a high-level goal.
    """
    app = build_graph()

    # Define a high-level goal for the agent
    goal = "Develop a simple python script to fetch the weather and then post a tweet about it."

    # The input to the graph is a dictionary
    inputs = {"goal": goal}

    print("\n--- Running Agentic Workflow ---")
    for output in app.stream(inputs, {"recursion_limit": 5}):
        # The stream method lets us see the output of each node as it runs
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value)
        print("\n---\n")
    print("--- Agentic Workflow Complete ---")


if __name__ == "__main__":
    main()