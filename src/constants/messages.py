from src.constants import emojis

welcome = f'{emojis.hello}Добро пожаловать'

access_denied = f'{emojis.block} Вам отказано в доступе к боту!'
access_denied_start = (
    f'{emojis.block} Вы зарегистрированы в системе, дождитесь, пока '
    f'администратор выдаст вам доступ.'
)
select_access_user = (
    f'{emojis.users}Нажмите на пользователя чтобы дать или забрать у него '
    f'доступ.'
)
select_access_self = f'{emojis.block}Невозможно забрать у себя доступ.'

manage_statistic = f'{emojis.statistics}Статистика'

manage_geo = f'{emojis.pin}Гео'
add_geo_name = f'{emojis.note}Напишите название для гео'
add_geo_finally = f'{emojis.check}Гео добавлено'

manage_channels = f'{emojis.speaker}Каналы'
add_channel_name = f'{emojis.note}Напишите имя для канала'
add_channel_link = f'{emojis.link}Напишите ссылку на канал или id канала'
add_channel_geo = f'{emojis.pin}Выберете гео для канала'
add_channel_incorrect_link = (
    f'{emojis.block}Некорректная ссылка на канал или id'
)
add_channel_duplicate_link = f'{emojis.block}Этот канал уже добавлен'
add_channel_duplicate_name = (
    f'{emojis.block}Канал с таким названием уже существует'
)
add_channel_finally = f'{emojis.check}Канал добавлен'
success_change_name = f'{emojis.check}Канал изменён'

manage_userbot = f'{emojis.setting}Юзербот'
userbot_phone = (
    f'{emojis.phone}Введите телефон для бота, на аккаунт с этим номером '
    f'придёт код'
)
userbot_code = f'{emojis.phone_arrow}Введите код'
bad_phone = f'{emojis.block}Номер не корректен'
success_auth = f'{emojis.check}Успешная авторизация'
user_not_found = f'{emojis.block}Пользователь не найден'
invalid_code = f'{emojis.block}Не правильный код'
expired_code = f'{emojis.block}Срок действия кода истёк'
cansel = f'{emojis.block}Отменено'
stat_not_allow = f'{emojis.block}Нет доступа к статистике'
bot_not_in_channel = f'{emojis.block}Юзербота нет в канале'
bot_not_admin_in_channel = f'{emojis.block}У юзербота нет админки'
not_actual_userbot = (
    f'{emojis.block}Проверьте состояние юзербота. Добавьте его заново'
)

not_defined_geo_name = 'Нераспредёленные'
