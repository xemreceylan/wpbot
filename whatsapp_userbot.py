#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp UserBot v4.0 - AI Powered
Google Gemini Integration
"""

import os
import sys
import time
import json
import re
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from typing import Dict, List, Optional, Callable
import importlib.util
import traceback
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.chrome.options import Options
except ImportError:
    print("pip install selenium")
    exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('userbot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GeminiAI:
    """Google Gemini AI"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.enabled = bool(self.api_key)
        
        if self.enabled:
            logger.info("✓ Gemini AI aktif")
        else:
            logger.warning("⚠ Gemini API yok")
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        if not self.enabled:
            return "❌ GEMINI_API_KEY ayarlanmamış!"
        
        try:
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7}
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result:
                    return result['candidates'][0]['content']['parts'][0]['text'].strip()
            return f"❌ AI hatası: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Gemini: {e}")
            return f"❌ {str(e)}"
    
    def chat(self, message: str) -> Optional[str]:
        return self.generate(message)
    
    def generate_plugin(self, description: str) -> Optional[str]:
        prompt = f"""WhatsApp UserBot için Python plugin kodu oluştur.

Açıklama: {description}

Kurallar:
1. Sadece execute fonksiyonu içindeki kodu yaz
2. 4 boşluk girintili
3. bot ve args parametrelerini kullan
4. return ile string döndür

Sadece kodu döndür."""
        
        result = self.generate(prompt, max_tokens=800)
        if result and not result.startswith("❌"):
            result = result.replace("```python", "").replace("```", "").strip()
        return result


class PluginManager:
    def __init__(self, plugin_dir='plugins'):
        self.plugin_dir = plugin_dir
        self.plugins: Dict[str, Callable] = {}
        self.plugin_metadata: Dict[str, Dict] = {}
        
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)
        
        self.load_all_plugins()
    
    def create_plugin_from_code(self, plugin_name: str, code: str, description: str = "") -> bool:
        try:
            safe_name = re.sub(r'[^a-z0-9_]', '', plugin_name.lower())
            plugin_path = os.path.join(self.plugin_dir, f"{safe_name}.py")
            
            full_code = f'''"""
{description}
Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""

def execute(bot, args):
{code}
'''
            
            with open(plugin_path, 'w', encoding='utf-8') as f:
                f.write(full_code)
            
            return self.load_plugin(plugin_path)
            
        except Exception as e:
            logger.error(f"Plugin create: {e}")
            return False
    
    def load_plugin(self, plugin_path: str) -> bool:
        try:
            plugin_name = os.path.splitext(os.path.basename(plugin_path))[0]
            
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'execute'):
                self.plugins[plugin_name] = module.execute
                self.plugin_metadata[plugin_name] = {
                    'description': module.__doc__ or 'No desc',
                    'path': plugin_path,
                    'loaded_at': datetime.now()
                }
                logger.info(f"Plugin: {plugin_name}")
                return True
            return False
                
        except Exception as e:
            logger.error(f"Plugin load: {e}")
            return False
    
    def load_all_plugins(self):
        if not os.path.exists(self.plugin_dir):
            return
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py') and not filename.startswith('_'):
                self.load_plugin(os.path.join(self.plugin_dir, filename))
    
    def delete_plugin(self, plugin_name: str) -> bool:
        try:
            if plugin_name in self.plugin_metadata:
                path = self.plugin_metadata[plugin_name]['path']
                if plugin_name in self.plugins:
                    del self.plugins[plugin_name]
                del self.plugin_metadata[plugin_name]
                if os.path.exists(path):
                    os.remove(path)
                return True
            return False
        except:
            return False
    
    def execute_plugin(self, plugin_name: str, bot, args: str) -> Optional[str]:
        if plugin_name not in self.plugins:
            return None
        try:
            return self.plugins[plugin_name](bot, args)
        except Exception as e:
            return f"❌ Plugin error: {str(e)}"
    
    def list_plugins(self) -> List[Dict]:
        return [
            {'name': name, 'description': meta['description'].split('\n')[0][:50]}
            for name, meta in self.plugin_metadata.items()
        ]


class DatabaseManager:
    def __init__(self, db_path='userbot_data.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_name TEXT, reminder_text TEXT, reminder_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, completed BOOLEAN DEFAULT 0)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT UNIQUE, content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS message_stats (
            chat_name TEXT PRIMARY KEY, message_count INTEGER DEFAULT 0, last_message TIMESTAMP)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS auto_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT, trigger TEXT UNIQUE, response TEXT, active BOOLEAN DEFAULT 1)''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS plugin_data (
            plugin_name TEXT, data_key TEXT, data_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (plugin_name, data_key))''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS ai_conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT, chat_name TEXT, user_message TEXT, ai_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        conn.commit()
        conn.close()
    
    def add_reminder(self, chat_name: str, text: str, time: datetime):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT INTO reminders (chat_name, reminder_text, reminder_time) VALUES (?, ?, ?)',
                     (chat_name, text, time))
        conn.commit()
        conn.close()
    
    def get_pending_reminders(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, chat_name, reminder_text FROM reminders WHERE reminder_time <= ? AND completed = 0',
                      (datetime.now(),))
        reminders = cursor.fetchall()
        conn.close()
        return reminders
    
    def complete_reminder(self, reminder_id: int):
        conn = sqlite3.connect(self.db_path)
        conn.execute('UPDATE reminders SET completed = 1 WHERE id = ?', (reminder_id,))
        conn.commit()
        conn.close()
    
    def save_note(self, tag: str, content: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT OR REPLACE INTO notes (tag, content) VALUES (?, ?)', (tag, content))
        conn.commit()
        conn.close()
    
    def get_note(self, tag: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT content FROM notes WHERE tag = ?', (tag,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def list_notes(self) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT tag FROM notes ORDER BY created_at DESC')
        notes = [row[0] for row in cursor.fetchall()]
        conn.close()
        return notes
    
    def delete_note(self, tag: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM notes WHERE tag = ?', (tag,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return deleted
    
    def update_message_stats(self, chat_name: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''INSERT INTO message_stats (chat_name, message_count, last_message) VALUES (?, 1, ?) 
                       ON CONFLICT(chat_name) DO UPDATE SET message_count = message_count + 1, last_message = ?''',
                    (chat_name, datetime.now(), datetime.now()))
        conn.commit()
        conn.close()
    
    def get_stats(self) -> List[tuple]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT chat_name, message_count FROM message_stats ORDER BY message_count DESC LIMIT 10')
        stats = cursor.fetchall()
        conn.close()
        return stats
    
    def add_auto_reply(self, trigger: str, response: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT OR REPLACE INTO auto_replies (trigger, response) VALUES (?, ?)', (trigger, response))
        conn.commit()
        conn.close()
    
    def get_auto_reply(self, message: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT trigger, response FROM auto_replies WHERE active = 1')
        for trigger, response in cursor.fetchall():
            if trigger.lower() in message.lower():
                conn.close()
                return response
        conn.close()
        return None
    
    def save_plugin_data(self, plugin_name: str, key: str, value: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT OR REPLACE INTO plugin_data (plugin_name, data_key, data_value) VALUES (?, ?, ?)',
                    (plugin_name, key, value))
        conn.commit()
        conn.close()
    
    def get_plugin_data(self, plugin_name: str, key: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT data_value FROM plugin_data WHERE plugin_name = ? AND data_key = ?',
                      (plugin_name, key))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def save_ai_conversation(self, chat_name: str, user_msg: str, ai_resp: str):
        conn = sqlite3.connect(self.db_path)
        conn.execute('INSERT INTO ai_conversations (chat_name, user_message, ai_response) VALUES (?, ?, ?)',
                    (chat_name, user_msg, ai_resp))
        conn.commit()
        conn.close()


class WhatsAppUserBot:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.db = DatabaseManager()
        self.plugin_manager = PluginManager()
        self.ai = GeminiAI()
        self.last_messages = defaultdict(str)
        self.afk_mode = False
        self.afk_message = "Müsait değilim."
        self.auto_reply_enabled = True
        self.ai_mode = False
        self.prefix = "."
        
        self.commands = {
            'help': self.cmd_help, 'yardim': self.cmd_help,
            'ai': self.cmd_ai, 'aisor': self.cmd_ai_ask, 'aichat': self.cmd_ai_chat,
            'aiplugin': self.cmd_ai_plugin,
            'hatirlatma': self.cmd_reminder, 'reminder': self.cmd_reminder,
            'not': self.cmd_note, 'notlar': self.cmd_list_notes, 'notsil': self.cmd_delete_note,
            'istatistik': self.cmd_stats, 'stats': self.cmd_stats,
            'afk': self.cmd_afk, 'otocevap': self.cmd_auto_reply,
            'hesapla': self.cmd_calculate, 'ping': self.cmd_ping,
            'zaman': self.cmd_time, 'google': self.cmd_google,
            'spam': self.cmd_spam, 'bilgi': self.cmd_info,
            'plugin': self.cmd_plugin, 'pluginler': self.cmd_list_plugins,
            'pluginsil': self.cmd_delete_plugin,
        }
    
    def setup_driver(self):
        logger.info("Chrome başlatılıyor...")
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--user-data-dir=./User_Data')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://web.whatsapp.com')
        logger.info("WhatsApp Web açıldı")
    
    def wait_for_login(self, timeout=60):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            logger.info("✓ Giriş başarılı!")
            return True
        except TimeoutException:
            logger.error("Giriş zaman aşımı!")
            return False
    
    def get_unread_chats(self):
        try:
            return self.driver.find_elements(By.XPATH, '//div[contains(@class, "unread")]//span[@data-icon="default-user"]/../../../..')
        except:
            return []
    
    def open_chat(self, chat_element):
        try:
            chat_element.click()
            time.sleep(1)
            return True
        except:
            return False
    
    def get_chat_name(self):
        try:
            return self.driver.find_element(By.XPATH, '//header//div[@contenteditable="false"]//span[@dir="auto"]').text
        except:
            return "Unknown"
    
    def get_last_message(self):
        try:
            messages = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]//span[@class="selectable-text copyable-text"]')
            return messages[-1].text if messages else ""
        except:
            return ""
    
    def send_message(self, message: str):
        try:
            box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            for i, line in enumerate(message.split('\n')):
                box.send_keys(line)
                if i < len(message.split('\n')) - 1:
                    box.send_keys(Keys.SHIFT + Keys.ENTER)
            box.send_keys(Keys.ENTER)
            time.sleep(0.5)
            return True
        except Exception as e:
            logger.error(f"Send: {e}")
            return False
    
    def parse_command(self, message: str):
        if not message.startswith(self.prefix):
            return None, None
        parts = message[len(self.prefix):].split(maxsplit=1)
        return parts[0].lower(), parts[1] if len(parts) > 1 else ""
    
    def cmd_help(self, args: str) -> str:
        return """🤖 *UserBot v4.0*

🧠 *AI:*
.ai - Yardım
.aisor <soru>
.aichat - Sohbet modu
.aiplugin <açıklama>

📝 *Temel:*
.help, .ping, .zaman, .bilgi

⏰ *Hatırlatma:*
.hatirlatma <dk> <mesaj>
.not <etiket> [içerik]

🔌 *Plugin:*
.plugin | .aiplugin
.pluginler | .pluginsil

🤖 *.afk | .otocevap
🛠 .hesapla | .google | .spam
📊 .istatistik"""
    
    def cmd_ai(self, args: str) -> str:
        return """🤖 *AI Komutları*

.ai <mesaj> - AI sohbet
.aisor <soru> - Soru sor
.aichat - Sürekli AI modu
.aiplugin <açıklama> - AI plugin oluştur

Örnek:
.aisor Python nedir?
.aiplugin bitcoin fiyatı gösteren plugin"""
    
    def cmd_ai_ask(self, args: str) -> str:
        if not args:
            return "❌ Kullanım: .aisor <soru>"
        response = self.ai.chat(args)
        if response:
            self.db.save_ai_conversation(self.get_chat_name(), args, response)
        return f"🤖 {response}"
    
    def cmd_ai_chat(self, args: str) -> str:
        self.ai_mode = not self.ai_mode
        return f"🤖 AI Sohbet: {'AÇIK' if self.ai_mode else 'KAPALI'}"
    
    def cmd_ai_plugin(self, args: str) -> str:
        if not args:
            return "❌ Kullanım: .aiplugin <açıklama>\n\nÖrnek: .aiplugin bitcoin fiyatı"
        
        self.send_message("🤖 AI plugin oluşturuyor...")
        code = self.ai.generate_plugin(args)
        
        if code and not code.startswith("❌"):
            name = "ai_" + re.sub(r'[^a-z0-9]', '', args.lower()[:20])
            if self.plugin_manager.create_plugin_from_code(name, code, f"AI: {args}"):
                return f"✅ Plugin oluşturuldu!\nAd: {name}\nKullanım: .{name}"
        return f"❌ Hata: {code}"
    
    def cmd_plugin(self, args: str) -> str:
        if not args:
            return "📦 Plugin:\n.plugin <ad> | <desc> | <kod>\n\nAI ile: .aiplugin <açıklama>"
        
        parts = args.split('|', 2)
        if len(parts) < 3:
            return "❌ Format: .plugin <ad> | <desc> | <kod>"
        
        name, desc, code = parts[0].strip(), parts[1].strip(), parts[2].strip()
        indented = '\n'.join(['    ' + l if l.strip() else l for l in code.split('\n')])
        
        if self.plugin_manager.create_plugin_from_code(name, indented, desc):
            return f"✅ Plugin: {name}"
        return "❌ Hata!"
    
    def cmd_list_plugins(self, args: str) -> str:
        plugins = self.plugin_manager.list_plugins()
        if not plugins:
            return "📦 Plugin yok!"
        result = "📦 *Pluginler*\n\n"
        for i, p in enumerate(plugins, 1):
            result += f"{i}. {p['name']}\n"
        return result
    
    def cmd_delete_plugin(self, args: str) -> str:
        if not args:
            return "❌ .pluginsil <ad>"
        return f"✅ Silindi: {args}" if self.plugin_manager.delete_plugin(args.strip().lower()) else "❌ Bulunamadı!"
    
    def cmd_reminder(self, args: str) -> str:
        try:
            parts = args.split(maxsplit=1)
            if len(parts) < 2:
                return "❌ .hatirlatma <dk> <mesaj>"
            minutes, text = int(parts[0]), parts[1]
            self.db.add_reminder(self.get_chat_name(), text, datetime.now() + timedelta(minutes=minutes))
            return f"✅ {minutes}dk sonra hatırlatılacak"
        except:
            return "❌ Hata!"
    
    def cmd_note(self, args: str) -> str:
        if not args:
            return "❌ .not <etiket> [içerik]"
        parts = args.split(maxsplit=1)
        if len(parts) == 1:
            content = self.db.get_note(parts[0])
            return f"📝 {parts[0]}\n\n{content}" if content else "❌ Bulunamadı!"
        self.db.save_note(parts[0], parts[1])
        return f"✅ Kaydedildi: {parts[0]}"
    
    def cmd_list_notes(self, args: str) -> str:
        notes = self.db.list_notes()
        return "📝 *Notlar*\n\n" + "\n".join([f"• {n}" for n in notes]) if notes else "📝 Not yok!"
    
    def cmd_delete_note(self, args: str) -> str:
        if not args:
            return "❌ .notsil <etiket>"
        return f"✅ Silindi: {args}" if self.db.delete_note(args.strip()) else "❌ Bulunamadı!"
    
    def cmd_stats(self, args: str) -> str:
        stats = self.db.get_stats()
        if not stats:
            return "📊 İstatistik yok!"
        result = "📊 *İstatistikler*\n\n"
        for i, (chat, count) in enumerate(stats, 1):
            result += f"{i}. {chat}: {count}\n"
        return result
    
    def cmd_afk(self, args: str) -> str:
        self.afk_mode = not self.afk_mode
        if self.afk_mode and args:
            self.afk_message = args
        return f"✅ AFK: {self.afk_message}" if self.afk_mode else "❌ AFK kapalı"
    
    def cmd_auto_reply(self, args: str) -> str:
        if not args or '|' not in args:
            return "❌ .otocevap <trigger> | <cevap>"
        parts = args.split('|', 1)
        self.db.add_auto_reply(parts[0].strip(), parts[1].strip())
        return f"✅ Eklendi: {parts[0].strip()}"
    
    def cmd_calculate(self, args: str) -> str:
        try:
            return f"🔢 {args} = {eval(args)}" if all(c in '0123456789+-*/(). ' for c in args) else "❌ Geçersiz!"
        except:
            return "❌ Hata!"
    
    def cmd_ping(self, args: str) -> str:
        return "🏓 Pong!"
    
    def cmd_time(self, args: str) -> str:
        now = datetime.now()
        return f"🕐 {now.strftime('%d.%m.%Y %H:%M:%S')}"
    
    def cmd_google(self, args: str) -> str:
        return f"🔍 https://www.google.com/search?q={args.replace(' ', '+')}" if args else "❌ .google <arama>"
    
    def cmd_spam(self, args: str) -> str:
        try:
            parts = args.split(maxsplit=1)
            count = min(int(parts[0]), 50)
            for _ in range(count):
                self.send_message(parts[1])
                time.sleep(0.3)
            return f"✅ {count} mesaj"
        except:
            return "❌ .spam <sayı> <mesaj>"
    
    def cmd_info(self, args: str) -> str:
        return f"""ℹ️ *UserBot v4.0*
🧠 AI: {'✅' if self.ai.enabled else '❌'}
🔌 Plugin: {len(self.plugin_manager.plugins)}"""
    
    def check_reminders(self):
        for rid, chat, text in self.db.get_pending_reminders():
            try:
                search = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
                search.clear()
                search.send_keys(chat)
                time.sleep(1)
                search.send_keys(Keys.ENTER)
                time.sleep(1)
                self.send_message(f"⏰ *Hatırlatma*\n\n{text}")
                self.db.complete_reminder(rid)
            except Exception as e:
                logger.error(f"Reminder: {e}")
    
    def process_message(self, message: str, chat_name: str):
        self.db.update_message_stats(chat_name)
        
        if self.afk_mode:
            self.send_message(self.afk_message)
            return
        
        if self.ai_mode and not message.startswith(self.prefix):
            if self.ai.enabled:
                response = self.ai.chat(message)
                if response:
                    self.db.save_ai_conversation(chat_name, message, response)
                    self.send_message(f"🤖 {response}")
            return
        
        command, args = self.parse_command(message)
        
        if command and command in self.commands:
            try:
                response = self.commands[command](args)
                if response:
                    self.send_message(response)
            except Exception as e:
                logger.error(f"CMD: {e}")
            return
        
        if command and command in self.plugin_manager.plugins:
            try:
                response = self.plugin_manager.execute_plugin(command, self, args)
                if response:
                    self.send_message(response)
            except Exception as e:
                logger.error(f"Plugin: {e}")
            return
        
        if self.auto_reply_enabled:
            auto_reply = self.db.get_auto_reply(message)
            if auto_reply:
                self.send_message(auto_reply)
    
    def run(self):
        try:
            self.setup_driver()
            if not self.wait_for_login():
                return
            
            logger.info(f"🤖 Bot aktif! AI: {'✅' if self.ai.enabled else '❌'}")
            
            while True:
                try:
                    self.check_reminders()
                    for chat in self.get_unread_chats():
                        if self.open_chat(chat):
                            name = self.get_chat_name()
                            msg = self.get_last_message()
                            if msg and msg != self.last_messages[name]:
                                self.last_messages[name] = msg
                                logger.info(f"📨 {name}: {msg[:50]}")
                                self.process_message(msg, name)
                    time.sleep(2)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"Loop: {e}")
                    time.sleep(5)
        finally:
            if self.driver:
                self.driver.quit()


def main():
    print("""
    ╔══════════════════════════════════════╗
    ║   WhatsApp UserBot v4.0             ║
    ║   AI Powered + Dynamic Plugins      ║
    ╚══════════════════════════════════════╝
    """)
    
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    bot = WhatsAppUserBot(headless=headless)
    bot.run()


if __name__ == '__main__':
    main()
