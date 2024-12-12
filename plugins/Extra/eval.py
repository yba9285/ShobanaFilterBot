import sys
import os
import traceback
from io import StringIO
from pyrogram import Client, filters
from pyrogram.errors import MessageTooLong
from info import ADMINS
import asyncio
import ast

# List of dangerous modules and functions to block
RESTRICTED_FUNCTIONS = [
    "os", "sys", "subprocess", "open", "eval", "exec", "import", "compile", 
    "shutil", "socket", "platform", "traceback", "multiprocessing", "pdb", "requests"
]

# Max execution time (seconds)
MAX_EXECUTION_TIME = 15


# Function to check for dangerous imports
def check_for_restricted_code(code):
    """Check for the presence of dangerous functions or modules in the code."""
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            if any(mod.name in RESTRICTED_FUNCTIONS for mod in node.names):
                return True
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in RESTRICTED_FUNCTIONS:
                    return True
    return False

# Function to safely execute the code
async def aexec(code, client, message):
    """Safely execute Python code."""
    try:
        exec(
            "async def __aexec(client, message): "
            + "".join(f"\n {a}" for a in code.split("\n"))
        )
        return await locals()["__aexec"](client, message)
    except Exception as e:
        return f"Error during execution: {str(e)}"


@Client.on_message(filters.command("eval") & filters.user(ADMINS))
async def executor(client, message):
    """Evaluate Python code safely."""
    try:
        # Get code from the message
        code = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply('Command Incomplete!\nUsage: /eval your_python_code')

    # Check for dangerous code
    if check_for_restricted_code(code):
        return await message.reply("This code contains restricted imports or functions and cannot be executed.")

    # Redirect stdout and stderr to capture the output
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    
    stdout, stderr, exc = None, None, None

    try:
        # Execute the code in a safe async environment with a timeout
        result = await asyncio.wait_for(aexec(code, client, message), timeout=MAX_EXECUTION_TIME)
    except asyncio.TimeoutError:
        result = "Code execution timed out after {} seconds.".format(MAX_EXECUTION_TIME)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    # Prepare the response based on the output captured
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = result

    final_output = f"Output:\n\n<code>{evaluation}</code>"

    # Send the result, and handle large outputs
    try:
        await message.reply(final_output)
    except MessageTooLong:
        with open('eval.txt', 'w+') as outfile:
            outfile.write(final_output)
        await message.reply_document('eval.txt')
        os.remove('eval.txt')

