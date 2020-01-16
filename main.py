import pandas as pd
import seaborn as sns
import fantasyfunctions as ff
import matplotlib.pyplot as plt
import glob
from os import path

# reading all _result.csvs in the DATA_DIR
DATA_DIR = ''
all_files = glob.glob(path.join(DATA_DIR, "*_results.csv"))
master_df = pd.concat((pd.read_csv(f, index_col=None, header=0, sep=';') for f in all_files))

availableSeasons = master_df["season"].drop_duplicates().sort_values().tolist()
print("Folgende Saisons sind verfügbar: " + ", ".join(str(year) for year in availableSeasons))

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

master_df = master_df.query('season == @season').copy()
master_df["winner"] = master_df.apply(ff.winner, axis=1)
master_df["margin"] = master_df.apply(ff.win_margin, axis=1)
master_df["teams"] = master_df.apply(ff.teams, axis=1)

teamA = master_df[["Week", "Type", "TeamA", "TeamAScore", "margin", "TeamB", "winner", "season"]].rename(columns={"Week": "week", "TeamA": "team", "TeamAScore": "score", "TeamB": "opponent"})
teamB = master_df[["Week", "Type", "TeamB", "TeamBScore", "margin", "TeamA", "winner", "season"]].rename(columns={"Week": "week", "TeamB": "team", "TeamBScore": "score", "TeamA": "opponent"})

complete = pd.concat([teamA, teamB], sort=False).sort_values(by=["week"])
complete["winner"] = complete.apply(ff.winner_bool, axis=1)

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
    output["opponentScore"] = output.apply(ff.opponent_score, axis=1)
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

complete["opponentScore"] = complete.apply(ff.opponent_score, axis=1)
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
                    team_df["winner"] = team_df.apply(ff.winner, axis=1)
                    team_df["margin"] = team_df.apply(ff.win_margin, axis=1)
                    team_df = team_df.rename(columns={"TeamA": "team", "TeamAScore": "score", "TeamB": "opponent", "TeamBScore": "opponentScore"})
                    team_df["winner"] = team_df.apply(ff.winner_bool, axis=1)
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
