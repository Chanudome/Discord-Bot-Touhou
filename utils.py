import json
import os
import datetime
import requests
from time import mktime
from config import LOG_FILE

def get_timestamp(entry):
    """ดึงเวลาจริงจากแหล่งข่าวและแปลงเป็นรูปแบบที่อ่านง่าย"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dt = datetime.datetime.fromtimestamp(mktime(entry.published_parsed))
            return dt.strftime("%d/%m/%Y %H:%M")
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            dt = datetime.datetime.fromtimestamp(mktime(entry.updated_parsed))
            return dt.strftime("%d/%m/%Y %H:%M")
        else:
            return "ไม่ระบุเวลา"
    except:
        return "N/A"

def load_history():
    """โหลดรายการข่าวที่เคยอ่านไปแล้ว"""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_history(history_list):
    """บันทึกรายการข่าว (เก็บแค่ 200 รายการล่าสุด)"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(history_list[-200:], f, ensure_ascii=False, indent=4)

def send_discord_webhook(webhook_url, content, source_name):
    """ส่งข้อความไปยัง Discord ผ่าน Webhook"""
    if not webhook_url:
        print("⚠️ ไม่พบ Discord Webhook URL (ข้ามการส่ง Discord)")
        return

    # ลิงก์รูปโปรไฟล์ของอายะ (เปลี่ยนรูปได้ตรงนี้)
    avatar_url = "    avatar_url = "https://media.discordapp.net/attachments/1445348472466182226/1445348535942905917/Th105Aya.png?ex=69300538&is=692eb3b8&hm=1dd0867f1bc9df7d16e0a714dc07413400daa744589154f4e0e5d8f53252cdc5&=&format=webp&quality=lossless" 

    data = {
        "username": "Bunbunmaru Newspaper (Shameimaru Aya)",
        "avatar_url": avatar_url,
        "content": content
    }

    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print(f"✅ ส่งข่าวจาก {source_name} เข้า Discord สำเร็จ")
    except Exception as e:
        print(f"❌ ส่ง Discord ล้มเหลว: {e}")
