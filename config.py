# การตั้งค่าแหล่งข่าว
# ฉบับคัดเน้นๆ: ข่าวทางการ + สินค้า + แฟนเกม (ตัด Steam และกระทู้ไร้สาระทิ้ง)

RSS_SOURCES = [
  # 1. Touhou Yomoyama (News)
    {
        "name": "Touhou Yomoyama (News)", 
        # ใช้ index.php?feed=rss2 เพื่อเจาะเข้าถึง Core Feed โดยตรง
        "url": "https://touhou-project.news/index.php?feed=rss2", 
        "type": "official"
    },
    # 2. Touhou Station (Live & Events)
    {
        "name": "Touhou Station (Live & Events)", 
        # ใช้ Query param '?tag=...' แทนการใช้ Path ยาวๆ (ลดโอกาส 404)
        "url": "https://touhougarakuta.com/index.php?feed=rss2&tag=touhou_station", 
        "type": "official"
    },
    # 3. Touhou Garakuta (Magazine)
    {
        "name": "Touhou Garakuta (Magazine)", 
        "url": "https://touhougarakuta.com/index.php?feed=rss2", 
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
