from flask import Flask, jsonify

app = Flask(__name__)

VERSION = "Version 2"

@app.route("/")
def home():
    return f"""
    <html>
      <head><title>Cloud CCA 2</title></head>
      <body>
        <h1>Flask CI/CD Application</h1>
        <h2>{VERSION}</h2>
        <p>Deployed using Jenkins, Docker and Kubernetes.</p>
      </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy", version=VERSION)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)