#!/usr/bin/env python3
"""
Expired Domain Sniper Bot
=========================

A bot that scrapes ExpiredDomains.net for expired .com domains,
filters them based on custom criteria, and exports results to CSV.
Optionally sends Telegram alerts for high-value matches.

Author: Senior Python Developer
Requirements: Python 3.10+, see requirements in main() function
"""

import requests
import csv
import re
import time
import random
import json
import logging
from datetime import datetime, timedelta
from urllib.parse import urljoin, quote
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    from fake_useragent import UserAgent
except ImportError:
    print("Missing required dependencies. Install with:")
    print("pip install requests beautifulsoup4 fake-useragent python-telegram-bot")
    exit(1)

# Import configuration
try:
    from config import Config, AggressiveConfig, PremiumConfig
except ImportError:
    # Fallback configuration if config.py is not available
    @dataclass
    class Config:
        """Fallback configuration settings for the domain sniper"""
        
        # Filtering criteria
        MIN_LENGTH = 4
        MAX_LENGTH = 12
        TARGET_TLD = ".com"
        
        # Blacklist keywords (domains containing these will be rejected)
        BLACKLIST = ["free", "porn", "hack", "loan", "xxx", "adult", "sex", "casino", "gambling"]
        
        # Watch keywords (domains containing these get priority alerts)
        WATCH_KEYWORDS = ["ai", "chat", "prompt", "labs", "bot", "wallet", "cloud", "ninja", "agent", "flow"]
        
        # Telegram settings (set to None to disable)
        TELEGRAM_BOT_TOKEN = None  # Add your bot token here
        TELEGRAM_CHAT_ID = None    # Add your chat ID here
        
        # Scraping settings
        REQUEST_DELAY = (1, 3)  # Random delay between requests (min, max seconds)
        MAX_RETRIES = 3
        TIMEOUT = 30
        
        # Output settings
        OUTPUT_FILE = "sniped_domains.csv"
        LOG_FILE = "expired_sniper.log"


class DomainSniper:
    """Main class for expired domain sniping operations"""
    
    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_logging()
        self.setup_session()
        self.domains_found = []
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_session(self):
        """Setup requests session with proper headers"""
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def random_delay(self):
        """Add random delay to avoid being blocked"""
        delay = random.uniform(*self.config.REQUEST_DELAY)
        time.sleep(delay)
        
    def make_request(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with retry logic and error handling"""
        for attempt in range(self.config.MAX_RETRIES):
            try:
                self.random_delay()
                response = self.session.get(url, timeout=self.config.TIMEOUT, **kwargs)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed for {url}: {e}")
                if attempt == self.config.MAX_RETRIES - 1:
                    self.logger.error(f"All attempts failed for {url}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
        
    def get_expired_domains_page(self, page: int = 1) -> Optional[BeautifulSoup]:
        """Fetch the expired domains list page"""
        # ExpiredDomains.net URL structure (this might need adjustment based on actual site)
        base_url = "https://www.expireddomains.net/expired-com-domains/"
        
        params = {
            'start': (page - 1) * 25,  # Typical pagination
            'searchinit': 1,
            'o': 'changed',  # Order by changed date
            'r': 'a',        # Ascending order
        }
        
        url = f"{base_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        
        self.logger.info(f"Fetching expired domains page {page}")
        response = self.make_request(url)
        
        if not response:
            return None
            
        return BeautifulSoup(response.content, 'html.parser')
        
    def parse_domain_row(self, row) -> Optional[Dict]:
        """Parse a single domain row from the table"""
        try:
            cells = row.find_all('td')
            if len(cells) < 5:
                return None
                
            # Extract domain name (usually in first cell)
            domain_cell = cells[0]
            domain_link = domain_cell.find('a')
            if not domain_link:
                return None
                
            domain_name = domain_link.text.strip()
            
            # Only process .com domains
            if not domain_name.endswith(self.config.TARGET_TLD):
                return None
                
            # Extract other information from subsequent cells
            # Note: This structure might need adjustment based on actual website layout
            tld_count = self.extract_text_from_cell(cells, 1, "0")
            status = self.extract_text_from_cell(cells, 2, "Unknown")
            drop_date = self.extract_text_from_cell(cells, 3, "")
            
            # Additional data extraction
            backlinks = self.extract_text_from_cell(cells, 4, "0")
            
            return {
                'domain': domain_name,
                'tld': self.config.TARGET_TLD,
                'length': len(domain_name.replace(self.config.TARGET_TLD, '')),
                'status': status,
                'drop_date': drop_date,
                'tld_count': tld_count,
                'backlinks': backlinks,
                'archive_url': f"https://web.archive.org/web/*/{domain_name}"
            }
            
        except Exception as e:
            self.logger.warning(f"Error parsing domain row: {e}")
            return None
            
    def extract_text_from_cell(self, cells: List, index: int, default: str = "") -> str:
        """Safely extract text from table cell"""
        try:
            if index < len(cells):
                return cells[index].get_text(strip=True)
            return default
        except:
            return default
            
    def is_valid_domain(self, domain_info: Dict) -> bool:
        """Check if domain meets filtering criteria"""
        domain_name = domain_info['domain'].replace(self.config.TARGET_TLD, '')
        
        # Length check
        if not (self.config.MIN_LENGTH <= domain_info['length'] <= self.config.MAX_LENGTH):
            return False
            
        # Only letters check (no numbers, hyphens, or special characters)
        if not re.match(r'^[a-zA-Z]+$', domain_name):
            return False
            
        # Blacklist check
        domain_lower = domain_name.lower()
        for blacklisted in self.config.BLACKLIST:
            if blacklisted in domain_lower:
                return False
                
        # Status check (should be available for registration)
        status_lower = domain_info['status'].lower()
        if 'registered' in status_lower or 'taken' in status_lower:
            return False
            
        return True
        
    def has_watch_keywords(self, domain_name: str) -> bool:
        """Check if domain contains any watch keywords"""
        domain_lower = domain_name.lower()
        return any(keyword in domain_lower for keyword in self.config.WATCH_KEYWORDS)
        
    def scrape_expired_domains(self, max_pages: int = 5) -> List[Dict]:
        """Scrape expired domains from multiple pages"""
        all_domains = []
        
        for page in range(1, max_pages + 1):
            self.logger.info(f"Scraping page {page}/{max_pages}")
            
            soup = self.get_expired_domains_page(page)
            if not soup:
                self.logger.warning(f"Failed to fetch page {page}")
                continue
                
            # Find the main table (this selector might need adjustment)
            table = soup.find('table', {'class': ['base1', 'sortable']}) or soup.find('table')
            if not table:
                self.logger.warning(f"No table found on page {page}")
                continue
                
            rows = table.find_all('tr')[1:]  # Skip header row
            
            page_domains = 0
            for row in rows:
                domain_info = self.parse_domain_row(row)
                if domain_info and self.is_valid_domain(domain_info):
                    # Add watch match flag
                    domain_info['watch_match'] = self.has_watch_keywords(domain_info['domain'])
                    all_domains.append(domain_info)
                    page_domains += 1
                    
            self.logger.info(f"Found {page_domains} valid domains on page {page}")
            
            # Be respectful to the server
            self.random_delay()
            
        self.logger.info(f"Total valid domains found: {len(all_domains)}")
        return all_domains
        
    def check_domain_availability(self, domain: str) -> str:
        """Check domain availability via WHOIS (simplified version)"""
        try:
            # This is a simplified check - you might want to use python-whois library
            whois_url = f"https://www.whois.com/whois/{domain}"
            response = self.make_request(whois_url)
            
            if response and "No match for" in response.text:
                return "Available"
            elif response and "Registry Expiry Date" in response.text:
                return "Registered"
            else:
                return "Unknown"
        except:
            return "Unknown"
            
    def send_telegram_alert(self, domain_info: Dict):
        """Send Telegram alert for high-value domains"""
        if not self.config.TELEGRAM_BOT_TOKEN or not self.config.TELEGRAM_CHAT_ID:
            return
            
        try:
            message = (
                f"🔥 New watch match: {domain_info['domain']}\n"
                f"📊 Status: {domain_info['status']}\n"
                f"📅 Drop Date: {domain_info['drop_date']}\n"
                f"📏 Length: {domain_info['length']} chars\n"
                f"🔗 Archive: {domain_info['archive_url']}"
            )
            
            url = f"https://api.telegram.org/bot{self.config.TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                'chat_id': self.config.TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, data=data, timeout=10)
            if response.status_code == 200:
                self.logger.info(f"Telegram alert sent for {domain_info['domain']}")
            else:
                self.logger.warning(f"Failed to send Telegram alert: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error sending Telegram alert: {e}")
            
    def export_to_csv(self, domains: List[Dict]):
        """Export filtered domains to CSV file"""
        if not domains:
            self.logger.info("No domains to export")
            return
            
        fieldnames = ["Domain", "Length", "Status", "DropDate", "TLD_Count", "WatchMatch", "ArchiveURL"]
        
        try:
            with open(self.config.OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for domain in domains:
                    writer.writerow({
                        "Domain": domain['domain'],
                        "Length": domain['length'],
                        "Status": domain['status'],
                        "DropDate": domain['drop_date'],
                        "TLD_Count": domain['tld_count'],
                        "WatchMatch": domain['watch_match'],
                        "ArchiveURL": domain['archive_url']
                    })
                    
            self.logger.info(f"Exported {len(domains)} domains to {self.config.OUTPUT_FILE}")
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            
    def process_alerts(self, domains: List[Dict]):
        """Process and send alerts for high-value domains"""
        alert_domains = [
            d for d in domains 
            if d['watch_match'] and d['length'] < 10
        ]
        
        self.logger.info(f"Found {len(alert_domains)} domains for alerts")
        
        for domain in alert_domains:
            self.send_telegram_alert(domain)
            time.sleep(1)  # Rate limit Telegram messages
            
    def run(self, max_pages: int = 5):
        """Main execution method"""
        self.logger.info("🚀 Starting Expired Domain Sniper")
        start_time = datetime.now()
        
        try:
            # Scrape domains
            domains = self.scrape_expired_domains(max_pages)
            
            if not domains:
                self.logger.warning("No domains found matching criteria")
                return
                
            # Sort by length and watch matches (prioritize shorter domains with watch keywords)
            domains.sort(key=lambda x: (not x['watch_match'], x['length']))
            
            # Export to CSV
            self.export_to_csv(domains)
            
            # Send alerts
            self.process_alerts(domains)
            
            # Summary
            watch_matches = sum(1 for d in domains if d['watch_match'])
            elapsed = datetime.now() - start_time
            
            self.logger.info(f"✅ Completed in {elapsed.total_seconds():.1f}s")
            self.logger.info(f"📊 Total domains: {len(domains)}")
            self.logger.info(f"🎯 Watch matches: {watch_matches}")
            self.logger.info(f"💾 Results saved to: {self.config.OUTPUT_FILE}")
            
        except KeyboardInterrupt:
            self.logger.info("⏹️ Process interrupted by user")
        except Exception as e:
            self.logger.error(f"❌ Unexpected error: {e}")
            raise


def simulate_login_expireddomains(session: requests.Session) -> bool:
    """
    Simulate login to ExpiredDomains.net
    Note: This is a placeholder - you'll need to implement actual login logic
    """
    try:
        # Get login page
        login_url = "https://www.expireddomains.net/login/"
        response = session.get(login_url)
        
        if response.status_code != 200:
            return False
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract CSRF token or other required fields
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'}) or soup.find('input', {'name': '_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
            
        # Login data (you'll need to replace with actual credentials)
        login_data = {
            'username': 'your_username',  # Replace with actual username
            'password': 'your_password',  # Replace with actual password
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
            
        # Attempt login
        response = session.post(login_url, data=login_data)
        
        # Check if login was successful (adjust based on actual response)
        if 'dashboard' in response.url.lower() or 'logout' in response.text.lower():
            return True
            
        return False
        
    except Exception as e:
        logging.error(f"Login simulation failed: {e}")
        return False


def main():
    """Main entry point"""
    print("🎯 Expired Domain Sniper v1.0")
    print("=" * 40)
    
    # Check dependencies
    required_packages = {
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'fake-useragent': 'fake_useragent'
    }
    
    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
            
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return
        
    # Initialize configuration
    config = Config()
    
    # Create sniper instance
    sniper = DomainSniper(config)
    
    # Optional: Attempt login simulation
    # login_success = simulate_login_expireddomains(sniper.session)
    # if login_success:
    #     sniper.logger.info("✅ Login simulation successful")
    # else:
    #     sniper.logger.warning("⚠️ Login simulation failed, proceeding with public access")
    
    # Run the sniper
    try:
        sniper.run(max_pages=3)  # Start with 3 pages
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        logging.error(f"Fatal error in main: {e}")


if __name__ == "__main__":
    main()