import requests

BASE_URL = "http://127.0.0.1:5000"

def update_server(lobby_code, current_players, lobby_name=None, is_18plus=None):
    """
    Sends a POST request to update server details.
    """
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

def get_servers():
    """
    Sends a GET request to retrieve the list of active servers.
    """
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


def update_server_by_code():
    """
    Prompts the user to input a lobby code and new details to update the corresponding server.
    """
    lobby_code = input("Enter the lobby code of the server you want to update: ")
    new_lobby_name = input("Enter the new lobby name (or press Enter to keep the current name): ")
    current_players = input("Enter the current number of players: ")
    is_18plus_input = input("Is this an 18+ server? (yes/no): ")

    # Convert input values to appropriate types
    try:
        current_players = int(current_players)
    except ValueError:
        print("Invalid input for current players. Please enter a valid number.")
        return

    is_18plus = is_18plus_input.lower() == "yes"

    # Update the server with the new data
    update_server(lobby_code, current_players, lobby_name=new_lobby_name if new_lobby_name else None, is_18plus=is_18plus)


if __name__ == "__main__":
    print("\nRetrieving active servers...")
    get_servers()

    # Prompt the user to update a server
    print("\nUpdating a server by user input...")
    update_server_by_code()

    print("\nRetrieving active servers after updating a server...")
    get_servers()

