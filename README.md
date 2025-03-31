# E-Scooter Demand Dashboard – Projektüberblick

**Ziel:** In nur **zwei Wochen** einen einsatzfähigen Prototypen entwickeln, der **E-Scooter-Nachfrage** sowohl zeitlich (Temporal) als auch räumlich (Spatial) präzise vorhersagt und in einem interaktiven Dashboard präsentiert.

---

## Hintergrund & Motivation

- **Datenherkunft:** Ich bin auf öffentlich verfügbare **E-Scooter-Trips** aus Chicago gestoßen, die ab 2022 gesammelt werden. Leider erwiesen sich diese Daten als unvollständig oder fehlerhaft.  
- **Doppelte Rolle:** Um den Zeitplan einzuhalten, übernahm ich neben der **Projektleitung** auch zuerst Aufgaben der **Data-Engineer-Rolle**, um die Daten schnellstmöglich zu bereinigen. Anschließend fokussierte ich mich wieder auf meine Hauptaufgaben als **AI-Engineer**.

---

## Projektstrategie & Rollenverteilung

Um innerhalb von zwei Wochen den größtmöglichen Nutzen zu erzielen, habe ich vor Projektstart einen klaren **Fahrplan** (Overall Project Flow) definiert:

1. **Data Engineer (DE)**
   - Stellt die Daten (Trip-Daten, Wetter, Events) in einer **angereicherten** Form bereit.  
   - Beginnt mit **einfachen Tagesaggregationen**, damit der AI-Engineer schnell ein Baseline-Modell starten kann.  
   - Reserviert **die letzten drei Wochen** der Daten als **Hold-Out**-Set, das erst ganz am Ende zur realistischen Modellbewertung genutzt wird.

2. **Machine Learning Engineer (MLE) – (Meine Rolle als AI-Engineer)**
   - Entwickelt **Prognosemodelle** (z. B. basierend auf Prophet oder weiteren ML-Methoden).  
   - Realisiert **räumliche Binning- bzw. Clustering-Ansätze**, um regionale Nachfrage (Region X, Datum Y) zu modellieren.  
   - Testet und verfeinert verschiedene Modelle schrittweise, wertet die Ergebnisse zunächst an älteren Daten aus und nimmt das **finale 3-Wochen-Hold-Out** erst ganz zum Schluss für den echten „Zukunftstest“.

3. **Data Visualizer / Streamlit Developer (DV)**
   - Baut das **interaktive Dashboard** (z. B. mit Streamlit).  
   - Erzeugt **Szenario-Ansichten** für temporale und räumliche Nachfrageprognosen.  
   - Erlaubt **Was-wäre-wenn-Analysen** (z. B. „Rabatt in Region A“ → Demand-Shift).

Durch **tägliche Abstimmungen** und **inkrementelle Updates** konnte jeder schnell auf neue Daten, Features oder Modelle reagieren.

---

## Projektablauf in Kürze

1. **Woche 1**  
   - **Datenbereinigung**: Ich kümmerte mich zunächst mit dem Data-Engineer-Prozess um die Trip-Daten, da sie unerwartet unvollständig oder fehlerhaft waren.  
   - **Erster Prototyp**: Sobald eine minimale „Daily Demand“-Version verfügbar war, begann ich mit einem **Baseline-Modell** (z. B. einfache Mittelwert- oder Prophet-Prognose).

2. **Woche 2**  
   - **Räumliche Modelle**: Implementierung von Clustering (k-means) oder hexagonalem Binning (z. B. h3) zur **regionalen** Nachfragedarstellung.  
   - **Dashboard-Ausbau**: Unser Data-Visualizer integrierte z. B. **3D-Polygone**, um die Höhe (Tripaufkommen) in verschiedenen Regionen zu zeigen, sowie eine **KeplerGL-Seite** zum Visualisieren der Trip-Vektoren.  
   - **Szenario-Decks**: Wir erstellten drei Decks (ein Temporal und zwei Spatial), um zeitliche Nachfrageverläufe und die regionale Verteilung der Trips darzustellen.  
   - **Abschluss & Validierung**: Erst ganz am Ende spielten wir das **letzte 3-Wochen-Hold-Out**-Set ein, um zu prüfen, wie gut die Modelle künftige Daten vorhersagen.

---

## Was wir erreicht haben

- **Umfangreicher Prototyp** in nur **zwei Wochen**:  
  - **Sowohl zeitliche Prognosen** (Wann steigt die Nachfrage?)  
  - **Als auch räumliche Analysen** (In welchen Regionen sind wie viele Scooter erforderlich?)  
  - **Interaktive Szenario-Simulationen** für hypothetische Eingriffe wie regionale Discounts.

- **Generalisiertes Vorgehen**:  
  Das verwendete Konzept lässt sich leicht auf andere Fragestellungen übertragen:  
  - Statt Scooter-Trips könnte es um **Verkaufszahlen** gehen.  
  - Statt Wetterdaten oder Events könnten **Werbekampagnen**, **Preisänderungen** oder **Einführung neuer Produkte** als Einflussfaktoren dienen.

- **Kompromiss zwischen Zeit & Design**:  
  Auch wenn **Streamlit** in puncto Gestaltung Grenzen setzt, besitzt unser Dashboard alle Kernfunktionen für aussagekräftige Analysen. Mehr Feinschliff ist in einer längeren Projektlaufzeit problemlos umsetzbar.

---

## Fazit

- **Datenbereinigung & Projektleitung**: In der Anfangsphase habe ich als Projektleiter die **Data-Engineer-Aufgaben** übernommen, um die Trip-Daten schnell nutzbar zu machen.  
- **AI-Engineering**: Mein Hauptfokus lag auf der Entwicklung der **Vorhersagemodelle** und deren Einbindung in das Dashboard.  
- **Erfolgsfaktoren**: Täglicher Austausch, klar abgegrenzte Zuständigkeiten und das schrittweise Einbinden neuer Features ins Modell haben wesentlich zum Erfolg beigetragen.  
- **Ergebnis**: Ein vielseitiger Prototyp, der zeigt, **wie E-Scooter-Nachfrage zeitlich und räumlich vorhergesagt** werden kann und gleichzeitig eine Grundlage für weitere KI-gestützte Szenarien oder Branchenanwendungen legt.

**Vielen Dank für dein Interesse – ich freue mich auf künftige Projekte und spannende Kooperationen!**
