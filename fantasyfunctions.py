def winner(row):
  """ USE ON MASTER_DF returns the winner (Teamname) of the matchups """
  if row["TeamAScore"] > row["TeamBScore"]:
    return row["TeamA"]
  elif row["TeamAScore"] < row["TeamBScore"]:
    return row["TeamB"]
  else:
    return "draw"


def teams(row):
  """ USE ON MASTER_DF returns the teams ins the specific matchup """
  return [row["TeamA"], row["TeamB"]]


def win_margin(row):
  """ USE ON MASTER_DF returns the win_margin of TeamA, negative return value indicates a loss """
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