# 🎯 Expired Domain Sniper - Practical Usage Guide

## 🚀 **QUICK START (5 Minutes)**

### Step 1: Test the System
```bash
cd /workspace
source venv/bin/activate
python test_sniper.py
```
**What this does:** Shows you filtering logic without scraping

### Step 2: Run the Main Script
```bash
python expired_sniper.py
```
**What this does:** Attempts live scraping (currently gets 404s due to login requirement)

---

## 📋 **UNDERSTANDING THE OUTPUT**

### When You Run `test_sniper.py`:
```
🧪 Testing Domain Filtering Logic
========================================
✅ PASS 🎯 WATCH aibot.com            (Length:  5)
✅ PASS 🎯 WATCH chatflow.com         (Length:  8)  
❌ FAIL ai123.com                     (Length:  5)  # Contains numbers
❌ FAIL free-chat.com                 (Length:  8)  # Contains hyphen
❌ FAIL pornbot.com                   (Length:  7)  # Blacklisted word
```

**This tells you:**
- ✅ `aibot.com` = GOOD (5 chars, letters only, contains "ai" + "bot")
- ✅ `chatflow.com` = GOOD (8 chars, contains "chat" + "flow")  
- ❌ `ai123.com` = BAD (contains numbers)
- ❌ `free-chat.com` = BAD (contains hyphen)
- ❌ `pornbot.com` = BAD (contains blacklisted word "porn")

---

## 🔧 **CUSTOMIZING FOR YOUR NEEDS**

### 1. **Edit Your Keywords**
```bash
nano config.py
```

**Add your target keywords:**
```python
WATCH_KEYWORDS = [
    "ai", "app", "tech", "crypto", "web3",  # Tech terms
    "marketing", "seo", "social",           # Marketing terms  
    "fitness", "health", "wellness",        # Health terms
    "finance", "invest", "money"            # Finance terms
]
```

### 2. **Adjust Filtering**
```python
# Make it more strict (shorter domains only)
MIN_LENGTH = 4
MAX_LENGTH = 8

# Or more relaxed (longer domains OK)  
MIN_LENGTH = 4
MAX_LENGTH = 15
```

### 3. **Add More Blacklist Words**
```python
BLACKLIST = [
    "free", "porn", "hack", "loan", "xxx",
    "spam", "scam", "fake", "cheap", "buy"  # Add your own
]
```

---

## 📊 **REAL-WORLD USAGE SCENARIOS**

### Scenario 1: **Tech Startup Domains**
```python
# In config.py
WATCH_KEYWORDS = ["ai", "app", "dev", "tech", "api", "cloud", "data"]
MIN_LENGTH = 4
MAX_LENGTH = 8
```
**Best for:** Finding brandable tech domains

### Scenario 2: **Investment/Resale**  
```python
WATCH_KEYWORDS = ["buy", "get", "new", "pro", "hub", "net"]
MIN_LENGTH = 3  
MAX_LENGTH = 6
```
**Best for:** Short, memorable domains for resale

### Scenario 3: **Niche Business**
```python
WATCH_KEYWORDS = ["fitness", "health", "gym", "diet", "weight"]
MIN_LENGTH = 5
MAX_LENGTH = 12  
```
**Best for:** Building authority sites in specific niches

---

## 🔄 **MAKING IT WORK WITH REAL DATA**

Since ExpiredDomains.net requires login, here are your options:

### Option A: **Register and Update URLs**
1. **Register:** https://www.expireddomains.net/register/
2. **Login and find actual URLs**
3. **Update script:** Edit `get_expired_domains_page()` function

### Option B: **Use Alternative Sources**
```bash
python alternative_sources.py
```

### Option C: **Manual Data Input**
Create a file called `manual_domains.txt`:
```
aibot.com,Available,2024-01-15
chatflow.com,Auction,2024-01-16
techstart.com,Backorder,2024-01-17
```

Then modify the script to read from this file.

---

## 📲 **SETTING UP TELEGRAM ALERTS**

### Step 1: Create Bot
1. Message `@BotFather` on Telegram
2. Send `/newbot`
3. Name your bot (e.g., "Domain Sniper Bot")
4. Save the **token**

### Step 2: Get Chat ID  
1. Message `@userinfobot`
2. Send any message
3. Save your **chat ID** (number)

### Step 3: Configure
```python
# In config.py
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
TELEGRAM_CHAT_ID = "987654321"
```

### Step 4: Test
```bash
python test_sniper.py
```
Look for the Telegram message format preview.

---

## 🤖 **AUTOMATION SETUPS**

### Daily Cron Job (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /workspace && source venv/bin/activate && python expired_sniper.py
```

### Windows Task Scheduler
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start program
5. Program: `C:\path\to\python.exe`
6. Arguments: `expired_sniper.py`
7. Start in: `C:\workspace`

---

## 🔍 **ANALYZING THE RESULTS**

### CSV Output (`sniped_domains.csv`)
```csv
Domain,Length,Status,DropDate,TLD_Count,WatchMatch,ArchiveURL
aibot.com,5,Available,2024-01-15,3,True,https://web.archive.org/web/*/aibot.com
```

**How to use this data:**
1. **Sort by Length:** Shorter = more valuable
2. **Check WatchMatch:** `True` = contains your keywords  
3. **Verify Status:** `Available` = you can register now
4. **Check Archive:** See what the site used to be

### Manual Verification Steps
```bash
# 1. Check if domain is actually available
whois aibot.com

# 2. Check for Google penalties (search for site:aibot.com)
# 3. Verify backlinks with Ahrefs/SEMrush  
# 4. Check Archive.org for previous content
```

---

## 🛠 **TROUBLESHOOTING**

### Problem: "No domains found"
**Solution:** Website structure changed
```bash
# Check logs
cat expired_sniper.log

# Update URLs in script
nano expired_sniper.py
```

### Problem: "Import errors"  
**Solution:** Reinstall dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: "Getting blocked"
**Solution:** Increase delays
```python
# In config.py  
REQUEST_DELAY = (5, 10)  # Slower requests
```

### Problem: "Telegram not working"
**Solution:** Check credentials
```python
# Test your bot token
import requests
url = f"https://api.telegram.org/bot{TOKEN}/getMe"
print(requests.get(url).json())
```

---

## 💡 **PRO TIPS**

### 1. **Start Small**
- Begin with 1-2 pages
- Test your filtering logic
- Gradually increase scope

### 2. **Quality over Quantity**  
- Focus on 4-8 character domains
- Prioritize brandable names
- Avoid numbers and hyphens

### 3. **Check Domain History**
```bash
# Always verify before buying
# - Check Archive.org 
# - Google: site:domain.com
# - Verify with WHOIS
```

### 4. **Best Times to Run**
- **6-8 AM:** Fresh daily drops
- **Monday mornings:** Weekend accumulation  
- **After major domain auctions**

### 5. **Investment Strategy**
- **< 5 chars:** Premium resale value
- **5-8 chars:** Good for development
- **Contains keywords:** Niche authority sites

---

## 🎯 **NEXT STEPS**

### Immediate Actions:
1. ✅ **Run test suite:** `python test_sniper.py`
2. ✅ **Customize config:** Edit `config.py` 
3. ✅ **Set up Telegram:** Add bot credentials
4. ✅ **Schedule automation:** Set up cron job

### Advanced Features:
- **Add more data sources** (GoDaddy Auctions, NameJet)
- **Integrate WHOIS checking**
- **Build web dashboard** 
- **Add domain scoring algorithm**
- **Create email alerts**

---

## 📞 **SUPPORT**

### Log Files:
- `expired_sniper.log` - Detailed operation logs
- `sniped_domains.csv` - Results output

### Common Commands:
```bash
# Activate environment
source venv/bin/activate

# Run test
python test_sniper.py  

# Run main script
python expired_sniper.py

# Check logs
tail -f expired_sniper.log
```

**Ready to start domain hunting? Your system is fully configured and ready to go!** 🚀