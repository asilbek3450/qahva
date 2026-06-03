from datetime import datetime

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "qahva-dasturi-demo-secret"

# ---------------------------------------------------------------------------
# Til (i18n) sozlamalari
# ---------------------------------------------------------------------------
DEFAULT_LANG = "uz"

LANGUAGES = {
    "uz": {"label": "O'zbekcha", "short": "UZ", "flag": "🇺🇿"},
    "ru": {"label": "Русский", "short": "RU", "flag": "🇷🇺"},
}

# Navigatsiya: endpoint -> har bir til uchun yorliq
NAV_LINKS = [
    ("bosh_sahifa", {"uz": "Bosh sahifa", "ru": "Главная"}),
    ("menu_page", {"uz": "Menyu", "ru": "Меню"}),
    ("about_page", {"uz": "Biz haqimizda", "ru": "О нас"}),
    ("gallery_page", {"uz": "Galereya", "ru": "Галерея"}),
    ("booking_page", {"uz": "Band qilish", "ru": "Бронь"}),
    ("contact_page", {"uz": "Aloqa", "ru": "Контакты"}),
]

# Interfeys matnlari
UI = {
    "uz": {
        "brand": "Qahva Dasturi",
        "lang_label": "Til",
        "skip_to_content": "Asosiy qismga o'tish",
        "open_menu": "Menyuni ochish",
        # Footer
        "footer_tagline": "Specialty qahva, nonushta va desertlar uchun sokin qahvaxona.",
        "footer_hours_title": "Ish vaqti",
        "footer_hours_value": "Har kuni: 09:00 - 22:00",
        "footer_contact_title": "Aloqa",
        "footer_rights": "Barcha huquqlar himoyalangan.",
        # Umumiy kontakt ma'lumotlari
        "phone": "+998 71 123 45 67",
        "email": "hello@qahvadasturi.uz",
        "address": "Toshkent, Mirzo Ulug'bek ko'chasi 27",
        "hours_full": "Har kuni 09:00 - 22:00",
        # Bosh sahifa
        "home_eyebrow": "Toshkent specialty coffee",
        "home_title": "Qahva Dasturi",
        "home_text": "Yangi qovurilgan donlar, aniq retseptlar va sokin muhit. Har kuni ertalabdan kechgacha qahva, choy, nonushta va desertlar tayyorlaymiz.",
        "home_btn_menu": "Menyuni ko'rish",
        "home_btn_booking": "Joy band qilish",
        "featured_eyebrow": "Bugungi tanlov",
        "featured_heading": "Eng ko'p so'raladigan ichimliklar",
        "atmos_eyebrow": "Atmosfera",
        "atmos_heading": "Ish, suhbat va dam olish uchun qulay joy",
        "atmos_text": "Qahvaxonamizda tez Wi-Fi, qulay o'tirish joylari, sokin musiqa va barista tavsiyalari bor. Yolg'iz ishlash, do'stlar bilan uchrashish yoki kichik jamoaviy suhbatlar uchun mos muhit yaratdik.",
        "atmos_link": "Biz haqimizda",
        "stats_exp": "yillik tajriba",
        "stats_drinks": "turdagi ichimlik",
        "stats_open": "har kuni ochilish",
        "home_gallery_eyebrow": "Galereya",
        "home_gallery_heading": "Qahvaxonadan lavhalar",
        # Menyu sahifasi
        "menu_eyebrow": "Menyu",
        "menu_title": "Qahva, choy, nonushta va desertlar",
        "menu_subtitle": "Har bir bo'lim tez tanlash uchun alohida saralangan.",
        "menu_filter_all": "Barchasi",
        "menu_count_one": "ta mahsulot",
        "menu_order": "Buyurtma berish",
        # Biz haqimizda
        "about_eyebrow": "Biz haqimizda",
        "about_title": "Qahva madaniyatini yaqinroq qilamiz",
        "about_subtitle": "2018-yildan beri Toshkentda sifatli qahva va mehmondo'st xizmatni bir joyga jamlaymiz.",
        "about_hist_eyebrow": "Tariximiz",
        "about_hist_heading": "Har bir retsept ortida aniq jarayon bor",
        "about_hist_p1": "Donlarni kichik partiyalarda tanlaymiz, maydalash darajasini ichimlikka qarab sozlaymiz va har bir buyurtmani barista standartlari asosida tayyorlaymiz.",
        "about_hist_p2": "Maqsadimiz oddiy: mehmon qahvani ichganda ta'm, hid va muhit bir xil darajada yoqimli bo'lishi kerak.",
        "about_val_eyebrow": "Qadriyatlar",
        "about_val_heading": "Nimalarga e'tibor beramiz",
        "value1_title": "Sifat",
        "value1_text": "Don, suv, sut va harorat nazorati bitta retsept kabi boshqariladi.",
        "value2_title": "Ochiqlik",
        "value2_text": "Baristalar ichimlik tanlashda mijozga oddiy va tushunarli tavsiya beradi.",
        "value3_title": "Qulaylik",
        "value3_text": "Zal, yorug'lik, musiqa va xizmat tezligi mehmonning kayfiyatiga moslangan.",
        # Galereya sahifasi
        "gallery_eyebrow": "Galereya",
        "gallery_title": "Ichimliklar, zal va jarayon",
        "gallery_subtitle": "Qahvaxonadagi muhitni rasmlar orqali ko'ring.",
        # Band qilish
        "booking_eyebrow": "Band qilish",
        "booking_title": "Stolni oldindan band qiling",
        "booking_subtitle": "Kichik uchrashuv, nonushta yoki kechki suhbat uchun joy ajratamiz.",
        "booking_reserve_eyebrow": "Rezerv",
        "booking_reserve_heading": "Mehmonlar soni va vaqtni yuboring",
        "booking_reserve_text": "Band qilish so'rovi qabul qilingandan keyin administrator siz bilan bog'lanadi va tafsilotlarni tasdiqlaydi.",
        "label_phone": "Telefon",
        "label_hours": "Ish vaqti",
        "label_address": "Manzil",
        "label_email": "Email",
        # Formalar
        "form_name": "Ismingiz",
        "form_phone": "Telefon",
        "form_date": "Sana",
        "form_time": "Vaqt",
        "form_guests": "Mehmonlar soni",
        "form_note": "Izoh",
        "form_note_ph": "Masalan: deraza yonidan joy",
        "form_submit_booking": "Yuborish",
        "form_contact": "Email yoki telefon",
        "form_subject": "Mavzu",
        "form_message": "Xabar",
        "form_submit_contact": "Xabar yuborish",
        # Aloqa
        "contact_eyebrow": "Aloqa",
        "contact_title": "Savol va takliflar uchun bog'laning",
        "contact_subtitle": "Buyurtma, tadbir yoki hamkorlik masalasida yozishingiz mumkin.",
        "contact_info_heading": "Ma'lumotlar",
        # JS xabarlari
        "js_alert_named": "{name}, so'rovingiz qabul qilindi.",
        "js_alert_plain": "So'rovingiz qabul qilindi.",
        "js_alert_tail": "Tez orada siz bilan bog'lanamiz.",
    },
    "ru": {
        "brand": "Qahva Dasturi",
        "lang_label": "Язык",
        "skip_to_content": "Перейти к содержимому",
        "open_menu": "Открыть меню",
        # Footer
        "footer_tagline": "Уютная кофейня для спешелти кофе, завтраков и десертов.",
        "footer_hours_title": "Часы работы",
        "footer_hours_value": "Ежедневно: 09:00 - 22:00",
        "footer_contact_title": "Контакты",
        "footer_rights": "Все права защищены.",
        # Umumiy kontakt
        "phone": "+998 71 123 45 67",
        "email": "hello@qahvadasturi.uz",
        "address": "Ташкент, улица Мирзо Улугбека 27",
        "hours_full": "Ежедневно 09:00 - 22:00",
        # Glavnaya
        "home_eyebrow": "Спешелти кофе в Ташкенте",
        "home_title": "Qahva Dasturi",
        "home_text": "Свежеобжаренные зёрна, точные рецепты и спокойная атмосфера. Каждый день с утра до вечера готовим кофе, чай, завтраки и десерты.",
        "home_btn_menu": "Смотреть меню",
        "home_btn_booking": "Забронировать столик",
        "featured_eyebrow": "Выбор дня",
        "featured_heading": "Самые популярные напитки",
        "atmos_eyebrow": "Атмосфера",
        "atmos_heading": "Удобное место для работы, встреч и отдыха",
        "atmos_text": "В нашей кофейне есть быстрый Wi-Fi, удобные места, спокойная музыка и рекомендации бариста. Мы создали среду для работы в одиночку, встреч с друзьями и небольших командных бесед.",
        "atmos_link": "О нас",
        "stats_exp": "лет опыта",
        "stats_drinks": "видов напитков",
        "stats_open": "открытие каждый день",
        "home_gallery_eyebrow": "Галерея",
        "home_gallery_heading": "Моменты из кофейни",
        # Menu
        "menu_eyebrow": "Меню",
        "menu_title": "Кофе, чай, завтраки и десерты",
        "menu_subtitle": "Каждый раздел отсортирован для быстрого выбора.",
        "menu_filter_all": "Все",
        "menu_count_one": "товаров",
        "menu_order": "Заказать",
        # O nas
        "about_eyebrow": "О нас",
        "about_title": "Делаем культуру кофе ближе",
        "about_subtitle": "С 2018 года объединяем в Ташкенте качественный кофе и гостеприимный сервис.",
        "about_hist_eyebrow": "Наша история",
        "about_hist_heading": "За каждым рецептом — чёткий процесс",
        "about_hist_p1": "Мы выбираем зёрна небольшими партиями, настраиваем степень помола под напиток и готовим каждый заказ по стандартам бариста.",
        "about_hist_p2": "Наша цель проста: когда гость пьёт кофе, вкус, аромат и атмосфера должны быть одинаково приятными.",
        "about_val_eyebrow": "Ценности",
        "about_val_heading": "На что мы обращаем внимание",
        "value1_title": "Качество",
        "value1_text": "Контроль зерна, воды, молока и температуры ведётся как единый рецепт.",
        "value2_title": "Открытость",
        "value2_text": "Бариста дают гостю простые и понятные рекомендации при выборе напитка.",
        "value3_title": "Комфорт",
        "value3_text": "Зал, освещение, музыка и скорость сервиса подстроены под настроение гостя.",
        # Galereya
        "gallery_eyebrow": "Галерея",
        "gallery_title": "Напитки, зал и процесс",
        "gallery_subtitle": "Посмотрите атмосферу кофейни в фотографиях.",
        # Bron
        "booking_eyebrow": "Бронь",
        "booking_title": "Забронируйте столик заранее",
        "booking_subtitle": "Выделим место для небольшой встречи, завтрака или вечерней беседы.",
        "booking_reserve_eyebrow": "Резерв",
        "booking_reserve_heading": "Укажите количество гостей и время",
        "booking_reserve_text": "После получения заявки на бронь администратор свяжется с вами и подтвердит детали.",
        "label_phone": "Телефон",
        "label_hours": "Часы работы",
        "label_address": "Адрес",
        "label_email": "Email",
        # Formy
        "form_name": "Ваше имя",
        "form_phone": "Телефон",
        "form_date": "Дата",
        "form_time": "Время",
        "form_guests": "Количество гостей",
        "form_note": "Комментарий",
        "form_note_ph": "Например: место у окна",
        "form_submit_booking": "Отправить",
        "form_contact": "Email или телефон",
        "form_subject": "Тема",
        "form_message": "Сообщение",
        "form_submit_contact": "Отправить сообщение",
        # Kontakty
        "contact_eyebrow": "Контакты",
        "contact_title": "Свяжитесь с нами по вопросам и предложениям",
        "contact_subtitle": "Можете написать по заказу, мероприятию или сотрудничеству.",
        "contact_info_heading": "Информация",
        # JS
        "js_alert_named": "{name}, ваша заявка принята.",
        "js_alert_plain": "Ваша заявка принята.",
        "js_alert_tail": "Мы скоро свяжемся с вами.",
    },
}

# ---------------------------------------------------------------------------
# Menyu va galereya ma'lumotlari (ikki tilli)
# ---------------------------------------------------------------------------
MENU_CATEGORIES = [
    {
        "slug": "coffee",
        "name": {"uz": "Qahva", "ru": "Кофе"},
        "items": [
            {
                "name": {"uz": "Americano", "ru": "Американо"},
                "price": {"uz": "18 000 so'm", "ru": "18 000 сум"},
                "image": "americano.jpg",
                "description": {
                    "uz": "Yengil achchiqlik va uzun ta'mga ega klassik espresso.",
                    "ru": "Классический эспрессо с лёгкой горчинкой и долгим послевкусием.",
                },
            },
            {
                "name": {"uz": "Latte", "ru": "Латте"},
                "price": {"uz": "22 000 so'm", "ru": "22 000 сум"},
                "image": "latte.jpg",
                "description": {
                    "uz": "Yumshoq sut, espresso va ipakdek nozik ko'pik.",
                    "ru": "Мягкое молоко, эспрессо и шелковистая нежная пенка.",
                },
            },
            {
                "name": {"uz": "Cappuccino", "ru": "Капучино"},
                "price": {"uz": "24 000 so'm", "ru": "24 000 сум"},
                "image": "cappuccino.jpg",
                "description": {
                    "uz": "Qalin ko'pik, espresso va sutning muvozanatli uyg'unligi.",
                    "ru": "Сбалансированное сочетание плотной пенки, эспрессо и молока.",
                },
            },
            {
                "name": {"uz": "Raf Coffee", "ru": "Раф кофе"},
                "price": {"uz": "28 000 so'm", "ru": "28 000 сум"},
                "image": "raf-coffee.jpg",
                "description": {
                    "uz": "Vanil, qaymoq va espresso asosidagi mayin ichimlik.",
                    "ru": "Нежный напиток на основе ванили, сливок и эспрессо.",
                },
            },
        ],
    },
    {
        "slug": "tea",
        "name": {"uz": "Choy", "ru": "Чай"},
        "items": [
            {
                "name": {"uz": "Ko'k choy", "ru": "Зелёный чай"},
                "price": {"uz": "14 000 so'm", "ru": "14 000 сум"},
                "image": "green-tea.jpg",
                "description": {
                    "uz": "Yangi damlangan, xushbo'y va yengil choy.",
                    "ru": "Свежезаваренный, ароматный и лёгкий чай.",
                },
            },
            {
                "name": {"uz": "Qora choy", "ru": "Чёрный чай"},
                "price": {"uz": "12 000 so'm", "ru": "12 000 сум"},
                "image": "black-tea.jpg",
                "description": {
                    "uz": "Limon yoki sut bilan tortiladigan an'anaviy choy.",
                    "ru": "Традиционный чай, который подают с лимоном или молоком.",
                },
            },
            {
                "name": {"uz": "Mevali choy", "ru": "Фруктовый чай"},
                "price": {"uz": "20 000 so'm", "ru": "20 000 сум"},
                "image": "fruit-tea.jpg",
                "description": {
                    "uz": "Olma, rezavor va dolchin notalari bilan iliq aralashma.",
                    "ru": "Тёплая смесь с нотами яблока, ягод и корицы.",
                },
            },
        ],
    },
    {
        "slug": "desserts",
        "name": {"uz": "Shirinliklar", "ru": "Десерты"},
        "items": [
            {
                "name": {"uz": "Tiramisu", "ru": "Тирамису"},
                "price": {"uz": "35 000 so'm", "ru": "35 000 сум"},
                "image": "tiramisu.jpg",
                "description": {
                    "uz": "Mascarpone kremi, kakao va espresso bilan tayyorlanadi.",
                    "ru": "Готовится с кремом маскарпоне, какао и эспрессо.",
                },
            },
            {
                "name": {"uz": "Cheesecake", "ru": "Чизкейк"},
                "price": {"uz": "32 000 so'm", "ru": "32 000 сум"},
                "image": "cheesecake.jpg",
                "description": {
                    "uz": "Qaymoqli tekstura va mevali sous bilan.",
                    "ru": "Со сливочной текстурой и фруктовым соусом.",
                },
            },
            {
                "name": {"uz": "Shokoladli tart", "ru": "Шоколадный тарт"},
                "price": {"uz": "30 000 so'm", "ru": "30 000 сум"},
                "image": "chocolate-tart.jpg",
                "description": {
                    "uz": "To'q shokolad ganashi va qarsildoq asos.",
                    "ru": "Ганаш из тёмного шоколада и хрустящая основа.",
                },
            },
        ],
    },
    {
        "slug": "breakfast",
        "name": {"uz": "Nonushta", "ru": "Завтрак"},
        "items": [
            {
                "name": {"uz": "Croissant set", "ru": "Сет с круассаном"},
                "price": {"uz": "38 000 so'm", "ru": "38 000 сум"},
                "image": "croissant.jpg",
                "description": {
                    "uz": "Croissant, sariyog', murabbo va kichik americano.",
                    "ru": "Круассан, сливочное масло, джем и маленький американо.",
                },
            },
            {
                "name": {"uz": "Avocado toast", "ru": "Тост с авокадо"},
                "price": {"uz": "42 000 so'm", "ru": "42 000 сум"},
                "image": "avocado-toast.jpg",
                "description": {
                    "uz": "Qovurilgan non, avocado, tuxum va ko'katlar.",
                    "ru": "Поджаренный хлеб, авокадо, яйцо и зелень.",
                },
            },
            {
                "name": {"uz": "Club sandwich", "ru": "Клаб-сэндвич"},
                "price": {"uz": "39 000 so'm", "ru": "39 000 сум"},
                "image": "club-sandwich.jpg",
                "description": {
                    "uz": "Tovuq, pishloq, sabzavot va maxsus sous.",
                    "ru": "Курица, сыр, овощи и фирменный соус.",
                },
            },
        ],
    },
]

GALLERY_IMAGES = [
    {
        "image": "gallery-barista.jpg",
        "title": {"uz": "Barista stoli", "ru": "Стол бариста"},
        "alt": {
            "uz": "Barista qahva tayyorlayotgan jarayon",
            "ru": "Процесс приготовления кофе бариста",
        },
    },
    {
        "image": "gallery-latte-art.jpg",
        "title": {"uz": "Latte art", "ru": "Латте-арт"},
        "alt": {
            "uz": "Latte ustidagi sut naqshi",
            "ru": "Молочный рисунок на латте",
        },
    },
    {
        "image": "gallery-hall.jpg",
        "title": {"uz": "Qulay zal", "ru": "Уютный зал"},
        "alt": {
            "uz": "Yorug' va qulay qahvaxona zali",
            "ru": "Светлый и уютный зал кофейни",
        },
    },
    {
        "image": "gallery-dessert.jpg",
        "title": {"uz": "Yangi desertlar", "ru": "Свежие десерты"},
        "alt": {
            "uz": "Qahva yonidagi desert",
            "ru": "Десерт рядом с кофе",
        },
    },
    {
        "image": "gallery-beans.jpg",
        "title": {"uz": "Qovurilgan donlar", "ru": "Обжаренные зёрна"},
        "alt": {
            "uz": "Qahva donlari yaqin planda",
            "ru": "Кофейные зёрна крупным планом",
        },
    },
    {
        "image": "gallery-friends.jpg",
        "title": {"uz": "Do'stlar uchrashuvi", "ru": "Встреча друзей"},
        "alt": {
            "uz": "Qahvaxonada suhbatlashayotgan mehmonlar",
            "ru": "Гости, беседующие в кофейне",
        },
    },
]


# ---------------------------------------------------------------------------
# Yordamchi funksiyalar
# ---------------------------------------------------------------------------
def localize(value, lang):
    """Ikki tilli qiymatdan joriy tildagisini qaytaradi."""
    if isinstance(value, dict):
        return value.get(lang, value.get(DEFAULT_LANG, ""))
    return value


def localize_node(node, lang):
    """Lug'at/ro'yxat ichidagi barcha ikki tilli qiymatlarni tarjima qiladi."""
    if isinstance(node, dict):
        if set(node.keys()) <= set(LANGUAGES) and node:
            return localize(node, lang)
        return {key: localize_node(val, lang) for key, val in node.items()}
    if isinstance(node, list):
        return [localize_node(item, lang) for item in node]
    return node


@app.before_request
def set_language():
    lang = session.get("lang", DEFAULT_LANG)
    g.lang = lang if lang in LANGUAGES else DEFAULT_LANG


@app.route("/lang/<code>")
def set_lang(code):
    if code in LANGUAGES:
        session["lang"] = code
    target = request.referrer or url_for("bosh_sahifa")
    return redirect(target)


@app.context_processor
def inject_layout_data():
    lang = getattr(g, "lang", DEFAULT_LANG)
    return {
        "lang": lang,
        "t": UI[lang],
        "languages": LANGUAGES,
        "nav_links": [(endpoint, labels[lang]) for endpoint, labels in NAV_LINKS],
        "current_year": datetime.now().year,
    }


# ---------------------------------------------------------------------------
# Sahifalar
# ---------------------------------------------------------------------------
@app.route("/")
def bosh_sahifa():
    lang = g.lang
    featured = [localize_node(item, lang) for item in MENU_CATEGORIES[0]["items"][:3]]
    gallery_preview = [localize_node(image, lang) for image in GALLERY_IMAGES[:3]]
    return render_template(
        "index.html",
        title=UI[lang]["home_title"],
        featured_items=featured,
        gallery_preview=gallery_preview,
    )


@app.route("/menu")
def menu_page():
    lang = g.lang
    categories = [localize_node(category, lang) for category in MENU_CATEGORIES]
    return render_template("menu.html", title=UI[lang]["menu_eyebrow"], menu_categories=categories)


@app.route("/about")
def about_page():
    return render_template("about.html", title=UI[g.lang]["about_eyebrow"])


@app.route("/gallery")
def gallery_page():
    lang = g.lang
    images = [localize_node(image, lang) for image in GALLERY_IMAGES]
    return render_template("gallery.html", title=UI[lang]["gallery_eyebrow"], gallery_images=images)


@app.route("/booking")
def booking_page():
    return render_template("booking.html", title=UI[g.lang]["booking_eyebrow"])


@app.route("/contact")
def contact_page():
    return render_template("contact.html", title=UI[g.lang]["contact_eyebrow"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
