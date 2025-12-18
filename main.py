import feedparser
import time
import datetime
import os
import re 
import requests # [เพิ่ม] ต้องใช้ requests เพื่อดึงข้อมูลเว็บที่บล็อกบอท
from config import RSS_SOURCES
from utils import get_timestamp, load_history, save_history, send_discord_webhook
from aya_brain import aya_process_news

# กำหนด User-Agent ให้ดูเหมือนคนใช้ Browser จริงๆ
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def fetch_rss_feed(url):
    """
    ฟังก์ชันดึง RSS โดยใช้ requests เพื่อแก้ปัญหาเว็บที่บล็อก feedparser
    """
    try:
        # 1. ลองดึงด้วย requests ก่อน (เนียนกว่า)
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        # ส่งเนื้อหา (content) ไปให้ feedparser แปลง
        feed = feedparser.parse(response.content)
        
        # เช็คว่าอ่านรู้เรื่องไหม
        if feed.bozo == 0 or len(feed.entries) > 0:
            return feed
            
    except Exception as e:
        print(f"   ⚠️ Requests failed ({e}), trying fallback...")

    # 2. ถ้าวิธีแรกไม่ได้ผล ลองใช้ feedparser ดึงตรงๆ (Fallback)
    return feedparser.parse(url)

def extract_image(entry):
    """พยายามดึง URL รูปภาพจากข่าว"""
    if 'media_content' in entry:
        try: return entry.media_content[0]['url']
        except: pass
    if 'media_thumbnail' in entry:
        try: return entry.media_thumbnail[0]['url']
        except: pass
    if 'links' in entry:
        for link in entry.links:
            if link.type.startswith('image/'):
                return link.href
    content_html = ""
    if 'content' in entry:
        content_html = entry.content[0].value
    elif 'summary' in entry:
        content_html = entry.summary
    if content_html:
        match = re.search(r'<img [^>]*src="([^"]+)"', content_html)
        if match: return match.group(1)
    return None

def is_interesting_reddit_post(entry):
    """กรองกระทู้ Reddit"""
    wanted_flairs = ["News", "Game News", "Merchandise", "Cosplay", "Official News", "Game Discussion"]
    
    if 'tags' in entry:
        for tag in entry.tags:
            if tag.term in wanted_flairs:
                return True
                
    title_lower = entry.title.lower()
    if "[news]" in title_lower or "[game]" in title_lower or "release" in title_lower:
        return True
        
    return False

def run_once():
    print(f"[{datetime.datetime.now()}] 🌪️ อายะตื่นมาเช็คข่าวรอบใหม่...")
    
    webhook_env = os.getenv("DISCORD_WEBHOOK_URL")
    target_webhooks = []
    if webhook_env:
        target_webhooks = [url.strip() for url in webhook_env.split(',') if url.strip()]
    
    print(f"📡 พบเป้าหมายการส่งข่าวทั้งหมด: {len(target_webhooks)} แห่ง")

    read_history = load_history()
    new_items_found = False

    processed_count = 0 
    MAX_NEWS_PER_RUN = 10 

    for source in RSS_SOURCES:
        print(f"Flying to... {source['name']} 🦅")
        try:
            # [แก้ไข] เรียกใช้ฟังก์ชันใหม่ fetch_rss_feed แทน feedparser.parse โดยตรง
            feed = fetch_rss_feed(source['url'])
            
            print(f"   🔎 เจอทั้งหมด {len(feed.entries)} ข่าวใน Feed นี้")
            
            if len(feed.entries) == 0:
                print("   ⚠️ ไม่พบข้อมูลเลย (เว็บอาจจะบล็อก หรือลิงก์ผิด)")
                continue

            # เช็คย้อนหลัง 100 ข่าว (เผื่อข่าวเก่า)
            check_limit = 100 
            
            for entry in feed.entries[:check_limit]:
                
                if processed_count >= MAX_NEWS_PER_RUN:
                    print("🛑 ส่งข่าวครบโควต้าต่อรอบแล้ว พักก่อน...")
                    break

                news_id = entry.id if 'id' in entry else entry.link
                
                # กรอง Reddit
                if source['type'] == 'community':
                    if not is_interesting_reddit_post(entry):
                        continue 
                
                if news_id not in read_history:
                    print(f"     ✨ เจอข่าวใหม่! กำลังประมวลผล: {entry.title}")
                    pub_date = get_timestamp(entry)
                    
                    content = ""
                    if 'content' in entry:
                        content = entry.content[0].value
                    elif 'summary' in entry:
                        content = entry.summary
                    
                    image_url = extract_image(entry)
                    
                    aya_article = aya_process_news(source['type'], entry.title, content, entry.link, pub_date)
                    
                    if "AI_ERROR" in aya_article:
                        print(f"     💨 Error: {aya_article}")
                        if "429" in aya_article: 
                            print("⛔ โควต้าเต็ม (429) หยุดทันที")
                            processed_count = MAX_NEWS_PER_RUN
                            break
                    elif "SKIP" in aya_article:
                        print("     🗑️ (ข่าวน่าเบื่อ ข้ามไป)")
                        read_history.append(news_id)
                        new_items_found = True
                        time.sleep(2) 
                    else:
                        print("\n" + "📰"*20)
                        print(f"📍 {source['name']} | 🕒 {pub_date}")
                        print(aya_article)
                        if image_url: print(f"🖼️ Image: {image_url}")
                        print("-" * 50)
                        
                        if target_webhooks:
                            for i, webhook_url in enumerate(target_webhooks):
                                print(f"🚀 กำลังส่ง (Embed) ไปที่เซิร์ฟเวอร์ลำดับที่ {i+1}...")
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
                        processed_count += 1
                        
                        print("⏳ พัก 20 วินาที...")
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
