## Inspiration
GPS-Marker werden an zu fertigende Teile gebunden und durchlaufen mit den Teilen diverse Prozesse. Für den Gesamtprozess existiert also ein Start- und ein Endzeitpunkt, wobei diese manuell gesetzt werden müssen. Das Setzen der Zeitpunkte wird in der Praxis nicht immer gemacht, was zu fehlerhaften und falschen Daten führt.

## What it does

Das Vorhaben lässt die GPS-Marker "smart" werden und erkennen automatisiert den Endzeitpunkt einer industriellen Prozesskette, sodass diese Information nicht manuell erfasst werden muss und die Datenqualität dadurch rapide ansteigt.

* KI: Automatisierte Prediction eines Prozessendes durch Eingabe einer Prozesssequenz eines Markers

  * Dadurch können auch fehlende Endzeitpunkte vorhergesagt werden
  * Erhöhte Datenqualität für andere Datenverarbeitungen und KIs
  * KI kann für Transfer-Learning verwendet werden


* Fusions-Algorithmus:
  * Prozess-Area für jeden Timestamp eines Markers wird durch (x,y)-Koordinaten ermitteln und ein neuer Datensatz fü die Positions-Historie aller Marker generiert


  * Erstellt Datensatz von Batches für jede vollständig vorhandene Prozessekette aus den Daten, um damit das RNN-Modell zu trainieren
    * Auch Batches für unvollständige Prozessketten


## How we built it
* Tools: Python & torch

* Verständnis der Daten:

  * Alle Datenpunkte auf der gegebenen Karte von Trumpf geplottet und interpretiert

* Datenaufbereitung:

  * Positions-Historie um Prozess-Area für jeden Timestamp und Marker erweitert
    * Erreicht bessere Generalisierung
  * Batch-Datensatz zum Trainieren der KI aus den aufbereiteten Datensätzen generiert und unvollständige Sequenzen verworfen

* RNN:

  * Nutzen für LSTMs für Zustandshaltung von relevanten Prozessschritten

  * Sequence-to-Sequence-Learning

![RNN - Many to One](https://i.stack.imgur.com/F7qzk.jpg)
<img src="https://i.ytimg.com/vi/kMLl-TKaEnc/maxresdefault.jpg" alt="LSTM" height="10"/>

## Challenges we ran into
* Relativ wenige Daten für heterogene Prozesse, die umständlich fusioniert, aufbereitet und aussortiert werden mussten


* Wenig Zeit, um lokal neuronales Netz zu trainieren und zu optimieren
* Rechenpower
  * 11h Daten-Aufbereitung
  * 7h RNN-Training

## Accomplishments that we are proud of
* Fertiges RNN mit LSTMs
* Durch Fusionieren der Daten und Zusammenführen mehrerer Tabellen deutlich bessere Ergebnisse erzielt

## What we learned
* Auslagern von rechenintensiven Operationen wie Trainieren und Aufbereiten von Daten


* Mehrere Modelle parallel trainieren wirkt kurzer Zeit entgegen und optimiert die KI wenigstens etwas

## What's next for smart_gps
* Sammeln von mehreren Samples für ähnliche Prozesse, damit die KI besser generalisiert


* Optimieren der Aufbereitung der Daten
* Optimieren der Hyperparameter, vor allem tieferes Netz



### How to run

* Um die Datenaufbereitung durchzuführen, müssen die Datensätze von TRUMPF GmbH + Co. KG in der geforderten Ordnerstruktur vorliegen (*siehe data_magic.py & data_merger.py*)
* Für Prediction von 5 Testdaten: *python rnn.py*