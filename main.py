import os
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ChatMemberHandler,
    filters,
)
from handlers.admin import ban_user, unban_user, mute_user, unmute_user, kick_user
from handlers.welcome import welcome_new_member, set_welcome, show_welcome
from handlers.help import help_command, start_command
from handlers.warn import warn_user, unwarn_user, show_warns, reset_warns
from handlers.pin import pin_message, unpin_message
from handlers.info import user_info
from handlers.rules import show_rules, set_rules
from handlers.filters import (
    filter_messages, antilink, antiforward,
    add_bad_word, remove_bad_word, list_bad_words,
)
from handlers.fun import poll_command, dice_command, weather_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(token).build()

    # ── Info & help ──────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", user_info))

    # ── Moderation ───────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("unban", unban_user))
    app.add_handler(CommandHandler("kick", kick_user))
    app.add_handler(CommandHandler("mute", mute_user))
    app.add_handler(CommandHandler("unmute", unmute_user))

    # ── Warn system ──────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("warn", warn_user))
    app.add_handler(CommandHandler("unwarn", unwarn_user))
    app.add_handler(CommandHandler("warns", show_warns))
    app.add_handler(CommandHandler("resetwarns", reset_warns))

    # ── Pin ──────────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("pin", pin_message))
    app.add_handler(CommandHandler("unpin", unpin_message))

    # ── Rules ────────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("rules", show_rules))
    app.add_handler(CommandHandler("setrules", set_rules))

    # ── Welcome ──────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("setwelcome", set_welcome))
    app.add_handler(CommandHandler("welcome", show_welcome))
    app.add_handler(
        ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER)
    )

    # ── Filters ──────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("antilink", antilink))
    app.add_handler(CommandHandler("antiforward", antiforward))
    app.add_handler(CommandHandler("addbadword", add_bad_word))
    app.add_handler(CommandHandler("rmbadword", remove_bad_word))
    app.add_handler(CommandHandler("badwords", list_bad_words))

    # Message filter (anti-link, anti-forward, bad words) — must be last
    app.add_handler(
        MessageHandler(filters.TEXT | filters.CAPTION, filter_messages)
    )

    # ── Fun ──────────────────────────────────────────────────────────────────
    app.add_handler(CommandHandler("poll", poll_command))
    app.add_handler(CommandHandler("dice", dice_command))
    app.add_handler(CommandHandler("weather", weather_command))

    logger.info("Bot started. Polling for updates...")
    app.run_polling(allowed_updates=["message", "chat_member"])


if __name__ == "__main__":
    main()
