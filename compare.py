import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "/Users/fabian.baiersdoerfer/Desktop/ff_data/raw"

results2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_results.csv"), sep=";")
owner2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_owners.csv"), sep=";")

results1 = results2017[["Week", "Type", "TeamA", "TeamAScore"]]
results2 = results2017[["Week", "Type", "TeamB", "TeamBScore"]]

print("Gib' die Namen der beiden Teams ein, die du vergleichen willst!")
input1 = input("Team 1: ")
input2 = input("Team 2: ")

def winner(row):
    if row["TeamAScore"] > row["TeamBScore"]:
        return row["TeamA"]
    elif row["TeamAScore"] < row["TeamBScore"]:
        return row["TeamB"]
    else:
        return "draw"

def teams(row):
    return [row["TeamA"], row["TeamB"]]

def win_margin(row):
    if row["TeamAScore"] > row["TeamBScore"]:
        return row["TeamAScore"] - row["TeamBScore"]
    elif row["TeamAScore"] < row["TeamBScore"]:
        return row["TeamBScore"] - row["TeamAScore"]
    else:
        return 0

def set_winner(row):
    if row["team"] == row["winner"]:
        return True
    else:
        return False

def get_opponent_score(row):
    if row["winner"]:
        return row["score"] - row["margin"]
    elif not row["winner"]:
        return row["score"] + row["margin"]
    else:
        return row["score"]


# print columns of results2017

results2017["winner"] = results2017.apply(winner, axis=1)
results2017["margin"] = results2017.apply(win_margin, axis=1)
results2017["teams"] = results2017.apply(teams, axis=1)

# splitting and reducing the df for concatinating later
teamA = results2017[["Week", "Type", "TeamA", "TeamAScore", "margin", "TeamB", "winner"]]
teamB = results2017[["Week", "Type", "TeamB", "TeamBScore", "margin", "TeamA", "winner"]]

# renaming the columns to concatenate
teamA = teamA.rename(columns={"Week": "week", "TeamA": "team", "TeamAScore": "score", "TeamB": "opponent"})
teamB = teamB.rename(columns={"Week": "week", "TeamB": "team", "TeamBScore": "score", "TeamA": "opponent"})

# concatenation of the two created dataframes
complete = pd.concat([teamA, teamB], sort = False)
complete = complete.sort_values(by = ["week"])
complete["winner"] = complete.apply(set_winner, axis = 1)

# copy to avoid getting the 'SettingwithCopyWarning' error
output = complete.query("team == @input1").copy()
output["opponentScore"] = output.apply(get_opponent_score, axis = 1)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(output)

output2 = complete.query("team == @input2").copy()
output2["opponentScore"] = output2.apply(get_opponent_score, axis = 1)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(output2)

comparison = pd.concat([output, output2], sort = False)

g = sns.relplot(x='week', y='score', hue = "team", kind='line', data=comparison)
plt.show()