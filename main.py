# ==========================================================
# SO HUEPFT DER HASE
# KI-Projekt mit A*-Algorithmus
# FINAL VERSION
# ==========================================================

import pygame
from search import finde_weg

# ==========================================================
# Initialisierung
# ==========================================================
pygame.init()

# ==========================================================
# Fenster
# ==========================================================
BREITE = 1000
HOEHE = 800

screen = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("So huepft der Hase")

# ==========================================================
# Bilder laden
# ==========================================================
rabbit_img = pygame.image.load("assets/rabbit.png").convert_alpha()
rabbit_img = pygame.transform.scale(rabbit_img, (70, 70))

hole_img = pygame.image.load("assets/holes.png").convert_alpha()
hole_img = pygame.transform.scale(hole_img, (90, 90))

rock_img = pygame.image.load("assets/rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (70, 70))

background_img = pygame.image.load("assets/background.png").convert()
background_img = pygame.transform.scale(background_img, (1000, 800))

# ==========================================================
# Farben
# ==========================================================
SCHWARZ = (0, 0, 0)
ROT = (220, 50, 50)
BLAU = (50, 100, 220)
GELB = (255, 215, 0)
WEISS = (255, 255, 255)

GRID_FARBE = (240, 240, 220)

# ==========================================================
# Grid
# ==========================================================
ZEILEN = 5
SPALTEN = 5
ZELLENGROESSE = 100

GRID_BREITE = SPALTEN * ZELLENGROESSE
GRID_HOEHE = ZEILEN * ZELLENGROESSE

START_X = (BREITE - GRID_BREITE) // 2
START_Y = (HOEHE - GRID_HOEHE) // 2

# ==========================================================
# Buttons
# ==========================================================
solve_button = pygame.Rect(250, 730, 150, 50)

reset_button = pygame.Rect(430, 730, 150, 50)

menu_button = pygame.Rect(610, 730, 150, 50)

play_button = pygame.Rect(350, 250, 300, 70)

levels_button = pygame.Rect(350, 350, 300, 70)

about_button = pygame.Rect(350, 450, 300, 70)

exit_button = pygame.Rect(350, 550, 300, 70)


level_buttons = []

for i in range(5):

    level_buttons.append(

        pygame.Rect(
            350,
            220 + i * 90,
            300,
            60
        )
    )

# ==========================================================
# Levels
# ==========================================================
LEVELS = [

    # ======================================================
    # Level 1
    # ======================================================
    {
        "hasen": [
            (0, 0),
        ],

        "loecher": [
            (4, 4),
        ],

        "hindernisse": [
            (2, 2),
            (2, 4),
            (3, 2),
        ],

    

        "optimale_schritte": 9,
        "max_schritte": 10
    },

    # ======================================================
    # Level 2
    # ======================================================
    {
        "hasen": [
            (4, 0),
            (0, 4),
        ],

        "loecher": [
            (0, 0),
            (4, 4),
        ],

        "hindernisse": [
            (1, 1),
            (1, 2),
            (2, 2),
            (3, 2),
        ],

        "optimale_schritte": 9,
        "max_schritte": 10
    },

    # ======================================================
    # Level 3
    # ======================================================
    {
        "hasen": [
            (2, 0),
            (4, 2),
        ],

        "loecher": [
            (0, 2),
            (2, 4),
        ],

        "hindernisse": [
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 1),
            (3, 2),
            (3, 3),
        ],

        "optimale_schritte": 16,
        "max_schritte": 18
    },

    # ======================================================
    # Level 4
    # ======================================================
    {
        "grid": 6,

        "hasen": [
            (0, 0),
            (5, 1),
            (3, 0),
        ],

        "loecher": [
            (5, 5),
            (0, 5),
            (2, 4),
        ],

        "hindernisse": [
            (1, 1),
            (1, 2),
            (1, 4),
            (2, 2),
            (2, 3),
            (3, 1),
            (3, 3),
            (4, 2),
            (4, 4),
        ],

        "optimale_schritte": 24,
        "max_schritte": 26
    },

    # ======================================================
    # Level 5 (Hard but possible)
    # ======================================================
    {
        "grid": 6,

        "hasen": [
            (0, 1),
            (5, 4),
            (3, 0),
        ],

        "loecher": [
            (0, 5),
            (5, 0),
            (2, 5),
        ],

        "hindernisse": [

            (1, 1),
            (1, 2),
            (1, 4),

            (2, 2),

            (3, 1),
            (3, 4),

            (4, 1),
            (4, 3),
        ],

        "optimale_schritte": 24,
        "max_schritte": 26
    }
]

# ==========================================================
# Spielstatus
# ==========================================================
aktuelles_level = 0

HASEN = []
LOECHER = []
HINDERNISSE = []
START_HASEN = []

aktueller_hase_index = 0

pfad = []

letzte_bewegung = 0
BEWEGUNGS_DELAY = 300

ziel_erreicht = False
ziel_erreicht_start = 0

auto_queue = []
solve_all_mode = False

# ==========================================================
# Schritte
# ==========================================================
schritte = 0
max_schritte = 0
optimale_schritte = 0

# ==========================================================
# States
# ==========================================================
im_menu = True
level_geschafft = False
game_over = False
final_win = False
show_levels = False
show_about = False

# ==========================================================
# Animation
# ==========================================================
animating = False

animation_start = (0, 0)
animation_target = (0, 0)

animation_progress = 0
animation_speed = 0.08

# ==========================================================
# Schrift
# ==========================================================
font = pygame.font.SysFont(None, 38)

# ==========================================================
# Level laden
# ==========================================================
def lade_level(level_index):

    global aktuelles_level
    global HASEN
    global LOECHER
    global HINDERNISSE
    global START_HASEN
    global pfad
    global auto_queue
    global solve_all_mode
    global aktueller_hase_index
    global level_geschafft
    global schritte
    global max_schritte
    global optimale_schritte
    global game_over

    global ZEILEN
    global SPALTEN
    global GRID_BREITE
    global GRID_HOEHE
    global START_X
    global START_Y

    aktuelles_level = level_index

    level = LEVELS[level_index]

    if "grid" in level:

        ZEILEN = level["grid"]
        SPALTEN = level["grid"]

    else:

        ZEILEN = 5
        SPALTEN = 5

    GRID_BREITE = SPALTEN * ZELLENGROESSE
    GRID_HOEHE = ZEILEN * ZELLENGROESSE

    START_X = (BREITE - GRID_BREITE) // 2
    START_Y = (HOEHE - GRID_HOEHE) // 2

    HASEN = level["hasen"].copy()

    LOECHER = level["loecher"]

    HINDERNISSE = level["hindernisse"]

    START_HASEN = HASEN.copy()

    max_schritte = level["max_schritte"]

    optimale_schritte = level["optimale_schritte"]

    schritte = 0

    aktueller_hase_index = 0

    pfad = []

    auto_queue = []

    solve_all_mode = False

    level_geschafft = False

    game_over = False

# ==========================================================
# zeichne_buttons
# ==========================================================

def zeichne_buttons():

    maus_x, maus_y = pygame.mouse.get_pos()

    buttons = [
        (solve_button, "Solve", (70, 140, 255)),
        (reset_button, "Reset", (255, 180, 60)),
        (menu_button, "Menu", (255, 80, 80))
    ]

    for button, text, color in buttons:

        aktuelle_farbe = color

        if button.collidepoint(maus_x, maus_y):

            aktuelle_farbe = (
                min(color[0] + 40, 255),
                min(color[1] + 40, 255),
                min(color[2] + 40, 255)
            )
        if button.collidepoint(maus_x, maus_y):

             shadow_rect = button.inflate(12, 12)

             pygame.draw.rect(
                screen,
                (255, 255, 255),
                shadow_rect,
                border_radius=18
        )

        pygame.draw.rect(
            screen,
            aktuelle_farbe,
            button,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            WEISS,
            button,
            2,
            border_radius=15
        )

        text_surface = font.render(
            text,
            True,
            WEISS
        )

        text_rect = text_surface.get_rect(
            center=button.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

# ==========================================================
# zeichne_menu buttons
# ==========================================================
def zeichne_menu_button(rect, text):

    mx, my = pygame.mouse.get_pos()

    farbe = (70, 70, 70)

    if rect.collidepoint(mx, my):

        farbe = (120, 120, 120)

    pygame.draw.rect(
        screen,
        farbe,
        rect,
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        WEISS,
        rect,
        2,
        border_radius=15
    )

    text_surface = font.render(
        text,
        True,
        WEISS
    )

    text_rect = text_surface.get_rect(
        center=rect.center
    )

    screen.blit(
        text_surface,
        text_rect
    )
# ==========================================================
# Reset
# ==========================================================
def reset_spiel():

    global HASEN
    global aktueller_hase_index
    global pfad
    global auto_queue
    global solve_all_mode
    global level_geschafft
    global schritte
    global game_over

    HASEN = START_HASEN.copy()

    aktueller_hase_index = 0

    pfad = []

    auto_queue = []

    solve_all_mode = False

    level_geschafft = False

    schritte = 0

    game_over = False


# ==========================================================
# Feld Position
# ==========================================================
def feld_position(zeile, spalte):

    x = START_X + spalte * ZELLENGROESSE
    y = START_Y + zeile * ZELLENGROESSE

    return x, y


# ==========================================================
# Maus -> Feld
# ==========================================================
def maus_zu_feld(mx, my):

    if mx < START_X or my < START_Y:
        return None

    spalte = (mx - START_X) // ZELLENGROESSE
    zeile = (my - START_Y) // ZELLENGROESSE

    if 0 <= zeile < ZEILEN and 0 <= spalte < SPALTEN:
        return (zeile, spalte)

    return None


# ==========================================================
# Level geschafft?
# ==========================================================
def pruefe_level_geschafft():

    for hase in HASEN:

        if hase not in LOECHER:
            return False

    return True


# ==========================================================
# Nächstes Loch finden
# ==========================================================
# KI:
# Findet mit A* den kürzesten Weg
# zum nächstgelegenen erreichbaren Loch
def finde_naechstes_loch(start):

    global aktueller_hase_index

    beste_pfad = None
    bestes_loch = None

    andere_hasen = []

    for i, pos in enumerate(HASEN):

      if i == aktueller_hase_index:
        continue

      if pos not in LOECHER:
        andere_hasen.append(pos)
   

    for loch in LOECHER:

        pfad_test = finde_weg(
            start,
            loch,
            HINDERNISSE,
            ZEILEN,
            SPALTEN,
            andere_hasen
        )

        if pfad_test is None:
            continue

        if beste_pfad is None or len(pfad_test) < len(beste_pfad):

            beste_pfad = pfad_test
            bestes_loch = loch

    return bestes_loch, beste_pfad


# ==========================================================
# Grid zeichnen
# ==========================================================
def zeichne_grid():

    for zeile in range(ZEILEN):

        for spalte in range(SPALTEN):

            x, y = feld_position(zeile, spalte)

            rect = pygame.Rect(
                x,
                y,
                ZELLENGROESSE,
                ZELLENGROESSE
            )

            pygame.draw.rect(screen, GRID_FARBE, rect)
            pygame.draw.rect(
                screen,
                (80, 80, 80),
                rect,
                1
)


# ==========================================================
# Hindernisse
# ==========================================================
def zeichne_hindernisse():

    for zeile, spalte in HINDERNISSE:

        x, y = feld_position(zeile, spalte)

        screen.blit(
            rock_img,
            (x + 18, y + 10)
        )


# ==========================================================
# Löcher
# ==========================================================
def zeichne_loecher():

    for zeile, spalte in LOECHER:

        x, y = feld_position(zeile, spalte)

        screen.blit(
            hole_img,
            (x + 5, y + 5)
        )


# ==========================================================
# Pfad
# ==========================================================
def zeichne_pfad():

    for zeile, spalte in pfad:

        x, y = feld_position(zeile, spalte)

        rect = pygame.Rect(
            x + 35,
            y + 35,
            30,
            30
        )

        pygame.draw.rect(
            screen,
            GELB,
            rect,
            border_radius=15
        )


# ==========================================================
# Hasen
# ==========================================================
def zeichne_hasen():

    global animating

    for index, (zeile, spalte) in enumerate(HASEN):

        if animating and index == aktueller_hase_index:

            start_x, start_y = feld_position(
                animation_start[0],
                animation_start[1]
            )

            ziel_x, ziel_y = feld_position(
                animation_target[0],
                animation_target[1]
            )

            x = start_x + (ziel_x - start_x) * animation_progress
            y = start_y + (ziel_y - start_y) * animation_progress

        else:

            x, y = feld_position(zeile, spalte)

        if index == aktueller_hase_index:

            rahmen = pygame.Rect(
                x + 5,
                y + 5,
                90,
                90
            )

            pygame.draw.rect(
                screen,
                BLAU,
                rahmen,
                4,
                border_radius=12
            )

        screen.blit(
            rabbit_img,
            (x + 15, y + 10)
        )


# ==========================================================
# UI Text
# ==========================================================
def zeichne_text():

    # ==========================================
    # HUD Hintergrund
    # ==========================================
    panel = pygame.Rect(
        15,
        10,
        BREITE - 30,
        85
    )

    pygame.draw.rect(
        screen,
        (25, 25, 25),
        panel,
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        (180, 180, 180),
        panel,
        2,
        border_radius=15
    )

    # ==========================================
    # Level
    # ==========================================
    level_font = pygame.font.SysFont(None, 42)

    level_text = level_font.render(
        f"Level {aktuelles_level + 1}",
        True,
        WEISS
    )

    screen.blit(
        level_text,
        (35, 25)
    )

    # ==========================================
    # Schritte
    # ==========================================
    schritte_text = font.render(
        f"Schritte: {schritte} / {max_schritte}",
        True,
        WEISS
    )

    screen.blit(
        schritte_text,
        (35, 50)
    )

    # ==========================================
    # Optimal
    # ==========================================
    optimal_text = font.render(
        f"Optimal: {optimale_schritte}",
        True,
        GELB
    )

    screen.blit(
        optimal_text,
        (280, 50)
    )

    # ==========================================
    # Aktiver Hase
    # ==========================================
    hase_text = font.render(
        f"Aktiver Hase: {aktueller_hase_index + 1}",
        True,
        WEISS
    )

    screen.blit(
        hase_text,
        (500, 50)
    )

    # ==========================================
    # KI Status
    # ==========================================
    status = "KI Aktiv" if (solve_all_mode or pfad) else "Manuell"

    status_farbe = (
        (100, 255, 100)
        if solve_all_mode
        else
        (255, 255, 255)
    )

    status_text = font.render(
        status,
        True,
        status_farbe
    )

    screen.blit(
        status_text,
        (760, 50)
    )

# ==========================================================
# Progress Bar
# ==========================================================
def zeichne_progress_bar():

    progress = (aktuelles_level + 1) / len(LEVELS)

    bar_x = 320
    bar_y = 28

    bar_w = 350
    bar_h = 20

    pygame.draw.rect(
        screen,
        (70, 70, 70),
        (bar_x, bar_y, bar_w, bar_h),
        border_radius=10
    )

    pygame.draw.rect(
        screen,
        (255, 215, 0),
        (
            bar_x,
            bar_y,
            int(bar_w * progress),
            bar_h
        ),
        border_radius=10
    )

    text = font.render(
        f"{aktuelles_level + 1}/{len(LEVELS)}",
        True,
        WEISS
    )

    screen.blit(
        text,
        (bar_x + 140, bar_y - 3)
    )

# ==========================================================
# Ziel erreicht
# ==========================================================
def zeichne_ziel_erreicht():

    vergangene_zeit = pygame.time.get_ticks() - ziel_erreicht_start

    alpha = min(180, vergangene_zeit // 3)

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(alpha)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    glow = abs(math.sin(vergangene_zeit / 250))

    text_groesse = 70 + int(glow * 8)

    grosse_font = pygame.font.SysFont(None, text_groesse)

    text = grosse_font.render(
        "Ziel erreicht!",
        True,
        WEISS
    )

    text_rect = text.get_rect(
        center=(BREITE // 2, HOEHE // 2)
    )

    screen.blit(text, text_rect)


# ==========================================================
# Menü
# ==========================================================
def zeichne_menu():

    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 90)

    titel = titel_font.render(
        "SO HUEPFT DER HASE",
        True,
        WEISS
    )

    titel_rect = titel.get_rect(
        center=(BREITE // 2, 180)
    )

    screen.blit(titel, titel_rect)

    zeichne_menu_button(
        play_button,
        "PLAY"
    )

    zeichne_menu_button(
        levels_button,
        "LEVELS"
    )

    zeichne_menu_button(
        about_button,
    "ABOUT"
    )

    zeichne_menu_button(
        exit_button,
        "EXIT"
    )

# ==========================================================
# zeichne_levels
# ==========================================================

def zeichne_levels():

    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 80)

    titel = titel_font.render(
        "LEVEL AUSWAHL",
        True,
        WEISS
    )

    screen.blit(
        titel,
        (
            BREITE // 2 - titel.get_width() // 2,
            100
        )
    )

    for i, button in enumerate(level_buttons):

        zeichne_menu_button(
            button,
            f"LEVEL {i+1}"
        )

    info = font.render(
        "ESC = Zurück",
        True,
        WEISS
    )

    screen.blit(
        info,
        (
            BREITE // 2 - info.get_width() // 2,
            700
        )
    )

# ==========================================================
# zeichne_about
# ==========================================================

def zeichne_about():

    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 80)

    titel = titel_font.render(
        "ABOUT",
        True,
        WEISS
    )

    screen.blit(
        titel,
        (
            BREITE//2 - titel.get_width()//2,
            100
        )
    )

    texte = [
        "So Huepft Der Hase",
        "",
        "AI Features:",
        "- A* Pathfinding",
        "- Multiple Rabbits",
        "- Auto Solve",
        "",
        "UI Features:",
        "- Mouse Interaction",
        "- Level System",
        "- Animations",
        "",
        "ESC = Zurueck"
    ]

    y = 220

    for zeile in texte:

        txt = font.render(
            zeile,
            True,
            WEISS
        )

        screen.blit(
            txt,
            (
                BREITE//2 - txt.get_width()//2,
                y
            )
        )

        y += 40




# ==========================================================
# Effizienz
# ==========================================================
def berechne_effizienz():

    if schritte <= 0:
        return 100

    effizienz = int(
        (optimale_schritte / schritte) * 100
    )

    if effizienz > 100:
        effizienz = 100

    return effizienz

# ==========================================================
# Level geschafft
# ==========================================================
def zeichne_level_geschafft():

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(210)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 90)

    titel = titel_font.render(
        f"LEVEL {aktuelles_level + 1} GESCHAFFT!",
        True,
        (255, 220, 100)
    )

    titel_rect = titel.get_rect(
        center=(BREITE // 2, 220)
    )

    screen.blit(titel, titel_rect)

    bewertung_font = pygame.font.SysFont(None, 55)

    differenz = schritte - optimale_schritte

    if differenz <= 0:

        bewertung = "PERFEKT!"

    elif differenz <= 2:

        bewertung = "SEHR GUT!"

    else:

        bewertung = "GUT!"

    bewertung_text = bewertung_font.render(
        bewertung,
        True,
        WEISS
    )

    bewertung_rect = bewertung_text.get_rect(
        center=(BREITE // 2, 330)
    )

    screen.blit(bewertung_text, bewertung_rect)

    effizienz = berechne_effizienz()

    if effizienz >= 95:

        sterne = "★★★"

    elif effizienz >= 80:

         sterne = "★★"

    else:

         sterne = "★"

    info_font = pygame.font.SysFont(None, 45)

    spieler_text = info_font.render(
     f"Deine Schritte: {schritte}",
     True,
     WEISS
    )

    optimal_text = info_font.render(
        f"Optimale Schritte: {optimale_schritte}",
        True,
        GELB
    )

    effizienz_text = info_font.render(
        f"Effizienz: {effizienz} %",
        True,
        (100,255,100)
    )
    sterne_font = pygame.font.SysFont(None, 70)

    sterne_text = sterne_font.render(
        sterne,
        True,
        GELB
    )


    screen.blit(
        spieler_text,
        (100, 620)
    )

    screen.blit(
        optimal_text,
        (100, 670)
    )

    screen.blit(
        effizienz_text,
        (100, 720)
    )

    menu_font = pygame.font.SysFont(None, 50)

    zeilen = [
        "ENTER -> Nächstes Level",
        "R -> Neustart",
        "ESC -> Menü"
    ]

    y = 460

    for zeile in zeilen:

        text = menu_font.render(
            zeile,
            True,
            WEISS
        )

        rect = text.get_rect(
            center=(BREITE // 2, y)
        )

        screen.blit(text, rect)

        y += 70

    


# ==========================================================
# Final Win
# ==========================================================
def zeichne_final_win():

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(230)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 100)

    titel = titel_font.render(
        "ALLE 5 LEVEL GESCHAFFT!",
        True,
        (255, 215, 0)
    )

    titel_rect = titel.get_rect(
        center=(BREITE // 2, 250)
    )

    screen.blit(titel, titel_rect)

    info_font = pygame.font.SysFont(None, 55)

    text = info_font.render(
        "Du hast das ganze Spiel geschafft!",
        True,
        WEISS
    )

    rect = text.get_rect(
        center=(BREITE // 2, 420)
    )

    screen.blit(text, rect)

    esc = info_font.render(
        "ESC -> Menü",
        True,
        WEISS
    )

    esc_rect = esc.get_rect(
        center=(BREITE // 2, 520)
    )

    screen.blit(esc, esc_rect)


# ==========================================================
# Game Over
# ==========================================================
def zeichne_game_over():

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 90)

    titel = titel_font.render(
        "KEINE SCHRITTE MEHR!",
        True,
        (255, 80, 80)
    )

    titel_rect = titel.get_rect(
        center=(BREITE // 2, 250)
    )

    screen.blit(titel, titel_rect)

    info_font = pygame.font.SysFont(None, 50)

    texte = [
        "R -> Neustart",
        "ESC -> Menü"
    ]

    y = 420

    for zeile in texte:

        text = info_font.render(
            zeile,
            True,
            WEISS
        )

        rect = text.get_rect(
            center=(BREITE // 2, y)
        )

        screen.blit(text, rect)

        y += 80


# ==========================================================
# Erstes Level laden
# ==========================================================
lade_level(0)

# ==========================================================
# Hauptschleife
# ==========================================================
clock = pygame.time.Clock()

running = True

while running:

    for event in pygame.event.get():

    # ==========================================
    # QUIT
    # ==========================================
     if event.type == pygame.QUIT:

        running = False

    # ==========================================
    # MOUSE
    # ==========================================
     elif event.type == pygame.MOUSEBUTTONDOWN:

        mx, my = event.pos

        # ======================================
        # LEVEL SCREEN
        # ======================================
        if show_levels:

            for i, button in enumerate(level_buttons):

                if button.collidepoint(mx, my):

                    lade_level(i)

                    im_menu = False
                    show_levels = False
                    show_about = False

                    break

            continue

        # ======================================
        # ABOUT SCREEN
        # ======================================
        if show_about:

            continue

        # ======================================
        # MAIN MENU
        # ======================================
        if im_menu:

            if play_button.collidepoint(mx, my):

                lade_level(0)
                im_menu = False

            elif levels_button.collidepoint(mx, my):

                show_levels = True
                show_about = False

            elif about_button.collidepoint(mx, my):

                show_about = True
                show_levels = False

            elif exit_button.collidepoint(mx, my):

                running = False

            continue

        # ======================================
        # BLOCK INPUT
        # ======================================
        if game_over or level_geschafft or final_win:

            continue

        # ======================================
        # SOLVE BUTTON
        # ======================================
        if solve_button.collidepoint(mx, my):

            start = HASEN[aktueller_hase_index]

            ziel, neuer_pfad = finde_naechstes_loch(start)

            if neuer_pfad:

                pfad = neuer_pfad[1:]

            continue

        # ======================================
        # RESET BUTTON
        # ======================================
        if reset_button.collidepoint(mx, my):

            reset_spiel()

            continue

        # ======================================
        # MENU BUTTON
        # ======================================
        if menu_button.collidepoint(mx, my):

            im_menu = True
            show_levels = False
            show_about = False

            continue

        # ======================================
        # RABBIT SELECTION
        # ======================================
        feld = maus_zu_feld(mx, my)

        if feld is not None:

            for index, position in enumerate(HASEN):

                if position == feld:

                    aktueller_hase_index = index

                    pfad = []

                    solve_all_mode = False

                    auto_queue = []

                    break

    # ==========================================
    # KEYBOARD
    # ==========================================
     elif event.type == pygame.KEYDOWN:

        if show_levels:

            if event.key == pygame.K_ESCAPE:

                show_levels = False

            continue

        if show_about:

            if event.key == pygame.K_ESCAPE:

                show_about = False

            continue

        if final_win:

            if event.key == pygame.K_ESCAPE:

                final_win = False
                im_menu = True

            continue

        if game_over:

            if event.key == pygame.K_r:

                reset_spiel()

            elif event.key == pygame.K_ESCAPE:

                game_over = False
                im_menu = True

            continue

        if level_geschafft:

            if event.key == pygame.K_RETURN:

                if aktuelles_level < len(LEVELS) - 1:

                    lade_level(aktuelles_level + 1)

                else:

                    final_win = True

            elif event.key == pygame.K_r:

                reset_spiel()

            elif event.key == pygame.K_ESCAPE:

                level_geschafft = False
                im_menu = True

            continue

        if im_menu:

            if event.key == pygame.K_ESCAPE:

                running = False

            continue

        if event.key == pygame.K_r:

            reset_spiel()

        elif event.key == pygame.K_SPACE:

             solve_all_mode = False

             auto_queue = []

             start = HASEN[aktueller_hase_index]

             ziel, neuer_pfad = finde_naechstes_loch(start)

             if neuer_pfad:

                 pfad = neuer_pfad[1:]

# ==========================================
# ALL RABBITS A*
# ==========================================
        elif event.key == pygame.K_a:

            auto_queue = list(range(len(HASEN)))

            solve_all_mode = True

            if auto_queue:

                aktueller_hase_index = auto_queue.pop(0)

                start = HASEN[aktueller_hase_index]

                ziel, neuer_pfad = finde_naechstes_loch(start)

                if neuer_pfad:

                    pfad = neuer_pfad[1:]

        # ==========================================
        # MANUELLE BEWEGUNG
        # ==========================================
        elif event.key in (
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT
        ):

            zeile, spalte = HASEN[aktueller_hase_index]

            neue_pos = (zeile, spalte)

            if event.key == pygame.K_UP and zeile > 0:

                neue_pos = (zeile - 1, spalte)

            elif event.key == pygame.K_DOWN and zeile < ZEILEN - 1:

                neue_pos = (zeile + 1, spalte)

            elif event.key == pygame.K_LEFT and spalte > 0:

                neue_pos = (zeile, spalte - 1)

            elif event.key == pygame.K_RIGHT and spalte < SPALTEN - 1:

                neue_pos = (zeile, spalte + 1)

            if neue_pos not in HINDERNISSE:

              if neue_pos in HASEN and neue_pos not in LOECHER:

                pass

              else:

                HASEN[aktueller_hase_index] = neue_pos

                schritte += 1

                pfad = []

                solve_all_mode = False

                auto_queue = []


                if schritte >= max_schritte:

                    game_over = True

                if HASEN[aktueller_hase_index] in LOECHER:

                    ziel_erreicht = True
                    ziel_erreicht_start = pygame.time.get_ticks()

                if pruefe_level_geschafft():

                    level_geschafft = True


    # ======================================================
    # Animation
    # ======================================================
    if animating:

        animation_progress += animation_speed

        if animation_progress >= 1:

            animation_progress = 1
            animating = False

    # ======================================================
    # A* Bewegung
    # ======================================================
    aktuelle_zeit = pygame.time.get_ticks()

    if pfad and aktuelle_zeit - letzte_bewegung > BEWEGUNGS_DELAY:

        naechste_position = pfad.pop(0)

        animation_start = HASEN[aktueller_hase_index]
        animation_target = naechste_position

        animating = True
        animation_progress = 0

        HASEN[aktueller_hase_index] = naechste_position

        schritte += 1

        if schritte >= max_schritte:

            game_over = True

        letzte_bewegung = aktuelle_zeit

        if not pfad:

            if HASEN[aktueller_hase_index] in LOECHER:

                ziel_erreicht = True
                ziel_erreicht_start = pygame.time.get_ticks()

                if pruefe_level_geschafft():

                    level_geschafft = True

                if solve_all_mode and auto_queue:

                    aktueller_hase_index = auto_queue.pop(0)

                    start = HASEN[aktueller_hase_index]

                    ziel, neuer_pfad = finde_naechstes_loch(start)

                    if neuer_pfad:

                        pfad = neuer_pfad[1:]

                else:

                    solve_all_mode = False
                    auto_queue = []

    # ======================================================
    # Zeichnen
    # ======================================================
    if im_menu:

        if show_levels:

            zeichne_levels()

        elif show_about:

            zeichne_about()

        else:

            zeichne_menu()

    else:

        screen.blit(background_img, (0, 0))

        zeichne_grid()
        zeichne_hindernisse()
        zeichne_loecher()
        zeichne_pfad()
        zeichne_hasen()
        zeichne_text()
        zeichne_progress_bar()
        zeichne_buttons()

    # ======================================================
    # Ziel erreicht
    # ======================================================
    if ziel_erreicht and not level_geschafft:

        zeichne_ziel_erreicht()

        if pygame.time.get_ticks() - ziel_erreicht_start > 1200:

            ziel_erreicht = False

    # ======================================================
    # Level geschafft
    # ======================================================
    if level_geschafft:

        zeichne_level_geschafft()

    # ======================================================
    # Final Win
    # ======================================================
    if final_win:

        zeichne_final_win()

    # ======================================================
    # Game Over
    # ======================================================
    if game_over:

        zeichne_game_over()

    # ======================================================
    # Update
    # ======================================================
    pygame.display.flip()

    clock.tick(60)

# ==========================================================
# Ende
# ==========================================================
pygame.quit()
sys.exit()