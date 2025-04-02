from flask import Flask, redirect, request, url_for, session, render_template, send_from_directory, jsonify
from authlib.integrations.flask_client import OAuth
import os
import json
import jwt
import datetime
import requests
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import secrets
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, Identity, AnonymousIdentity, identity_changed
from jwt.algorithms import RSAAlgorithm

# Function to load credentials from JSON file
def load_credentials(filename='creds.json'):
    """Load credentials from a JSON file and return as a dictionary."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        return {}

# Load credentials
creds = load_credentials('creds.json')

app = Flask(__name__)

# Add a secret key for session management and JWT signing
app.secret_key = creds.get('SECRET_KEY', secrets.token_hex(16))
jwt_secret = creds.get('JWT_SECRET', secrets.token_hex(32))

# Okta configuration
OKTA_DOMAIN = creds.get('OKTA_DOMAIN', '')
JWKS_URL = f'https://{OKTA_DOMAIN}/oauth2/default/v1/keys'
AUDIENCE = 'api://default'
ISSUER = f'https://{OKTA_DOMAIN}/oauth2/default'

# Initialize Principal for RBAC
principals = Principal(app)

# Define roles and permissions
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))

# Configure OAuth with explicit OAuth 2.0 parameters
oauth = OAuth(app)
oauth.register(
    name='okta',
    client_id=creds.get('CLIENT_ID', ''),
    client_secret=creds.get('CLIENT_SECRET', ''),
    server_metadata_url=f'https://{OKTA_DOMAIN}/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'response_type': 'code',
        'nonce': lambda: session.get('nonce')
    }
)

# Set up MongoDB connection
mongo_uri = "mongodb://localhost:27017/auth_app"
client = MongoClient(mongo_uri)
db = client.auth_app  # Database name
users = db.users  # Collection name

# Create unique index on username and email
try:
    users.create_index([('username', 1)], unique=True)
    users.create_index([('email', 1)], unique=True)
except Exception as e:
    print(f"Warning: Could not create indexes: {e}")

# Fetch the JWKS from Okta
def get_jwks():
    response = requests.get(JWKS_URL)
    if response.status_code != 200:
        raise Exception('Failed to fetch JWKS from Okta')
    return response.json()

# Get the public key for a given 'kid' from the JWKS
def get_public_key(jwks, kid):
    for key in jwks['keys']:
        if key['kid'] == kid:
            return RSAAlgorithm.from_jwk(key)
    raise Exception(f'Public key with kid {kid} not found')

# Verify the JWT token
def verify_jwt(token):
    try:
        # Decode the JWT to extract the header and get the 'kid'
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header is None:
            raise Exception('Invalid JWT')

        # Get the 'kid' from the JWT header
        kid = unverified_header.get('kid')
        if not kid:
            raise Exception('Missing kid in JWT header')

        # Fetch the JWKS
        jwks = get_jwks()

        # Get the public key corresponding to the 'kid'
        public_key = get_public_key(jwks, kid)

        # Decode and verify the JWT using the public key
        decoded_token = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=AUDIENCE,
            issuer=ISSUER
        )

        return decoded_token  # Return the decoded token if valid
    except Exception as e:
        return str(e)  # Return the error message if verification fails

# Setup identity loader
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = session.get('user')

    # Add the UserNeed to the identity
    if hasattr(identity, 'user'):
        # Add the role based on the user type
        if identity.user and identity.user.get('is_admin', False):
            identity.provides.add(RoleNeed('admin'))
        if identity.user:
            identity.provides.add(RoleNeed('user'))

# Token authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # Extract token from "Bearer <token>"
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token
            data = jwt.decode(token, jwt_secret, algorithms=["HS256"])
            # Get user from MongoDB
            current_user = users.find_one({'_id': data['user_id']})
            if not current_user:
                return jsonify({'message': 'Invalid token',
                                'current_user':current_user,
                                'isAdmin':users.find_one({'_id': data['is_admin']})}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        # Set current_user for the route
        return f(current_user, *args, **kwargs)

    return decorated

# Admin token check decorator
def admin_token_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        # Check if the user is an admin
        if not current_user.get('is_admin', False):
            return jsonify({'message': 'Admin privilege required!'}), 403

        return f(current_user, *args, **kwargs)

    return decorated

# Login required decorator for web views
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator for web views
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not admin_permission.can():
            return render_template('unauthorized.html'), 403
        return f(*args, **kwargs)
    return decorated_function

# New API endpoint for authentication - returns token
@app.route('/api/auth', methods=['POST'])
def auth_api():
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Missing username or password!'}), 400

    username = auth.get('username')
    password = auth.get('password')

    # Find user in database
    user = users.find_one({'username': username})

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    # Create JWT token with expiration
    token_payload = {
        'user_id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'is_admin': user.get('is_admin', False),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }

    token = jwt.encode(token_payload, jwt_secret, algorithm="HS256")
    print(f"Generated Token for {user['username']}: {token}")

    return jsonify({
        'token': token,
        'user': {
            'username': user['username'],
            'email': user['email'],
            'is_admin': user.get('is_admin', False)
        }
    })

# Hello World API requiring admin privileges
@app.route('/api/hello', methods=['GET'])
@token_required
@admin_token_required
def hello_api(current_user):
    return jsonify({
        'message': 'Hello, Admin!',
        'user': current_user['username']
    })

# Protected API endpoint accessible by any authenticated user
@app.route('/api/user-info', methods=['GET'])
@token_required
def user_info_api(current_user):
    return jsonify({
        'username': current_user['username'],
        'email': current_user['email'],
        'is_admin': current_user.get('is_admin', False)
    })

# Home route - redirects to appropriate dashboard
@app.route('/')
@login_required
def home():
    user = session.get('user', {})
    if user.get('is_admin', False):
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

# Normal authentication flow
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        is_admin = request.form.get('is_admin') == 'on'  # Checkbox for admin role

        # Basic validation
        if not username or not email or not password:
            return render_template('signup.html', error="All fields are required")

        # Hash password
        password_hash = generate_password_hash(password)

        # Store user in MongoDB with role
        try:
            user_id = users.insert_one({
                'username': username,
                'email': email,
                'password': password_hash,
                'is_admin': is_admin,
                'is_normal_user': True # Flag to indicate regular user
            }).inserted_id

            return redirect(url_for('signin'))
        except Exception as e:
            error_msg = "Username or email already exists"
            if "duplicate key error" not in str(e):
                error_msg = f"Registration error: {str(e)}"
            return render_template('signup.html', error=error_msg)

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate credentials with MongoDB
        user = users.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            # Create session for user
            user_data = {
                'id': str(user['_id']),
                'name': user['username'],
                'email': user['email'],
                'is_admin': user.get('is_admin', False),
                'is_normal_user': user.get('is_normal_user', True)
            }
            session['user'] = user_data

            # Tell Flask-Principal the identity changed
            identity_changed.send(app, identity=Identity(user_data['id']))

            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')

# Separate Okta SSO flow with no database user creation
@app.route('/login-okta')
def login_okta():
    # Generate and store a nonce value for OIDC authentication
    session['nonce'] = secrets.token_urlsafe(16)
    # Initialize the OAuth state
    redirect_uri = url_for('callback', _external=True)
    return oauth.okta.authorize_redirect(redirect_uri)



@app.route('/auth/callback')
def callback():
    try:
        print("Callback received")
        print(f"Request args: {request.args}")

        # Process the callback - simplified as requested
        token = oauth.okta.authorize_access_token()
        user_info = oauth.okta.userinfo()

        # Store user info in session
        session['user'] = user_info

        # Redirect to dashboard
        return redirect(url_for('home'))
    except Exception as e:
        error_details = str(e)
        print(f"Authentication error: {error_details}")

        # Simple error handling
        return f"Error during authentication: {error_details}. <a href='{url_for('login_okta')}'>Try again</a>"


@app.route('/logout')
def logout():
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app, identity=AnonymousIdentity())

    # Get id_token before clearing the session
    id_token = session.get('okta_id_token')

    # Clear the Flask session for both authentication methods
    session.clear()

    # Check if this was an Okta login by looking for Okta-specific session data
    if id_token:
        # Get the Okta logout URL
        okta_logout_url = f"{OKTA_DOMAIN}/oauth2/default/v1/logout?id_token_hint={id_token}&post_logout_redirect_uri=http://localhost:8000"

        # Redirect to Okta's logout endpoint
        return redirect(okta_logout_url)
    else:
        # For regular authentication, just redirect to signin page
        return redirect(url_for('signin'))

# User dashboard
@app.route('/dashboard/user')
@login_required
def user_dashboard():
    user = session.get('user', {})
    return render_template('user_dashboard.html', user=user)

# Admin dashboard
@app.route('/dashboard/admin')
@login_required
@admin_required
def admin_dashboard():
    user = session.get('user', {})
    return render_template('admin_dashboard.html', user=user)

# Unauthorized page
@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html'), 403

@app.route('/hello-auth', methods=['GET'])
def hello_world():
    # Get the Authorization token from the header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    # Extract the token from the header (the format is "Bearer <token>")
    token = auth_header.split(" ")[1]

    # Verify the JWT token
    result = verify_jwt(token)  # Only one value will be returned, either the decoded token or an error message
    if isinstance(result, str):  # If it's a string, then it's an error message
        return jsonify({"error": result}), 401

    # result['scope'] != 'scope' returns 401
    # result['scope'] == 'scope' returns 200
    if 'role' in result and 'Custom Group' in result['role']:
        return jsonify({"message": "Hello, World!", "user": result['sub']}), 200
    else:
        return jsonify({"message":"User is unauthorized","user":None}),401

    # If JWT is valid, return Hello World
    # return jsonify({"message": "Hello, World!", "user": result['role']}), 200

@app.route('/hello-cc', methods=['GET'])
def hello_world_cc():
    # Get the Authorization token from the header
    auth_header = request.headers.get('Authorization')
    scope = request.headers.get('Scope')
    if not auth_header:
        return jsonify({"error": "Authorization header missing"}), 401

    # Extract the token from the header (the format is "Bearer <token>")
    token = auth_header.split(" ")[1]

    # Verify the JWT token
    result = verify_jwt(token)  # Only one value will be returned, either the decoded token or an error message
    if isinstance(result, str):  # If it's a string, then it's an error message
        return jsonify({"error": result}), 401

    # result['scope'] != 'scope' returns 401
    # result['scope'] == 'scope' returns 200
    if 'scp' in result:
        if scope in result['scp']:
            return jsonify({"message": "Hello, World!"}), 200
        else:
            return jsonify({"message": "Scope not in Client"}), 401
    else:
        return jsonify({"message":"User is unauthorized","user":None}),403

if __name__ == '__main__':
    # Check if credentials were loaded for Okta (only needed for SSO)
    if not creds.get('OKTA_DOMAIN') or not creds.get('CLIENT_ID') or not creds.get('CLIENT_SECRET'):
        print("WARNING: Missing Okta credentials. SSO login will not work.")
        print("Required variables: OKTA_DOMAIN, CLIENT_ID, CLIENT_SECRET")

    # Test MongoDB connection
    try:
        client.admin.command('ping')
        print("MongoDB connection successful")
    except Exception as e:
        print(f"ERROR: MongoDB connection failed: {e}")
        print("Please check your MongoDB connection")
        exit(1)

    app.run(host='0.0.0.0', port=8000, debug=True)