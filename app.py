from flask import Flask, render_template,jsonify,request,Response
from util.db import db, User , Webpage
from config import config
from flask_login import LoginManager
from datetime import datetime
import pytz, requests, os, traceback
from util.functions import tcolor, handle_exception, setup_logging, START_FLAG, STOP_FLAG
from util.helper import safe_import
from util.auth import configure_oauth
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def create_app():
    """Initialize and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config)
    oauth = configure_oauth(app)
    db.init_app(app)

    # Safe imports
    comp = safe_import('routes.compiler', 'comp')
    todo = safe_import('routes.todo', 'todo')
    admin = safe_import('routes.admin_routes', 'admin_routes')


    # Register blueprints
    app.register_blueprint(comp.comp)
    app.register_blueprint(todo.todo)
    app.register_blueprint(admin.admin_routes)

    # Global error handler
    app.register_error_handler(Exception, handle_exception)

    # Setup login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'todo.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Define routes inside create_app
    @app.route('/')
    def index():
        """Handles the home page route."""
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist).strftime('%I:%M %p').lstrip("0")
        formatted_date = datetime.now(ist).strftime('%a, %b %d %p')
        api_key = 'cea78d1d78e04732a47112844250902'  # Your WeatherAPI key
        location = 'Panipat,Haryana'
        api_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no'

        # try:
        #     response = requests.get(api_url)
        #     weather_data = response.json()
        #     temperature_c = weather_data['current']['temp_c']
        # except Exception as e:
        #     temperature_c = 'N/A'
        #     print(f"Error fetching weather data: {e}")
        temperature_c = 4
        page = Webpage.query.filter_by(slug='home').first()
        return render_template('home.html', time=current_time, hometime=formatted_date, temp=temperature_c,page=page)


    TIMEOUT = 60
    CACHE = {}

    @app.route('/proxy')
    def proxy():
        url = request.args.get('url')
        if not url:
            return "URL parameter is required", 400

        try:
            # Return cached response if available
            if url in CACHE:
                return CACHE[url]

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, allow_redirects=True, timeout=TIMEOUT)

            # Get content type
            content_type = response.headers.get("Content-Type", "")

            # Process HTML pages to rewrite URLs
            if "text/html" in content_type:
                soup = BeautifulSoup(response.text, "html.parser")

                for tag in soup.find_all(["a", "link", "script", "img"]):
                    if tag.has_attr("href"):
                        tag["href"] = f"/proxy?url={urljoin(url, tag['href'])}"
                    if tag.has_attr("src"):
                        tag["src"] = f"/proxy?url={urljoin(url, tag['src'])}"

                modified_html = str(soup)
                CACHE[url] = Response(modified_html, content_type="text/html")
                return CACHE[url]

            # Cache and return other content types (CSS, JS, images, etc.)
            CACHE[url] = Response(response.content, content_type=content_type)
            return CACHE[url]

        except requests.exceptions.Timeout:
            return "Request timed out", 504
        except requests.exceptions.RequestException as e:
            return f"Error fetching page: {str(e)}", 500

    return app


def run_app():
    """Runs the Flask app with logging and database setup."""
    setup_logging()
    app = create_app()

    if os.path.exists(STOP_FLAG):
        os.remove(STOP_FLAG)

    with app.app_context():
        db.create_all()
        
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':  # Run only in child process
            if not os.path.exists(START_FLAG):
                open(START_FLAG, 'w').close()
                print(f"{tcolor.GREEN}{tcolor.BOLD}App has been started{tcolor.RESET}")
            else:
                print(f"{tcolor.YELLOW}App has been reloaded{tcolor.RESET}")

    app.run(debug=True)
    
if __name__ == '__main__':
    try:
        run_app()
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)[-1]
        function_name, file_name, line_number = tb.name, tb.filename, tb.lineno
        error_message = (
            f"{tcolor.MAGENTA}Error in function '{function_name}' {tcolor.RESET}"
            f"{tcolor.MAGENTA}(File: {file_name}, Line: {line_number}): {str(e)}{tcolor.RESET}\n"
        )
        print(error_message)  