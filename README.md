# Angebote Lübeck

Wochenangebote von Aldi Nord, Lidl, Penny, REWE, Netto, Norma, Jawoll und Krümet für Lübeck 23566.

`data.json` wird jeden Freitag automatisch mit den Angeboten der folgenden Woche aktualisiert.
Die Android-App „Angebote Lübeck“ lädt diese Datei beim Start. Bilder werden direkt von den
Seiten der Händler bzw. Prospekt-Portale geladen und liegen nicht in diesem Repository.

Alle Angaben ohne Gewähr – Preise können je Filiale abweichen.

## App-Oberfläche (ab v4)
- `app/app.html` – Oberfläche (Prospekte · Einkaufsliste · Rezepte), `app/recipes.js` – Grundrezepte und Zutaten-Erkennung, `app/icons.js` – Symbole.
- `python3 app/build.py` baut daraus `android/assets/index.html` (mit aktueller `data.json` als Offline-Fallback).
- Optionales Feld `rezepte` in `data.json`: Wochenrezepte im Format
  `{"id","t" (Titel),"z" (Minuten),"p" (Portionen),"h" (Hauptzutat-Schlüssel),"i":[[Menge,Name,Schlüssel|null]],"s":[Schritte]}` –
  Schlüssel wie in `app/recipes.js` (`KEYS`), `null` für Vorrat (Salz, Öl …).
