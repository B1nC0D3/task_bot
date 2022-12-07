# Бот-органайзер
Бот органайзер позволяющий записывать и просматривать задачи на день.

---
## Запуск приложения
В корневой папке скачанного репозитория выполните:
```
    python3 -m venv venv    # use 'python' instead 'python3' for Win
    source venv/bin/activate # source venv/Scripts/activate for Win
    pip3 install -r requirements.txt
```
 В случае запуска с локальной машины без выделенного IP выполните следующеее:
```
 ngrok http 5000
```
Добавьте IP в файл расположенный в server/bot/main.py ссылку на ваш тоннель
Далее перейдите в папку server и запустите сервер
```
uvicorn api:app --port 5000
```

---

## Заполнение .env файла
```
TELEGRAM_TOKEN=ur_telegram_token
API_ADDRESS='http://ur_server_address:port'
```
 ---

## Технологии

- Python 3.9
- Aiogram
- FASTAPI
- SQlAlchemy