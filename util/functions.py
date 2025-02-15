import os,traceback,sys,logging
import atexit,traceback
from functools import wraps
from flask import jsonify,render_template
from datetime import datetime

class tcolor:
    BLACK   = "\033[0;30m"   # Black
    RED     = "\033[0;31m"   # Red
    GREEN   = "\033[0;32m"   # Green
    YELLOW  = "\033[0;33m"   # Yellow
    BLUE    = "\033[0;34m"   # Blue
    MAGENTA = "\033[0;35m"   # Magenta
    CYAN    = "\033[0;36m"   # Cyan
    WHITE   = "\033[0;37m"   # White

    # Bright versions
    BBLACK  = "\033[0;90m"   # Bright Black (Gray)
    BRED    = "\033[0;91m"   # Bright Red
    BGREEN  = "\033[0;92m"   # Bright Green
    BYELLOW = "\033[0;93m"   # Bright Yellow
    BBLUE   = "\033[0;94m"   # Bright Blue
    BMAGENTA= "\033[0;95m"   # Bright Magenta
    BCYAN   = "\033[0;96m"   # Bright Cyan
    BWHITE  = "\033[0;97m"   # Bright White

    RESET   = "\033[0m"      # Reset to default

    B_BLACK   = "\033[40m"   # Black background
    B_RED     = "\033[41m"   # Red background
    B_GREEN   = "\033[42m"   # Green background
    B_YELLOW  = "\033[43m"   # Yellow background
    B_BLUE    = "\033[44m"   # Blue background
    B_MAGENTA = "\033[45m"   # Magenta background
    B_CYAN    = "\033[46m"   # Cyan background
    B_WHITE   = "\033[47m"   # White background

    # Bright background versions (some terminals may not support these)
    BB_BLACK   = "\033[100m"  # Bright Black background
    BB_RED     = "\033[101m"  # Bright Red background
    BB_GREEN   = "\033[102m"  # Bright Green background
    BB_YELLOW  = "\033[103m"  # Bright Yellow background
    BB_BLUE    = "\033[104m"  # Bright Blue background
    BB_MAGENTA = "\033[105m"  # Bright Magenta background
    BB_CYAN    = "\033[106m"  # Bright Cyan background
    BB_WHITE   = "\033[107m"  # Bright White background

    BOLD    = "\033[1m"    # Bold
    FAINT   = "\033[2m"    # Faint (dim)
    ITALIC  = "\033[3m"    # Italic
    UNDERLINE = "\033[4m"    # Underline
    BLINK   = "\033[5m"    # Blink (may not be supported)
    REVERSE = "\033[7m"    # Reverse (swap foreground and background)
    STRIKETHROUGH = "\033[9m" # Strikethrough

    RESET   = "\033[0m"      # Reset to default


STOP_FLAG = 'FLAG_APP_STOPPED'
START_FLAG = 'FLAG_APP_STARTED'

@atexit.register
def stopping():
    """ Ensure stopping only runs once and cleans up properly. """
    # Only execute in the main process
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return  

    if os.path.exists(STOP_FLAG):
        return  # Avoid duplicate stop messages

    print(f"{tcolor.RED}{tcolor.BOLD} App has been stopped{tcolor.RESET}")

    try:
        if os.path.exists(START_FLAG):
            os.remove(START_FLAG)  # Remove start flag

        # Mark as stopped
        open(STOP_FLAG, 'w').close()
    except Exception as e:
        print(f"{tcolor.YELLOW}Error during cleanup: {e}{tcolor.RESET}")
# Ensure logs directory exists

log_dir = "Log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, "error.log")

def handle_exception(e):
    """Handles exceptions globally, logs errors, and displays a simple message."""
    tb = traceback.extract_tb(e.__traceback__)  # Get traceback details
    if tb:
        last_trace = tb[-1]  # Get the last traceback entry (most recent error)
        function_name = last_trace.name  # Function name
        file_name = last_trace.filename  # File where error occurred
        line_number = last_trace.lineno  # Line number where error occurred
    else:
        function_name = "Unknown"
        file_name = "Unknown"
        line_number = "Unknown"

    # Generate error message
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = (
        f"{tcolor.MAGENTA}[{timestamp}] Error in function '{function_name}' {tcolor.RESET}"
        f"{tcolor.MAGENTA}(File: {file_name}, Line: {line_number}): {str(e)}{tcolor.RESET}\n"
    )

    error_message_plain = (
        f"[{timestamp}] Error in function '{function_name}' "
        f"(File: {file_name}, Line: {line_number}): {str(e)}\n"
    )

    # Log error to terminal
    print(error_message)

    # Append error to log file
    with open(log_file, "a") as f:
        f.write(error_message_plain)

    # Return a simple response (no JSON)
    return render_template("error.html", log_file=log_file), 500


def timetaken(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        duration = end - start
        print(f"{tcolor.MAGENTA}Time taken to execute {func.__name__}: {duration} {tcolor.RESET}\n")
        return result
    return wrapper

def setup_logging():
    """ Configure logging in a separate function """
    log_dir = 'Log'
    log_file = os.path.join(log_dir, 'app.log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )