import localization
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton

main = ReplyKeyboardBuilder()
for main_text in localization.student_main:
    main.add(
        KeyboardButton(text=main_text)
    )
main.adjust(3)
