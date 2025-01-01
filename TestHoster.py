import requests

BASE_URL = "http://127.0.0.1:5000"


def create_server(lobby_code, lobby_name, current_players, max_players, is_18plus):
    payload = {
        "lobby_code": lobby_code,
        "lobby_name": lobby_name,
        "current_players": current_players,
        "max_players": max_players,
        "18plus": is_18plus
    }
    response = requests.post(f"{BASE_URL}/create", json=payload)
    if response.ok:
        print(f"Server '{lobby_name}' created successfully.")
    else:
        print(f"Failed to create server: {response.status_code} - {response.json()}")


def update_server(lobby_code, current_players, lobby_name=None, is_18plus=None):
    payload = {
        "lobby_code": lobby_code,
        "current_players": current_players
    }
    if lobby_name is not None:
        payload["lobby_name"] = lobby_name
    if is_18plus is not None:
        payload["18plus"] = is_18plus

    response = requests.post(f"{BASE_URL}/update", json=payload)
    if response.ok:
        print(f"Server '{lobby_code}' updated successfully.")
    else:
        print(f"Failed to update server: {response.status_code} - {response.json()}")


def close_server(lobby_code):
    payload = {"lobby_code": lobby_code}
    response = requests.post(f"{BASE_URL}/close", json=payload)
    if response.ok:
        print(f"Server '{lobby_code}' closed successfully.")
    else:
        print(f"Failed to close server: {response.status_code} - {response.json()}")


def get_servers():
    response = requests.get(f"{BASE_URL}/servers")
    if response.ok:
        servers = response.json().get('servers', [])
        if servers:
            print("Active servers:")
            for server in servers:
                print(f"- Lobby Name: {server.get('lobby_name', 'Unknown')}, "
                      f"Lobby Code: {server.get('lobby_code', 'N/A')}, "
                      f"Players: {server.get('current_players', 0)}/{server.get('max_players', 0)}, "
                      f"18+: {'Yes' if server.get('18plus', False) else 'No'}")
        else:
            print("No active servers.")
    else:
        print(f"Failed to retrieve servers: {response.status_code} - {response.json()}")


if __name__ == "__main__":
    print("Creating test servers...")
    create_server("CODE11", "Test Lobby0", 4, 12, is_18plus=False)
    create_server("CODE12", "Test Lobby1", 2, 12, is_18plus=True)
    create_server("CODE13", "Test Lobby2", 0, 12, is_18plus=False)

    print("\nUpdating the test server (CODE12)...")
    update_server("CODE12", 5, lobby_name="Updated Test Lobby1", is_18plus=False)

    print("\nRetrieving active servers after update...")
    get_servers()
