import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ----------------- কনফিগারেশন -----------------
# BotFather থেকে পাওয়া টোকেনটি এখানে বসাবেন
BOT_TOKEN = '8053851661:AAHIvTgROeFSTSUg_oUjYKDlyz2N7IWzvjE'

# আপনার চ্যানেলের ইউজারনেম (লিঙ্ক থেকে নেওয়া: bdsiminfonews)
CHANNEL_USERNAME = '@bdsiminfonews' 
CHANNEL_LINK = 'https://t.me/bdsiminfonews'
# -----------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)

# ইউজার চ্যানেলে জয়েন আছে কি না তা চেক করার ফানশন
def check_user_membership(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        # ইউজার যদি এডমিন, ওনার বা মেম্বার হয় তবে True রিটার্ন করবে
        if member.status in ['creator', 'administrator', 'member']:
            return True
        return False
    except Exception as e:
        # যদি চ্যানেল না পাওয়া যায় বা বট এডমিন না থাকে
        print(f"Error checking status: {e}")
        return False

# জয়েন করার সুন্দর বাটন তৈরি করার ফাংশন
def get_join_keyboard():
    markup = InlineKeyboardMarkup()
    btn_join = InlineKeyboardButton("📢 চ্যানেলে জয়েন করুন", url=CHANNEL_LINK)
    btn_check = InlineKeyboardButton("✅ আমি জয়েন করেছি", callback_data="check_membership")
    
    # বাটন দুটি নিচে নিচে সুন্দর করে সাজানো
    markup.add(btn_join)
    markup.add(btn_check)
    return markup

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if check_user_membership(user_id):
        # ইউজার চ্যানেলে জয়েন থাকলে মূল সার্ভিস মেসেজ
        welcome_text = (
            f"👋 **হ্যালো {first_name}!**\n\n"
            f"🎉 আপনাকে আমাদের বটে স্বাগতম!\n"
            f"আপনি সফলভাবে চ্যানেল সাবস্ক্রাইব করেছেন। এখন বটের সকল ফিচার ব্যবহার করতে পারবেন।"
        )
        bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown")
    else:
        # ইউজার জয়েন না থাকলে এই মেসেজ দেখাবে
        lock_text = (
            f"👋 **হ্যালো {first_name}!**\n\n"
            f"⚠️ **বট ব্যবহারের শর্তাবলী:**\n"
            f"আমাদের বটের সার্ভিসগুলো ব্যবহার করতে হলে আপনাকে অবশ্যই আমাদের অফিশিয়াল চ্যানেলে জয়েন করতে হবে।\n\n"
            f"👉 নিচের **'📢 চ্যানেলে জয়েন করুন'** বাটনে ক্লিক করে জয়েন করুন এবং তারপর **'✅ আমি জয়েন করেছি'** বাটনে চাপ দিন।"
        )
        bot.send_message(message.chat.id, lock_text, reply_markup=get_join_keyboard(), parse_mode="Markdown")

# "আমি জয়েন করেছি" বাটনে চাপ দিলে যা হবে
@bot.callback_query_handler(func=lambda call: call.data == "check_membership")
def verify_join_button(call):
    user_id = call.from_user.id
    
    if check_user_membership(user_id):
        # পপআপ নোটিফিকেশন দেবে
        bot.answer_callback_query(call.id, "✅ ধন্যবাদ! আপনার এক্সেস আনলক করা হয়েছে।", show_alert=True)
        
        # পূর্বের জয়েন করার মেসেজটি পরিবর্তন করে মূল মেনু দিয়ে দেবে
        success_text = (
            "🎉 **অভিনন্দন!**\n\n"
            "আপনার চ্যানেল সাবস্ক্রিপশন সফল হয়েছে। এখন আপনি বটের সকল ফিচার ও সার্ভিস ব্যবহার করতে পারবেন।"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, 
            message_id=call.message.message_id, 
            text=success_text, 
            parse_mode="Markdown"
        )
    else:
        # জয়েন না করে বাটনে ক্লিক করলে অ্যালার্ট পপআপ দেখাবে
        bot.answer_callback_query(
            call.id, 
            "❌ আপনি এখনো আমাদের চ্যানেলে জয়েন করেননি!\n\nঅনুগ্রহ করে আগে জয়েন করুন, তারপর বাটনে চাপ দিন।", 
            show_alert=True
        )

# বটের বাকি সব মেসেজ বা ফিচারের জন্য প্রটেকশন
@bot.message_handler(func=lambda message: True)
def restrict_other_messages(message):
    user_id = message.from_user.id
    
    if check_user_membership(user_id):
        # এখানে আপনার বটের মূল ফিচার ও রিপ্লাইগুলোর কোড থাকবে
        bot.reply_to(message, "আপনার মেসেজটি পাওয়া গেছে। বটের ফিচার প্রসেস হচ্ছে...")
    else:
        # চ্যানেলে জয়েন না থাকলে যেকোনো মেসেজ দিলেই জয়েন করতে বলবে
        bot.send_message(
            message.chat.id, 
            "⚠️ আপনি চ্যানেলে জয়েন না করা পর্যন্ত বটের কোনো ফিচার ব্যবহার করতে পারবেন না। আগে জয়েন করুন!", 
            reply_markup=get_join_keyboard()
        )

# বট চালু রাখা
print("🤖 Bot is running...")
bot.polling(none_stop=True)