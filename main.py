import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ParseMode, \
    ChatAction
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from newsapi import NewsApiClient
from random import randrange
from functools import wraps
import os

TOKEN = '1027411203:AAEuKTaCQLPDkzBh6o3L0vfe9nrOcoE9_HY'
api = NewsApiClient(api_key='cbd9310b8e8e4159ac00599c29e6e6d0')
# PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN, use_context=True)
MENU, CHOOSE_NEWS, CHOOSE_SOURCES1, CHOOSE_SOURCES2 = range(4)
# article_num = []

def send_typing_action(func):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return func(update, context, *args, **kwargs)

    return command_func


def get_random(num_articles):
    return randrange(num_articles)

def time_change(utc_time):
    datetime_str = utc_time
    datetime_str = datetime_str.replace("T", " ")
    datetime_str = datetime_str.replace("Z", "")
    i = int(datetime_str[11:13])
    i = i + 8
    hours = 0
    if i >24:
        hours = i -24
        return (datetime_str[:10] + ' 0' + str(hours) + datetime_str[13:])
    elif i < 10:
        hours = i
        return (datetime_str[:10] + ' 0' + str(hours) + datetime_str[13:])
    elif i == 24:
        hours = i
        return (datetime_str[:10] + ' 00' + datetime_str[13:])
    else:
        hours = i
        return (datetime_str[:10] + " " + str(hours) + datetime_str[13:])

def check_valid(article, data):
    print(article)
    if article['title'] == "None" or article['urlToImage'] == "None" or article['description'] == "None" or article[
        'url'] == "None" or article['description'] is None or article['urlToImage'] == 'null' or article[
        'urlToImage'] is None:
        search_article(data)
    else:
        title = article['title']
        img_pic = article['urlToImage']
        description = article['description']
        # content = re.sub("[\(\[].*?[\)\]]", "", content)
        url = article['url']
        published_at = article['publishedAt']
        published_at_modified = time_change(published_at)
        caption = '*{}*\n\n{}\n\n'.format(title, description)
        return caption, img_pic, url, published_at_modified


def search_article(data):
    num_articles = data['totalResults']
    if num_articles > 100:
        num_articles = 100
    num = get_random(num_articles)
    article = data['articles'][num]
    return check_valid(article, data)


def get_news(category):
    print("called get_news")
    data = api.get_top_headlines(country="sg", page_size=100, category=category)
    return search_article(data)


def print_news(category, published_at, caption, img_pic, url, chat_id, context):
    keyboard = [[InlineKeyboardButton(text="Read more", url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_photo(chat_id=chat_id, photo=img_pic, caption="*{}*\n\n".format(category) + caption + "Published at: _{}_".format(published_at), parse_mode=telegram.ParseMode.MARKDOWN,
                           reply_markup=reply_markup)

"""=============================SG TOP HEADLINES=============================="""

@send_typing_action
def news(update, context):
    print("called")
    caption, img_pic, url, published_at= get_news("general")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "General 🌎"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def business(update, context):
    print("called")
    caption, img_pic, url, published_at = get_news("business")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Business 💰"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)

@send_typing_action
def health(update, context):
    print("called")
    caption, img_pic, url, published_at = get_news("health")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Health 💊"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def sports(update, context):
    print("called")
    caption, img_pic, url, published_at = get_news("sports")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Sports 🥇"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def entertainment(update, context):
    print("called")
    caption, img_pic, url, published_at = get_news("entertainment")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Entertainment 🎮"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def technology(update, context):
    print("called")
    caption, img_pic, url, published_at = get_news("science")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Science 🧬"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def science(update, context):
    print("called")
    caption, img_pic, url, published_at = get_news("entertainment")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Entertainment 🎮"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


"""=============================TOP NEWS CHANNEL=============================="""

def get_sources(source):
    print("called get_sources")
    data = api.get_everything(sources=source, page_size=100)
    print(data)
    return search_article(data)

@send_typing_action
def abc(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("abc-news")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "ABC News 🔤"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def bbc(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("bbc-news")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "BBC News ⚫"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def bi(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("business-insider")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Business Insider 👔"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def cnbc(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("cnbc")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "CNBC 🌈"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def cnn(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("cnn")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "CNN 🔴"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def espn(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("espn")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "ESPN 🏅"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)

@send_typing_action
def fox(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("fox-news")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "FOX News 🦊"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def independent(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("independent")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "The Independent 🦅"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def natgeo(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("national-geographic")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "National Geographic 🟡"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def techcrunch(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("techcrunch")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Techcrunch ‍💻"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def verge(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("the-verge")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "The Verge 📱"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def time(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("time")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "TIME 🕒"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)


@send_typing_action
def wired(update, context):
    print("called")
    caption, img_pic, url, published_at = get_sources("wired")
    print(caption, img_pic, url)
    chat_id = update.message.chat_id
    category = "Wired 🔬"
    print_news(category, published_at, caption, img_pic, url, chat_id, context)

@send_typing_action
def about(update, context):
    menu_reply_keyboard = [['SG Top Headlines 🇸🇬'], ['Popular News Channel 📰'], ['About ℹ️']]
    update.message.reply_text('SG Top News Bot is free-to-use. It is developed in Python and built on News API. More information on the API can be found on <a href="https://newsapi.org/">here</a>.', parse_mode=telegram.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard))
    return MENU

#\n\nThis bot is developed as a side project by Gerald Lim(SUTD) and contributed by Boon Siong(NTU). \n\nSpecial mention to Teng Fone(SUTD) for his guidance.

def categories(update, context):
    categories_reply_keyboard = [['General 🌎', 'Business 💰'], ['Health 💊', 'Sports 🥇'],
                                 ['Entertainment 🎮', 'Technology 💻'], ['Science 🧬', 'Menu️']]
    update.message.reply_text("Choose a news category of your choice! News articles are randomly generated.",
                              reply_markup=ReplyKeyboardMarkup(categories_reply_keyboard))
    return CHOOSE_NEWS


def sources(update, context):
    sources_reply_keyboard = [['ABC News 🔤', 'BBC News ⚫'], ['Business Insider 👔', 'CNBC 🌈'], ['CNN 🔴', 'ESPN 🏅'],
                              ['Menu️', 'Next']]
    update.message.reply_text("Choose from a list of our top news sources! News articles are randomly generated.",
                              reply_markup=ReplyKeyboardMarkup(sources_reply_keyboard))
    return CHOOSE_SOURCES1


def more_sources(update, context):
    more_sources_reply_keyboard = [['Fox News 🦊', 'Independent 🦅'], ['Nat Geo 🟡', 'Techcrunch 👨‍💻'],
                                   ['The Verge 📱', 'TIME 🕒'], ['Back️', 'Wired 🔬']]
    update.message.reply_text("Choose from more top news sources!",
                              reply_markup=ReplyKeyboardMarkup(more_sources_reply_keyboard))
    return CHOOSE_SOURCES2


def start(update, context):
    menu_reply_keyboard = [['SG Top Headlines 🇸🇬'], ['Popular News Channel 📰'], ['About ℹ️']]
    update.message.reply_text(
        "Welcome to SG Top News 📰, where we provide you your daily dose of top headlines from Singapore 🇸🇬 and from popular news channels such as CNN 🔴 , ESPN 🏅️, Fox News 🦊 and many more.",
        reply_markup=ReplyKeyboardMarkup(menu_reply_keyboard))
    return MENU

def main():
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('about', about)],
        states={
            MENU: [MessageHandler(Filters.regex('^SG Top Headlines 🇸🇬'), categories),
                   MessageHandler(Filters.regex('^Popular News Channel 📰'), sources),
                   MessageHandler(Filters.regex('^About ℹ️'), about)],
            CHOOSE_NEWS: [MessageHandler(Filters.regex('^General'), news),
                          MessageHandler(Filters.regex('^Business'), business),
                          MessageHandler(Filters.regex('^Health'), health),
                          MessageHandler(Filters.regex('^Sports'), sports),
                          MessageHandler(Filters.regex('^Entertainment'), entertainment),
                          MessageHandler(Filters.regex('^Technology'), technology),
                          MessageHandler(Filters.regex('^Science'), science)],
            CHOOSE_SOURCES1: [MessageHandler(Filters.regex('^ABC News'), abc),
                              MessageHandler(Filters.regex('^BBC News'), bbc),
                              MessageHandler(Filters.regex('^Business Insider'), bi),
                              MessageHandler(Filters.regex('^CNBC'), cnbc),
                              MessageHandler(Filters.regex('^CNN'), cnn),
                              MessageHandler(Filters.regex('^ESPN'), espn),
                              MessageHandler(Filters.regex('Next'), more_sources)],
            CHOOSE_SOURCES2: [MessageHandler(Filters.regex('^Fox News'), fox),
                              MessageHandler(Filters.regex('^Independent'), independent),
                              MessageHandler(Filters.regex('^Nat Geo'), natgeo),
                              MessageHandler(Filters.regex('^Techcrunch'), techcrunch),
                              MessageHandler(Filters.regex('^TIME'), time),
                              MessageHandler(Filters.regex('^The Verge'), verge),
                              MessageHandler(Filters.regex('^Wired'), wired)]
        },
        fallbacks=[MessageHandler(Filters.regex('Menu'), start, pass_user_data=True),
                   MessageHandler(Filters.regex("Back"), sources, pass_user_data=True)],
        allow_reentry=True  # this line is important as it allows the user to talk to the bot anytime
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    # updater.bot.set_webhook("https://thawing-reef-95123.herokuapp.com/ " + TOKEN)
    updater.idle()


if __name__ == "__main__":
    main()
