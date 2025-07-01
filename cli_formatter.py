from rich.console import Console
from rich.theme import Theme

# Define our custom color and style theme
custom_theme = Theme({
    "info": "dim cyan",
    "ceo": "bold magenta",
    "team": "cyan",
    "result": "bold green",
    "memory": "yellow",
    "raw_response": "dim white",
    "error": "bold red"
})

# Create a console object with our theme
console = Console(theme=custom_theme)


# We can create simple wrapper functions to make printing even easier
def print_info(text):
    console.print(text, style="info")


def print_ceo(text):
    console.print(f"🧠 [CEO]: {text}", style="ceo")


def print_team(text):
    console.print(f"👥 [TEAM]: {text}", style="team")


def print_result(text):
    console.print(f"✅ [RESULT]: {text}", style="result")


def print_memory(text):
    console.print(f"💾 [MEMORY]: {text}", style="memory")


def print_raw(text):
    console.print(f"📄 [RAW RESPONSE]:\n{text}", style="raw_response")


def print_error(text):
    console.print(f"❌ [ERROR]: {text}", style="error")


def print_heading(text):
    console.rule(f"[bold green]{text}", style="bold green")