# Pandas-Functions

Sammlung der Pandas-Functions

## Laden von Daten

`DATA_DIR` gibt an, wo die zu ladenden Daten auf dem System vorliegen.

```python
import pandas as pd
from os import path

DATA_DIR = '/User/etc/...'

data = pd.read_csv(path.join(DATA_DIR, 'data.csv'))
```



## Anwendung auf DataFrames

```markdown
|Function   | Beschreibung  |
|---|---|
|`data.head()`   |   |
|   |   |
```