#!/bin/bash

# Expired Domain Sniper Setup Script
# ==================================

echo "🎯 Setting up Expired Domain Sniper..."
echo "======================================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+' | head -1)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version detected (>= $required_version required)"
else
    echo "❌ Python $required_version or higher is required. Current: $python_version"
    echo "Please upgrade Python and try again."
    exit 1
fi

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
else
    echo "✅ pip3 is available"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make scripts executable
chmod +x expired_sniper.py
chmod +x test_sniper.py

# Run test suite
echo ""
echo "🧪 Running test suite..."
python3 test_sniper.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Edit config.py to customize settings"
    echo "   2. Add Telegram bot credentials (optional)"
    echo "   3. Run: python3 expired_sniper.py"
    echo ""
    echo "🔧 For automation, add to crontab:"
    echo "   0 9 * * * $(pwd)/expired_sniper.py"
else
    echo "❌ Tests failed. Please check the error messages above."
    exit 1
fi