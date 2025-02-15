import uuid
import subprocess
import os
import re
from util.db import db,Webpage
from flask import request, jsonify, render_template,blueprints

sessions = {}

comp = blueprints.Blueprint('comp', __name__)

def run_interactive_code(code, session_id, user_input):
    """Executes Python code interactively and handles multiple inputs."""
    try:
        file_name = f"temp_{uuid.uuid4().hex}.py"
        with open(file_name, "w") as f:
            f.write(code)

        process = subprocess.Popen(
            ["python3", file_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        session = sessions.get(session_id, {"code": code, "input": []})

        # **Ensure user input is always a string**
        user_input = "" if user_input is None else str(user_input)
        session["input"].append(user_input)
        sessions[session_id] = session

        # **Send input text properly**
        input_text = "\n".join(session["input"]) + "\n" if session["input"] else None
        stdout, stderr = process.communicate(input=input_text)

        os.remove(file_name)  # Cleanup

        return stdout, stderr
    except subprocess.TimeoutExpired:
        process.kill()
        return "Execution timed out!", ""
    except Exception as e:
        return "", str(e)

@comp.route("/compiler", methods=["GET"])
def compiler_page():
    return render_template('compiler.html')

@comp.route("/compiler", methods=["POST"])
def compiler():
    data = request.json
    code = data.get("code")
    session_id = data.get("session_id")
    user_input = data.get("user_input", "")

    if not code and not session_id:
        return jsonify({"error": "No code provided"}), 400

    if session_id and session_id in sessions:
        # **Continue existing session with user input**
        stdout, stderr = run_interactive_code(code, session_id, user_input)

        if input_is_still_needed(stdout + stderr):
            return jsonify({"output": stdout + stderr, "session_id": session_id})

        # **Clear session when execution completes**
        del sessions[session_id]
        return jsonify({"output": stdout + stderr, "session_id": None})
    else:
        # **Start a new session**
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"code": code, "input": []}

        if requires_input(code):
            first_prompt = extract_first_input_prompt(code)
            return jsonify({"output": first_prompt, "session_id": session_id})

    # **If no input is required, execute immediately**
    stdout, stderr = run_interactive_code(code, session_id, "")

    return jsonify({"output": stdout + stderr, "session_id": None})

def requires_input(code):
    """Detects if the code contains input() statements."""
    return bool(re.search(r'\binput\s*\(', code))

def extract_first_input_prompt(code):
    """Extracts the first input prompt."""
    input_lines = re.findall(r'input\s*\(\s*["\'](.*?)["\']\s*\)', code)
    return input_lines[0] if input_lines else "Enter input:"

def input_is_still_needed(output):
    """Checks if another input is required based on output."""
    return "enter a number" in output.lower() or "again" in output.lower()



