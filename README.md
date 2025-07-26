# 🎯 Expired Domain Sniper

A powerful Python bot that automatically scrapes ExpiredDomains.net for expired .com domains, filters them based on custom criteria, and alerts you to high-value opportunities.

## 🚀 Features

- **Automated Scraping**: Scrapes ExpiredDomains.net for expired .com domains
- **Smart Filtering**: Advanced filtering based on length, keywords, and blacklists
- **CSV Export**: Exports results to CSV for easy analysis
- **Telegram Alerts**: Real-time notifications for high-value domain matches
- **Anti-Bot Protection**: Built-in delays, user agent rotation, and retry logic
- **Modular Configuration**: Easy customization with separate config files
- **Logging**: Comprehensive logging for monitoring and debugging

## 📋 Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

## 🛠️ Installation

1. **Clone or download the script files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure settings (optional):**
   - Edit `config.py` to customize filtering criteria
   - Set up Telegram bot (see Telegram Setup section)

## 🔧 Configuration

### Basic Configuration

Edit `config.py` to customize:

```python
from config import Config

# Use default configuration
config = Config()

# Or use aggressive filtering
config = AggressiveConfig()

# Or premium domain hunting
config = PremiumConfig()
```

### Filtering Criteria

- **Length**: 4-12 characters (customizable)
- **Characters**: Letters only (no numbers or hyphens)
- **TLD**: .com domains only
- **Blacklist**: Excludes domains with unwanted keywords
- **Watch Keywords**: Prioritizes domains with valuable keywords

### Default Blacklist
```python
["free", "porn", "hack", "loan", "xxx", "adult", "sex", "casino", "gambling"]
```

### Default Watch Keywords
```python
["ai", "chat", "prompt", "labs", "bot", "wallet", "cloud", "ninja", "agent", "flow"]
```

## 📲 Telegram Setup (Optional)

1. **Create a Telegram Bot:**
   - Message @BotFather on Telegram
   - Send `/newbot` and follow instructions
   - Save the bot token

2. **Get your Chat ID:**
   - Message @userinfobot on Telegram
   - Save your chat ID

3. **Update configuration:**
```python
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"
```

## 🚀 Usage

### Basic Usage

```bash
python expired_sniper.py
```

### Configuration Options

The script supports different configuration modes:

```python
# Standard filtering
python expired_sniper.py

# Edit config.py to use aggressive filtering
config = AggressiveConfig()

# Edit config.py to use premium filtering  
config = PremiumConfig()
```

### Command Line Arguments (Future Enhancement)

```bash
# Specify number of pages to scrape
python expired_sniper.py --pages 10

# Use specific configuration
python expired_sniper.py --config aggressive

# Dry run (no alerts)
python expired_sniper.py --dry-run
```

## 📊 Output

### CSV Export

Results are saved to `sniped_domains.csv` with columns:
- **Domain**: The domain name
- **Length**: Character count (excluding .com)
- **Status**: Available/Auction/Backorder
- **DropDate**: When the domain expired
- **TLD_Count**: Number of TLD variations registered
- **WatchMatch**: True if contains watch keywords
- **ArchiveURL**: Web Archive link for historical data

### Telegram Alerts

For domains matching watch keywords and < 10 characters:
```
🔥 New match: aideal.com
📊 Status: Available
📅 Drop Date: 2024-01-15
📏 Length: 6 chars
🔗 Archive: https://web.archive.org/web/*/aideal.com
```

## 🤖 Anti-Bot Measures

The script includes several measures to avoid detection:

- **Random User Agents**: Rotates browser identities
- **Request Delays**: Random delays between requests (1-3 seconds)
- **Retry Logic**: Exponential backoff for failed requests
- **Session Persistence**: Maintains cookies across requests
- **Realistic Headers**: Mimics real browser behavior

## 📁 File Structure

```
expired_sniper/
├── expired_sniper.py      # Main script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── sniped_domains.csv    # Output file (generated)
└── expired_sniper.log    # Log file (generated)
```

## 🔄 Automation

### Cron Job Setup

Run daily at 9 AM:
```bash
# Edit crontab
crontab -e

# Add this line
0 9 * * * /usr/bin/python3 /path/to/expired_sniper.py
```

### Systemd Service

Create `/etc/systemd/system/expired-sniper.service`:
```ini
[Unit]
Description=Expired Domain Sniper
After=network.target

[Service]
Type=oneshot
User=yourusername
WorkingDirectory=/path/to/expired_sniper
ExecStart=/usr/bin/python3 expired_sniper.py

[Install]
WantedBy=multi-user.target
```

## 🛡️ Legal & Ethical Considerations

- **Respect robots.txt**: Check site's crawling policies
- **Rate Limiting**: Script includes delays to be respectful
- **Terms of Service**: Ensure compliance with ExpiredDomains.net ToS
- **Personal Use**: Intended for personal domain research only

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Install all dependencies with `pip install -r requirements.txt`
2. **No Domains Found**: Website structure may have changed, check parsing logic
3. **Blocked Requests**: Increase delays in configuration
4. **Telegram Not Working**: Verify bot token and chat ID

### Debugging

Enable debug logging:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

### Website Changes

If ExpiredDomains.net changes their structure:
1. Update URL patterns in `get_expired_domains_page()`
2. Adjust table parsing in `parse_domain_row()`
3. Check CSS selectors for table elements

## 🚧 Future Enhancements

- [ ] GUI dashboard with Streamlit
- [ ] Proxy rotation support
- [ ] Multiple domain registrars
- [ ] WHOIS integration
- [ ] Domain scoring algorithm
- [ ] Email alerts
- [ ] Database storage
- [ ] RESTful API
- [ ] Docker containerization

## 📝 License

This project is for educational and personal use only. Please respect website terms of service and rate limiting.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the script.

## ⚠️ Disclaimer

This tool is for educational purposes only. Users are responsible for complying with all applicable laws and website terms of service. The author is not responsible for any misuse of this software.
