from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Configure the limiter
limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

@app.route('/api/resource', methods=['GET'])
@limiter.limit("10 per minute")  # Per-minute rate limit for this endpoint
def get_resource():
    return jsonify({"message": "Resource accessed successfully"})

if __name__ == '__main__':
    app.run(debug=True)
