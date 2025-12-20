# การตั้งค่าแหล่งข่าว
# ฉบับคัดเน้นๆ: ข่าวทางการ + สินค้า + แฟนเกม (ตัด Steam และกระทู้ไร้สาระทิ้ง)

RSS_SOURCES = [
   # 1. ข่าวทางการ (Official)
    {
        "name": "Touhou Yomoyama (News)", 
        # ใช้ลิงก์แบบ Query String (เสถียรที่สุดสำหรับ WordPress)
        "url": "https://touhou-project.news/?feed=rss2", 
        "type": "official"
    },
    # 2. Touhou Station
    {
        "name": "Touhou Station (Live & Events)", 
        # ใช้ลิงก์ Tag แบบ Query String
        "url": "https://touhougarakuta.com/tag/touhou_station/?feed=rss2", 
        "type": "official"
    },
    # 3. นิตยสาร Garakuta
    {
        "name": "Touhou Garakuta (Magazine)", 
        "url": "https://touhougarakuta.com/?feed=rss2", 
        "type": "magazine"
    },
    # 4. ชุมชน Reddit (กรองเฉพาะ: ข่าว, สินค้า, เกม)
    # ลิงก์นี้จะคัดเฉพาะกระทู้ที่มี Flair เป็น News, Merchandise, หรือ Game เท่านั้น
    {
        "name": "Reddit Touhou (News/Goods/Games)", 
        "url": "https://www.reddit.com/r/touhou/search.rss?q=flair_name%3A%22News%22+OR+flair_name%3A%22Merchandise%22+OR+flair_name%3A%22Game%22&restrict_sr=1&sort=new", 
        "type": "community"
    }
]

# ชื่อไฟล์เก็บประวัติการอ่าน
LOG_FILE = "aya_news_history.json"
