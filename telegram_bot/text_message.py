START_MESSAGE = """
👋 <b>Doggy Logy</b> - сервис для владельцев собак и кошек.

🎬 Мы помогаем продакшнам с поиском животных для съемок.
Ваш питомец может стать актером!
📝 Используйте /form для заполнения анкеты!

🗣 Наши соцсети: /contact
ℹ️ Подробнее о нашем сервисе: /about"""

CONTACT = """🙋‍♀️ <b>Контактная информация:
@doggy_logy
@manager_DoggyLogy</b>\n
🌐 <b>Следите за нами в социальных сетях:</b> - <a href="https://doggy-logy.ru/">Сайт</a> | <a href="https://vk.com/doggylogy">VK</a> | <a href="https://youtube.com/@doggylogy?si=TfojM_-KXnH6YckN">YouTube</a> | <a href="https://t.me/DoggyLogyChannel">Наш канал</a> | <a href="https://t.me/DoggyLogy">Чат</a> | <a href="https://www.instagram.com/doggy.logy">Instagram</a> | <a href="https://www.tiktok.com/@doggy.logy?_t=ZS-90EzzqHoy5X&_r=1">TikTok</a>"""

ABOUT = """<b>DoggyLogy</b>: комплексная поддержка для владельцев собак и кошек🐾\n
<blockquote>Чтобы узнать подробнее об услугах, перейдите по кнопке «сервис».</blockquote>"""

FORM = """📝 Заполните анкету для участия <b>Вашего</b> питомца в съемках <i>рекламы, клипа или фильма</i>!\n
ℹ Для участия в съемке питомец должен быть <b>социализирован</b> и <b>управляем</b>.\n
<i>Заполняя анкету, вы даете <b>согласие</b> на обработку персональных данных.</i>"""

DATA_TO_SEND = """
• ФИО: {fullname}
• Номер телефона: {phone_number}
• Город: {city}
• Порода питомца: {dog_breed}
• Возраст питомца: {dog_age}
• Как питомец переносит поездки на транспорте: {transport_question}
• День для съемки: {shooting_day_question}
• Особенности и навыки питомца: {dog_skills}
"""

CHOOSE_ACTION = """Выберите следующее действие:"""

INCORRECT_REQUEST = """🚫 Некорректный запрос.\n\n Перепроверьте формат введенных вами данных."""

SUCCESS_FORM = """✅ Анкетирование пройдено!"""

CANCEL_FORM = """❌ Анкетирование отменено!"""

CANCEL_SEND = """❌ Отправка отменена!"""