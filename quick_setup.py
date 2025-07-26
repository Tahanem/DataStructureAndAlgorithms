#!/usr/bin/env python3
"""
Quick Setup Script for Expired Domain Sniper
===========================================

This script downloads all necessary files for the domain sniper.
Run: python quick_setup.py
"""

import os
import urllib.request

def create_file(filename, content):
    """Create a file with given content"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filename}")

def main():
    print("🎯 Setting up Expired Domain Sniper...")
    print("=" * 50)
    
    # Create requirements.txt
    requirements = """requests>=2.31.0
beautifulsoup4>=4.12.0
fake-useragent>=1.4.0
python-telegram-bot>=20.0
lxml>=4.9.0"""
    
    create_file("requirements.txt", requirements)
    
    # Create config.py
    config_py = '''"""
Configuration file for Expired Domain Sniper
============================================

Customize these settings according to your needs.
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    """Configuration settings for the domain sniper"""
    
    # Filtering criteria
    MIN_LENGTH: int = 4
    MAX_LENGTH: int = 12
    TARGET_TLD: str = ".com"
    
    # Blacklist keywords (domains containing these will be rejected)
    BLACKLIST: List[str] = None
    
    # Watch keywords (domains containing these get priority alerts)
    WATCH_KEYWORDS: List[str] = None
    
    # Telegram settings (set to None to disable alerts)
    TELEGRAM_BOT_TOKEN: str = None  # Get from @BotFather on Telegram
    TELEGRAM_CHAT_ID: str = None    # Get from @userinfobot or group info
    
    # Scraping settings
    REQUEST_DELAY: tuple = (1, 3)  # Random delay between requests (min, max seconds)
    MAX_RETRIES: int = 3
    TIMEOUT: int = 30
    MAX_PAGES: int = 5  # Number of pages to scrape
    
    # Output settings
    OUTPUT_FILE: str = "sniped_domains.csv"
    LOG_FILE: str = "expired_sniper.log"
    
    # ExpiredDomains.net login (optional)
    LOGIN_USERNAME: str = None
    LOGIN_PASSWORD: str = None
    
    def __post_init__(self):
        """Set default values after initialization"""
        if self.BLACKLIST is None:
            self.BLACKLIST = [
                "free", "porn", "hack", "loan", "xxx", "adult", "sex", 
                "casino", "gambling", "debt", "credit", "mortgage", "insurance"
            ]
            
        if self.WATCH_KEYWORDS is None:
            self.WATCH_KEYWORDS = [
                "ai", "chat", "prompt", "labs", "bot", "wallet", "cloud", 
                "ninja", "agent", "flow", "tech", "app", "crypto", "web3",
                "nft", "meta", "verse", "smart", "auto", "dev", "code"
            ]


# Alternative configuration for more aggressive filtering
@dataclass 
class AggressiveConfig(Config):
    """More aggressive filtering configuration"""
    MIN_LENGTH: int = 5
    MAX_LENGTH: int = 8
    MAX_PAGES: int = 10
    
    def __post_init__(self):
        super().__post_init__()
        # Add more restrictive blacklist
        self.BLACKLIST.extend([
            "buy", "sell", "cheap", "best", "top", "review", "guide",
            "how", "what", "when", "where", "why", "tips", "help"
        ])


# Premium configuration for high-value domains only
@dataclass
class PremiumConfig(Config):
    """Configuration for premium domain hunting"""
    MIN_LENGTH: int = 4
    MAX_LENGTH: int = 6  # Shorter domains only
    MAX_PAGES: int = 15
    
    def __post_init__(self):
        super().__post_init__()
        # Focus on premium keywords
        self.WATCH_KEYWORDS = [
            "ai", "app", "bot", "pay", "buy", "get", "use", "new", "pro",
            "hub", "lab", "dev", "api", "web", "net", "sys", "tech", "data"
        ]
'''
    
    create_file("config.py", config_py)
    
    print("\n🚀 Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Get the main script from the conversation above")
    print("3. Edit config.py with your settings")
    print("4. Run: python expired_sniper.py")
    
    print("\n📥 Files to copy from conversation:")
    print("- expired_sniper.py (main script)")
    print("- test_sniper.py (test suite)")
    print("- USAGE_GUIDE.md (instructions)")

if __name__ == "__main__":
    main()