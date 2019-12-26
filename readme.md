# Pandas

## Einführung zu Pandas
Die fünf Schritte der Datenanalyse:
1. sammeln
2. speichern
3. laden
4. manipulieren
5. analysieren

Primär wird Pandas hierbei für Schritt 4 (Manipulieren) eingesetzt. 
Jedoch liefert es auch Funktionalität für das Speichern (2), das Laden (3) und Analysieren mit (5).

## Typen und Funktionen
Data ist eine Sammlung strukturierter Informationen.
Jede Spalte ist eine Observation und jede Reihe ein Attribut.

Pandas ermöglicht es mit dieser tabellenartigen Data zu arbeiten.
Der wichtigste Datentyp von Pandas ist der DataFrame. Eine Art Container (wie Liste oder Dict), welche tabellenartige Daten beinhaltet.
Jede Spalte eines DataFrames ist eine Series.
Grundsätzlich kann man sagen, dass Pandas als Lib Möglichkeiten zur Verfügung stellt, auf diese zwei Typen zuzugreifen und mit diesen zu arbeiten.

## DataFrame - Grundlagen

### Laden von Daten
Für das Laden von Daten muss grunsätzlich sowohl pandas, als auch path von der Lib os importiert werden.
Anschließen wird unter DATA_DIR der Pfad, unter welchem die zu verarbeitenden Daten abgelegt wurden.

Mit `path.join(DATA_DIR, 'file.csv')` wird der gesamte Pfad zusammengesetzt.
Data wird dann mit `pd.read_csv` definiert. also dem Inhalt der entsprechenden CSV-Datei

```python
import pandas as pd
from os import path

DATA_DIR = '/Folder/Path'

data = pd.read_csv(path.join(DATA_DIR, 'file.csv'))
```

Der Typ von data ist ein Dataframe:
```python
Input: type(adp)
Output: pandas.core.frame.DataFrame
```
