from flask import Flask
from flask_session import Session

from views import create_views

from quickbooks_api import auth_url, auth_client

app = Flask(__name__)

# Config
SESSION_TYPE = 'filesystem'
SECRET_KEY = 'random string for secrets'
app.config.from_object(__name__)
Session(app)

# Create the views for the app
views = create_views({
    'url': auth_url,
    'client': auth_client
})

# Register the views
app.register_blueprint(views)

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=5000)
