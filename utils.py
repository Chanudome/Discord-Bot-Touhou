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

def send_discord_webhook(webhook_url, content, source_name, news_url=None, image_url=None):
    """ส่งข้อความไปยัง Discord ผ่าน Webhook (แบบ Embed)"""
    if not webhook_url:
        print("⚠️ ไม่พบ Discord Webhook URL")
        return

    # รูปโปรไฟล์อายะ (ภาค 10.5)
    avatar_url = "https://en.touhouwiki.net/images/thumb/8/87/Th105Aya.png/200px-Th105Aya.png"

    # เอาลิงก์มาต่อท้ายเนื้อหาข่าวตรงๆ เลย (ให้กดง่ายๆ)
    final_description = content
    if news_url:
        final_description += f"\n\n🔗 **อ่านต่อ:** {news_url}"

    # สร้าง Embed Object (กรอบข้อความสวยๆ)
    embed = {
        "description": final_description, 
        "color": 12525102,              # สีแดงโทนอายะ (#BF1E2E)
        "footer": {
            "text": f"📰 {source_name} • Bunbunmaru Newspaper"
        },
        "author": {
            "name": "Shameimaru Aya",
            "icon_url": avatar_url
        }
    }

    # ถ้ามีรูปภาพข่าว ให้แนบไปด้วย
    if image_url:
        embed["image"] = {"url": image_url}

    # ประกอบร่าง JSON ตามมาตรฐาน Discord
    data = {
        "username": "Bunbunmaru Newspaper",
        "avatar_url": avatar_url,
        "embeds": [embed]
    }

    try:
        response = requests.post(webhook_url, json=data)
        response.raise_for_status()
        print(f"✅ ส่งข่าว (Embed) จาก {source_name} สำเร็จ")
    except Exception as e:
        print(f"❌ ส่ง Discord ล้มเหลว: {e}")
