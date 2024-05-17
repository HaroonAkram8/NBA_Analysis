from src.globals import H_ELO_BOOST, START_ELO_RATING

# Reference: https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/

def generate_elo_ratings(latest_elo_ratings: dict, games: list):
    elo_ratings = []
    curr_season_year = games[0][0]

    for game in games:
        season_year, game_id, h_team_id, a_team_id, h_pts, a_pts = game

        if curr_season_year != season_year:
            season_year = curr_season_year
            latest_elo_ratings = new_season_carryover(last_season_elo_ratings=latest_elo_ratings)

        h_wins = h_pts >= a_pts
        mov_winner = abs(h_pts - a_pts)
        h_new_elo = calculate_elo_rating(team_elo=latest_elo_ratings[h_team_id] + H_ELO_BOOST, opp_elo=latest_elo_ratings[a_team_id], won=h_wins, MOV_winner=mov_winner)
        a_new_elo = calculate_elo_rating(team_elo=latest_elo_ratings[a_team_id], opp_elo=latest_elo_ratings[h_team_id] + H_ELO_BOOST, won=not h_wins, MOV_winner=mov_winner)

        latest_elo_ratings[h_team_id] = h_new_elo
        latest_elo_ratings[a_team_id] = a_new_elo

        elo_ratings.append([game_id, h_team_id, a_team_id, h_new_elo, a_new_elo])
    
    return elo_ratings

def new_season_carryover(last_season_elo_ratings: dict, base_elo: float=1505.0):
    new_season_elo_ratings = {}

    for team_id in last_season_elo_ratings.keys():
        new_season_elo_ratings[team_id] = last_season_elo_ratings[team_id] * 0.75 + base_elo * 0.25
    
    return new_season_elo_ratings

def calculate_elo_rating(team_elo: float, opp_elo: float, won: bool, MOV_winner: int):
    # R_i = k * (S_team - E_team + R_(i-1))

    E_ratio = (opp_elo - team_elo) / 400.0
    E_team = 1.0 / (1 + 10 ** E_ratio)

    S_team = 0
    elo_diff = opp_elo - team_elo
    if won:
        S_team = 1
        elo_diff = -1.0 * elo_diff
    
    k = 20.0 * ((MOV_winner + 3) ** 0.8) / (7.5 + 0.006 * elo_diff)

    return k * (S_team - E_team) + team_elo

def set_init_elo(teaminfo: list, default_elo: float=START_ELO_RATING):
    default_elo_ratings = {}

    for team in teaminfo:
        id = team[0]
        default_elo_ratings[id] = default_elo

    return default_elo_ratings