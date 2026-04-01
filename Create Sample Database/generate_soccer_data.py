import random
import datetime

NUM_LEAGUES = 5
NUM_TEAMS = 50
NUM_PLAYERS = 1000
NUM_MATCHES = 20000
NUM_GOALS = 40000

# Utility
def random_date():
    start = datetime.date(2020, 1, 1)
    end = datetime.date(2025, 1, 1)
    delta = end - start
    return (start + datetime.timedelta(days=random.randint(0, delta.days))).isoformat()

# 1. Generate Leagues
with open("data_league.csv", "w") as f:
    for i in range(1, NUM_LEAGUES + 1):
        f.write(f"{i},League_{i},Country_{i},Domestic\n")

# 2. Generate Teams
with open("data_team.csv", "w") as f:
    for i in range(1, NUM_TEAMS + 1):
        league_id = random.randint(1, NUM_LEAGUES)
        f.write(f"{i},Team_{i},City_{i},{league_id}\n")

# 3. Generate Players
with open("data_player.csv", "w") as f:
    positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
    for i in range(1, NUM_PLAYERS + 1):
        team_id = random.randint(1, NUM_TEAMS)
        pos = random.choice(positions)
        f.write(f"{i},Player_{i},{pos},Nation_{i},{team_id}\n")

# 4. Generate Matches
with open("data_matches.csv", "w") as f:
    for i in range(1, NUM_MATCHES + 1):
        date = random_date()
        league_id = random.randint(1, NUM_LEAGUES)
        home = random.randint(1, NUM_TEAMS)
        away = random.randint(1, NUM_TEAMS)
        while home == away:
            away = random.randint(1, NUM_TEAMS)
        f.write(f"{i},{date},{home},{away},{league_id}\n")

# 5. Generate Goals
with open("data_goal.csv", "w") as f:
    for i in range(1, NUM_GOALS + 1):
        match_id = random.randint(1, NUM_MATCHES)
        player_id = random.randint(1, NUM_PLAYERS)
        minute = random.randint(1, 90)
        f.write(f"{i},{match_id},{player_id},{minute}\n")
