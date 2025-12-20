# การตั้งค่าแหล่งข่าว
# ฉบับคัดเน้นๆ: ข่าวทางการ + สินค้า + แฟนเกม (ตัด Steam และกระทู้ไร้สาระทิ้ง)

RSS_SOURCES = [
   # 1. Touhou Yomoyama (News)
    {
        "name": "Touhou Yomoyama (News)", 
        # ลิงก์ที่ถูกต้องสำหรับเว็บนี้คือ feed.rss (ยืนยันจากหน้าเว็บ)
        "url": "https://touhou-project.news/feed.rss", 
        "type": "official"
    },
    # 2. Touhou Station (Live & Events)
    {
        "name": "Touhou Station (Live & Events)", 
        # ลองใช้โครงสร้างแบบ WordPress มาตรฐาน (มักจะใช้ได้กับ Garakuta)
        "url": "https://touhougarakuta.com/tag/touhou_station/feed", 
        "type": "official"
    },
    # 3. Touhou Garakuta (Magazine)
    {
        "name": "Touhou Garakuta (Magazine)", 
        # ลิงก์มาตรฐาน
        "url": "https://touhougarakuta.com/feed", 
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
