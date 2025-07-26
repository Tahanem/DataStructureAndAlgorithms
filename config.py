"""
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