import feedparser
import time
import datetime
import os
import re 
from config import RSS_SOURCES
from utils import get_timestamp, load_history, save_history, send_discord_webhook
from aya_brain import aya_process_news

def extract_image(entry):
    """พยายามดึง URL รูปภาพจากข่าว"""
    # 1. ลองหาจาก media_content (Reddit/News มักใช้อันนี้)
    if 'media_content' in entry:
        try:
            return entry.media_content[0]['url']
        except: pass
    
    # 2. ลองหาจาก media_thumbnail
    if 'media_thumbnail' in entry:
        try:
            return entry.media_thumbnail[0]['url']
        except: pass

    # 3. ลองหาจาก links (พวกไฟล์แนบ enclosure)
    if 'links' in entry:
        for link in entry.links:
            if link.type.startswith('image/'):
                return link.href

    # 4. ถ้าไม่มีเลย ลองแกะจาก HTML content โดยตรง
    content_html = ""
    if 'content' in entry:
        content_html = entry.content[0].value
    elif 'summary' in entry:
        content_html = entry.summary
        
    if content_html:
        # ใช้ Regular Expression หา tag <img src="...">
        match = re.search(r'<img [^>]*src="([^"]+)"', content_html)
        if match:
            return match.group(1)
            
    return None

def run_once():
    print(f"[{datetime.datetime.now()}] 🌪️ อายะตื่นมาเช็คข่าวรอบใหม่...")
    
    # 1. ดึง Webhook URL ทั้งหมดมา (รองรับหลายลิงก์คั่นด้วยลูกน้ำ)
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
            
            # [Debug] แจ้งจำนวนข่าวที่เจอใน Feed นี้
            print(f"   🔎 เจอทั้งหมด {len(feed.entries)} ข่าวใน Feed นี้")
            
            # เช็คย้อนหลัง 10 ข่าว
            for entry in feed.entries[:10]:
                news_id = entry.id if 'id' in entry else entry.link
                
                # [Debug] แสดงชื่อข่าวที่กำลังเช็ค (จะได้รู้ว่าบอทเห็นข่าวไหม)
                # print(f"   - [Check] {entry.title}") 
                
                if news_id not in read_history:
                    pub_date = get_timestamp(entry)
                    print(f"📸 พบข่าวใหม่ ({pub_date}): {entry.title}")
                    
                    content = ""
                    if 'content' in entry:
                        content = entry.content[0].value
                    elif 'summary' in entry:
                        content = entry.summary
                    
                    # 1. ดึงรูปภาพออกมา
                    image_url = extract_image(entry)
                    if image_url:
                        print(f"🖼️ เจอรูปภาพประกอบ: {image_url}")

                    # 2. ให้ AI เขียนข่าว
                    aya_article = aya_process_news(source['type'], entry.title, content, entry.link, pub_date)
                    
                    if "AI_ERROR" in aya_article:
                        print(f"💨 Error: {aya_article}")
                        # ถ้า Error ให้ break ออกจากลูปข่าวนี้ แล้วไปรอรอบหน้าเลย (เพื่อความปลอดภัย)
                        break 
                    elif "SKIP" in aya_article:
                        print("🗑️ (ข่าวน่าเบื่อ ข้ามไป)")
                        read_history.append(news_id)
                        new_items_found = True
                        time.sleep(5) # พักนิดหน่อยสำหรับข่าวที่ข้าม
                    else:
                        print("\n" + "📰"*20)
                        print(f"📍 {source['name']} | 🕒 {pub_date}")
                        print(aya_article)
                        if image_url: print(f"🖼️ Image: {image_url}")
                        print("-" * 50)
                        
                        # 3. ส่งเข้า Discord แบบ Embed (มีรูป + วันที่)
                        if target_webhooks:
                            for i, webhook_url in enumerate(target_webhooks):
                                print(f"🚀 กำลังส่ง (Embed) ไปที่เซิร์ฟเวอร์ลำดับที่ {i+1}...")
                                # ส่งข้อมูลครบชุด: เนื้อหา, ชื่อแหล่ง, ลิงก์ข่าว, รูปภาพ, และวันที่
                                send_discord_webhook(
                                    webhook_url, 
                                    aya_article, 
                                    source['name'], 
                                    news_url=entry.link, 
                                    image_url=image_url,
                                    pub_date=pub_date
                                )
                        else:
                            print("⚠️ ไม่ได้ตั้งค่า DISCORD_WEBHOOK_URL")
                        
                        read_history.append(news_id)
                        new_items_found = True
                        
                        # [จุดสำคัญ] พัก 20 วินาที เพื่อป้องกัน API Rate Limit
                        print("⏳ พัก 20 วินาที... (กันโดนแบน)")
                        time.sleep(20) 

        except Exception as e:
            print(f"⚠️ Error accessing {source['name']}: {e}")

    if new_items_found:
        save_history(read_history)
        print("💾 บันทึกประวัติเรียบร้อย")
    else:
        print("💤 ไม่พบข่าวใหม่")

if __name__ == "__main__":
    run_once()
