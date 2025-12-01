import feedparser
import time
import datetime
from config import RSS_SOURCES
from utils import get_timestamp, load_history, save_history
from aya_brain import aya_process_news

def run_once():
    print(f"[{datetime.datetime.now()}] 🌪️ อายะตื่นมาเช็คข่าวรอบใหม่...")
    read_history = load_history()
    new_items_found = False

    for source in RSS_SOURCES:
        print(f"Flying to... {source['name']} 🦅")
        try:
            feed = feedparser.parse(source['url'])
            
            # เช็ค 3 ข่าวล่าสุดของแต่ละเว็บ
            for entry in feed.entries[:3]:
                news_id = entry.id if 'id' in entry else entry.link
                
                if news_id not in read_history:
                    pub_date = get_timestamp(entry)
                    print(f"📸 พบข่าวใหม่ ({pub_date}): {entry.title}")
                    
                    # เตรียมข้อมูล
                    content = ""
                    if 'content' in entry:
                        content = entry.content[0].value
                    elif 'summary' in entry:
                        content = entry.summary
                    
                    # ส่งให้อายะเขียนข่าว
                    aya_article = aya_process_news(source['type'], entry.title, content, entry.link, pub_date)
                    
                    if "AI_ERROR" in aya_article:
                        print(f"💨 Error: {aya_article}")
                        # ไม่ continue เพื่อให้เช็คข่าวอื่นต่อ แต่ไม่บันทึก ID นี้
                    elif "SKIP" in aya_article:
                        print("🗑️ (ข่าวน่าเบื่อ ข้ามไป)")
                        read_history.append(news_id)
                        new_items_found = True
                    else:
                        # แสดงผล (ใน GitHub Actions จะโผล่ใน Log)
                        print("\n" + "📰"*20)
                        print(f"📍 {source['name']} | 🕒 {pub_date}")
                        print("-" * 50)
                        print(aya_article)
                        print("-" * 50)
                        print(f"👉 {entry.link}")
                        print("📰"*20 + "\n")
                        
                        read_history.append(news_id)
                        new_items_found = True
                    
                    time.sleep(2) # พักนิดหน่อยกันโดนแบน
        except Exception as e:
            print(f"⚠️ Error accessing {source['name']}: {e}")

    # บันทึกประวัติเฉพาะเมื่อมีข่าวใหม่หรือมีการข้ามข่าว
    if new_items_found:
        save_history(read_history)
        print("💾 บันทึกประวัติการอ่านเรียบร้อย")
    else:
        print("💤 ไม่พบข่าวใหม่ในรอบนี้ กลับไปนอนต่อ...")

if __name__ == "__main__":
    run_once()
