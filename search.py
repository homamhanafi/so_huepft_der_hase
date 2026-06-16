import heapq


# ==========================================================
# Heuristik-Funktion
# ==========================================================
def heuristik(a, b):
    """
    Berechnet die Manhattan-Distanz zwischen zwei Positionen.

    Beispiel:
    a = (0, 0)
    b = (2, 3)

    Ergebnis:
    |0 - 2| + |0 - 3| = 5
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ==========================================================
# A*-Algorithmus
# ==========================================================
def finde_weg(start, ziel, hindernisse, zeilen, spalten, blockierte_felder=None):
    """
    Findet mit dem A*-Algorithmus den kürzesten Weg von Start zu Ziel.

    Parameter:
    ----------
    start : tuple
        Startposition, z. B. (0, 0)

    ziel : tuple
        Zielposition, z. B. (4, 4)

    hindernisse : list
        Liste von Hindernissen, die nicht betreten werden dürfen

    zeilen : int
        Anzahl der Zeilen im Spielfeld

    spalten : int
        Anzahl der Spalten im Spielfeld

    blockierte_felder : list oder set, optional
        Weitere gesperrte Felder, z. B. Positionen anderer Hasen

    Rückgabe:
    ---------
    list
        Liste von Positionen, die den Pfad darstellen

    None
        Falls kein Pfad gefunden wird
    """

    # Falls keine zusätzlichen blockierten Felder übergeben wurden
    if blockierte_felder is None:
        blockierte_felder = set()
    else:
        blockierte_felder = set(blockierte_felder)

    # Start und Ziel dürfen nicht blockiert sein
    blockierte_felder.discard(start)
    blockierte_felder.discard(ziel)

    # Alle gesperrten Felder zusammenfassen
    gesperrte_felder = set(hindernisse) | blockierte_felder

    # Prioritätswarteschlange (Open List)
    offene_liste = []

    # Startknoten einfügen
    heapq.heappush(
        offene_liste,
        (heuristik(start, ziel), start)
    )

    # Vorgänger jedes Knotens
    came_from = {}

    # Bisherige Kosten vom Start
    g_score = {
        start: 0
    }

    # Geschätzte Gesamtkosten
    f_score = {
        start: heuristik(start, ziel)
    }

    # Bewegungsrichtungen:
    # oben, unten, links, rechts
    richtungen = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    # Solange noch Knoten in der Open List sind
    while offene_liste:

        # Knoten mit kleinsten f-Kosten entnehmen
        _, aktuell = heapq.heappop(offene_liste)

        # Ziel erreicht
        if aktuell == ziel:
            pfad = [aktuell]

            # Pfad rückwärts rekonstruieren
            while aktuell in came_from:
                aktuell = came_from[aktuell]
                pfad.append(aktuell)

            # Reihenfolge umdrehen (Start -> Ziel)
            pfad.reverse()
            return pfad

        # Aktuelle Position
        zeile, spalte = aktuell

        # Alle Nachbarn untersuchen
        for dz, ds in richtungen:
            neue_zeile = zeile + dz
            neue_spalte = spalte + ds
            nachbar = (neue_zeile, neue_spalte)

            # --------------------------------------
            # 1. Prüfen, ob Nachbar innerhalb
            #    des Spielfelds liegt
            # --------------------------------------
            if not (
                0 <= neue_zeile < zeilen
                and
                0 <= neue_spalte < spalten
            ):
                continue

            # --------------------------------------
            # 2. Prüfen, ob Feld blockiert ist
            # --------------------------------------
            if nachbar in gesperrte_felder:
                continue

            # --------------------------------------
            # 3. Neue Kosten berechnen
            # --------------------------------------
            tentative_g = g_score[aktuell] + 1

            # --------------------------------------
            # 4. Besserer Weg gefunden?
            # --------------------------------------
            if (
                nachbar not in g_score
                or
                tentative_g < g_score[nachbar]
            ):
                # Vorgänger speichern
                came_from[nachbar] = aktuell

                # Neue Kosten speichern
                g_score[nachbar] = tentative_g

                # f = g + h
                f_score[nachbar] = (
                    tentative_g
                    +
                    heuristik(nachbar, ziel)
                )

                # In Open List einfügen
                heapq.heappush(
                    offene_liste,
                    (f_score[nachbar], nachbar)
                )

    # Kein Pfad gefunden
    return None