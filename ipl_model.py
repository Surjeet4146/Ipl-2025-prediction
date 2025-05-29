import numpy as np

# Team stats based on IPL 2025 data
teams = {
    "RCB": {"points": 19, "nrr": 0.301, "recent_wins": 3, "defensive": (0.35, 0.60), "aggressive": (0.35, 0.50), "boundary": (0.30, 0.40)},
    "PBKS": {"points": 19, "nrr": 0.372, "recent_wins": 4, "defensive": (0.40, 0.62), "aggressive": (0.30, 0.52), "boundary": (0.30, 0.42)},
    "GT": {"points": 18, "nrr": 0.254, "recent_wins": 3, "defensive": (0.45, 0.60), "aggressive": (0.30, 0.50), "boundary": (0.25, 0.40)},
    "MI": {"points": 16, "nrr": 1.142, "recent_wins": 2, "defensive": (0.30, 0.58), "aggressive": (0.40, 0.53), "boundary": (0.30, 0.43)}
}

# Simulate a single match
def simulate_match(team1, team2):
    # Possessions and wickets
    possessions = min(120, int(np.random.normal(120, 10)))
    wickets_t1 = min(10, max(0, int(np.random.normal(6, 1))))
    wickets_t2 = min(10, max(0, int(np.random.normal(6, 1))))
    balls_t1 = min(possessions, 120 - wickets_t1 * 10)
    balls_t2 = min(possessions, 120 - wickets_t2 * 10)

    # Home advantage (randomly assign)
    home_team = np.random.choice([team1, team2])
    home_boost = 0.01 if home_team == team1 else -0.01

    # Simulate runs for team 1
    runs_t1, success_rate_t1 = 0, 0
    for _ in range(balls_t1):
        shot = np.random.choice(["defensive", "aggressive", "boundary"], p=[teams[team1][shot][0] for shot in ["defensive", "aggressive", "boundary"]])
        base_success = teams[team1][shot][1] + (home_boost if team1 == home_team else 0) + success_rate_t1
        if np.random.random() < base_success:
            runs = 2 if shot == "defensive" else 4 if shot == "aggressive" else 6
            runs_t1 += runs
            success_rate_t1 += 0.01
        else:
            success_rate_t1 -= 0.01

    # Simulate runs for team 2
    runs_t2, success_rate_t2 = 0, 0
    for _ in range(balls_t2):
        shot = np.random.choice(["defensive", "aggressive", "boundary"], p=[teams[team2][shot][0] for shot in ["defensive", "aggressive", "boundary"]])
        base_success = teams[team2][shot][1] + (home_boost if team2 == home_team else 0) + success_rate_t2
        if np.random.random() < base_success:
            runs = 2 if shot == "defensive" else 4 if shot == "aggressive" else 6
            runs_t2 += runs
            success_rate_t2 += 0.01
        else:
            success_rate_t2 -= 0.01

    return team1 if runs_t1 > runs_t2 else team2

# Simulate playoffs
def simulate_playoffs(num_simulations=10000):
    eliminator_wins = {"GT": 0, "MI": 0}
    qualifier2_wins = {"PBKS": 0, "GT": 0, "MI": 0}
    final_wins = {"RCB": 0, "PBKS": 0, "GT": 0, "MI": 0}

    for _ in range(num_simulations):
        # Eliminator: GT vs MI
        elim_winner = simulate_match("GT", "MI")
        eliminator_wins[elim_winner] += 1

        # Qualifier 2: PBKS vs Eliminator winner
        q2_opponent = elim_winner
        q2_winner = simulate_match("PBKS", q2_opponent)
        qualifier2_wins[q2_winner] += 1

        # Final: RCB vs Qualifier 2 winner
        final_winner = simulate_match("RCB", q2_winner)
        final_wins[final_winner] += 1

    # Calculate probabilities
    elim_probs = {team: wins/num_simulations for team, wins in eliminator_wins.items()}
    q2_probs = {team: wins/num_simulations for team, wins in qualifier2_wins.items()}
final_probs = {team: wins/num_simulations for team, wins in final_wins.items()}

    print("Eliminator Probabilities:", elim_probs)
    print("Qualifier 2 Probabilities:", q2_probs)
    print("Tournament Win Probabilities:", final_probs)

# Run the simulation
simulate_playoffs()