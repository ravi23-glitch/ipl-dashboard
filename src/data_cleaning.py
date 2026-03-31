import pandas as pd

def load_data():
    matches = pd.read_csv('data/matches.csv')
    deliveries = pd.read_csv('data/deliveries.csv')
    return matches, deliveries


def clean_matches(matches):

    # 🔹 1. Handle missing values
    matches['winner'] = matches['winner'].fillna('No Result')

    # 🔹 2. Standardize team names
    matches.replace({
        'Delhi Daredevils': 'Delhi Capitals'
    }, inplace=True)

    # 🔹 3. Remove old teams
    invalid_teams = [
        'Rising Pune Supergiant',
        'Gujarat Lions',
        'Kochi Tuskers Kerala'
    ]

    matches = matches[~matches['team1'].isin(invalid_teams)]
    matches = matches[~matches['team2'].isin(invalid_teams)]
    matches = matches[~matches['winner'].isin(invalid_teams)]

    # 🔹 4. Remove duplicates (if any)
    matches = matches.drop_duplicates()

    # 🔹 5. Reset index
    matches = matches.reset_index(drop=True)

    return matches
