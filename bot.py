import requests
import time
import json
from datetime import datetime

TOKEN = "8307606973:AAFZt4Dr3qxEwlsOFSGFAaVvigbPvUwSppw"

print("🚀 TenderTop_bot запущен на Heroku!")

class TenderBot:
    def __init__(self):
        self.users = {}
        self.tenders = [
            {
                'id': 1,
                'title': '🏗️ Строительство школы в Нур-Султане',
                'deadline': '25.12.2024',
                'budget': '2.5 млн ₸',
                'contacts': '+7 777 123 4567',
                'category': 'construction'
            },
            {
                'id': 2, 
                'title': '📦 Поставка компьютеров для университета',
                'deadline': '30.12.2024',
                'budget': '3.8 млн ₸',
                'contacts': '+7 701 234 5678',
                'category': 'supply'
            },
            {
                'id': 3,
                'title': '🔧 Ремонт дорожного покрытия в Алматы',
                'deadline': '15.01.2025', 
                'budget': '5.2 млн ₸',
                'contacts': '+7 705 555 8899',
                'category': 'construction'
            }
        ]
        self.start_time = datetime.now()
    
    def send_message(self, chat_id, text):
        try:
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def handle_start(self, chat_id, username):
        if str(chat_id) not in self.users:
            self.users[str(chat_id)] = {
                'username': username,
                'joined': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'message_count': 0
            }
        
        self.users[str(chat_id)]['message_count'] += 1
        
        return f"""🤖 <b>Добро пожаловать в TenderTop_bot, {username}!</b>

✅ <b>Бот работает на Heroku 24/7!</b>

🚀 <b>Команды:</b>
/start - информация
/tender - тендеры  
/stats - статистика
/help - справка

📊 <b>Функции:</b>
• Актуальные тендеры
• Детальная информация
• Быстрые ответы

🌐 <b>Хостинг:</b> Heroku"""

    def handle_tender(self, chat_id, username):
        if str(chat_id) not in self.users:
            self.users[str(chat_id)] = {'username': username, 'message_count': 0}
        
        self.users[str(chat_id)]['message_count'] += 1
        
        response = "🏗️ <b>АКТИВНЫЕ ТЕНДЕРЫ</b>\n\n"
        
        for tender in self.tenders:
            response += f"<b>{tender['title']}</b>\n"
            response += f"   📅 <i>Срок:</i> {tender['deadline']}\n"
            response += f"   💰 <i>Бюджет:</i> {tender['budget']}\n"
            response += f"   📞 <i>Контакты:</i> {tender['contacts']}\n"
            response += f"   🏷️ <i>Категория:</i> {tender['category']}\n\n"
        
        response += f"<i>Всего тендеров: {len(self.tenders)}</i>"
        return response

    def handle_stats(self, chat_id, username):
        if str(chat_id) not in self.users:
            self.users[str(chat_id)] = {'username': username, 'message_count': 0}
        
        self.users[str(chat_id)]['message_count'] += 1
        
        users_count = len(self.users)
        uptime = datetime.now() - self.start_time
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        
        return f"""📊 <b>СТАТИСТИКА СИСТЕМЫ</b>

👥 <b>Пользователей:</b> {users_count}
📋 <b>Тендеров:</b> {len(self.tenders)}
⏰ <b>Время работы:</b> {hours}ч {minutes}м
🕒 <b>Запущен:</b> {self.start_time.strftime('%H:%M:%S')}

🌐 <b>Хостинг:</b> Heroku
✅ <b>Статус:</b> Работает нормально"""

    def handle_help(self, chat_id, username):
        if str(chat_id) not in self.users:
            self.users[str(chat_id)] = {'username': username, 'message_count': 0}
        
        self.users[str(chat_id)]['message_count'] += 1
        
        return """📖 <b>СПРАВКА TENDERTOP_BOT</b>

<b>Основные команды:</b>
/start - информация о боте
/tender - просмотр активных тендеров  
/stats - статистика системы
/help - эта справка

<b>Как использовать:</b>
1. Напишите команду боту
2. Получите мгновенный ответ
3. Используйте /tender для тендеров

<b>Техническая информация:</b>
• Хостинг: Heroku
• Статус: 24/7 онлайн
• Версия: 2.0

💡 <b>Совет:</b> Начните с команды /tender"""

bot = TenderBot()

def main():
    offset = 0
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
            params = {'offset': offset, 'timeout': 30}
            response = requests.get(url, params=params, timeout=35)
            data = response.json()
            
            if data.get('ok') and data.get('result'):
                updates = data['result']
                
                for update in updates:
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        text = message.get('text', '').strip()
                        username = message['chat'].get('first_name', 'User')
                        
                        print(f"📩 {username}: {text}")
                        
                        if text == '/start':
                            response_text = bot.handle_start(chat_id, username)
                        elif text == '/tender':
                            response_text = bot.handle_tender(chat_id, username)
                        elif text == '/stats':
                            response_text = bot.handle_stats(chat_id, username)
                        elif text == '/help':
                            response_text = bot.handle_help(chat_id, username)
                        else:
                            response_text = f"💬 <b>{username}</b>, я получил: \"{text}\"\n\n🤖 Используйте /help для списка команд"
                        
                        bot.send_message(chat_id, response_text)
                        offset = update['update_id'] + 1
                        
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
