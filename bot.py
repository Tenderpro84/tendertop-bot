import os
import requests
import time

TOKEN = "8307606973:AAFZt4Dr3qxEwlsOFSGFAaVvigbPvUwSppw"

print("🚀 TenderTop_bot запущен на Heroku!")

offset = 0
while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=30"
        response = requests.get(url, timeout=35)
        data = response.json()
        
        if data.get('ok') and data.get('result'):
            for update in data['result']:
                if 'message' in update:
                    msg = update['message']
                    chat_id = msg['chat']['id']
                    text = msg.get('text', '')
                    username = msg['chat'].get('first_name', 'User')
                    
                    print(f"📩 {username}: {text}")
                    
                    if text == '/start':
                        response_text = f"🤖 Привет {username}! Бот работает на Heroku! 🚀"
                    elif text == '/tender':
                        response_text = "🏗️ Тендеры:\n• Строительство\n• Поставки\n• Ремонт"
                    else:
                        response_text = f"💬 Получил: {text}"
                    
                    requests.post(
                        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                        json={'chat_id': chat_id, 'text': response_text}
                    )
                    
                    print("📤 Ответ отправлен")
                    offset = update['update_id'] + 1
                    
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
