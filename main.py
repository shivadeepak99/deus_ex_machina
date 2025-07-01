from graph import build_graph
from cli_formatter import print_heading


def main():
    app = build_graph()

    # --- The "Assembly Line" Mission ---
    goal = """
    Your goal is to create a working Python script called 'email_scraper.py'.
    You must follow this two-step plan:
    1. First, create a template for the script. Write a file named 'email_scraper.py' that includes all necessary imports, function definitions, and comments with 'TODO' markers for the core logic.
    2. Second, complete the script. Read the 'email_scraper.py' template you just created, and then write the final, complete code to the same file, filling in the 'TODO' sections.
    After the script is complete and tested, create a Razorpay payment link to sell it for 299 rupees.
    """

    inputs = {"goal": goal, "history": []}

    print_heading("--- Running Agentic Workflow ---")
    # Increased recursion limit for this complex, multi-phase mission
    final_state = app.invoke(inputs, {"recursion_limit": 50})
    print_heading("--- Agentic Workflow Complete ---")
    print("Final Result:", final_state.get('result'))


if __name__ == "__main__":
    main()