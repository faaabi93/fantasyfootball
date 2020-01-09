import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "/Users/fabian.baiersdoerfer/Desktop/ff_data"

results2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_results.csv"), sep=";")
owner2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_owners.csv"), sep=";")

results1 = results2017[["Week", "Type", "TeamA", "TeamAScore"]]
results2 = results2017[["Week", "Type", "TeamB", "TeamBScore"]]

availableSeasons = [2017, 2018, 2019]
season = 0

while True:
  try:
    season = int(input("Welche Saison möchtest du analysieren? "))
    if season in availableSeasons:
      print("Du hast die Saison " + str(season) + " gewählt")
      break
    else:
      print("Diese Saison ist nicht verfügbar!")
  except ValueError:
    print("Das ist kein zulässiges Format. Gib einfach nur ein Jahr ein. Beispielsweise '2017'")

print("Welche Teams möchtest du vergleichen?")

a = {}
k = 0
if season == 2017:
  b = 10
  print("Maximal 10 Teams möglich")
else:
  b = 12
  print("Maximal 12 Teams möglich")

print("Geben Sie die zu vergleichenden Teamnamen ein. stop für break")

while k < b:
  key = k
  value = input("Teamnamen für das " + str(k+1) + ". Team eingeben: ")
  if value == "stop":
    break
  else:
    a[key] = value 
    k += 1

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
complete = pd.concat([teamA, teamB], sort=False)
complete = complete.sort_values(by=["week"])
complete["winner"] = complete.apply(set_winner, axis=1)

a_list = list(a.values())
output_list = []

mean_df = complete.mean()
print(mean_df)
mean_score = mean_df.iloc[2]

for i in a_list:
  output = complete.query("team == @i").copy()
  output["opponentScore"] = output.apply(get_opponent_score, axis=1)
  with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print("Dataframe für das Team von " + i)
    print(output)
  output_list.append(output)

comparison = pd.concat(output_list, sort=False)

# Array of specific colors I later want to use in the hue in the replot-function
colors = ["#4374B3", "#FF0B04", "#3CB44B", "#FFE119", "#FF5733", "#911EB4", "#42D4F4",
"#F032E6", "#BFEF45", "#469990", "#000000"]
# Setting the custom colorpalette
sns.set_palette(sns.color_palette(colors))

g = sns.relplot(x='week', y='score', hue="team", kind='line', data=comparison)
# kwargs for vertical line
keyword = {"color": "black", "linestyle": "--", "linewidth": 0.75}
# Creating a vertical line where the playoffs start
plt.axvline(14, 0, 200, **keyword)
plt.axhline(100, **keyword)
plt.axhline(mean_score, **keyword)
# Set x and y limit to the graph
g.set(ylim=(0, 200))
g.set(xlim=(0, 16))
g.savefig("test.png")
plt.show()