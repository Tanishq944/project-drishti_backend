from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/crowd-data", methods=["POST"])
def crowd_data():
    data = request.get_json()
    print("📥 Received crowd data:", data)
    # You can store this into a DB here
    return jsonify({"status": "success", "received": data}), 200

if __name__ == "__main__":
    app.run(debug=True)
