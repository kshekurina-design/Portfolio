# Generates ddx-fitness.html (case study page). Run: python3 tools/build_ddx.py
import struct, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
V = '15'

def size(name):
    b = (root / 'assets/ddx' / f'{name}.png').read_bytes()
    return struct.unpack('>II', b[16:24])

def shot(name, cap, cls=''):
    w, h = size(name)
    crop = h > 1000 and 'shot--blur' not in cls
    c = 'shot' + (' shot--crop' if crop else '') + (' ' + cls if cls else '')
    badge = '<span class="shot__badge">Ещё не в проде</span>' if 'shot--blur' in cls else ''
    zoom = '' if 'shot--blur' in cls else ' data-zoom'
    return (f'<figure class="{c}"><div class="shot__frame">'
            f'<img src="assets/ddx/{name}.png" width="{w}" height="{h}" loading="lazy" alt="{cap}"{zoom}>{badge}</div>'
            f'<figcaption>{cap}</figcaption></figure>')

def shots(*items, cls=''):
    c = 'shots' + (' ' + cls if cls else '')
    return f'<div class="{c}">' + ''.join(shot(*i) for i in items) + '</div>'

def ul(*items):
    return '<ul class="case-list">' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'

def note(text, label='Вывод'):
    return f'<p class="case-note"><span class="case-note__label">{label}</span>{text}</p>'

def stage(num, title, sub, body, open_=False):
    o = ' is-open' if open_ else ''
    e = 'true' if open_ else 'false'
    return f'''
        <article class="acc__item{o}">
          <button class="acc__head" type="button" aria-expanded="{e}" aria-controls="stage-{num}">
            <span class="acc__num">{num}</span>
            <span class="acc__titles"><span class="acc__title">{title}</span><span class="acc__sub">{sub}</span></span>
            <span class="acc__btn" aria-hidden="true"><i></i><i></i></span>
          </button>
          <div class="acc__panel" id="stage-{num}"><div class="acc__inner"><div class="acc__body">{body}</div></div></div>
        </article>'''

s01 = f'''
<div class="case-text">
  <p>DDX Fitness развивал концепцию SuperApp — приложения, которое помогает не только посещать клуб, но и планировать тренировки, управлять активностями и отслеживать прогресс. Для этого тренировочным продуктам нужно было единое пространство.</p>
  <h3 class="case-h">Что должен уметь пользователь</h3>
  {ul('Быстро найти подходящий тип тренировки', 'Посмотреть активности на сегодня и следующие дни', 'Запланировать тренировку', 'Различать типы занятий', 'Видеть предстоящие тренировки в одном месте', 'В дальнейшем использовать календарь для новых тренировочных форматов')}
</div>
<h3 class="case-h">Как было устроено приложение</h3>
<div class="arch">
  <div class="arch__row"><span class="arch__node">Групповые</span><span class="arch__arrow">→</span><span class="arch__path">отдельный раздел «Расписание»</span></div>
  <div class="arch__row"><span class="arch__node">Самостоятельные</span><span class="arch__arrow">→</span><span class="arch__path">Профиль → Дневник тренировок</span></div>
  <div class="arch__row"><span class="arch__node">Action</span><span class="arch__arrow">→</span><span class="arch__path">отдельная вкладка приложения</span></div>
  <div class="arch__row"><span class="arch__node">Персональные</span><span class="arch__arrow">→</span><span class="arch__path">страницы тренеров, без единого сценария</span></div>
</div>
{shots(('old-home', 'Главная: блок «Расписание»'), ('old-schedule', 'Расписание групповых'), ('old-diary', 'Дневник тренировок'))}
{note('Задача заключалась не в создании нового календарного экрана, а в переосмыслении способа доступа к тренировочным продуктам.')}
'''

s02 = f'''
<div class="case-grid3">
  <div class="case-card"><span class="case-card__num">1</span><h3 class="case-h">Групповые</h3><p>Раздел был доступен, но пользователям было непросто разобраться с фильтрами и датами.</p></div>
  <div class="case-card"><span class="case-card__num">2</span><h3 class="case-h">Самостоятельные</h3><p>Тренировки находились внутри дневника, который сначала нужно было найти через профиль.</p></div>
  <div class="case-card"><span class="case-card__num">3</span><h3 class="case-h">Action</h3><p>Существовал как отдельный продукт, ценность которого была понятна не всем пользователям.</p></div>
</div>
<div class="case-text"><p>Мы опирались на данные использования разделов, глубинные интервью и поведенческие метрики.</p></div>
<h3 class="case-h">Before: отдельные точки входа</h3>
{shots(('old-home', 'Главная'), ('old-schedule', 'Расписание групповых'), ('old-group', 'Карточка групповой тренировки'), ('old-profile', 'Профиль — вход в дневник'), ('old-diary', 'Дневник тренировок'), ('old-trainer', 'Профиль тренера'))}
{note('У каждого типа тренировок был собственный путь, и пользователю приходилось помнить, где что находится.')}
'''

s03 = f'''
<div class="case-cols">
  <div class="case-text">
    <h3 class="case-h">Методы</h3>
    {ul('Глубинные интервью', 'Анализ продуктовой аналитики', 'Анализ бенчмарков', 'Usability-тестирование интерактивных прототипов')}
    <p>Организацию и проведение исследований вёл исследователь. Я определяла продуктовые вопросы, гипотезы и варианты решений, готовила прототипы и участвовала в анализе результатов.</p>
    <p>При отборе участников учитывали пол, возраст, опыт в фитнесе, занятия спортом и опыт использования приложения DDX.</p>
  </div>
  <div class="case-fact"><span class="case-fact__value">100+</span><span class="case-fact__label">человек приняли участие в тестировании прототипов на разных этапах — это суммарная цифра, а не размер одного теста</span></div>
</div>
<h3 class="case-h">Ключевой инсайт</h3>
<div class="case-cols case-cols--shot">
  {shots(('tabs-v1', 'Вариант с выпадающим single-select'))}
  <div class="case-text"><p>Переключение типа тренировки через выпадающий single-select оказалось недостаточно понятным: пользователи не всегда замечали, что тип можно сменить.</p>
  {note('Навигация должна показывать доступные типы занятий, а не скрывать их внутри дополнительных действий.')}</div>
</div>
'''

s04 = f'''
<div class="concept">
  <div class="concept__text"><span class="concept__letter">A</span><h3 class="case-h">Общая лента тренировок</h3>
    <dl class="case-dl"><dt>Идея</dt><dd>Все тренировки дня в одной ленте с сортировкой по типам.</dd>
    <dt>Взаимодействие</dt><dd>Пользователь выбирает день и фильтрует ленту чипами по типу занятия.</dd>
    <dt>Что проверяли</dt><dd>Удобно ли искать нужный тип тренировки в общем списке.</dd>
    <dt>Плюсы и ограничения</dt><dd>Вся активность видна сразу, но разные типы тренировок оказываются в одном потоке.</dd></dl></div>
  {shots(('proto-empty-v1', 'Пустой день'), ('proto-full-v1', 'Заполненный день'), ('proto-add-v1', 'Добавление тренировки'))}
</div>
<div class="concept">
  <div class="concept__text"><span class="concept__letter">B</span><h3 class="case-h">Календарная модель</h3>
    <dl class="case-dl"><dt>Идея</dt><dd>Таймлайн дня по аналогии с Google Calendar.</dd>
    <dt>Взаимодействие</dt><dd>Пользователь выбирает время и затем тип занятия.</dd>
    <dt>Что проверяли</dt><dd>Готовы ли пользователи планировать тренировку от времени, а не от типа.</dd>
    <dt>Плюсы и ограничения</dt><dd>Привычная календарная механика, но тип тренировки выбирается только на втором шаге.</dd></dl></div>
  {shots(('proto-empty-v2', 'Пустой таймлайн'), ('cal-default-v2', 'День с отметкой времени'), ('cal-planned-v2', 'Все тренировки дня: запланированные и нет'))}
</div>
<div class="concept">
  <div class="concept__text"><span class="concept__letter">C</span><h3 class="case-h">Календарь с табами и карточками</h3>
    <dl class="case-dl"><dt>Идея</dt><dd>Календарь, в котором типы тренировок вынесены в навигацию.</dd>
    <dt>Взаимодействие</dt><dd>Пользователь переключает тип тренировки табом и работает с карточками выбранного раздела.</dd>
    <dt>Что проверяли</dt><dd>Замечают ли пользователи доступные типы тренировок и понимают ли, как между ними переключаться.</dd>
    <dt>Плюсы и ограничения</dt><dd>Типы занятий видны сразу; требуется единая структура карточек для разных продуктов.</dd></dl></div>
  {shots(('cal-default-v1', 'Пустой день'), ('cal-planned-v1', 'Все тренировки дня: запланированные и нет'), ('tabs-v6', 'Табы по типам тренировок'))}
</div>
{note('Дальше мы развивали концепцию C: она делала типы тренировок видимыми без дополнительных действий.')}
'''

s05 = f'''
<div class="decision">
  <div class="case-text"><h3 class="case-h">Акцентные табы</h3><p>Пользователь сразу видит доступные типы тренировок и переключается между ними без скрытых выпадающих списков.</p></div>
  {shots(('final-active', 'Мой календарь'), ('tabs-final', 'Групповые'), ('self-default', 'Самостоятельные'))}
</div>
<div class="decision">
  <div class="case-text"><h3 class="case-h">Специализированные фильтры</h3>
    <dl class="case-dl"><dt>Групповые</dt><dd>Время, клуб, интенсивность, категории, тренеры, доступность записи и свободные места.</dd>
    <dt>Самостоятельные</dt><dd>Группы мышц, оборудование, автор программы и длительность.</dd>
    <dt>Action</dt><dd>Группы мышц, интенсивность, длительность, категории, тренировки дома или в зале и тренеры.</dd></dl>
    <p>Ключевые параметры видны сразу в чипах, расширенные настройки открываются в нижних панелях.</p></div>
  {shots(('group-filters', 'Групповые: активный фильтр'), ('self-filters', 'Самостоятельные: фильтры'), ('group-empty', 'Пустой результат фильтрации'))}
</div>
<div class="decision">
  <div class="case-text"><h3 class="case-h">Ближайшие тренировки</h3><p>В групповых сначала показываются ближайшие записи пользователя, затем остальные занятия.</p>
    <h3 class="case-h">Планирование из дневника</h3><p>Путь к самостоятельным тренировкам стал короче: дневник больше не нужно искать внутри профиля.</p></div>
  {shots(('near-2', 'Групповые: сначала записи пользователя'), ('near-all', 'Самостоятельные: запланированная и все тренировки'))}
</div>
<div class="decision">
  <div class="case-text"><h3 class="case-h">Календарь и пустые состояния</h3><p>В блоке календаря отображаются ближайшие активности или empty state с возможностью выбрать тренировку. Месячный вид показывает тренировочную активность по датам.</p></div>
  {shots(('flow-empty', 'Empty state'), ('flow-3', 'Три тренировки в один день'), ('flow-add', 'Нажатие на «Добавить тренировку»'), ('flow-calendar', 'Календарь'), cls='shots--flow')}
</div>
<div class="decision">
  <div class="case-text"><h3 class="case-h">Общие паттерны и цвет</h3><p>Карточки разных тренировочных продуктов приведены к согласованной структуре с сохранением важной для каждого информации. Архитектура рассчитана на подключение новых типов тренировок.</p>
    <ul class="legend"><li><img src="assets/ddx/chip-group.png" width="74" height="20" alt="Групповая"></li><li><img src="assets/ddx/chip-self.png" width="112" height="20" alt="Самостоятельная"></li><li><img src="assets/ddx/chip-action.png" width="50" height="20" alt="Action"></li></ul></div>
  {shots(('final-diary-active', 'Типы тренировок в одном дне'), ('personal', 'Персональные', 'shot--blur'), ('action', 'Action', 'shot--blur'))}
</div>
'''

s06 = f'''
<div class="case-text"><p>Мы проводили usability-тестирование альтернативных прототипов — это не A/B-тест на реальном трафике.</p></div>
<ol class="steps">
  <li class="steps__item"><span class="steps__num">1</span><h3 class="case-h">Исходная концепция</h3><p>Все типы тренировок предлагались как равнозначный выбор.</p>{shots(('cal-default-v1', 'Равнозначный выбор типа'))}</li>
  <li class="steps__item"><span class="steps__num">2</span><h3 class="case-h">Результаты тестирования</h3><p>Пользователи предпочли более явную навигацию по типам тренировок. При сравнении реализаций табов акцентный вариант получил более 58% предпочтений.</p>{shots(('tabs-v2', 'Версия 2'), ('tabs-v6', 'Версия 6'))}</li>
  <li class="steps__item"><span class="steps__num">3</span><h3 class="case-h">Обнаруженная проблема</h3><p>Гипотеза о равнозначном выборе уступила варианту с приоритетом групповых: они оставались основным пользовательским сценарием.</p>{shots(('tabs-v1', 'Single-select скрывал типы'))}</li>
  <li class="steps__item"><span class="steps__num">4</span><h3 class="case-h">Изменённое решение</h3><p>Групповые тренировки открываются сразу. Переход к календарю и выбор других типов сохранены в табах.</p></li>
  <li class="steps__item"><span class="steps__num">5</span><h3 class="case-h">Финальный вариант</h3><p>Акцентные табы: «Мой календарь», «Групповые», «Самостоятельные».</p>{shots(('tabs-final', 'Групповые открыты по умолчанию'))}</li>
</ol>
<p class="case-foot">58% — доля предпочтений в отдельном сравнении вариантов табов; она не относится ко всей выборке 100+ участников.</p>
{note('Дизайн-решение должно учитывать не только логичность архитектуры, но и реальное поведение аудитории.', 'Ключевой вывод')}
'''

s07 = f'''
<div class="case-text">
  <h3 class="case-h">Что изменилось</h3>
  {ul('Путь к самостоятельной тренировке сократился примерно в 2 раза по числу шагов', 'Пользователь работает с тренировками через общую календарную механику', 'Разные сценарии получили согласованную визуальную структуру', 'Тренировочная активность видна по датам', 'Использование календаря растёт — точный процент не раскрывается', 'Подготовлены onboarding stories для знакомства с новой функциональностью')}
</div>
<div class="case-grid3 status">
  <div class="case-card"><span class="status__label status__label--done">Уже реализовано</span><p>В продакшен выпущен календарь для двух разделов — групповых и самостоятельных тренировок.</p></div>
  <div class="case-card"><span class="status__label status__label--wip">На ревью и в разработке</span><p>Персональные тренировки и Action проходят ревью и готовятся к разработке.</p></div>
  <div class="case-card"><span class="status__label">Дальнейшее развитие</span><p>Подключение новых тренировочных форматов к общей календарной механике.</p></div>
</div>
{shots(('final-active', 'В продакшене: календарь'), ('group-default', 'В продакшене: групповые'), ('self-default', 'В продакшене: самостоятельные'), ('personal', 'Персональные', 'shot--blur'), ('action', 'Action', 'shot--blur'))}
'''

stages = ''.join([
    stage('01', 'Контекст и задача', 'Как объединить несколько тренировочных продуктов в одном приложении?', s01, True),
    stage('02', 'Проблема', 'Тренировки были распределены по разным частям приложения', s02),
    stage('03', 'Исследования', 'Как пользователи воспринимают тренировочные сценарии?', s03),
    stage('04', 'Гипотезы и альтернативы', 'Поиск подходящей архитектуры календаря', s04),
    stage('05', 'UX-решение', 'Единый календарь с понятной навигацией по типам тренировок', s05),
    stage('06', 'Тестирование, ошибки и итерации', 'Почему первоначальная гипотеза изменилась после тестирования', s06),
    stage('07', 'Релиз, результаты и развитие', 'От концепции к масштабируемому тренировочному пространству', s07),
])

main = f'''
  <main class="case">
    <section class="case-hero">
      <div class="case-hero__top">
        <h1 class="case-hero__title" data-split>DDX Fitness</h1>
        <p class="case-hero__role" data-reveal>Lead Product Designer · iOS</p>
      </div>
      <div class="case-hero__lead" data-reveal style="--d: 150ms">
        <h2 class="case-hero__h">От отдельных тренировок к единому календарю DDX Fitness</h2>
        <p>Как мы переосмыслили архитектуру тренировок, объединили пользовательские сценарии и разработали новую модель планирования активности.</p>
      </div>
      <dl class="case-facts" data-reveal style="--d: 300ms">
        <div><dt>100+</dt><dd>участников тестирования прототипов</dd></div>
        <div><dt>58%+</dt><dd>предпочтений в пользу акцентных табов при сравнении вариантов</dd></div>
        <div><dt>≈2x</dt><dd>короче путь к самостоятельной тренировке по числу шагов</dd></div>
      </dl>
    </section>

    <section class="case-ba">
      <div class="case-ba__panel" data-reveal>
        <span class="case-ba__label">Before</span>
        <h2 class="case-h">Отдельные разделы и разные пути к тренировкам</h2>
        {shots(('old-home', 'Главная'), ('old-schedule', 'Расписание'), ('old-diary', 'Дневник через профиль'))}
      </div>
      <div class="case-ba__panel" data-reveal style="--d: 120ms">
        <span class="case-ba__label case-ba__label--after">After</span>
        <h2 class="case-h">Единый календарь с табами по типам тренировок</h2>
        {shots(('final-active', 'Мой календарь'), ('tabs-final', 'Групповые'), ('self-default', 'Самостоятельные'))}
      </div>
    </section>

    <section class="acc" aria-label="Этапы проекта">{stages}
    </section>

    <section class="takeaways">
      <h2 class="takeaways__title" data-split>Мои выводы</h2>
      <div class="takeaways__grid">
        <div class="case-card" data-reveal><span class="case-card__num">1</span><h3 class="case-h">Единая архитектура не означает одинаковый сценарий для всех</h3><p>Объединяя продукты, важно учитывать реальную частотность использования каждого из них. Исследование показало, что равнозначная навигация не всегда эффективнее приоритизации основного сценария.</p></div>
        <div class="case-card" data-reveal style="--d: 80ms"><span class="case-card__num">2</span><h3 class="case-h">Видимая навигация может быть понятнее компактной</h3><p>Single-select экономил пространство, но скрывал доступные возможности. Акцентные табы сделали выбор более очевидным.</p></div>
        <div class="case-card" data-reveal><span class="case-card__num">3</span><h3 class="case-h">Консистентность интерфейса начинается с системы</h3><p>Объединение разных карточек потребовало работы не только над визуальным стилем, но и над структурой данных, компонентами и правилами их использования.</p></div>
        <div class="case-card" data-reveal style="--d: 80ms"><span class="case-card__num">4</span><h3 class="case-h">Исследования должны менять продуктовые решения</h3><p>Первоначальная идея не обязана становиться финальной. Ценность исследований в том, чтобы вовремя обнаружить расхождение между дизайнерскими предположениями и поведением пользователей.</p></div>
      </div>
      <blockquote class="takeaways__quote" data-reveal>Этот проект показал мне, что сильное продуктовое решение рождается не из стремления объединить всё в одном интерфейсе, а из понимания того, как люди действительно используют продукт.</blockquote>
      <a class="case-back" href="index.html#projects" data-reveal><span aria-hidden="true">←</span> Все проекты</a>
    </section>
  </main>

  <div class="lightbox" id="lightbox" aria-hidden="true"><img alt=""></div>
'''

old = (root / 'ddx-fitness.html').read_text(encoding='utf-8')
index = (root / 'index.html').read_text(encoding='utf-8')
head = old[:old.index('  <main')]
head = re.sub(r'\?v=\d+', '?v=' + V, head)
footer = index[index.index('  <footer class="footer"'):index.index('  <script')]
html = head + main.lstrip('\n') + '\n' + footer + f'  <script src="js/main.js?v={V}"></script>\n</body>\n</html>\n'
(root / 'ddx-fitness.html').write_text(html, encoding='utf-8')
(root / 'index.html').write_text(re.sub(r'\?v=\d+', '?v=' + V, index), encoding='utf-8')
print('ok', len(html))
