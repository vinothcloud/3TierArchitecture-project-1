from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Your DB config
db_config = {
    "host": "fbdb.cpk8oagkgyaz.ap-south-1.rds.amazonaws.com",
    "user": "admin",
    "password": "Admin123#",
    "database": "fbdatabase"
}

@app.route('/login', methods=['POST'])
def login():
    try:
        # Get JSON data from request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password required"}), 400

        # Connect to database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch user by email
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # Compare password directly (plain-text)
        if user and user['password'] == password:
            user.pop('password')  # Remove password from response
            return jsonify(user), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
