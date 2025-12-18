import feedparser
import time
import datetime
import os
import re 
import requests 
from config import RSS_SOURCES
from utils import get_timestamp, load_history, save_history, send_discord_webhook
from aya_brain import aya_process_news

# ปรับ User-Agent ให้เหมือนคนใช้งานจริงที่สุด (แก้ปัญหาเว็บ Official บล็อกบอท)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, application/atom+xml, text/xml, text/html, */*"
}

def fetch_rss_feed(url):
    """ฟังก์ชันดึง RSS แบบทะลุบล็อก 404/403"""
    try:
        # ลองดึงด้วย requests ก่อน (เนียนกว่า)
        response = requests.get(url, headers=HEADERS, timeout=20)
        
        # ถ้าเจอ 404 ให้ลองส่งกลับไปให้ feedparser จัดการต่อ (เผื่อ redirect)
        if response.status_code == 404:
            print(f"   ⚠️ เจอ 404 ที่ {url} - กำลังลองวิธีสำรอง...")
            return feedparser.parse(url)
            
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        return feed
    except Exception as e:
        print(f"   ⚠️ Requests failed ({e}), trying fallback...")
        return feedparser.parse(url)

def extract_image(entry):
    """พยายามแกะ URL รูปภาพจากข่าว"""
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
    """กรองกระทู้ Reddit เอาเฉพาะที่น่าสนใจ"""
    wanted_flairs = ["News", "Game News", "Merchandise", "Cosplay", "Official News", "Game Discussion"]
    if 'tags' in entry:
        for tag in entry.tags:
            if tag.term in wanted_flairs: return True
    title_lower = entry.title.lower()
    keywords = ["[news]", "[game]", "release", "announcement", "trailer", "pv"]
    if any(k in title_lower for k in keywords): return True
    return False

def run_once():
    print(f"[{datetime.datetime.now()}] 🌪️ อายะตื่นมาเช็คข่าวรอบใหม่...")
    
    webhook_env = os.getenv("DISCORD_WEBHOOK_URL")
    target_webhooks = []
    if webhook_env:
        target_webhooks = [url.strip() for url in webhook_env.split(',') if url.strip()]
    
    print(f"📡 พบเป้าหมายการส่งข่าวทั้งหมด: {len(target_webhooks)} แห่ง")

    read_history = load_history()
    processed_count = 0 
    MAX_NEWS_PER_RUN = 5 # จำกัดจำนวนข่าวต่อรอบเพื่อเซฟโควต้า

    for source in RSS_SOURCES:
        if processed_count >= MAX_NEWS_PER_RUN:
            print("🛑 ครบโควต้า 5 ข่าวแล้ว พักก่อน...")
            break

        print(f"Flying to... {source['name']} 🦅")
        try:
            feed = fetch_rss_feed(source['url'])
            
            # เช็คว่าเจอข่าวไหม
            count = len(feed.entries)
            print(f"   🔎 เจอทั้งหมด {count} ข่าวใน Feed นี้")
            
            if count == 0:
                print("   ⚠️ ไม่พบข้อมูลเลย (ข้าม)")
                continue

            # เช็คย้อนหลัง 50 ข่าว (เผื่อกรณีลบประวัติแล้วอยากได้ข่าวเก่าคืน)
            check_limit = 50
            
            for entry in feed.entries[:check_limit]:
                
                if processed_count >= MAX_NEWS_PER_RUN: break

                news_id = entry.id if 'id' in entry else entry.link
                
                # กรอง Reddit
                if source['type'] == 'community':
                    if not is_interesting_reddit_post(entry):
                        continue 
                
                if news_id not in read_history:
                    print(f"     ✨ เจอข่าวใหม่! กำลังประมวลผล: {entry.title}")
                    pub_date = get_timestamp(entry)
                    
                    content = ""
                    if 'content' in entry: content = entry.content[0].value
                    elif 'summary' in entry: content = entry.summary
                    
                    image_url = extract_image(entry)
                    
                    # ส่งให้ AI แปล
                    aya_article = aya_process_news(source['type'], entry.title, content, entry.link, pub_date)
                    
                    if "AI_ERROR" in aya_article:
                        print(f"     💨 Error: {aya_article}")
                        if "429" in aya_article: 
                            print("⛔ โควต้าเต็ม (429) หยุดทันที")
                            processed_count = MAX_NEWS_PER_RUN
                            break
                    
                    elif "SKIP" in aya_article:
                        print("     🗑️ (ข่าวน่าเบื่อ ข้ามไป)")
                        # บันทึก ID แม้จะข้าม เพื่อไม่ให้วนซ้ำ
                        read_history.append(news_id)
                        save_history(read_history) # บันทึกทันที
                        time.sleep(2) 
                    
                    else:
                        print("\n" + "📰"*20)
                        print(f"📍 {source['name']} | 🕒 {pub_date}")
                        print(aya_article)
                        if image_url: print(f"🖼️ Image: {image_url}")
                        print("-" * 50)
                        
                        if target_webhooks:
                            for i, webhook_url in enumerate(target_webhooks):
                                print(f"🚀 กำลังส่งไปที่เซิร์ฟเวอร์ลำดับที่ {i+1}...")
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
                        
                        # บันทึกทันทีหลังส่ง
                        read_history.append(news_id)
                        save_history(read_history)
                        
                        processed_count += 1
                        
                        print("⏳ พัก 20 วินาที...")
                        time.sleep(20) 

        except Exception as e:
            print(f"⚠️ Error accessing {source['name']}: {e}")

    # Save ปิดท้ายอีกรอบ
    save_history(read_history)
    print("💤 จบการทำงานรอบนี้")

if __name__ == "__main__":
    run_once()



