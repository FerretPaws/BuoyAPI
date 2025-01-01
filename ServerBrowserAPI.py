import os
import sys


sys.path.insert(0, os.path.dirname(__file__))


from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

# In-memory storage for server instances
server_list = []

# Lock to handle thread-safety for the server list
lock = threading.Lock()


@app.route('/create', methods=['POST'])
def create_server():
    """
    Endpoint to create a new server instance.
    Expected JSON: { "lobby_code": str, "lobby_name": str, "current_players": int, "max_players": int, "18plus": bool }
    """
    data = request.json

    # Validate input
    required_keys = ['lobby_code', 'lobby_name', 'current_players', 'max_players', '18plus']
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data['18plus'], bool):
        return jsonify({"error": "The '18plus' field must be a boolean"}), 400

    with lock:
        # Check if a server with the same lobby_code already exists
        if any(server['lobby_code'] == data['lobby_code'] for server in server_list):
            return jsonify({"error": "Lobby code already exists"}), 400

        # Add the new server
        server_list.append({
            "lobby_code": data['lobby_code'],
            "lobby_name": data['lobby_name'],
            "current_players": data['current_players'],
            "max_players": data['max_players'],
            "18plus": data['18plus']
        })

    return jsonify({"message": "Server created successfully"}), 201

@app.route('/update', methods=['POST'])
def update_server():
    """
    Endpoint to update server information.
    Expected JSON: { "lobby_code": str, "current_players": int, "lobby_name": str (optional), "18plus": bool (optional) }
    """
    data = request.json

    # Validate input
    if 'lobby_code' not in data or 'current_players' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    if '18plus' in data and not isinstance(data['18plus'], bool):
        return jsonify({"error": "The '18plus' field must be a boolean"}), 400

    with lock:
        # Find the server by lobby_code
        for server in server_list:
            if server['lobby_code'] == data['lobby_code']:
                # Update fields
                server['current_players'] = data['current_players']
                if 'lobby_name' in data:
                    server['lobby_name'] = data['lobby_name']
                if '18plus' in data:
                    server['18plus'] = data['18plus']
                return jsonify({"message": "Server updated successfully"}), 200

        return jsonify({"error": "Lobby code does not exist"}), 404

@app.route('/close', methods=['POST'])
def close_server():
    """
    Endpoint to close a server instance.
    Expected JSON: { "lobby_code": str }
    """
    data = request.json

    # Validate input
    if 'lobby_code' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    with lock:
        # Find and remove the server by lobby_code
        for i, server in enumerate(server_list):
            if server['lobby_code'] == data['lobby_code']:
                del server_list[i]
                return jsonify({"message": "Server closed successfully"}), 200

        return jsonify({"error": "Lobby code does not exist"}), 404


@app.route('/servers', methods=['GET'])
def get_servers():
    """
    Endpoint to retrieve the list of active servers.
    """
    with lock:
        return jsonify({"servers": server_list}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'It works!\n'
    version = 'Python %s\n' % sys.version.split()[0]
    response = '\n'.join([message, version])
    return [response.encode()]