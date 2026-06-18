import heapq  # مكتبة جاهزة لعمل Priority Queue، وهي مهمة لأن A* يحتاج دائماً اختيار أقل كلفة أولاً.


# ==========================================================
# دالة التقدير Heuristic
# ==========================================================
def heuristik(a, b):
    """
    تحسب مسافة Manhattan بين نقطتين داخل شبكة مربعة.

    اخترنا Manhattan لأن الحركة في اللعبة تكون باتجاهات أربعة فقط:
    فوق، تحت، يسار، يمين.
    لذلك لا توجد حركة قطرية، وهذه المعادلة تعطي تقديراً مناسباً لخوارزمية A*.

    مثال:
    a = (0, 0)
    b = (2, 3)

    النتيجة:
    |0 - 2| + |0 - 3| = 5
    """
    # a[0] و b[0] يمثلان رقم السطر، و a[1] و b[1] يمثلان رقم العمود.
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ==========================================================
# خوارزمية A*
# ==========================================================
def finde_weg(start, ziel, hindernisse, zeilen, spalten, blockierte_felder=None):
    """
    تبحث عن أقصر طريق من نقطة البداية إلى نقطة الهدف باستخدام خوارزمية A*.

    start:
        مكان البداية، مثل (0, 0).

    ziel:
        مكان الهدف، مثل (4, 4).

    hindernisse:
        قائمة الصخور أو العوائق التي لا يسمح للحارس/الأرنب بالمرور عليها.

    zeilen:
        عدد صفوف الشبكة.

    spalten:
        عدد أعمدة الشبكة.

    blockierte_felder:
        حقول إضافية ممنوعة، مثل أماكن الأرانب الأخرى حتى لا يصطدم بها الأرنب الحالي.

    ترجع:
        قائمة مواقع تمثل الطريق من البداية إلى الهدف.
        أو None إذا لم يوجد طريق ممكن.
    """

    # إذا لم يتم تمرير حقول إضافية ممنوعة، نبدأ بمجموعة فارغة.
    if blockierte_felder is None:
        blockierte_felder = set()
    else:
        # نحولها إلى set لأن البحث داخل set أسرع من البحث داخل list.
        blockierte_felder = set(blockierte_felder)

    # نسمح بالبداية والهدف حتى لو كانا ضمن الحقول المحجوزة بالخطأ.
    blockierte_felder.discard(start)
    blockierte_felder.discard(ziel)

    # نجمع العوائق الثابتة مع الحقول المحجوزة في مجموعة واحدة لتسهيل الفحص.
    gesperrte_felder = set(hindernisse) | blockierte_felder

    # Open List: قائمة الأولويات التي تحتوي العقد التي سنفحصها لاحقاً.
    offene_liste = []

    # نضيف نقطة البداية، والأولوية هي التقدير المبدئي من البداية إلى الهدف.
    heapq.heappush(
        offene_liste,
        (heuristik(start, ziel), start)
    )

    # هذا القاموس يحفظ من أين وصلنا لكل خلية، حتى نعيد بناء الطريق في النهاية.
    came_from = {}

    # g_score يخزن الكلفة الحقيقية من البداية إلى كل خلية.
    g_score = {
        start: 0
    }

    # f_score = الكلفة الحقيقية g + التقدير h، وهذا ما يعتمد عليه A* في ترتيب الفحص.
    f_score = {
        start: heuristik(start, ziel)
    }

    # الاتجاهات الممكنة للحركة: فوق، تحت، يسار، يمين.
    richtungen = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ]

    # نستمر طالما توجد خلايا مرشحة للفحص.
    while offene_liste:

        # نأخذ الخلية ذات أقل f_score، لأنها غالباً الأقرب للحل.
        _, aktuell = heapq.heappop(offene_liste)

        # إذا وصلنا للهدف، نبدأ ببناء الطريق النهائي.
        if aktuell == ziel:
            pfad = [aktuell]

            # نرجع للخلف من الهدف إلى البداية باستخدام came_from.
            while aktuell in came_from:
                aktuell = came_from[aktuell]
                pfad.append(aktuell)

            # الطريق بُني من الهدف للبداية، لذلك نعكسه ليصبح من البداية للهدف.
            pfad.reverse()
            return pfad

        # نفصل موقع الخلية الحالية إلى سطر وعمود لتسهيل حساب الجيران.
        zeile, spalte = aktuell

        # نفحص كل جار ممكن حسب الاتجاهات الأربعة.
        for dz, ds in richtungen:
            neue_zeile = zeile + dz
            neue_spalte = spalte + ds
            nachbar = (neue_zeile, neue_spalte)

            # نتأكد أن الجار داخل حدود الشبكة، وليس خارج اللوحة.
            if not (
                0 <= neue_zeile < zeilen
                and
                0 <= neue_spalte < spalten
            ):
                continue

            # نتجاهل الجار إذا كان صخرة أو خلية محجوزة من أرنب آخر.
            if nachbar in gesperrte_felder:
                continue

            # كل حركة في الشبكة تكلف خطوة واحدة.
            tentative_g = g_score[aktuell] + 1

            # إذا لم نزر الجار من قبل، أو وجدنا طريقاً أقصر إليه، نحدث معلوماته.
            if (
                nachbar not in g_score
                or
                tentative_g < g_score[nachbar]
            ):
                # نحفظ أن الخلية الحالية هي السابقة للجار في أفضل طريق معروف.
                came_from[nachbar] = aktuell

                # نحفظ الكلفة الجديدة من البداية إلى هذا الجار.
                g_score[nachbar] = tentative_g

                # نحسب f = g + h حتى نعرف أولوية فحص هذا الجار.
                f_score[nachbar] = (
                    tentative_g
                    +
                    heuristik(nachbar, ziel)
                )

                # نضيف الجار لقائمة الأولويات كي يتم فحصه لاحقاً.
                heapq.heappush(
                    offene_liste,
                    (f_score[nachbar], nachbar)
                )

    # إذا انتهت Open List ولم نصل للهدف، فهذا يعني أنه لا يوجد طريق ممكن.
    return None
