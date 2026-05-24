# Aya News Bot (อายะบอทส่งข่าว)

[🇬🇧 Click here for the English Version](#-english-version)

บอทอัจฉริยะสำหรับติดตามข่าวสารเกี่ยวกับ **Touhou Project** จากหลากหลายแหล่งข่าว นำมาสรุป แปลเป็นภาษาไทย และสวมบทบาทเป็นนักข่าวสาว **Shameimaru Aya** แห่งหนังสือพิมพ์บุนบุนมารุ ก่อนส่งตรงเข้าสู่เซิร์ฟเวอร์ Discord ของคุณแบบอัตโนมัติ!

##  ฟีเจอร์หลัก (Features)

* **Auto RSS Fetching:** ดึงข่าวอัตโนมัติจากแหล่งข่าวสำคัญ เช่น 
  * Touhou Yomoyama (Official News)
  * Reddit r/touhou (เฉพาะหมวด News, Merchandise, Game)
  * Steam News (อัปเดตเกมที่เกี่ยวข้อง)
* **AI Powered (Google Gemini):** ใช้ขุมพลัง AI ในการอ่านข่าว สรุปใจความสำคัญ แยกแยะข้อเท็จจริง และเล่าเรื่องในสไตล์ของ "อายะ" (ร่าเริง กระตือรือร้น)
* **Discord Webhook Integration:** ส่งข่าวเข้า Discord ในรูปแบบ Embed ที่สวยงาม พร้อมรูปภาพประกอบและลิงก์ไปยังต้นฉบับ
* **Serverless Automation:** ทำงานอัตโนมัติ 100% ผ่าน **GitHub Actions** (รันทุกๆ 6 ชั่วโมง) ไม่ต้องเปิดคอมพิวเตอร์หรือเช่าเซิร์ฟเวอร์ทิ้งไว้
* **Smart Fallback & Anti-Spam:** มีระบบคัดกรองโมเดล AI ที่พร้อมใช้งาน และระบบบันทึกประวัติข่าวเพื่อป้องกันการส่งข้อความซ้ำ

## โครงสร้างโปรเจกต์ (Project Structure)

* `main.py` - สคริปต์หลัก ควบคุมการดึงข้อมูลและส่งข่าว
* `aya_brain.py` - สมองกล AI จัดการการเชื่อมต่อ Google Gemini API และ Prompt ของอายะ
* `config.py` - ตั้งค่าแหล่งข่าว RSS (สามารถเพิ่ม/ลด แหล่งข่าวได้ที่นี่)
* `utils.py` - ฟังก์ชันช่วยเหลือ (จัดการเวลา, บันทึกไฟล์ประวัติ, ยิง Discord Webhook)
* `requirements.txt` - รายชื่อไลบรารี Python ที่ต้องใช้
* `aya_news_history.json` - ไฟล์ฐานข้อมูล (Local) สำหรับจำว่าข่าวไหนส่งไปแล้วบ้าง
* `.github/workflows/run_aya.yml` - สคริปต์สั่งให้ GitHub ทำงานตามเวลาที่กำหนดอัตโนมัติ

## วิธีการติดตั้งและการใช้งาน (Setup & Deployment)

โปรเจกต์นี้ออกแบบมาให้รันบน **GitHub Actions** คุณสามารถติดตั้งได้ตามขั้นตอนดังนี้:

### 1. Fork หรือ Clone Repository นี้
นำโค้ดทั้งหมดใน Repository นี้ไปไว้ใน GitHub ของคุณ

### 2. ตั้งค่า Secrets ใน GitHub
บอทต้องการ API Key เพื่อทำงาน ให้ไปที่ Repository ของคุณ -> **Settings** -> **Secrets and variables** -> **Actions** -> กด **New repository secret** เพิ่มค่าดังต่อไปนี้:
* `GEMINI_API_KEY` : คีย์ API ของ Google Gemini (รับฟรีได้ที่ [Google AI Studio](https://aistudio.google.com/))
* `DISCORD_WEBHOOK_URL` : ลิงก์ Webhook จากห้อง Discord ที่ต้องการให้บอทส่งข่าวไป

### 3. เปิดการทำงานของ GitHub Actions
* ไปที่แท็บ **Actions** ใน Repository ของคุณ
* หากมีปุ่มเตือนให้เปิดใช้งาน (Enable workflow) ให้กดเปิด
* คุณสามารถทดสอบรันบอททันทีได้โดยเลือก **Aya News Bot (Auto Run)** ทางซ้ายมือ -> กด **Run workflow** ทางขวามือ

### 4. ปล่อยให้บอททำงาน 
หลังจากตั้งค่าเสร็จ บอทจะตื่นขึ้นมาเช็คข่าวใหม่ๆ และส่งเข้า Discord ของคุณอัตโนมัติ (ตามค่าเริ่มต้นคือทุกๆ 6 ชั่วโมง)

## การปรับแต่ง (Customization)

* **เพิ่มแหล่งข่าวใหม่:** แก้ไขไฟล์ `config.py` แล้วเพิ่มลิงก์ RSS เข้าไปในตัวแปร `RSS_SOURCES`
* **ปรับความถี่:** แก้ไขไฟล์ `.github/workflows/run_aya.yml` ตรงบรรทัด `- cron: "0 */6 * * *"` (ใช้รูปแบบ Cron expression)
* **เปลี่ยนนิสัยบอท:** แก้ไข Prompt ในตัวแปร `system_instruction` ภายในไฟล์ `aya_brain.py`

---

<br>

<a id="-english-version"></a>
# Aya News Bot (English Version)

An intelligent bot designed to track **Touhou Project** news from various sources, summarize it, translate it into Thai, and roleplay as the tengu reporter **Shameimaru Aya** from the Bunbunmaru Newspaper, delivering updates straight to your Discord server automatically!

## Features

* **📡 Auto RSS Fetching:** Automatically fetches news from essential sources such as:
  * Touhou Yomoyama (Official News)
  * Reddit r/touhou (News, Merchandise, and Game flairs only)
  * Steam News (Related game updates)
* **AI Powered (Google Gemini):** Utilizes AI to read news, summarize key points, separate facts from lore, and narrate in Aya's signature energetic and cheerful style.
* **Discord Webhook Integration:** Delivers news to Discord using beautiful Embed formats, complete with cover images and original source links.
* **Serverless Automation:** Runs 100% automatically via **GitHub Actions** (every 6 hours). No need to keep your PC on or rent a dedicated server.
* **Smart Fallback & Anti-Spam:** Features an AI model fallback mechanism to handle API limits and a local history log system to prevent duplicate news broadcasts.

## Setup & Deployment

This project is designed to run seamlessly on **GitHub Actions**. Follow these steps to set it up:

1. **Fork or Clone this Repository:** Bring all the code into your own GitHub account.
2. **Set up GitHub Secrets:** Go to your repository's **Settings** -> **Secrets and variables** -> **Actions** -> click **New repository secret** and add:
   * `GEMINI_API_KEY` : Your Google Gemini API key.
   * `DISCORD_WEBHOOK_URL` : The Webhook URL of your target Discord channel.
3. **Enable GitHub Actions:** Go to the **Actions** tab and enable workflows. You can manually test the bot by running the workflow.
4. **Let the bot work:** The bot will automatically wake up and check for new updates based on the set schedule.

---

> ⚠️ **Disclaimer:** This project is powered by Artificial Intelligence (AI - Google Gemini). The process of reading, summarizing, and translating news is entirely automated by a language model. Some content or context may deviate from the original source. Please use your discretion and always refer to the original news links provided.
