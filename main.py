import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "ff_data"

results2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_results.csv"), sep=";")
results2018 = pd.read_csv(path.join(DATA_DIR, "2018_season_results.csv"), sep=";")
results = pd.concat([results2017, results2018], sort=False)
owners2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_owners.csv"), sep=";")
owners2018 = pd.read_csv(path.join(DATA_DIR, "2018_season_owners.csv"), sep=";")
owners2019 = pd.read_csv(path.join(DATA_DIR, "2019_season_owners.csv"), sep=";")
owners = pd.concat([owners2017, owners2018, owners2019], sort=False)

results1 = results[["Week", "Type", "TeamA", "TeamAScore"]]
results2 = results[["Week", "Type", "TeamB", "TeamBScore"]]

availableSeasons = [2017, 2018, 2019]
season = 0

def winner(row):
  ''' returns the winner (Teamname) of the matchup '''
  if row["TeamAScore"] > row["TeamBScore"]:
      return row["TeamA"]
  elif row["TeamAScore"] < row["TeamBScore"]:
      return row["TeamB"]
  else:
      return "draw"


def teams(row):
  ''' returns the teams ins the specific matchup '''
  return [row["TeamA"], row["TeamB"]]


def win_margin(row):
  ''' returns the win_margin of TeamA, negative return value indicates a loss '''
  if row["TeamAScore"] > row["TeamBScore"]:
    return row["TeamAScore"] - row["TeamBScore"]
  elif row["TeamAScore"] < row["TeamBScore"]:
    return row["TeamBScore"] - row["TeamAScore"]
  else:
    return 0


def winner_bool(row):
  ''' returns a bool which indicates whether the team has won the matchup '''
  if row["team"] == row["winner"]:
    return True
  else:
    return False


def opponent_score(row):
  ''' calculates the opponents score based on own score and the win/los margin '''
  if row["winner"]:
    return row["score"] - row["margin"]
  elif not row["winner"]:
    return row["score"] + row["margin"]
  else:
    return row["score"]


while True:
    try:
        season = int(input("Welche Saison möchtest du analysieren? "))
        if season in availableSeasons:
            print("---------------------------------------------------------")
            break
        else:
            print("Diese Saison ist nicht verfügbar!")
    except ValueError:
        print("Das ist kein zulässiges Format. Gib einfach nur ein Jahr ein. Beispielsweise '2017'")

results_a = results.query("season == @season").copy()
results_a["winner"] = results_a.apply(winner, axis=1)
results_a["margin"] = results_a.apply(win_margin, axis=1)
results_a["teams"] = results_a.apply(teams, axis=1)

# Aufteilen des DF in teamA und teamB, sowie verkleinern. Anschleißend umbenennen der Columns um sie später zu concatenaten
teamA = results_a[["Week", "Type", "TeamA", "TeamAScore", "margin", "TeamB", "winner", "season"]].rename(columns={"Week": "week", "TeamA": "team", "TeamAScore": "score", "TeamB": "opponent"})
teamB = results_a[["Week", "Type", "TeamB", "TeamBScore", "margin", "TeamA", "winner", "season"]].rename(columns={"Week": "week", "TeamB": "team", "TeamBScore": "score", "TeamA": "opponent"})

complete = pd.concat([teamA, teamB], sort=False).sort_values(by=["week"])
complete["winner"] = complete.apply(winner_bool, axis=1)

help_df = complete.query("season == @season")
availableOwners = help_df["team"].drop_duplicates().sort_values().tolist()
print("Folgende Spieler sind für die Saison " + str(season) + " verfügbar:\n" +  
' & '.join([', '.join(availableOwners[:-1]),availableOwners[-1]]))

# TODO: Alle Season und dann für jede Season eigenes Bild
requestedOwners = {}
k = 0
b = len(availableOwners)
usedOwners = []

print("Geben Sie die zu vergleichenden Spieler ein.\nEingabe von 'stop' oder keine Eingabe (Enter) führt zum fortfahren\nEingabe von 'all', um alle Spieler anzufordern.")
while k < b:
    key = k
    value = input("Teamnamen für das " + str(k + 1) + ". Team eingeben: ")
    if value == "stop":
        break
    elif value == "":
        break
    elif value == "all":
      for owner in availableOwners:
        requestedOwners[availableOwners.index(owner)] = owner
      break
    else:
        if value in availableOwners and value not in usedOwners:
          requestedOwners[key] = value
          k += 1
          usedOwners.append(value)
        elif value in usedOwners:
          print("Du forderst diesen Spieler bereits an!")
        else:
          print("Dieser Spieler ist nicht verfügbar!")

requestedOwners_list = list(requestedOwners.values())
output_list = []

mean_df = complete.mean()
mean_score = mean_df.iloc[1]

for i in requestedOwners_list:
    output = complete.query("team == @i").copy()
    output["opponentScore"] = output.apply(opponent_score, axis=1)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print("Dataframe für das Team von " + i)
        print(output)
    output_list.append(output)

completeList = pd.concat(output_list, sort=False)

# Array of specific colors I later want to use in the hue in the replot-function
colors = ["#4374B3", "#FF0B04", "#3CB44B", "#FFE119", "#FF5733", "#911EB4", "#42D4F4",
          "#F032E6", "#BFEF45", "#469990", "#000000"]
# kwargs for vertical line
pltlines = {"color": "black", "linestyle": "--", "linewidth": 0.75}
pltmeanline = {"color": "grey", "linestyle": "-", "linewidth": 0.75}

# Setting the custom colorpalette
sns.set_palette(sns.color_palette(colors))
g = sns.relplot(x='week', y='score', hue="team", kind='line', data=completeList)
plt.axvline(14, 0, 200, **pltlines)
plt.axhline(100, **pltlines)
plt.axhline(mean_score, **pltmeanline)
plt.title("Season " +str(season))
g.set(ylim=(0, 200), xlim=(0, 16), ylabel="Punkte", xlabel="Woche")
g.savefig("test.png")
plt.show()