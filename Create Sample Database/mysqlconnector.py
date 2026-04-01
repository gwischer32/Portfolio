import mysql.connector

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # empty password
    database="SoccerDB"
)

cursor = db.cursor()

def show_players_on_team():
    team_id = input("Enter Team ID to view its players: ")
    
    query = """
    SELECT PlayerID, Name, Position 
    FROM Player 
    WHERE TeamID = %s;
    """
    cursor.execute(query, (team_id,))
    results = cursor.fetchall()

    if results:
        print("\nPlayers on team", team_id)
        for row in results:
            print(row)
    else:
        print("No players found for that team.")

def add_player():
    name = input("Player Name: ")
    position = input("Position: ")
    nationality = input("Nationality: ")
    team_id = input("Team ID: ")

    query = """
    INSERT INTO Player (Name, Position, Nationality, TeamID)
    VALUES (%s, %s, %s, %s);
    """

    cursor.execute(query, (name, position, nationality, team_id))
    db.commit()
    print(f"{name} was added successfully!")

def count_players_by_position():
    query = """
    SELECT Position, COUNT(*) 
    FROM Player 
    GROUP BY Position;
    """
    cursor.execute(query)
    results = cursor.fetchall()

    print("\nPlayers by position:")
    for row in results:
        print(f"{row[0]}: {row[1]}")

# Menu
while True:
    print("\n--- SoccerDB Menu ---")
    print("1. Show players on a team")
    print("2. Add a new player")
    print("3. Show player count by position")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        show_players_on_team()
    elif choice == "2":
        add_player()
    elif choice == "3":
        count_players_by_position()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option. Try again.")
