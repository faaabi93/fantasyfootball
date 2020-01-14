import pandas as pd
from os import path
import matplotlib.pyplot as plt
import seaborn as sns

DATA_DIR = "/Users/fabian.baiersdoerfer/Desktop/ff_data"

results2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_results.csv"), sep=";")
results2018 = pd.read_csv(path.join(DATA_DIR, "2018_season_results.csv"), sep=";")
results2019 = pd.read_csv(path.join(DATA_DIR, "2019_season_results.csv"), sep=";")
results = pd.concat([results2017, results2018, results2019], sort=False)
owners2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_owners.csv"), sep=";")
owners2018 = pd.read_csv(path.join(DATA_DIR, "2018_season_owners.csv"), sep=";")
owners2019 = pd.read_csv(path.join(DATA_DIR, "2019_season_owners.csv"), sep=";")
owners = pd.concat([owners2017, owners2018, owners2019], sort=False)

availableSeasons = [2017, 2018, 2019]
season = 0


def winner(row):
    """ returns the winner (Teamname) of the matchup """
    if row["TeamAScore"] > row["TeamBScore"]:
        return row["TeamA"]
    elif row["TeamAScore"] < row["TeamBScore"]:
        return row["TeamB"]
    else:
        return "draw"


def teams(row):
    """ returns the teams ins the specific matchup """
    return [row["TeamA"], row["TeamB"]]


def win_margin(row):
    """ returns the win_margin of TeamA, negative return value indicates a loss """
    if row["TeamAScore"] > row["TeamBScore"]:
        return row["TeamAScore"] - row["TeamBScore"]
    elif row["TeamAScore"] < row["TeamBScore"]:
        return row["TeamBScore"] - row["TeamAScore"]
    else:
        return 0


def winner_bool(row):
    """ returns a bool which indicates whether the team has won the matchup """
    if row["team"] == row["winner"]:
        return True
    else:
        return False


def opponent_score(row):
    """ calculates the opponents score based on own score and the win/los margin """
    if row["winner"]:
        return row["score"] - row["margin"]
    elif not row["winner"]:
        return row["score"] + row["margin"]
    else:
        return row["score"]


while True:
    try:
        season = int(str(input("Welche Saison möchtest du analysieren? ")).strip())
        print(season)
        if season in availableSeasons:
            print("---------------------------------------------------------")
            break
        else:
            print("Diese Saison ist nicht verfügbar!")
    except ValueError:
        print("Das ist kein zulässiges Format. Gib einfach nur ein Jahr ein. Beispielsweise '2017'")

results = results.query('season == @season').copy()
results["winner"] = results.apply(winner, axis=1)
results["margin"] = results.apply(win_margin, axis=1)
results["teams"] = results.apply(teams, axis=1)

# Aufteilen des DF in teamA und teamB, sowie verkleinern. Anschleißend umbenennen der Columns um sie später zu
# concatenaten
teamA = results[["Week", "Type", "TeamA", "TeamAScore", "margin", "TeamB", "winner", "season"]].rename(
    columns={"Week": "week", "TeamA": "team", "TeamAScore": "score", "TeamB": "opponent"})
teamB = results[["Week", "Type", "TeamB", "TeamBScore", "margin", "TeamA", "winner", "season"]].rename(
    columns={"Week": "week", "TeamB": "team", "TeamBScore": "score", "TeamA": "opponent"})

complete = pd.concat([teamA, teamB], sort=False).sort_values(by=["week"])
complete["winner"] = complete.apply(winner_bool, axis=1)

help_df = complete.query("season == @season")
availableOwners = help_df["team"].drop_duplicates().sort_values().tolist()
print("Folgende Spieler sind für die Saison " + str(season) + " verfügbar:\n" +
      ' & '.join([', '.join(availableOwners[:-1]), availableOwners[-1]]))

# TODO: Alle Season und dann für jede Season eigenes Bild
requestedOwners = {}
count = 0
ownerCount = len(availableOwners)
usedOwners = []

print(
    "Geben Sie die zu vergleichenden Spieler ein.\nEingabe von 'stop' oder keine Eingabe (Enter) führt zum "
    "fortfahren\nEingabe von 'all', um alle Spieler anzufordern.")
while count < ownerCount:
    key = count
    value = input("Teamnamen für das " + str(count + 1) + ". Team eingeben: ").strip()
    if value == "stop":
        break
    elif value == "":
        break
    elif value == "all":
        usedOwners = []
        for owner in availableOwners:
            requestedOwners[availableOwners.index(owner)] = owner
        break
    else:
        if value in availableOwners and value not in usedOwners:
            requestedOwners[key] = value
            count += 1
            usedOwners.append(value)
        elif value in usedOwners:
            print("Du forderst diesen Spieler bereits an!")
        else:
            print("Dieser Spieler ist nicht verfügbar!")

requestedOwners_list = list(requestedOwners.values())
output_list = []

if len(requestedOwners) == 2:
    confirmation = input("Möchtest du diese beiden Spieler genauer betrachten?")

mean_df = complete.mean()
mean_score = mean_df.iloc[1]
output_dict = {}

for owner in requestedOwners_list:
    output = complete.query("team == @owner").copy()
    output["opponentScore"] = output.apply(opponent_score, axis=1)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print("Dataframe für das Team von " + owner)
        print(output)
        """ 
        TODO: Anzeige der Durchschnittswerte der beiden Teams:
        Team------------Fabian-------Peter
        ---------------------------------
        durschn. Punkte----100---------80
        Siege---------------15----------2
        etc.
        """
        if len(usedOwners) == int(2):
            output_dict[owner] = output[["score", "winner", "opponentScore"]].sum()
    output_list.append(output)

# TODO: Team1 vs Team2 simulieren und Ergebnis anzeigen.
# TODO: Immer gegen den Genger von Team2 simulieren
# TODO: Tabelle?!

print("output_dict:")
print(output_dict)
output_df = pd.concat(output_list, sort=False)

complete["opponentScore"] = complete.apply(opponent_score, axis=1)
print(complete.groupby("team").agg({"winner":"sum", "score":["max", "min", "sum", "mean"], "opponentScore":["sum",  "mean"]}))

# TODO: Saison mit dem Schedule eines anderen Teams durchspielen

if confirmation:
    if confirmation == "all":
        for team1 in availableOwners:
            for team2 in availableOwners:
                if team1 != team2:
                    print(team1 + " vs " + team2)
                    team1_df = complete.query("team == @team1")[["week", "team", "score"]]
                    team2_df = complete.query("team == @team2")[["week", "opponent", "opponentScore"]]
                    team_df = pd.merge(team1_df, team2_df, on="week")
                    team_df = team_df.rename(columns={"team": "TeamA", "score": "TeamAScore", "opponent": "TeamB", "opponentScore": "TeamBScore"})
                    team_df["winner"] = team_df.apply(winner, axis=1)
                    team_df["margin"] = team_df.apply(win_margin, axis=1)
                    team_df = team_df.rename(columns={"TeamA": "team", "TeamAScore": "score", "TeamB": "opponent", "TeamBScore": "opponentScore"})
                    team_df["winner"] = team_df.apply(winner_bool, axis=1)
                    print(team_df)


# Array of specific colors I later want to use in the hue in the replot-function
colors = ["#4374B3", "#FF0B04", "#3CB44B", "#FFE119", "#FF5733", "#911EB4", "#42D4F4",
          "#F032E6", "#BFEF45", "#469990", "#000000"]
# kwargs for vertical line
pltlines = {"color": "black", "linestyle": "--", "linewidth": 0.75}
pltmeanline = {"color": "grey", "linestyle": "-", "linewidth": 0.75}

# Setting the custom colorpalette
sns.set_palette(sns.color_palette(colors))
sns.set_style("whitegrid")
g = sns.relplot(x='week', y='score', hue="team", kind='line', data=output_df)
plt.axvline(14, 0, 200, **pltlines)
plt.axhline(100, **pltlines)
plt.axhline(mean_score, **pltmeanline)
plt.title("Season " + str(season))
g.set(ylim=(0, 200), xlim=(1, 16), ylabel="Punkte", xlabel="Woche")
g.savefig("test.png")
plt.show()
