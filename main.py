# ==========================================================
# SO HUEPFT DER HASE
# مشروع لعبة Pygame يستخدم خوارزمية A* لحساب طريق الأرنب إلى الحفرة.
# ==========================================================

import pygame  # مكتبة الألعاب المسؤولة عن النافذة، الرسم، الصور، والأحداث.
import sys  # نستخدمها لإغلاق البرنامج بشكل نظيف في النهاية.
import math  # نستخدمها في تأثير النبض/اللمعان عند الوصول للهدف.
from search import finde_weg  # نستورد دالة A* التي تبحث عن أقصر طريق.


# ==========================================================
# تهيئة Pygame
# ==========================================================
pygame.init()  # يجب تشغيلها قبل استخدام أغلب وظائف Pygame.


# ==========================================================
# إعدادات النافذة
# ==========================================================
BREITE = 1000  # عرض نافذة اللعبة بالبكسل.
HOEHE = 800  # ارتفاع نافذة اللعبة بالبكسل.

screen = pygame.display.set_mode((BREITE, HOEHE))  # إنشاء نافذة الرسم الرئيسية.
pygame.display.set_caption("So huepft der Hase")  # عنوان النافذة.


# ==========================================================
# تحميل الصور
# ==========================================================
# convert_alpha يحافظ على شفافية الصورة، وهذا مهم للصور مثل الأرنب والحفرة.
rabbit_img = pygame.image.load("assets/rabbit.png").convert_alpha()
rabbit_img = pygame.transform.scale(rabbit_img, (70, 70))  # توحيد حجم الأرنب داخل الخلية.

hole_img = pygame.image.load("assets/holes.png").convert_alpha()
hole_img = pygame.transform.scale(hole_img, (90, 90))  # الحفرة أكبر قليلاً كي تظهر بوضوح.

rock_img = pygame.image.load("assets/rock.png").convert_alpha()
rock_img = pygame.transform.scale(rock_img, (70, 70))  # الصخرة تمثل العائق داخل الشبكة.

background_img = pygame.image.load("assets/background.png").convert()
background_img = pygame.transform.scale(background_img, (BREITE, HOEHE))  # الخلفية تغطي النافذة كاملة.


# ==========================================================
# الألوان
# ==========================================================
SCHWARZ = (0, 0, 0)  # لون أسود للتظليل.
ROT = (220, 50, 50)  # لون أحمر للحالات الخطرة أو الخسارة.
BLAU = (50, 100, 220)  # لون أزرق لتحديد الأرنب النشط.
GELB = (255, 215, 0)  # لون أصفر للهدف أو المسار أو النجوم.
WEISS = (255, 255, 255)  # لون أبيض للنصوص والحدود.
GRID_FARBE = (240, 240, 220)  # لون خلايا الشبكة.


# ==========================================================
# إعدادات الشبكة
# ==========================================================
ZEILEN = 5  # عدد الصفوف الافتراضي.
SPALTEN = 5  # عدد الأعمدة الافتراضي.
ZELLENGROESSE = 100  # حجم كل خلية بالبكسل.

GRID_BREITE = SPALTEN * ZELLENGROESSE  # عرض الشبكة الكامل.
GRID_HOEHE = ZEILEN * ZELLENGROESSE  # ارتفاع الشبكة الكامل.

START_X = (BREITE - GRID_BREITE) // 2  # بداية الشبكة أفقياً حتى تكون في الوسط.
START_Y = (HOEHE - GRID_HOEHE) // 2  # بداية الشبكة عمودياً حتى تكون في الوسط.


# ==========================================================
# الأزرار
# ==========================================================
solve_button = pygame.Rect(250, 730, 150, 50)  # زر حل الأرنب الحالي باستخدام A*.
reset_button = pygame.Rect(430, 730, 150, 50)  # زر إعادة المستوى من البداية.
menu_button = pygame.Rect(610, 730, 150, 50)  # زر العودة إلى القائمة.

play_button = pygame.Rect(350, 250, 300, 70)  # زر بدء اللعب من المستوى الأول.
levels_button = pygame.Rect(350, 350, 300, 70)  # زر اختيار مستوى.
about_button = pygame.Rect(350, 450, 300, 70)  # زر صفحة المعلومات.
exit_button = pygame.Rect(350, 550, 300, 70)  # زر الخروج من اللعبة.

level_buttons = []  # قائمة أزرار اختيار المستويات.
for i in range(5):
    # ننشئ خمسة أزرار متساوية، وكل زر يفتح مستوى مختلفاً.
    level_buttons.append(pygame.Rect(350, 220 + i * 90, 300, 60))


# ==========================================================
# بيانات المستويات
# ==========================================================
LEVELS = [
    {
        # hasen: أماكن الأرانب في بداية المستوى.
        "hasen": [(0, 0)],
        # loecher: أماكن الحفر التي يجب أن تصل إليها الأرانب.
        "loecher": [(4, 4)],
        # hindernisse: أماكن الصخور التي تمنع الحركة.
        "hindernisse": [(2, 2), (2, 4), (3, 2)],
        # optimale_schritte يستخدم لحساب تقييم اللاعب.
        "optimale_schritte": 9,
        # max_schritte هو الحد الأعلى قبل Game Over.
        "max_schritte": 10,
    },
    {
        "hasen": [(4, 0), (0, 4)],
        "loecher": [(0, 0), (4, 4)],
        "hindernisse": [(1, 1), (1, 2), (2, 2), (3, 2)],
        "optimale_schritte": 9,
        "max_schritte": 10,
    },
    {
        "hasen": [(2, 0), (4, 2)],
        "loecher": [(0, 2), (2, 4)],
        "hindernisse": [(1, 1), (1, 2), (1, 3), (2, 1), (3, 2), (3, 3)],
        "optimale_schritte": 16,
        "max_schritte": 18,
    },
    {
        # grid يغير حجم الشبكة لهذا المستوى من 5x5 إلى 6x6.
        "grid": 6,
        "hasen": [(0, 0), (5, 1), (3, 0)],
        "loecher": [(5, 5), (0, 5), (2, 4)],
        "hindernisse": [(1, 1), (1, 2), (1, 4), (2, 2), (2, 3), (3, 1), (3, 3), (4, 2), (4, 4)],
        "optimale_schritte": 24,
        "max_schritte": 26,
    },
    {
        "grid": 6,
        "hasen": [(0, 1), (5, 4), (3, 0)],
        "loecher": [(0, 5), (5, 0), (2, 5)],
        "hindernisse": [(1, 1), (1, 2), (1, 4), (2, 2), (3, 1), (3, 4), (4, 1), (4, 3)],
        "optimale_schritte": 24,
        "max_schritte": 26,
    },
]


# ==========================================================
# حالة اللعبة العامة
# ==========================================================
aktuelles_level = 0  # رقم المستوى الحالي داخل القائمة LEVELS.

HASEN = []  # أماكن الأرانب الحالية أثناء اللعب.
LOECHER = []  # أماكن الحفر في المستوى الحالي.
HINDERNISSE = []  # أماكن العوائق في المستوى الحالي.
START_HASEN = []  # نسخة من أماكن بداية الأرانب لإعادة المستوى.

aktueller_hase_index = 0  # الأرنب المحدد حالياً للتحريك أو الحل.
pfad = []  # المسار الذي تحسبه خوارزمية A* للأرنب الحالي.

letzte_bewegung = 0  # وقت آخر حركة تلقائية، لمنع الحركة السريعة جداً.
BEWEGUNGS_DELAY = 300  # مدة الانتظار بين خطوات الحل التلقائي بالميلي ثانية.

ziel_erreicht = False  # يحدد إن كان الأرنب وصل للتو إلى حفرة.
ziel_erreicht_start = 0  # وقت بداية تأثير "تم الوصول".

auto_queue = []  # قائمة أرقام الأرانب التي سيحلها وضع الحل الكامل.
solve_all_mode = False  # True عندما نستخدم A* لكل الأرانب بالتتابع.

schritte = 0  # عدد خطوات اللاعب أو الحل التلقائي.
max_schritte = 0  # الحد الأقصى للخطوات في المستوى الحالي.
optimale_schritte = 0  # عدد الخطوات المثالي للمقارنة.

im_menu = True  # هل اللاعب في القائمة الرئيسية؟
level_geschafft = False  # هل تم إنهاء المستوى؟
game_over = False  # هل انتهت الخطوات المسموحة؟
final_win = False  # هل تم إنهاء كل المستويات؟
show_levels = False  # هل شاشة اختيار المستويات ظاهرة؟
show_about = False  # هل شاشة المعلومات ظاهرة؟

animating = False  # هل يوجد أرنب يتحرك الآن بين خليتين؟
animation_start = (0, 0)  # خلية بداية الحركة المتحركة.
animation_target = (0, 0)  # خلية نهاية الحركة المتحركة.
animation_progress = 0  # نسبة التقدم بين البداية والنهاية من 0 إلى 1.
animation_speed = 0.08  # سرعة الحركة المرئية.

font = pygame.font.SysFont(None, 38)  # الخط الأساسي المستخدم في الأزرار والنصوص.


# ==========================================================
# تحميل مستوى
# ==========================================================
def lade_level(level_index):
    """يحمل بيانات مستوى معين ويعيد كل حالات اللعب إلى البداية."""
    global aktuelles_level, HASEN, LOECHER, HINDERNISSE, START_HASEN
    global pfad, auto_queue, solve_all_mode, aktueller_hase_index
    global level_geschafft, schritte, max_schritte, optimale_schritte, game_over
    global ZEILEN, SPALTEN, GRID_BREITE, GRID_HOEHE, START_X, START_Y

    aktuelles_level = level_index  # نحفظ المستوى الحالي حتى يظهر في الواجهة.
    level = LEVELS[level_index]  # نجلب قاموس بيانات المستوى.

    # بعض المستويات تستخدم شبكة 6x6، وإذا لم توجد قيمة grid نرجع إلى 5x5.
    if "grid" in level:
        ZEILEN = level["grid"]
        SPALTEN = level["grid"]
    else:
        ZEILEN = 5
        SPALTEN = 5

    # بعد تغيير حجم الشبكة يجب إعادة حساب أبعادها ومكانها.
    GRID_BREITE = SPALTEN * ZELLENGROESSE
    GRID_HOEHE = ZEILEN * ZELLENGROESSE
    START_X = (BREITE - GRID_BREITE) // 2
    START_Y = (HOEHE - GRID_HOEHE) // 2

    HASEN = level["hasen"].copy()  # copy حتى لا نغير بيانات المستوى الأصلية.
    LOECHER = level["loecher"]
    HINDERNISSE = level["hindernisse"]
    START_HASEN = HASEN.copy()  # نحتاجها عند الضغط على Reset.

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
# رسم أزرار اللعب
# ==========================================================
def zeichne_buttons():
    """يرسم أزرار Solve و Reset و Menu مع تأثير عند مرور الماوس."""
    maus_x, maus_y = pygame.mouse.get_pos()  # نحتاج موقع الماوس لتغيير لون الزر عند hover.

    buttons = [
        (solve_button, "Solve", (70, 140, 255)),
        (reset_button, "Reset", (255, 180, 60)),
        (menu_button, "Menu", (255, 80, 80)),
    ]

    for button, text, color in buttons:
        aktuelle_farbe = color  # اللون الأساسي للزر.

        if button.collidepoint(maus_x, maus_y):
            # نفتح اللون قليلاً عندما يكون الماوس فوق الزر.
            aktuelle_farbe = (
                min(color[0] + 40, 255),
                min(color[1] + 40, 255),
                min(color[2] + 40, 255),
            )

            # مستطيل أبيض أكبر قليلاً يعمل كتأثير ظل/إضاءة حول الزر.
            shadow_rect = button.inflate(12, 12)
            pygame.draw.rect(screen, WEISS, shadow_rect, border_radius=18)

        pygame.draw.rect(screen, aktuelle_farbe, button, border_radius=15)
        pygame.draw.rect(screen, WEISS, button, 2, border_radius=15)

        text_surface = font.render(text, True, WEISS)  # نحول النص إلى سطح يمكن رسمه.
        text_rect = text_surface.get_rect(center=button.center)  # نوسّط النص داخل الزر.
        screen.blit(text_surface, text_rect)


# ==========================================================
# رسم زر في القائمة
# ==========================================================
def zeichne_menu_button(rect, text):
    """يرسم زر قائمة واحد، ويغير لونه إذا كان الماوس فوقه."""
    mx, my = pygame.mouse.get_pos()
    farbe = (70, 70, 70)

    if rect.collidepoint(mx, my):
        farbe = (120, 120, 120)

    pygame.draw.rect(screen, farbe, rect, border_radius=15)
    pygame.draw.rect(screen, WEISS, rect, 2, border_radius=15)

    text_surface = font.render(text, True, WEISS)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


# ==========================================================
# إعادة المستوى
# ==========================================================
def reset_spiel():
    """يعيد الأرنب/الأرانب والخطوات وحالة الحل إلى بداية المستوى الحالي."""
    global HASEN, aktueller_hase_index, pfad, auto_queue, solve_all_mode
    global level_geschafft, schritte, game_over

    HASEN = START_HASEN.copy()
    aktueller_hase_index = 0
    pfad = []
    auto_queue = []
    solve_all_mode = False
    level_geschafft = False
    schritte = 0
    game_over = False


# ==========================================================
# تحويل خلية إلى موقع رسم
# ==========================================================
def feld_position(zeile, spalte):
    """يحول رقم السطر والعمود إلى إحداثيات بكسل داخل النافذة."""
    x = START_X + spalte * ZELLENGROESSE
    y = START_Y + zeile * ZELLENGROESSE
    return x, y


# ==========================================================
# تحويل موقع الماوس إلى خلية
# ==========================================================
def maus_zu_feld(mx, my):
    """يعرف أي خلية ضغط عليها اللاعب بالماوس، أو يرجع None إذا كانت خارج الشبكة."""
    if mx < START_X or my < START_Y:
        return None

    spalte = (mx - START_X) // ZELLENGROESSE
    zeile = (my - START_Y) // ZELLENGROESSE

    if 0 <= zeile < ZEILEN and 0 <= spalte < SPALTEN:
        return (zeile, spalte)

    return None


# ==========================================================
# فحص إنهاء المستوى
# ==========================================================
def pruefe_level_geschafft():
    """يرجع True فقط إذا كان كل أرنب موجوداً داخل حفرة."""
    for hase in HASEN:
        if hase not in LOECHER:
            return False
    return True


# ==========================================================
# اختيار أقرب حفرة ممكنة
# ==========================================================
def finde_naechstes_loch(start):
    """يحسب أفضل حفرة للأرنب الحالي حسب أقصر مسار A* متاح."""
    beste_pfad = None
    bestes_loch = None
    andere_hasen = []  # هذه الحقول ستمنع الأرنب الحالي من المرور فوق أرانب أخرى.

    for i, pos in enumerate(HASEN):
        if i == aktueller_hase_index:
            continue

        # إذا كان الأرنب الآخر لم يصل إلى حفرة، نعتبر مكانه محجوزاً.
        if pos not in LOECHER:
            andere_hasen.append(pos)

    for loch in LOECHER:
        # نجرب كل حفرة ونطلب من A* حساب طريق لها.
        pfad_test = finde_weg(start, loch, HINDERNISSE, ZEILEN, SPALTEN, andere_hasen)

        if pfad_test is None:
            continue

        # نختار أقصر مسار بين كل الحفر الممكن الوصول إليها.
        if beste_pfad is None or len(pfad_test) < len(beste_pfad):
            beste_pfad = pfad_test
            bestes_loch = loch

    return bestes_loch, beste_pfad


# ==========================================================
# رسم الشبكة
# ==========================================================
def zeichne_grid():
    """يرسم خلايا الشبكة وحدود كل خلية."""
    for zeile in range(ZEILEN):
        for spalte in range(SPALTEN):
            x, y = feld_position(zeile, spalte)
            rect = pygame.Rect(x, y, ZELLENGROESSE, ZELLENGROESSE)
            pygame.draw.rect(screen, GRID_FARBE, rect)
            pygame.draw.rect(screen, (80, 80, 80), rect, 1)


# ==========================================================
# رسم العوائق
# ==========================================================
def zeichne_hindernisse():
    """يرسم صورة الصخرة فوق كل خلية ممنوعة."""
    for zeile, spalte in HINDERNISSE:
        x, y = feld_position(zeile, spalte)
        screen.blit(rock_img, (x + 18, y + 10))


# ==========================================================
# رسم الحفر
# ==========================================================
def zeichne_loecher():
    """يرسم الحفر التي يجب أن تصل إليها الأرانب."""
    for zeile, spalte in LOECHER:
        x, y = feld_position(zeile, spalte)
        screen.blit(hole_img, (x + 5, y + 5))


# ==========================================================
# رسم مسار A*
# ==========================================================
def zeichne_pfad():
    """يرسم نقاطاً صفراء على المسار الذي حسبته خوارزمية A*."""
    for zeile, spalte in pfad:
        x, y = feld_position(zeile, spalte)
        rect = pygame.Rect(x + 35, y + 35, 30, 30)
        pygame.draw.rect(screen, GELB, rect, border_radius=15)


# ==========================================================
# رسم الأرانب
# ==========================================================
def zeichne_hasen():
    """يرسم الأرانب، ويظهر إطاراً أزرق حول الأرنب النشط."""
    for index, (zeile, spalte) in enumerate(HASEN):
        if animating and index == aktueller_hase_index:
            # أثناء الحركة التلقائية نرسم الأرنب بين خليتين حسب animation_progress.
            start_x, start_y = feld_position(animation_start[0], animation_start[1])
            ziel_x, ziel_y = feld_position(animation_target[0], animation_target[1])
            x = start_x + (ziel_x - start_x) * animation_progress
            y = start_y + (ziel_y - start_y) * animation_progress
        else:
            x, y = feld_position(zeile, spalte)

        if index == aktueller_hase_index:
            # الإطار الأزرق يساعد اللاعب يعرف أي أرنب يتحكم به الآن.
            rahmen = pygame.Rect(x + 5, y + 5, 90, 90)
            pygame.draw.rect(screen, BLAU, rahmen, 4, border_radius=12)

        screen.blit(rabbit_img, (x + 15, y + 10))


# ==========================================================
# رسم معلومات اللعب
# ==========================================================
def zeichne_text():
    """يرسم لوحة المعلومات العلوية: المستوى، الخطوات، الأرنب النشط، وحالة الذكاء."""
    panel = pygame.Rect(15, 10, BREITE - 30, 85)
    pygame.draw.rect(screen, (25, 25, 25), panel, border_radius=15)
    pygame.draw.rect(screen, (180, 180, 180), panel, 2, border_radius=15)

    level_font = pygame.font.SysFont(None, 42)
    level_text = level_font.render(f"Level {aktuelles_level + 1}", True, WEISS)
    screen.blit(level_text, (35, 25))

    schritte_text = font.render(f"Schritte: {schritte} / {max_schritte}", True, WEISS)
    screen.blit(schritte_text, (35, 50))

    optimal_text = font.render(f"Optimal: {optimale_schritte}", True, GELB)
    screen.blit(optimal_text, (280, 50))

    hase_text = font.render(f"Aktiver Hase: {aktueller_hase_index + 1}", True, WEISS)
    screen.blit(hase_text, (500, 50))

    # إذا كان يوجد مسار أو حل كامل، نعرض أن الذكاء الاصطناعي يعمل.
    status = "KI Aktiv" if (solve_all_mode or pfad) else "Manuell"
    status_farbe = (100, 255, 100) if solve_all_mode else WEISS
    status_text = font.render(status, True, status_farbe)
    screen.blit(status_text, (760, 50))


# ==========================================================
# شريط التقدم
# ==========================================================
def zeichne_progress_bar():
    """يرسم شريطاً يوضح تقدم اللاعب بين المستويات."""
    progress = (aktuelles_level + 1) / len(LEVELS)
    bar_x = 320
    bar_y = 28
    bar_w = 350
    bar_h = 20

    pygame.draw.rect(screen, (70, 70, 70), (bar_x, bar_y, bar_w, bar_h), border_radius=10)
    pygame.draw.rect(screen, GELB, (bar_x, bar_y, int(bar_w * progress), bar_h), border_radius=10)

    text = font.render(f"{aktuelles_level + 1}/{len(LEVELS)}", True, WEISS)
    screen.blit(text, (bar_x + 140, bar_y - 3))


# ==========================================================
# تأثير الوصول إلى الهدف
# ==========================================================
def zeichne_ziel_erreicht():
    """يعرض طبقة شفافة ونصاً نابضاً عندما يصل الأرنب إلى حفرة."""
    vergangene_zeit = pygame.time.get_ticks() - ziel_erreicht_start
    alpha = min(180, vergangene_zeit // 3)  # تزيد الشفافية تدريجياً.

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(alpha)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    glow = abs(math.sin(vergangene_zeit / 250))  # sin يعطي تأثير تكبير وتصغير ناعم.
    text_groesse = 70 + int(glow * 8)
    grosse_font = pygame.font.SysFont(None, text_groesse)

    text = grosse_font.render("Ziel erreicht!", True, WEISS)
    text_rect = text.get_rect(center=(BREITE // 2, HOEHE // 2))
    screen.blit(text, text_rect)


# ==========================================================
# القائمة الرئيسية
# ==========================================================
def zeichne_menu():
    """يرسم شاشة البداية وأزرار القائمة الرئيسية."""
    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(180)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 90)
    titel = titel_font.render("SO HUEPFT DER HASE", True, WEISS)
    titel_rect = titel.get_rect(center=(BREITE // 2, 180))
    screen.blit(titel, titel_rect)

    zeichne_menu_button(play_button, "PLAY")
    zeichne_menu_button(levels_button, "LEVELS")
    zeichne_menu_button(about_button, "ABOUT")
    zeichne_menu_button(exit_button, "EXIT")


# ==========================================================
# شاشة اختيار المستويات
# ==========================================================
def zeichne_levels():
    """يرسم أزرار اختيار المستوى."""
    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(200)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 80)
    titel = titel_font.render("LEVEL AUSWAHL", True, WEISS)
    screen.blit(titel, (BREITE // 2 - titel.get_width() // 2, 100))

    for i, button in enumerate(level_buttons):
        zeichne_menu_button(button, f"LEVEL {i + 1}")

    info = font.render("ESC = Zurueck", True, WEISS)
    screen.blit(info, (BREITE // 2 - info.get_width() // 2, 700))


# ==========================================================
# شاشة المعلومات
# ==========================================================
def zeichne_about():
    """يرسم معلومات مختصرة عن ميزات اللعبة."""
    screen.blit(background_img, (0, 0))

    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(220)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 80)
    titel = titel_font.render("ABOUT", True, WEISS)
    screen.blit(titel, (BREITE // 2 - titel.get_width() // 2, 100))

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
        "ESC = Zurueck",
    ]

    y = 220
    for zeile in texte:
        txt = font.render(zeile, True, WEISS)
        screen.blit(txt, (BREITE // 2 - txt.get_width() // 2, y))
        y += 40


# ==========================================================
# حساب الكفاءة
# ==========================================================
def berechne_effizienz():
    """يقارن خطوات اللاعب بالخطوات المثالية ويحولها إلى نسبة مئوية."""
    if schritte <= 0:
        return 100

    effizienz = int((optimale_schritte / schritte) * 100)

    if effizienz > 100:
        effizienz = 100

    return effizienz


# ==========================================================
# شاشة إنهاء المستوى
# ==========================================================
def zeichne_level_geschafft():
    """يرسم شاشة التقييم بعد حل المستوى."""
    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(210)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 90)
    titel = titel_font.render(f"LEVEL {aktuelles_level + 1} GESCHAFFT!", True, (255, 220, 100))
    titel_rect = titel.get_rect(center=(BREITE // 2, 220))
    screen.blit(titel, titel_rect)

    differenz = schritte - optimale_schritte
    if differenz <= 0:
        bewertung = "PERFEKT!"
    elif differenz <= 2:
        bewertung = "SEHR GUT!"
    else:
        bewertung = "GUT!"

    bewertung_font = pygame.font.SysFont(None, 55)
    bewertung_text = bewertung_font.render(bewertung, True, WEISS)
    bewertung_rect = bewertung_text.get_rect(center=(BREITE // 2, 330))
    screen.blit(bewertung_text, bewertung_rect)

    effizienz = berechne_effizienz()
    if effizienz >= 95:
        sterne = "***"
    elif effizienz >= 80:
        sterne = "**"
    else:
        sterne = "*"

    sterne_font = pygame.font.SysFont(None, 70)
    sterne_text = sterne_font.render(sterne, True, GELB)
    sterne_rect = sterne_text.get_rect(center=(BREITE // 2, 390))
    screen.blit(sterne_text, sterne_rect)

    menu_font = pygame.font.SysFont(None, 50)
    zeilen = ["ENTER -> Naechstes Level", "R -> Neustart", "ESC -> Menue"]
    y = 470
    for zeile in zeilen:
        text = menu_font.render(zeile, True, WEISS)
        rect = text.get_rect(center=(BREITE // 2, y))
        screen.blit(text, rect)
        y += 60

    info_font = pygame.font.SysFont(None, 45)
    spieler_text = info_font.render(f"Deine Schritte: {schritte}", True, WEISS)
    optimal_text = info_font.render(f"Optimale Schritte: {optimale_schritte}", True, GELB)
    effizienz_text = info_font.render(f"Effizienz: {effizienz} %", True, (100, 255, 100))

    screen.blit(spieler_text, (100, 620))
    screen.blit(optimal_text, (100, 670))
    screen.blit(effizienz_text, (100, 720))


# ==========================================================
# شاشة الفوز النهائي
# ==========================================================
def zeichne_final_win():
    """تظهر بعد إنهاء كل المستويات."""
    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(230)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 100)
    titel = titel_font.render("ALLE 5 LEVEL GESCHAFFT!", True, GELB)
    titel_rect = titel.get_rect(center=(BREITE // 2, 250))
    screen.blit(titel, titel_rect)

    info_font = pygame.font.SysFont(None, 55)
    text = info_font.render("Du hast das ganze Spiel geschafft!", True, WEISS)
    rect = text.get_rect(center=(BREITE // 2, 420))
    screen.blit(text, rect)

    esc = info_font.render("ESC -> Menue", True, WEISS)
    esc_rect = esc.get_rect(center=(BREITE // 2, 520))
    screen.blit(esc, esc_rect)


# ==========================================================
# شاشة الخسارة
# ==========================================================
def zeichne_game_over():
    """تظهر عندما يصل اللاعب إلى الحد الأقصى من الخطوات."""
    overlay = pygame.Surface((BREITE, HOEHE))
    overlay.set_alpha(220)
    overlay.fill(SCHWARZ)
    screen.blit(overlay, (0, 0))

    titel_font = pygame.font.SysFont(None, 90)
    titel = titel_font.render("KEINE SCHRITTE MEHR!", True, ROT)
    titel_rect = titel.get_rect(center=(BREITE // 2, 250))
    screen.blit(titel, titel_rect)

    info_font = pygame.font.SysFont(None, 50)
    texte = ["R -> Neustart", "ESC -> Menue"]
    y = 420
    for zeile in texte:
        text = info_font.render(zeile, True, WEISS)
        rect = text.get_rect(center=(BREITE // 2, y))
        screen.blit(text, rect)
        y += 80


# ==========================================================
# بدء اللعبة
# ==========================================================
lade_level(0)  # نحمّل أول مستوى حتى تكون بيانات اللعبة جاهزة.
clock = pygame.time.Clock()  # يتحكم بسرعة الحلقة الرئيسية.
running = True  # طالما True تستمر اللعبة بالعمل.


# ==========================================================
# الحلقة الرئيسية
# ==========================================================
while running:
    # ------------------------------------------------------
    # قراءة الأحداث: إغلاق النافذة، الماوس، الكيبورد.
    # ------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos  # مكان ضغطة الماوس.

            if show_levels:
                # إذا كنا في شاشة المستويات، أي ضغط على زر مستوى يحمّل ذلك المستوى.
                for i, button in enumerate(level_buttons):
                    if button.collidepoint(mx, my):
                        lade_level(i)
                        im_menu = False
                        show_levels = False
                        show_about = False
                        break
                continue

            if show_about:
                # شاشة About لا تحتاج أزرار بالماوس، الرجوع يتم بـ ESC.
                continue

            if im_menu:
                # أزرار القائمة الرئيسية.
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

            if game_over or level_geschafft or final_win:
                # عند ظهور شاشة نهاية، نمنع اللاعب من تحريك الأرانب بالماوس.
                continue

            if solve_button.collidepoint(mx, my):
                # زر Solve يحسب مساراً للأرنب النشط فقط.
                start = HASEN[aktueller_hase_index]
                ziel, neuer_pfad = finde_naechstes_loch(start)
                if neuer_pfad:
                    pfad = neuer_pfad[1:]  # نحذف أول عنصر لأنه هو مكان الأرنب الحالي.
                continue

            if reset_button.collidepoint(mx, my):
                reset_spiel()
                continue

            if menu_button.collidepoint(mx, my):
                im_menu = True
                show_levels = False
                show_about = False
                continue

            # إذا ضغط اللاعب على خلية فيها أرنب، نجعل هذا الأرنب هو النشط.
            feld = maus_zu_feld(mx, my)
            if feld is not None:
                for index, position in enumerate(HASEN):
                    if position == feld:
                        aktueller_hase_index = index
                        pfad = []
                        solve_all_mode = False
                        auto_queue = []
                        break

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
                    # ENTER ينتقل للمستوى التالي، أو يفتح شاشة الفوز النهائي بعد آخر مستوى.
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
                # Space يحسب مسار A* للأرنب الحالي مثل زر Solve.
                solve_all_mode = False
                auto_queue = []
                start = HASEN[aktueller_hase_index]
                ziel, neuer_pfad = finde_naechstes_loch(start)
                if neuer_pfad:
                    pfad = neuer_pfad[1:]

            elif event.key == pygame.K_a:
                # حرف A يشغل الحل الكامل لكل الأرانب بالتتابع.
                auto_queue = list(range(len(HASEN)))
                solve_all_mode = True

                if auto_queue:
                    aktueller_hase_index = auto_queue.pop(0)
                    start = HASEN[aktueller_hase_index]
                    ziel, neuer_pfad = finde_naechstes_loch(start)
                    if neuer_pfad:
                        pfad = neuer_pfad[1:]

            elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                # الأسهم تحرك الأرنب النشط يدوياً خطوة واحدة.
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
                    # لا نسمح بالوقوف فوق أرنب آخر إلا إذا كان ذلك الأرنب داخل حفرة.
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

    # ------------------------------------------------------
    # تحديث الأنيميشن.
    # ------------------------------------------------------
    if animating:
        animation_progress += animation_speed
        if animation_progress >= 1:
            animation_progress = 1
            animating = False

    # ------------------------------------------------------
    # تنفيذ حركة A* خطوة بخطوة.
    # ------------------------------------------------------
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

                # في وضع حل الكل، ننتقل للأرنب التالي بعد وصول الحالي.
                if solve_all_mode and auto_queue:
                    aktueller_hase_index = auto_queue.pop(0)
                    start = HASEN[aktueller_hase_index]
                    ziel, neuer_pfad = finde_naechstes_loch(start)
                    if neuer_pfad:
                        pfad = neuer_pfad[1:]
                else:
                    solve_all_mode = False
                    auto_queue = []

    # ------------------------------------------------------
    # الرسم: نختار الشاشة المناسبة حسب حالة اللعبة.
    # ------------------------------------------------------
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

    # ------------------------------------------------------
    # طبقات النهاية أو الرسائل المؤقتة.
    # ------------------------------------------------------
    if ziel_erreicht and not level_geschafft:
        zeichne_ziel_erreicht()
        if pygame.time.get_ticks() - ziel_erreicht_start > 1200:
            ziel_erreicht = False

    if level_geschafft:
        zeichne_level_geschafft()

    if final_win:
        zeichne_final_win()

    if game_over:
        zeichne_game_over()

    # ------------------------------------------------------
    # تحديث الشاشة وتثبيت سرعة اللعبة.
    # ------------------------------------------------------
    pygame.display.flip()
    clock.tick(60)


# ==========================================================
# إغلاق اللعبة
# ==========================================================
pygame.quit()  # إغلاق موارد Pygame.
sys.exit()  # إنهاء البرنامج.
