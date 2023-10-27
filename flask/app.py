from flask import Flask, request, jsonify
import time

class RateLimiter(object):
    def __init__(self, limit=10):
        self.limit = limit
        self.counts = {}

    def allow(self, ip_address):
        if ip_address not in self.counts:
            self.counts[ip_address] = 0

        if self.counts[ip_address] < self.limit:
            self.counts[ip_address] += 1
            return True
        else:
            return False

app = Flask(__name__)

rate_limiter = RateLimiter(limit=10)

@app.route("/")
def index():
    ip_address = request.remote_addr

    if not rate_limiter.allow(ip_address):
        return jsonify({"error": "Too many requests"}), 429

    return jsonify({"message": "Hello, world!"})

@app.route("/rate_limit", methods=["GET", "POST"])
def rate_limit():
    if request.method == "GET":
        return jsonify({"limit": rate_limiter.limit})
    elif request.method == "POST":
        limit = request.json["limit"]

        rate_limiter.limit = limit

        return jsonify({"message": "Rate limit successfully updated!"})

@app.route('/info')
def info():

	resp = {
		'connecting_ip': request.headers['X-Real-IP'],
		'proxy_ip': request.headers['X-Forwarded-For'],
		'host': request.headers['Host'],
		'user-agent': request.headers['User-Agent']
	}

	return jsonify(resp)

@app.route('/flask-health-check')
def flask_health_check():
	return "success"

if __name__ == "__main__":
    app.run(debug=True)
