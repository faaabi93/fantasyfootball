import pandas as pd
from os import path
import matplotlib.pyplot as plt

DATA_DIR = "/Users/fabian.baiersdoerfer/Desktop/ff_data/raw"

results2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_results.csv"), sep=";")
owner2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_owners.csv"), sep=";")

results1 = results2017[["Week", "Type", "TeamA", "TeamAScore"]]
results2 = results2017[["Week", "Type", "TeamB", "TeamBScore"]]

input = input("Gib' den Teamnamen ein: ")
print("---------------------------------------------------------------------")

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
    if row["winner"] == True:
        return row["score"] - row["margin"]
    elif row["winner"] == False:
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
# complete.reset_index()

"""
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(complete)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(complete.query("team == 'Fabian'"))
"""

# copy to avoid getting the 'SettingwithCopyWarning' error
output = complete.query("team == @input").copy()
output["opponentScore"] = output.apply(get_opponent_score, axis = 1)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(output)
    print(type(output))

series = output.winner
s_list = series.tolist()
win_count = 0
max_count = 0
for item in s_list:
    if item:
        win_count +=1
    else:
        if win_count > max_count:
            max_count = win_count
        win_count = 0
print("---------------------------------------------------------------------")
print("Die längste Siegesserie von " + output.iloc[0]["team"] + "betrug: "+ str(max_count))

s_list = series.tolist()
loss_count = 0
max_count = 0
for item in s_list:
    if item:
        if loss_count > max_count:
            max_count = loss_count
        loss_count = 0
    else:
        loss_count +=1
print("Die längste Niederlagenserie von " + output.iloc[0]["team"] + "betrug: "+ str(max_count))


print("Die Saisonbilanz von "  + output.iloc[0]["team"] + "für die Saison betrug: ")
print("---------------------------------------------------------------------")

ax = plt.gca()
# draws the lines in the graph
output.plot(kind = 'line',x = 'week',y = 'score',ax = ax)
output.plot(kind = 'line',x = 'week',y = 'opponentScore', color = 'red', ax = ax)
# sets the range for the x and y axis
ax.set_xlim([0,16])
ax.set_ylim([0,200])

plt.show()

