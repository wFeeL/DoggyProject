START_MESSAGE = """
👋 Здравствуй, {name}!

🐶 <b>Doggy Logy</b> - территория счастливых собак и людей.

🎬 Твоя собачка может поучаствовать в съемках рекламы, клипа, фильма или сюжета.
📝 Используй /form для заполнения анкеты!

🗣️ Наши соцсети: /contact
ℹ️ Подробнее о нашем сервисе: /about
"""

CONTACT = """🗣️ Мы в соцсетях:\n
Telegram - @doggy_logy
Сайт - doggy-logy.ru
VK - vk.com/doggylogy
YouTube - www.youtube.com/@doggylogy
"""

ABOUT = """🐶 <b>Doggy Logy</b> - это сервис для владельцев собак в Москве.

• @DoggyLogySale_bot - бесплатная подписка на сервис
• Гуманная коррекция поведения/ обучение командам 
• Помощь с выбором щенка
• Передержка
• Догситтер/выгул
• Разработка рациона 
• Консультации ветеринара
• Страхование здоровья питомца
• Подготовка к выставкам 
• Груминг 
• Зооюрист
• Зоотакси
• Пэт-фотограф 

Мы всегда открыты для обратной связи!
<i>С любовью к собакам и их людям, DoggyLogy ❤️</i>
@manager_DogyLogy
@doggy_logy"""

FORM = """📝 Заполните анкету для участия <b>Вашей</b> собачки в съемках <i>рекламы, клипа или фильма</i>!\n
ℹ Для участия в съемке питомец должен быть <b>социализирован</b> и <b>управляем</b>.\n
<i>Заполняя анкету, вы даете <b>согласие</b> на обработку персональных данных.</i>"""

DATA_TO_SEND = """
• ФИО: {fullname}
• Номер телефона: {phone_number}
• Город: {city}
• Порода собаки: {dog_breed}
• Возраст собаки: {dog_age}
• Как собака переносит поездки на транспорте: {transport_question}
• День для съемки: {shooting_day_question}
• Особенности и навыки собаки: {dog_skills}
"""

CHOOSE_ACTION = """Выберите следующее действие:"""

INCORRECT_REQUEST = """🚫 Некорректный запрос.\n\n Перепроверьте формат введенных вами данных."""

SUCCESS_FORM = """✅ Анкетирование пройдено!"""

CANCEL_FORM = """❌ Анкетирование отменено!"""

CANCEL_SEND = """❌ Отправка отменена!"""