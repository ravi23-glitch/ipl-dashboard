def create_features(matches):
    
    # Toss advantage
    matches['toss_win'] = (matches['toss_winner'] == matches['winner']).astype(int)

    # Home advantage
    matches['home_advantage'] = (matches['team1'] == matches['venue']).astype(int)

    # Team experience
    team_matches = matches['team1'].value_counts() + matches['team2'].value_counts()

    matches['team1_matches'] = matches['team1'].map(team_matches)
    matches['team2_matches'] = matches['team2'].map(team_matches)

    return matches
