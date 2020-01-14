import pandas as pd
from os import path
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# DATA_DIR = "/Users/fabian.baiersdoerfer/Desktop/ff_data"

""" results2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_results.csv"), sep=";") """
results = pd.read_csv(path.join(DATA_DIR, "2018_season_results.csv"), sep=";")
""" results2019 = pd.read_csv(path.join(DATA_DIR, "2019_season_results.csv"), sep=";")
results = pd.concat([results2017, results2018, results2019], sort=False)
owners2017 = pd.read_csv(path.join(DATA_DIR, "2017_season_owners.csv"), sep=";")
owners2018 = pd.read_csv(path.join(DATA_DIR, "2018_season_owners.csv"), sep=";")
owners2019 = pd.read_csv(path.join(DATA_DIR, "2019_season_owners.csv"), sep=";")
owners = pd.concat([owners2017, owners2018, owners2019], sort=False) 
"""

def generate_table(dataframe, max_rows=1000):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    dcc.Graph(
        id='example-graph-2',
        style={'height': 800},
        figure={
            'data': [
                dict(
                    x=complete[complete['team'] == i]['week'],
                    y=complete[complete['team'] == i]['score'],
                   # text=output_df[output_df['team'] == i]['country'],
                    mode='lines+markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in complete.team.unique()
            ],

            'layout': dict(
                xaxis={'title': 'Woche', 'dtick': 1, 'range':[1,16]},
                yaxis={'title': 'Punkte', 'dtick': 10, 'range':[50, 200]},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            ),
        },
    ),

    html.H4(children='Output_df:'),
    generate_table(output_df)
])


if __name__ == '__main__':
    app.run_server(debug=True)
