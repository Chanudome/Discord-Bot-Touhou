import feedparser
import time
import datetime
import os
from config import RSS_SOURCES
from utils import get_timestamp, load_history, save_history, send_discord_webhook
from aya_brain import aya_process_news

def run_once():
    print(f"[{datetime.datetime.now()}] 🌪️ อายะตื่นมาเช็คข่าวรอบใหม่...")
    
    # ดึง Webhook URL
    webhook_env = os.getenv("DISCORD_WEBHOOK_URL")
    target_webhooks = []
    if webhook_env:
        target_webhooks = [url.strip() for url in webhook_env.split(',') if url.strip()]
    
    print(f"📡 พบเป้าหมายการส่งข่าวทั้งหมด: {len(target_webhooks)} แห่ง")

    read_history = load_history()
    new_items_found = False

    for source in RSS_SOURCES:
        print(f"Flying to... {source['name']} 🦅")
        try:
            feed = feedparser.parse(source['url'])
            
            # [แก้ไข] เปลี่ยนจาก [:3] เป็น [:10] เพื่อให้ขุดข่าวเก่าๆ ย้อนหลังได้ลึกขึ้น
            for entry in feed.entries[:10]:
                news_id = entry.id if 'id' in entry else entry.link
                
                # ถ้าเป็นข่าวที่ยังไม่เคยอ่าน (และประวัติเราว่างอยู่ มันจะถือว่าเป็นข่าวใหม่หมด)
                if news_id not in read_history:
                    pub_date = get_timestamp(entry)
                    print(f"📸 พบข่าวใหม่ ({pub_date}): {entry.title}")
                    
                    content = ""
                    if 'content' in entry:
                        content = entry.content[0].value
                    elif 'summary' in entry:
                        content = entry.summary
                    
                    aya_article = aya_process_news(source['type'], entry.title, content, entry.link, pub_date)
                    
                    if "AI_ERROR" in aya_article:
                        print(f"💨 Error: {aya_article}")
                    elif "SKIP" in aya_article:
                        print("🗑️ (ข่าวน่าเบื่อ ข้ามไป)")
                        read_history.append(news_id)
                        new_items_found = True
                    else:
                        print("\n" + "📰"*20)
                        print(f"📍 {source['name']} | 🕒 {pub_date}")
                        print(aya_article)
                        print("📰"*20 + "\n")
                        
                        # ส่งเข้าทุก Discord
                        if target_webhooks:
                            for i, webhook_url in enumerate(target_webhooks):
                                print(f"🚀 กำลังส่งไปที่เซิร์ฟเวอร์ลำดับที่ {i+1}...")
                                send_discord_webhook(webhook_url, aya_article, source['name'])
                        else:
                            print("⚠️ ไม่ได้ตั้งค่า DISCORD_WEBHOOK_URL")
                        
                        read_history.append(news_id)
                        new_items_found = True
                    
                    time.sleep(2) 

        except Exception as e:
            print(f"⚠️ Error accessing {source['name']}: {e}")

    if new_items_found:
        save_history(read_history)
        print("💾 บันทึกประวัติเรียบร้อย")
    else:
        print("💤 ไม่พบข่าวใหม่")

if __name__ == "__main__":
    run_once()
