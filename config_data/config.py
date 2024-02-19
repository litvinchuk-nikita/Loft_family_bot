from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    pay_token: str  # Токен для платежной системы
    admin_ids: list[int]  # Список id администраторов бота
    security_ids: list[int]  # Список id охраны


@dataclass
class Config:
    tg_bot: TgBot


# Создаем функцию, которая будет читать файл .env и возвращать
# экземпляр класса Config с заполненными полями token, pay_token, security_ids и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        pay_token=env('PAYMENT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMIN_IDS'))),
        security_ids=list(map(int, env.list('SECURITY_IDS')))))
