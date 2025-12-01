import json
import os
import datetime
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
