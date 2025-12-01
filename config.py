# การตั้งค่าแหล่งข่าว
# หมายเหตุ: URL ต้องเป็นลิงก์ตรงๆ ไม่ใช่รูปแบบ Markdown [link](url)
RSS_SOURCES = [
    {
        "name": "Touhou Yomoyama (Official News)", 
        "url": "https://touhou-project.news/feed", 
        "type": "official"
    },
    {
        "name": "Touhou Garakuta (Official Magazine)", 
        "url": "https://touhougarakuta.com/feed", 
        "type": "magazine"
    },
    {
        "name": "Reddit r/touhou (Community)", 
        "url": "https://www.reddit.com/r/touhou/new/.rss", 
        "type": "community"
    }
]

# ชื่อไฟล์เก็บประวัติการอ่าน (กันข่าวซ้ำ)
LOG_FILE = "aya_news_history.json"
