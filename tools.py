import os
import subprocess
import platform
import razorpay
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright # <-- New Import


WORKSPACE_DIR = "workspace"

# Ensure the workspace directory exists
os.makedirs(WORKSPACE_DIR, exist_ok=True)

# --- LEVEL 6 UPGRADE: The System Info Tool ---
def get_system_info() -> str:
    """A tool to get the current operating system."""
    return f"Operating System: {platform.system()}"
# Define the secure workspace directory

def get_api_key(service_name: str) -> str:
    """A secure tool to get an API key from the environment variables."""
    if service_name.lower() == 'razorpay_id':
        return os.environ.get("RAZORPAY_KEY_ID")
    elif service_name.lower() == 'razorpay_secret':
        return os.environ.get("RAZORPAY_KEY_SECRET")
    else:
        return f"ERROR: No API key found for {service_name}"

def browse_website(url: str) -> str:
    """A tool to browse a website and get its text content."""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, "html.parser")
        return f"Successfully fetched content from {url}. Content: {soup.get_text()[:2000]}" # Truncate for brevity
    except Exception as e:
        return f"ERROR: Failed to browse website - {e}"

def write_file(filename: str, content: str) -> str:
    """A tool that allows the agent to write content to a file in its secure workspace."""
    if ".." in filename:
        return "ERROR: Path traversal is not allowed."

    safe_filename = os.path.basename(filename)
    file_path = os.path.join(WORKSPACE_DIR, safe_filename)

    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote {len(content)} bytes to {file_path}"
    except Exception as e:
        return f"ERROR: Failed to write to file - {e}"


# --- LEVEL 5 UPGRADE: The Terminal Tool ---
def execute_terminal_command(command: str) -> str:
    """
    A tool that allows the agent to execute shell commands within the secure workspace.
    """
    try:
        # Security: Run the command within the specified WORKSPACE_DIR
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=WORKSPACE_DIR,  # This ensures the command runs in the workspace
            check=True
        )
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except subprocess.CalledProcessError as e:
        # This catches errors from the command itself (e.g., command not found, python error)
        return f"COMMAND FAILED WITH ERROR:\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}"
    except Exception as e:
        return f"ERROR: Failed to execute command - {e}"


try:
    razorpay_client = razorpay.Client(
        auth=(os.environ.get("RAZORPAY_KEY_ID"), os.environ.get("RAZORPAY_KEY_SECRET"))
    )
    print("Razorpay client initialized successfully.")
except Exception as e:
    print(f"ERROR: Failed to initialize Razorpay client - {e}")
    razorpay_client = None


def create_razorpay_payment_link(name: str, description: str, amount_in_paise: int) -> str:
    """
    A tool to create a Razorpay payment link for a product.
    Amount must be in the smallest currency unit (e.g., 50000 for ₹500.00).
    """
    if not razorpay_client:
        return "ERROR: Razorpay client not initialized."

    try:
        link = razorpay_client.payment_link.create({
            "amount": amount_in_paise,
            "currency": "INR",  # Assuming Indian Rupees
            "accept_partial": False,
            "description": description,
            "notes": {
                "product_name": name
            }
        })
        return f"Successfully created Razorpay payment link for '{name}': {link['short_url']}"
    except Exception as e:
        return f"ERROR: Failed to create Razorpay payment link - {e}"


def read_file(filename: str) -> str:
    """
    A tool to read the content of a file in the secure workspace.
    """
    if ".." in filename:
        return "ERROR: Path traversal is not allowed."

    safe_filename = os.path.basename(filename)
    file_path = os.path.join(WORKSPACE_DIR, safe_filename)

    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return f"Successfully read content from {file_path}:\n\n{content}"
    except FileNotFoundError:
        return f"ERROR: File not found at {file_path}"
    except Exception as e:
        return f"ERROR: Failed to read file - {e}"
def browse_website_interactively(url: str) -> str:
    """
    A powerful tool to browse a website using a real browser,
    capable of handling JavaScript-heavy sites. Now in non-headless mode!
    """
    try:
        with sync_playwright() as p:
            # --- THE CHANGE IS HERE ---
            # We set headless=False to make the browser visible.
            # slow_mo adds a delay (in milliseconds) to make actions watchable.
            browser = p.chromium.launch(headless=False, slow_mo=500)

            page = browser.new_page()
            page.goto(url, timeout=30000)  # Increased timeout for visual Browse

            # Let the page sit for a moment so you can see it
            page.wait_for_timeout(3000)

            content = page.locator('body').inner_text()

            browser.close()
            # Return a cleaned and truncated summary
            cleaned_content = " ".join(content.split())
            return f"Successfully fetched interactive content from {url}. Content: {cleaned_content[:2500]}"
    except Exception as e:
        return f"ERROR: Failed to browse website interactively - {e}"