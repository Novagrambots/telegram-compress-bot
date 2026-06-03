"""Мультиязычность — русский, узбекский (латиница), узбекский (кириллица), английский
Использование: from bot.i18n import t
  t("start.welcome", lang="en", name="John")

Поддерживаемые языки: ru / uz_latn / uz_cyrl / en
"""

from bot.emojis import E

TRANSLATIONS = {
    # === /start ===
    "start.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет, {{name}}!</b>\n\n"
            f"{E['video']} Я помогу тебе сжать видео и фотографии.\n\n"
            f"{E['pin']} <b>Как пользоваться:</b>\n"
            "Отправь видео или фото — я сожму его быстро и без потери качества. "
            f"{E['plane']}\n\n"
            "Выбери действие ниже:"
        ),
        "uz_latn": (
            f"{E['bot']} <b>Salom, {{name}}!</b>\n\n"
            f"{E['video']} Video va rasmlarni siqishda yordam beraman.\n\n"
            f"{E['pin']} <b>Qanday foydalanish:</b>\n"
            "Menga video yoki rasm yuboring — men uni tez va sifatli siqaman. "
            f"{E['plane']}\n\n"
            "Quyidagi tugmalardan birini tanlang:"
        ),
        "uz_cyrl": (
            f"{E['bot']} <b>Салом, {{name}}!</b>\n\n"
            f"{E['video']} Видео ва расмларни сиқишда ёрдам бераман.\n\n"
            f"{E['pin']} <b>Қандай фойдаланиш:</b>\n"
            "Менга видео ёки расм юборинг — мен уни тез ва сифатли сиқаман. "
            f"{E['plane']}\n\n"
            "Қуйидаги тугмалардан бирини танланг:"
        ),
        "en": (
            f"{E['bot']} <b>Hello, {{name}}!</b>\n\n"
            f"{E['video']} I'll help you compress videos and photos.\n\n"
            f"{E['pin']} <b>How to use:</b>\n"
            "Send me a video or photo — I'll compress it quickly with great quality. "
            f"{E['plane']}\n\n"
            "Choose an action below:"
        ),
    },

    # === Кнопки главного меню ===
    "btn.compress": {
        "ru": "Сжать файл",
        "uz_latn": "Faylni siqish",
        "uz_cyrl": "Файлни сиқиш",
        "en": "Compress file",
    },
    "btn.profile": {
        "ru": "Мой профиль",
        "uz_latn": "Mening profilim",
        "uz_cyrl": "Менинг профилим",
        "en": "My profile",
    },
    "btn.help": {
        "ru": "Помощь",
        "uz_latn": "Yordam",
        "uz_cyrl": "Ёрдам",
        "en": "Help",
    },
    "btn.back": {
        "ru": "Назад",
        "uz_latn": "Orqaga",
        "uz_cyrl": "Орқага",
        "en": "Back",
    },
    "btn.language": {
        "ru": "Сменить язык",
        "uz_latn": "Tilni o'zgartirish",
        "uz_cyrl": "Тилни ўзгартириш",
        "en": "Change language",
    },

    # === Сжатие (FSM-флоу) ===
    "compress.send_file": {
        "ru": (
            f"{E['package']} <b>Отправьте видео или фото для сжатия</b>\n\n"
            f"{E['video']} Поддерживаются: MP4, MOV, MKV, AVI и другие видеоформаты\n"
            f"{E['camera']} Фото: JPEG, PNG, WebP, HEIC\n"
            f"{E['info']} До 2 ГБ"
        ),
        "uz_latn": (
            f"{E['package']} <b>Siqish uchun video yoki rasm yuboring</b>\n\n"
            f"{E['video']} Qo'llab-quvvatlanadi: MP4, MOV, MKV, AVI va boshqa formatlar\n"
            f"{E['camera']} Rasmlar: JPEG, PNG, WebP, HEIC\n"
            f"{E['info']} 2 GB gacha"
        ),
        "uz_cyrl": (
            f"{E['package']} <b>Сиқиш учун видео ёки расм юборинг</b>\n\n"
            f"{E['video']} Қўллаб-қувватланади: MP4, MOV, MKV, AVI ва бошқа форматлар\n"
            f"{E['camera']} Расмлар: JPEG, PNG, WebP, HEIC\n"
            f"{E['info']} 2 ГБ гача"
        ),
        "en": (
            f"{E['package']} <b>Send a video or photo to compress</b>\n\n"
            f"{E['video']} Supported: MP4, MOV, MKV, AVI and other video formats\n"
            f"{E['camera']} Photos: JPEG, PNG, WebP, HEIC\n"
            f"{E['info']} Up to 2 GB"
        ),
    },
    "compress.file_received_video": {
        "ru": (
            f"{E['video']} <b>Видео получено</b>\n\n"
            f"{E['clock']} Длительность: <b>{{duration}}</b>\n"
            f"{E['package']} Размер: <b>{{size}}</b>\n"
            f"{E['info']} Разрешение: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Выберите уровень сжатия:</b>"
        ),
        "uz_latn": (
            f"{E['video']} <b>Video qabul qilindi</b>\n\n"
            f"{E['clock']} Davomiyligi: <b>{{duration}}</b>\n"
            f"{E['package']} Hajmi: <b>{{size}}</b>\n"
            f"{E['info']} O'lchamlari: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Siqish darajasini tanlang:</b>"
        ),
        "uz_cyrl": (
            f"{E['video']} <b>Видео қабул қилинди</b>\n\n"
            f"{E['clock']} Давомийлиги: <b>{{duration}}</b>\n"
            f"{E['package']} Ҳажми: <b>{{size}}</b>\n"
            f"{E['info']} Ўлчамлари: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Сиқиш даражасини танланг:</b>"
        ),
        "en": (
            f"{E['video']} <b>Video received</b>\n\n"
            f"{E['clock']} Duration: <b>{{duration}}</b>\n"
            f"{E['package']} Size: <b>{{size}}</b>\n"
            f"{E['info']} Resolution: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Choose compression level:</b>"
        ),
    },
    "compress.file_received_photo": {
        "ru": (
            f"{E['camera']} <b>Фото получено</b>\n\n"
            f"{E['package']} Размер: <b>{{size}}</b>\n"
            f"{E['info']} Разрешение: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Выберите уровень сжатия:</b>"
        ),
        "uz_latn": (
            f"{E['camera']} <b>Rasm qabul qilindi</b>\n\n"
            f"{E['package']} Hajmi: <b>{{size}}</b>\n"
            f"{E['info']} O'lchamlari: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Siqish darajasini tanlang:</b>"
        ),
        "uz_cyrl": (
            f"{E['camera']} <b>Расм қабул қилинди</b>\n\n"
            f"{E['package']} Ҳажми: <b>{{size}}</b>\n"
            f"{E['info']} Ўлчамлари: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Сиқиш даражасини танланг:</b>"
        ),
        "en": (
            f"{E['camera']} <b>Photo received</b>\n\n"
            f"{E['package']} Size: <b>{{size}}</b>\n"
            f"{E['info']} Resolution: <b>{{width}}×{{height}}</b>\n\n"
            f"{E['gear']} <b>Choose compression level:</b>"
        ),
    },
    "compress.preset_low": {
        "ru": "Слабое сжатие",
        "uz_latn": "Yengil siqish",
        "uz_cyrl": "Енгил сиқиш",
        "en": "Light compression",
    },
    "compress.preset_medium": {
        "ru": "Среднее сжатие",
        "uz_latn": "O'rtacha siqish",
        "uz_cyrl": "Ўртача сиқиш",
        "en": "Medium compression",
    },
    "compress.preset_high": {
        "ru": "Сильное сжатие",
        "uz_latn": "Kuchli siqish",
        "uz_cyrl": "Кучли сиқиш",
        "en": "Heavy compression",
    },
    "compress.downloading": {
        "ru": f"{E['clock']} Скачиваю файл...",
        "uz_latn": f"{E['clock']} Fayl yuklanmoqda...",
        "uz_cyrl": f"{E['clock']} Файл юкланмоқда...",
        "en": f"{E['clock']} Downloading file...",
    },
    "compress.processing": {
        "ru": (
            f"{E['gear']} <b>Сжимаю файл...</b>\n\n"
            f"{E['clock']} Это может занять несколько минут — не закрывай чат."
        ),
        "uz_latn": (
            f"{E['gear']} <b>Faylni siqyapman...</b>\n\n"
            f"{E['clock']} Bu bir necha daqiqa olishi mumkin — chatni yopmang."
        ),
        "uz_cyrl": (
            f"{E['gear']} <b>Файлни сиқяпман...</b>\n\n"
            f"{E['clock']} Бу бир неча дақиқа олиши мумкин — чатни ёпманг."
        ),
        "en": (
            f"{E['gear']} <b>Compressing your file...</b>\n\n"
            f"{E['clock']} This may take a few minutes — please don't close the chat."
        ),
    },
    "compress.done_video": {
        "ru": (
            f"{E['check']} <b>Готово!</b>\n\n"
            f"{E['package']} Было: <b>{{size_before}}</b>\n"
            f"{E['package']} Стало: <b>{{size_after}}</b>\n"
            f"{E['chart']} Размер: <b>{{ratio}}%</b> от исходного"
        ),
        "uz_latn": (
            f"{E['check']} <b>Tayyor!</b>\n\n"
            f"{E['package']} Edi: <b>{{size_before}}</b>\n"
            f"{E['package']} Bo'ldi: <b>{{size_after}}</b>\n"
            f"{E['chart']} Hajmi: boshlang'ichning <b>{{ratio}}%</b> qismi"
        ),
        "uz_cyrl": (
            f"{E['check']} <b>Тайёр!</b>\n\n"
            f"{E['package']} Эди: <b>{{size_before}}</b>\n"
            f"{E['package']} Бўлди: <b>{{size_after}}</b>\n"
            f"{E['chart']} Ҳажми: бошланғичнинг <b>{{ratio}}%</b> қисми"
        ),
        "en": (
            f"{E['check']} <b>Done!</b>\n\n"
            f"{E['package']} Before: <b>{{size_before}}</b>\n"
            f"{E['package']} After: <b>{{size_after}}</b>\n"
            f"{E['chart']} Size: <b>{{ratio}}%</b> of the original"
        ),
    },
    "compress.done_photo": {
        "ru": (
            f"{E['check']} <b>Готово!</b>\n\n"
            f"{E['package']} Было: <b>{{size_before}}</b>\n"
            f"{E['package']} Стало: <b>{{size_after}}</b>\n"
            f"{E['chart']} Размер: <b>{{ratio}}%</b> от исходного"
        ),
        "uz_latn": (
            f"{E['check']} <b>Tayyor!</b>\n\n"
            f"{E['package']} Edi: <b>{{size_before}}</b>\n"
            f"{E['package']} Bo'ldi: <b>{{size_after}}</b>\n"
            f"{E['chart']} Hajmi: boshlang'ichning <b>{{ratio}}%</b> qismi"
        ),
        "uz_cyrl": (
            f"{E['check']} <b>Тайёр!</b>\n\n"
            f"{E['package']} Эди: <b>{{size_before}}</b>\n"
            f"{E['package']} Бўлди: <b>{{size_after}}</b>\n"
            f"{E['chart']} Ҳажми: бошланғичнинг <b>{{ratio}}%</b> қисми"
        ),
        "en": (
            f"{E['check']} <b>Done!</b>\n\n"
            f"{E['package']} Before: <b>{{size_before}}</b>\n"
            f"{E['package']} After: <b>{{size_after}}</b>\n"
            f"{E['chart']} Size: <b>{{ratio}}%</b> of the original"
        ),
    },
    "compress.already_small": {
        "ru": f"{E['warning']} <b>Файл уже хорошо сжат</b> — выигрыш меньше 10%.",
        "uz_latn": f"{E['warning']} <b>Fayl allaqachon yaxshi siqilgan</b> — yutuq 10% dan kam.",
        "uz_cyrl": f"{E['warning']} <b>Файл аллақачон яхши сиқилган</b> — ютуқ 10% дан кам.",
        "en": f"{E['warning']} <b>File is already well compressed</b> — savings below 10%.",
    },
    "compress.ad_caption": {
        "ru": f"{E['bot']} Сжато ботом @{{bot_username}}",
        "uz_latn": f"{E['bot']} @{{bot_username}} bot orqali siqildi",
        "uz_cyrl": f"{E['bot']} @{{bot_username}} бот орқали сиқилди",
        "en": f"{E['bot']} Compressed by @{{bot_username}}",
    },
    "compress.error_not_media": {
        "ru": f"{E['cross']} <b>Это не видео и не фото.</b>\n\nПришли мне видеофайл или картинку.",
        "uz_latn": f"{E['cross']} <b>Bu video yoki rasm emas.</b>\n\nVideo yoki rasm yuboring.",
        "uz_cyrl": f"{E['cross']} <b>Бу видео ёки расм эмас.</b>\n\nВидео ёки расм юборинг.",
        "en": f"{E['cross']} <b>That's not a video or photo.</b>\n\nSend me a video or an image.",
    },
    "compress.error_download": {
        "ru": f"{E['cross']} <b>Не удалось скачать файл</b>\n\nПопробуй ещё раз через минуту.",
        "uz_latn": f"{E['cross']} <b>Faylni yuklab bo'lmadi</b>\n\nBir daqiqadan keyin qayta urinib ko'ring.",
        "uz_cyrl": f"{E['cross']} <b>Файлни юклаб бўлмади</b>\n\nБир дақиқадан кейин қайта уриниб кўринг.",
        "en": f"{E['cross']} <b>Failed to download the file</b>\n\nTry again in a minute.",
    },
    "compress.error_ffmpeg": {
        "ru": f"{E['cross']} <b>Ошибка при обработке</b>\n\nПопробуй другой пресет или другой файл.",
        "uz_latn": f"{E['cross']} <b>Qayta ishlashda xatolik</b>\n\nBoshqa darajani yoki boshqa faylni sinab ko'ring.",
        "uz_cyrl": f"{E['cross']} <b>Қайта ишлашда хатолик</b>\n\nБошқа даражани ёки бошқа файлни синаб кўринг.",
        "en": f"{E['cross']} <b>Processing error</b>\n\nTry another preset or another file.",
    },
    "compress.error_too_big": {
        "ru": f"{E['package']} <b>Файл слишком большой</b>\n\nЛимит — 2 ГБ.",
        "uz_latn": f"{E['package']} <b>Fayl juda katta</b>\n\nLimit — 2 GB.",
        "uz_cyrl": f"{E['package']} <b>Файл жуда катта</b>\n\nЛимит — 2 ГБ.",
        "en": f"{E['package']} <b>File is too large</b>\n\nLimit is 2 GB.",
    },
    "compress.error_unsupported": {
        "ru": f"{E['cross']} <b>Неподдерживаемый формат</b>\n\nПришли видео или фото в стандартном формате.",
        "uz_latn": f"{E['cross']} <b>Qo'llab-quvvatlanmaydigan format</b>\n\nStandart formatdagi video yoki rasm yuboring.",
        "uz_cyrl": f"{E['cross']} <b>Қўллаб-қувватланмайдиган формат</b>\n\nСтандарт форматдаги видео ёки расм юборинг.",
        "en": f"{E['cross']} <b>Unsupported format</b>\n\nSend a video or photo in a common format.",
    },
    "compress.busy": {
        "ru": f"{E['clock']} <b>Сейчас обрабатываю предыдущий файл</b>\n\nДождись окончания и пришли следующий.",
        "uz_latn": f"{E['clock']} <b>Hozir oldingi fayl qayta ishlanyapti</b>\n\nTugashini kuting va keyingisini yuboring.",
        "uz_cyrl": f"{E['clock']} <b>Ҳозир олдинги файл қайта ишланяпти</b>\n\nТугашини кутинг ва кейингисини юборинг.",
        "en": f"{E['clock']} <b>Still processing the previous file</b>\n\nWait until it finishes, then send the next one.",
    },
    "compress.cancelled": {
        "ru": f"{E['cross']} <b>Сжатие отменено.</b>",
        "uz_latn": f"{E['cross']} <b>Siqish bekor qilindi.</b>",
        "uz_cyrl": f"{E['cross']} <b>Сиқиш бекор қилинди.</b>",
        "en": f"{E['cross']} <b>Compression cancelled.</b>",
    },
    "compress.cancel": {
        "ru": "Отмена",
        "uz_latn": "Bekor qilish",
        "uz_cyrl": "Бекор қилиш",
        "en": "Cancel",
    },

    # === Профиль ===
    "profile.title": {
        "ru": (
            f"{E['profile']} <b>Твой профиль</b>\n\n"
            f"{E['edit']} Имя: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['video']} Сжатий сделано: {{downloads}}\n"
        ),
        "uz_latn": (
            f"{E['profile']} <b>Mening profilim</b>\n\n"
            f"{E['edit']} Ism: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['video']} Siqishlar soni: {{downloads}}\n"
        ),
        "uz_cyrl": (
            f"{E['profile']} <b>Менинг профилим</b>\n\n"
            f"{E['edit']} Исм: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['video']} Сиқишлар сони: {{downloads}}\n"
        ),
        "en": (
            f"{E['profile']} <b>Your profile</b>\n\n"
            f"{E['edit']} Name: {{full_name}}\n"
            f"{E['info']} ID: <code>{{user_id}}</code>\n"
            f"{E['video']} Compressions done: {{downloads}}\n"
        ),
    },

    # === Помощь ===
    "help.text": {
        "ru": (
            f"{E['book']} <b>Помощь</b>\n\n"
            f"{E['star']} Отправь видео — бот сожмёт его в MP4/H.265\n"
            f"{E['star']} Отправь фото или HEIC — бот конвертирует в JPEG\n"
            f"{E['star']} Поддерживаются файлы до 2 ГБ\n"
            f"{E['lock']} Файл обрабатывается на сервере через ffmpeg + Pillow\n\n"
            f"{E['plane']} По вопросам: @{{admin_username}}"
        ),
        "uz_latn": (
            f"{E['book']} <b>Yordam</b>\n\n"
            f"{E['star']} Video yuboring — bot uni MP4/H.265 formatida siqadi\n"
            f"{E['star']} Rasm yoki HEIC yuboring — bot uni JPEG ga o'zgartiradi\n"
            f"{E['star']} 2 GB gacha fayllar qo'llab-quvvatlanadi\n"
            f"{E['lock']} Fayl serverda ffmpeg + Pillow orqali qayta ishlanadi\n\n"
            f"{E['plane']} Savollar uchun: @{{admin_username}}"
        ),
        "uz_cyrl": (
            f"{E['book']} <b>Ёрдам</b>\n\n"
            f"{E['star']} Видео юборинг — бот уни MP4/H.265 форматида сиқади\n"
            f"{E['star']} Расм ёки HEIC юборинг — бот уни JPEG га ўзгартиради\n"
            f"{E['star']} 2 ГБ гача файллар қўллаб-қувватланади\n"
            f"{E['lock']} Файл серверда ffmpeg + Pillow орқали қайта ишланади\n\n"
            f"{E['plane']} Саволлар учун: @{{admin_username}}"
        ),
        "en": (
            f"{E['book']} <b>Help</b>\n\n"
            f"{E['star']} Send a video — the bot will compress it to MP4/H.265\n"
            f"{E['star']} Send a photo or HEIC — the bot will convert it to JPEG\n"
            f"{E['star']} Files up to 2 GB are supported\n"
            f"{E['lock']} File is processed on the server via ffmpeg + Pillow\n\n"
            f"{E['plane']} Contact: @{{admin_username}}"
        ),
    },

    # === Подписка ===
    "sub.welcome": {
        "ru": (
            f"{E['bot']} <b>Привет!</b>\n\n"
            f"{E['video']} Этот бот сжимает видео и фото — быстро и бесплатно!\n\n"
            f"{E['lock']} <b>Для начала подпишись на каналы ниже:</b>\n\n"
            f"После подписки нажми «{E['check']} Проверить подписку»"
        ),
        "uz_latn": (
            f"{E['bot']} <b>Salom!</b>\n\n"
            f"{E['video']} Bu bot video va rasmlarni siqadi — tez va bepul!\n\n"
            f"{E['lock']} <b>Boshlash uchun quyidagi kanallarga obuna bo'ling:</b>\n\n"
            f"Obuna bo'lgandan keyin «{E['check']} Obunani tekshirish» tugmasini bosing"
        ),
        "uz_cyrl": (
            f"{E['bot']} <b>Салом!</b>\n\n"
            f"{E['video']} Бу бот видео ва расмларни сиқади — тез ва бепул!\n\n"
            f"{E['lock']} <b>Бошлаш учун қуйидаги каналларга обуна бўлинг:</b>\n\n"
            f"Обуна бўлгандан кейин «{E['check']} Обунани текшириш» тугмасини босинг"
        ),
        "en": (
            f"{E['bot']} <b>Hello!</b>\n\n"
            f"{E['video']} This bot compresses videos and photos — fast and free!\n\n"
            f"{E['lock']} <b>To start, subscribe to the channels below:</b>\n\n"
            f"After subscribing, tap «{E['check']} Check subscription»"
        ),
    },
    "sub.not_subscribed": {
        "ru": (
            f"{E['cross']} <b>Ты ещё не подписался на все каналы:</b>\n\n"
            f"Подпишись и нажми «{E['check']} Проверить подписку» ещё раз."
        ),
        "uz_latn": (
            f"{E['cross']} <b>Hali barcha kanallarga obuna bo'lmading:</b>\n\n"
            f"Obuna bo'l va «{E['check']} Obunani tekshirish» tugmasini qayta bos."
        ),
        "uz_cyrl": (
            f"{E['cross']} <b>Ҳали барча каналларга обуна бўлмадинг:</b>\n\n"
            f"Обуна бўл ва «{E['check']} Обунани текшириш» тугмасини қайта бос."
        ),
        "en": (
            f"{E['cross']} <b>You haven't subscribed to all channels yet:</b>\n\n"
            f"Subscribe and tap «{E['check']} Check subscription» again."
        ),
    },
    "sub.success": {
        "ru": (
            f"{E['check']} <b>Отлично, {{name}}!</b>\n\n"
            f"Теперь ты можешь пользоваться ботом! {E['plane']}\n\n"
            "Отправь видео или фото для сжатия."
        ),
        "uz_latn": (
            f"{E['check']} <b>Zo'r, {{name}}!</b>\n\n"
            f"Endi botdan foydalanishing mumkin! {E['plane']}\n\n"
            "Siqish uchun video yoki rasm yuboring."
        ),
        "uz_cyrl": (
            f"{E['check']} <b>Зўр, {{name}}!</b>\n\n"
            f"Энди ботдан фойдаланишинг мумкин! {E['plane']}\n\n"
            "Сиқиш учун видео ёки расм юборинг."
        ),
        "en": (
            f"{E['check']} <b>Great, {{name}}!</b>\n\n"
            f"You can now use the bot! {E['plane']}\n\n"
            "Send a video or photo to compress."
        ),
    },
    "btn.check_sub": {
        "ru": "Проверить подписку",
        "uz_latn": "Obunani tekshirish",
        "uz_cyrl": "Обунани текшириш",
        "en": "Check subscription",
    },
    "sub.check_alert_fail": {
        "ru": f"{E['cross']} Подпишись на все каналы!",
        "uz_latn": f"{E['cross']} Barcha kanallarga obuna bo'ling!",
        "uz_cyrl": f"{E['cross']} Барча каналларга обуна бўлинг!",
        "en": f"{E['cross']} Subscribe to all channels!",
    },
    "sub.check_alert_ok": {
        "ru": f"{E['check']} Подписка подтверждена!",
        "uz_latn": f"{E['check']} Obuna tasdiqlandi!",
        "uz_cyrl": f"{E['check']} Обуна тасдиқланди!",
        "en": f"{E['check']} Subscription confirmed!",
    },
    "sub.not_required": {
        "ru": f"{E['check']} Подписка не требуется!",
        "uz_latn": f"{E['check']} Obuna talab qilinmaydi!",
        "uz_cyrl": f"{E['check']} Обуна талаб қилинмайди!",
        "en": f"{E['check']} No subscription required!",
    },

    # === Ошибки ===
    "error.too_large": {
        "ru": f"{E['package']} <b>Файл слишком большой</b>\n\nTelegram ограничивает размер файла до 2 ГБ.",
        "uz_latn": f"{E['package']} <b>Fayl juda katta</b>\n\nTelegram fayl hajmini 2 GB bilan cheklaydi.",
        "uz_cyrl": f"{E['package']} <b>Файл жуда катта</b>\n\nTelegram файл ҳажмини 2 ГБ билан чеклайди.",
        "en": f"{E['package']} <b>File too large</b>\n\nTelegram limits file size to 2 GB.",
    },
    "error.timeout": {
        "ru": f"{E['clock']} <b>Превышено время ожидания</b>\n\nПопробуй ещё раз через пару минут.",
        "uz_latn": f"{E['clock']} <b>Kutish vaqti tugadi</b>\n\nBir necha daqiqadan keyin qayta urinib ko'ring.",
        "uz_cyrl": f"{E['clock']} <b>Кутиш вақти тугади</b>\n\nБир неча дақиқадан кейин қайта уриниб кўринг.",
        "en": f"{E['clock']} <b>Request timed out</b>\n\nPlease try again in a few minutes.",
    },
    "error.generic": {
        "ru": f"{E['cross']} <b>Что-то пошло не так</b>\n\nПопробуй позже.",
        "uz_latn": f"{E['cross']} <b>Nimadir noto'g'ri ketdi</b>\n\nKeyinroq urinib ko'ring.",
        "uz_cyrl": f"{E['cross']} <b>Нимадир нотўғри кетди</b>\n\nКейинроқ уриниб кўринг.",
        "en": f"{E['cross']} <b>Something went wrong</b>\n\nTry again later.",
    },
    "error.rate_limit": {
        "ru": f"{E['clock']} <b>Слишком много запросов!</b>\n\nПодожди {{seconds}} секунд и попробуй снова.",
        "uz_latn": f"{E['clock']} <b>Juda ko'p so'rovlar!</b>\n\n{{seconds}} soniya kuting va qayta urinib ko'ring.",
        "uz_cyrl": f"{E['clock']} <b>Жуда кўп сўровлар!</b>\n\n{{seconds}} сония кутинг ва қайта уриниб кўринг.",
        "en": f"{E['clock']} <b>Too many requests!</b>\n\nWait {{seconds}} seconds and try again.",
    },

    # === Выбор языка ===
    "lang.choose": {
        "ru": f"{E['gear']} <b>Выберите язык:</b>",
        "uz_latn": f"{E['gear']} <b>Tilni tanlang:</b>",
        "uz_cyrl": f"{E['gear']} <b>Тилни танланг:</b>",
        "en": f"{E['gear']} <b>Choose language:</b>",
    },
    "lang.changed": {
        "ru": f"{E['check']} Язык изменён на русский",
        "uz_latn": f"{E['check']} Til o'zbek tiliga o'zgartirildi (lotin)",
        "uz_cyrl": f"{E['check']} Тил ўзбек тилига ўзгартирилди (кирилл)",
        "en": f"{E['check']} Language changed to English",
    },

    # === Админ-панель ===
    "admin.title": {
        "ru": f"{E['gear']} <b>Админ-панель</b>\n\nВыбери действие:",
        "uz_latn": f"{E['gear']} <b>Admin panel</b>\n\nAmalni tanlang:",
        "uz_cyrl": f"{E['gear']} <b>Админ панел</b>\n\nАмални танланг:",
        "en": f"{E['gear']} <b>Admin panel</b>\n\nChoose an action:",
    },
    "admin.no_access": {
        "ru": f"{E['ban']} Нет доступа",
        "uz_latn": f"{E['ban']} Ruxsat yo'q",
        "uz_cyrl": f"{E['ban']} Рухсат йўқ",
        "en": f"{E['ban']} No access",
    },
    "admin.channel_deleted": {
        "ru": f"{E['check']} Канал удалён!",
        "uz_latn": f"{E['check']} Kanal o'chirildi!",
        "uz_cyrl": f"{E['check']} Канал ўчирилди!",
        "en": f"{E['check']} Channel deleted!",
    },
    "admin.channel_not_found": {
        "ru": f"{E['cross']} Канал не найден",
        "uz_latn": f"{E['cross']} Kanal topilmadi",
        "uz_cyrl": f"{E['cross']} Канал топилмади",
        "en": f"{E['cross']} Channel not found",
    },
    "admin.stats": {
        "ru": (
            f"{E['chart']} <b>Статистика бота</b>\n\n"
            f"{E['users']} Всего юзеров: <b>{{total_users}}</b>\n"
            f"{E['star']} Новых юзеров сегодня: <b>{{today_users}}</b>\n"
            f"{E['video']} Всего сжатий: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Каналов: <b>{{total_channels}}</b>"
        ),
        "uz_latn": (
            f"{E['chart']} <b>Bot statistikasi</b>\n\n"
            f"{E['users']} Jami foydalanuvchilar: <b>{{total_users}}</b>\n"
            f"{E['star']} Bugungi yangi foydalanuvchilar: <b>{{today_users}}</b>\n"
            f"{E['video']} Jami siqishlar: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Kanallar: <b>{{total_channels}}</b>"
        ),
        "uz_cyrl": (
            f"{E['chart']} <b>Бот статистикаси</b>\n\n"
            f"{E['users']} Жами фойдаланувчилар: <b>{{total_users}}</b>\n"
            f"{E['star']} Бугунги янги фойдаланувчилар: <b>{{today_users}}</b>\n"
            f"{E['video']} Жами сиқишлар: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Каналлар: <b>{{total_channels}}</b>"
        ),
        "en": (
            f"{E['chart']} <b>Bot statistics</b>\n\n"
            f"{E['users']} Total users: <b>{{total_users}}</b>\n"
            f"{E['star']} New users today: <b>{{today_users}}</b>\n"
            f"{E['video']} Total compressions: <b>{{total_downloads}}</b>\n"
            f"{E['megaphone']} Channels: <b>{{total_channels}}</b>"
        ),
    },
    "admin.channels_empty": {
        "ru": f"{E['megaphone']} <b>Каналы</b>\n\nСписок пуст. Добавь канал кнопкой ниже.",
        "uz_latn": f"{E['megaphone']} <b>Kanallar</b>\n\nRo'yxat bo'sh. Quyidagi tugma orqali kanal qo'shing.",
        "uz_cyrl": f"{E['megaphone']} <b>Каналлар</b>\n\nРўйхат бўш. Қуйидаги тугма орқали канал қўшинг.",
        "en": f"{E['megaphone']} <b>Channels</b>\n\nList is empty. Add a channel using the button below.",
    },
    "admin.channels_title": {
        "ru": f"{E['megaphone']} <b>Каналы для подписки:</b>\n",
        "uz_latn": f"{E['megaphone']} <b>Obuna kanallari:</b>\n",
        "uz_cyrl": f"{E['megaphone']} <b>Обуна каналлари:</b>\n",
        "en": f"{E['megaphone']} <b>Subscription channels:</b>\n",
    },
    "admin.add_channel_id": {
        "ru": (
            f"{E['megaphone']} <b>Добавление канала</b>\n\n"
            "Отправь <b>ID канала</b> (например <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} Узнать ID: добавь бота @getmyid_bot в канал"
        ),
        "uz_latn": (
            f"{E['megaphone']} <b>Kanal qo'shish</b>\n\n"
            "<b>Kanal ID</b> raqamini yuboring (masalan <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} ID bilish: @getmyid_bot ni kanalga qo'shing"
        ),
        "uz_cyrl": (
            f"{E['megaphone']} <b>Канал қўшиш</b>\n\n"
            "<b>Канал ID</b> рақамини юборинг (масалан <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} ID билиш: @getmyid_bot ни каналга қўшинг"
        ),
        "en": (
            f"{E['megaphone']} <b>Add channel</b>\n\n"
            "Send the <b>channel ID</b> (e.g. <code>-1001234567890</code>)\n\n"
            f"{E['bulb']} Get ID: add @getmyid_bot to the channel"
        ),
    },
    "admin.add_channel_title": {
        "ru": f"{E['edit']} Теперь отправь <b>название канала</b>:",
        "uz_latn": f"{E['edit']} Endi <b>kanal nomini</b> yuboring:",
        "uz_cyrl": f"{E['edit']} Энди <b>канал номини</b> юборинг:",
        "en": f"{E['edit']} Now send the <b>channel name</b>:",
    },
    "admin.add_channel_link": {
        "ru": (
            f"{E['link']} Теперь отправь <b>ссылку или юзернейм канала</b>\n\n"
            "Принимаю любой формат:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "uz_latn": (
            f"{E['link']} Endi <b>kanal havolasi yoki username</b> yuboring\n\n"
            "Istalgan formatda:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "uz_cyrl": (
            f"{E['link']} Энди <b>канал ҳаволаси ёки username</b> юборинг\n\n"
            "Исталган форматда:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
        "en": (
            f"{E['link']} Now send the <b>channel link or username</b>\n\n"
            "Any format accepted:\n"
            "• <code>https://t.me/your_channel</code>\n"
            "• <code>@your_channel</code>\n"
            "• <code>your_channel</code>"
        ),
    },
    "admin.channel_added": {
        "ru": f"{E['check']} <b>Канал добавлен!</b>",
        "uz_latn": f"{E['check']} <b>Kanal qo'shildi!</b>",
        "uz_cyrl": f"{E['check']} <b>Канал қўшилди!</b>",
        "en": f"{E['check']} <b>Channel added!</b>",
    },
    "admin.confirm_delete": {
        "ru": f"{E['warning']} <b>Удалить канал?</b>\n\nID: <code>{{channel_id}}</code>\n\nЭто действие нельзя отменить.",
        "uz_latn": f"{E['warning']} <b>Kanalni o'chirishni xohlaysizmi?</b>\n\nID: <code>{{channel_id}}</code>\n\nBu amalni qaytarib bo'lmaydi.",
        "uz_cyrl": f"{E['warning']} <b>Канални ўчиришни хоҳлайсизми?</b>\n\nID: <code>{{channel_id}}</code>\n\nБу амални қайтариб бўлмайди.",
        "en": f"{E['warning']} <b>Delete channel?</b>\n\nID: <code>{{channel_id}}</code>\n\nThis action cannot be undone.",
    },
    "admin.id_not_number": {
        "ru": f"{E['cross']} ID должен быть числом. Попробуй ещё раз:",
        "uz_latn": f"{E['cross']} ID raqam bo'lishi kerak. Qayta urinib ko'ring:",
        "uz_cyrl": f"{E['cross']} ID рақам бўлиши керак. Қайта уриниб кўринг:",
        "en": f"{E['cross']} ID must be a number. Try again:",
    },
    "admin.title_too_long": {
        "ru": f"{E['cross']} Название слишком длинное (макс 200 символов)",
        "uz_latn": f"{E['cross']} Nom juda uzun (maks 200 belgi)",
        "uz_cyrl": f"{E['cross']} Ном жуда узун (макс 200 белги)",
        "en": f"{E['cross']} Name is too long (max 200 characters)",
    },
    "admin.link_invalid": {
        "ru": f"{E['cross']} Не удалось распознать ссылку.\nПопробуй ещё:",
        "uz_latn": f"{E['cross']} Havolani aniqlab bo'lmadi.\nQayta urinib ko'ring:",
        "uz_cyrl": f"{E['cross']} Ҳаволани аниқлаб бўлмади.\nҚайта уриниб кўринг:",
        "en": f"{E['cross']} Could not parse the link.\nTry again:",
    },

    # === Кнопки админки ===
    "btn.admin_stats": {
        "ru": "Статистика", "uz_latn": "Statistika", "uz_cyrl": "Статистика", "en": "Statistics",
    },
    "btn.admin_channels": {
        "ru": "Каналы", "uz_latn": "Kanallar", "uz_cyrl": "Каналлар", "en": "Channels",
    },
    "btn.admin_home": {
        "ru": "Главное меню", "uz_latn": "Bosh menyu", "uz_cyrl": "Бош меню", "en": "Main menu",
    },
    "btn.admin_add": {
        "ru": "Добавить канал", "uz_latn": "Kanal qo'shish", "uz_cyrl": "Канал қўшиш", "en": "Add channel",
    },
    "btn.admin_back": {
        "ru": "Назад", "uz_latn": "Orqaga", "uz_cyrl": "Орқага", "en": "Back",
    },
    "btn.admin_cancel": {
        "ru": "Отмена", "uz_latn": "Bekor qilish", "uz_cyrl": "Бекор қилиш", "en": "Cancel",
    },
    "btn.admin_confirm_del": {
        "ru": "Да, удалить", "uz_latn": "Ha, o'chirish", "uz_cyrl": "Ҳа, ўчириш", "en": "Yes, delete",
    },
    "btn.admin_cancel_del": {
        "ru": "Отмена", "uz_latn": "Bekor qilish", "uz_cyrl": "Бекор қилиш", "en": "Cancel",
    },
    "btn.admin_panel": {
        "ru": "Админ-панель", "uz_latn": "Admin panel", "uz_cyrl": "Админ панел", "en": "Admin panel",
    },
    "btn.admin_broadcast": {
        "ru": "Рассылка", "uz_latn": "Xabar yuborish", "uz_cyrl": "Хабар юбориш", "en": "Broadcast",
    },

    # === Рассылка ===
    "admin.broadcast_prompt": {
        "ru": f"{E['plane']} <b>Массовая рассылка</b>\n\nОтправь текст/фото/видео для рассылки.\nПоддерживается HTML.",
        "uz_latn": f"{E['plane']} <b>Ommaviy xabar</b>\n\nYuborish uchun matn/rasm/video yuboring.\nHTML qo'llab-quvvatlanadi.",
        "uz_cyrl": f"{E['plane']} <b>Оммавий хабар</b>\n\nЮбориш учун матн/расм/видео юборинг.\nHTML қўллаб-қувватланади.",
        "en": f"{E['plane']} <b>Mass broadcast</b>\n\nSend text/photo/video to broadcast.\nHTML supported.",
    },
    "admin.broadcast_preview": {
        "ru": f"{E['eye']} <b>Предпросмотр</b>\n\nОтправить это сообщение всем юзерам?",
        "uz_latn": f"{E['eye']} <b>Oldindan ko'rish</b>\n\nBu xabarni barcha foydalanuvchilarga yuborishni xohlaysizmi?",
        "uz_cyrl": f"{E['eye']} <b>Олдиндан кўриш</b>\n\nБу хабарни барча фойдаланувчиларга юборишни хоҳлайсизми?",
        "en": f"{E['eye']} <b>Preview</b>\n\nSend this message to all users?",
    },
    "admin.broadcast_confirm": {
        "ru": "Да, отправить", "uz_latn": "Ha, yuborish", "uz_cyrl": "Ҳа, юбориш", "en": "Yes, send",
    },
    "admin.broadcast_cancel": {
        "ru": "Отмена", "uz_latn": "Bekor qilish", "uz_cyrl": "Бекор қилиш", "en": "Cancel",
    },
    "admin.broadcast_started": {
        "ru": f"{E['plane']} Рассылка запущена... Ожидай отчёт.",
        "uz_latn": f"{E['plane']} Xabar yuborilmoqda... Hisobotni kuting.",
        "uz_cyrl": f"{E['plane']} Хабар юборилмоқда... Ҳисоботни кутинг.",
        "en": f"{E['plane']} Broadcast started... Wait for report.",
    },
    "admin.broadcast_no_msg": {
        "ru": f"{E['cross']} Нет сообщения",
        "uz_latn": f"{E['cross']} Xabar yo'q",
        "uz_cyrl": f"{E['cross']} Хабар йўқ",
        "en": f"{E['cross']} No message",
    },
    "admin.channel_duplicate": {
        "ru": f"{E['cross']} Канал <code>{{channel_id}}</code> уже добавлен",
        "uz_latn": f"{E['cross']} Kanal <code>{{channel_id}}</code> allaqachon qo'shilgan",
        "uz_cyrl": f"{E['cross']} Канал <code>{{channel_id}}</code> аллақачон қўшилган",
        "en": f"{E['cross']} Channel <code>{{channel_id}}</code> is already added",
    },
    "admin.broadcast_done": {
        "ru": f"{E['chart']} <b>Рассылка завершена!</b>\n\n{E['check']} Доставлено: <b>{{success}}</b>\n{E['cross']} Ошибок: <b>{{failed}}</b>\n{E['users']} Всего: <b>{{total}}</b>",
        "uz_latn": f"{E['chart']} <b>Xabar yuborish tugadi!</b>\n\n{E['check']} Yetkazildi: <b>{{success}}</b>\n{E['cross']} Xatolar: <b>{{failed}}</b>\n{E['users']} Jami: <b>{{total}}</b>",
        "uz_cyrl": f"{E['chart']} <b>Хабар юбориш тугади!</b>\n\n{E['check']} Етказилди: <b>{{success}}</b>\n{E['cross']} Хатолар: <b>{{failed}}</b>\n{E['users']} Жами: <b>{{total}}</b>",
        "en": f"{E['chart']} <b>Broadcast complete!</b>\n\n{E['check']} Delivered: <b>{{success}}</b>\n{E['cross']} Failed: <b>{{failed}}</b>\n{E['users']} Total: <b>{{total}}</b>",
    },

    # === Описания команд бота (для меню Telegram) ===
    "cmd.start": {
        "ru": "Запустить бота",
        "uz_latn": "Botni boshlash",
        "uz_cyrl": "Ботни бошлаш",
        "en": "Start the bot",
    },
    "cmd.menu": {
        "ru": "Главное меню",
        "uz_latn": "Bosh menyu",
        "uz_cyrl": "Бош меню",
        "en": "Main menu",
    },
    "cmd.profile": {
        "ru": "Мой профиль",
        "uz_latn": "Mening profilim",
        "uz_cyrl": "Менинг профилим",
        "en": "My profile",
    },
    "cmd.help": {
        "ru": "Помощь",
        "uz_latn": "Yordam",
        "uz_cyrl": "Ёрдам",
        "en": "Help",
    },
    "cmd.language": {
        "ru": "Сменить язык",
        "uz_latn": "Tilni o'zgartirish",
        "uz_cyrl": "Тилни ўзгартириш",
        "en": "Change language",
    },
}


def t(key: str, lang: str = "ru", **kwargs) -> str:
    """Получить перевод по ключу и языку"""
    translations = TRANSLATIONS.get(key, {})
    text = translations.get(lang, translations.get("ru", f"[{key}]"))
    if kwargs:
        text = text.format(**kwargs)
    return text


def detect_language(language_code: str | None) -> str:
    """Определяет язык по Telegram: ru → русский, uz → узбекский (латиница), остальное → английский"""
    if not language_code:
        return "en"
    if language_code.startswith("ru"):
        return "ru"
    if language_code.startswith("uz"):
        return "uz_latn"
    return "en"
