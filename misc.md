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

| Function                                                     | Beschreibung                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `data.head()`                                                | Gibt die ersten fünf Zeilen des Dataframes aus               |
| `data.columns`                                               | Gibt die Spalten des Dataframes zurück                       |
| `data['column'].head()`                                      | Gibt die ersten fünf Einträge einer Spalte als **Series** zurück |
| `data['column'].to_frame()`                                  | Gibt eine Spalte als DataFrame zurück                        |
| `data[['column1', 'column2', 'column3']].head()`             | GIbt die ersten fünf Einträge der drei angegebenen Spalten als **DataFrame** zurück |
| `data.set_index('column', inplace=True)`                     | Setzt eine bestehende Spalte eines DataFrames als Index. `inplace=True`erstellt keine Kopie, sondern ändert den bestehenden DataFrame |
| `data.reset_index()`                                         | Setzt den Standard-Index (0, 1, 2, ...)                      |
| `data_1['new_column'] = data_2['column']`                    | Erzeugt in `data_1`eine neue Spalte mit den Werten von `column`aus `data_2`. Hier wird der Index verwendet. |
| `data.to_csv(path.join(PATH_DIR, 'new_file.csv'))`           | Speichert den DataFrame `data`als CSV-Datei mit dem angegebenen Namen unter `PATH_DIR`ab. |
| `data['new_column'] = 4`                                     | Erzeugt eine neue Spalte, die für alle Zeilen den Wert 4 besitzt oder ändert den bestehenden Wert für alle Zeilen zu 4 |
| `data['new_column'] = (data['column1'] + (2 * data['column2'])` | Hierbei sind selbstverständlich auch mathematische Operatoren möglich |
| `data['column'].sample(5)`                                   | Liefert eine "Stichprobe" von 5 zufälligen Zeilen zurück     |
| `data.['column'].str.upper()`                                | Auf String-Spalten kann auch mit String-Functions zugegriffen werden, wie beispielsweise `.str.upper()`, `.str.lower()` oder `.str.replace()` oder ähnlich ...<br />Beispielsweise wäre auch folgendes möglich:<br />`(data['column1'] + ', ' + data['column2'] + ' und ' + data['column3']` |
| `data.['is_new'] = (pg['status'] == 'new')`                  | Bool-Spalten:<br />Neue Spalte mit `true`, wenn `'status' 'new'`ist. |
| TODO                                                         | TODO                                                         |
|                                                              |                                                              |
|                                                              |                                                              |
|                                                              |                                                              |
|                                                              |                                                              |