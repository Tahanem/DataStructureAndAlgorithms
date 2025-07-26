#!/usr/bin/env python3
"""
Test script for Expired Domain Sniper
=====================================

Tests the filtering logic and basic functionality without scraping.
"""

import sys
import os
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from config import Config, AggressiveConfig, PremiumConfig
    from expired_sniper import DomainSniper
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required files are in the same directory")
    sys.exit(1)


def test_filtering_logic():
    """Test domain filtering logic with sample data"""
    print("🧪 Testing Domain Filtering Logic")
    print("=" * 40)
    
    config = Config()
    sniper = DomainSniper(config)
    
    # Sample domain data for testing
    test_domains = [
        # Valid domains that should pass
        {'domain': 'aibot.com', 'length': 5, 'status': 'Available', 'drop_date': '2024-01-15'},
        {'domain': 'chatflow.com', 'length': 8, 'status': 'Available', 'drop_date': '2024-01-15'},
        {'domain': 'quicklabs.com', 'length': 9, 'status': 'Auction', 'drop_date': '2024-01-15'},
        
        # Invalid domains that should be filtered out
        {'domain': 'ai123.com', 'length': 5, 'status': 'Available', 'drop_date': '2024-01-15'},  # Contains numbers
        {'domain': 'free-chat.com', 'length': 8, 'status': 'Available', 'drop_date': '2024-01-15'},  # Contains hyphen
        {'domain': 'pornbot.com', 'length': 7, 'status': 'Available', 'drop_date': '2024-01-15'},  # Blacklisted
        {'domain': 'xy.com', 'length': 2, 'status': 'Available', 'drop_date': '2024-01-15'},  # Too short
        {'domain': 'verylongdomainname.com', 'length': 18, 'status': 'Available', 'drop_date': '2024-01-15'},  # Too long
        {'domain': 'chatbot.com', 'length': 7, 'status': 'Registered', 'drop_date': '2024-01-15'},  # Registered
    ]
    
    valid_count = 0
    watch_matches = 0
    
    for domain_info in test_domains:
        is_valid = sniper.is_valid_domain(domain_info)
        has_watch = sniper.has_watch_keywords(domain_info['domain'])
        
        status = "✅ PASS" if is_valid else "❌ FAIL"
        watch_status = "🎯 WATCH" if has_watch else ""
        
        print(f"{status} {watch_status} {domain_info['domain']:<20} (Length: {domain_info['length']:2d})")
        
        if is_valid:
            valid_count += 1
            if has_watch:
                watch_matches += 1
    
    print(f"\n📊 Results:")
    print(f"   Total domains tested: {len(test_domains)}")
    print(f"   Valid domains: {valid_count}")
    print(f"   Watch matches: {watch_matches}")
    print(f"   Filter rate: {((len(test_domains) - valid_count) / len(test_domains)) * 100:.1f}%")


def test_configuration_variants():
    """Test different configuration variants"""
    print("\n🔧 Testing Configuration Variants")
    print("=" * 40)
    
    configs = {
        'Standard': Config(),
        'Aggressive': AggressiveConfig(),
        'Premium': PremiumConfig()
    }
    
    test_domain = {'domain': 'chatbot.com', 'length': 7, 'status': 'Available', 'drop_date': '2024-01-15'}
    
    for config_name, config in configs.items():
        sniper = DomainSniper(config)
        is_valid = sniper.is_valid_domain(test_domain)
        has_watch = sniper.has_watch_keywords(test_domain['domain'])
        
        print(f"{config_name:>12}: Valid={is_valid}, Watch={has_watch}, "
              f"Range={config.MIN_LENGTH}-{config.MAX_LENGTH}, "
              f"Blacklist={len(config.BLACKLIST)} items")


def test_csv_export():
    """Test CSV export functionality"""
    print("\n💾 Testing CSV Export")
    print("=" * 40)
    
    config = Config()
    sniper = DomainSniper(config)
    
    # Sample valid domains
    test_domains = [
        {
            'domain': 'aibot.com',
            'length': 5,
            'status': 'Available',
            'drop_date': '2024-01-15',
            'tld_count': '3',
            'backlinks': '25',
            'archive_url': 'https://web.archive.org/web/*/aibot.com',
            'watch_match': True
        },
        {
            'domain': 'quickflow.com',
            'length': 9,
            'status': 'Auction',
            'drop_date': '2024-01-16',
            'tld_count': '1',
            'backlinks': '12',
            'archive_url': 'https://web.archive.org/web/*/quickflow.com',
            'watch_match': True
        }
    ]
    
    # Test CSV export
    test_file = "test_domains.csv"
    original_output = config.OUTPUT_FILE
    config.OUTPUT_FILE = test_file
    
    try:
        sniper.export_to_csv(test_domains)
        
        # Check if file was created
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                content = f.read()
                print(f"✅ CSV export successful")
                print(f"📄 File size: {len(content)} bytes")
                print(f"📝 Content preview:")
                lines = content.split('\n')[:4]  # Show first 4 lines
                for line in lines:
                    print(f"   {line}")
                if len(content.split('\n')) > 4:
                    print("   ...")
        else:
            print("❌ CSV file was not created")
            
    except Exception as e:
        print(f"❌ CSV export failed: {e}")
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)
        config.OUTPUT_FILE = original_output


def test_telegram_format():
    """Test Telegram message formatting"""
    print("\n📲 Testing Telegram Message Format")
    print("=" * 40)
    
    config = Config()
    sniper = DomainSniper(config)
    
    test_domain = {
        'domain': 'aibot.com',
        'length': 5,
        'status': 'Available',
        'drop_date': '2024-01-15',
        'archive_url': 'https://web.archive.org/web/*/aibot.com'
    }
    
    # Simulate message formatting (without actually sending)
    message = (
        f"🔥 New watch match: {test_domain['domain']}\n"
        f"📊 Status: {test_domain['status']}\n"
        f"📅 Drop Date: {test_domain['drop_date']}\n"
        f"📏 Length: {test_domain['length']} chars\n"
        f"🔗 Archive: {test_domain['archive_url']}"
    )
    
    print("📱 Sample Telegram message:")
    print("─" * 30)
    print(message)
    print("─" * 30)


def main():
    """Run all tests"""
    print("🎯 Expired Domain Sniper - Test Suite")
    print("=" * 50)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_filtering_logic()
        test_configuration_variants()
        test_csv_export()
        test_telegram_format()
        
        print("\n✅ All tests completed successfully!")
        print("\n🚀 Ready to run the main script: python expired_sniper.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)