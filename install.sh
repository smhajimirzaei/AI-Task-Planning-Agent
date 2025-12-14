#!/bin/bash
# AI Task Planning Agent - Installation Script

set -e

echo "=================================="
echo "AI Task Planning Agent Installer"
echo "=================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.9"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" 2>/dev/null; then
    echo "Error: Python 3.9 or higher is required"
    echo "Current version: $python_version"
    exit 1
fi
echo "✓ Python $python_version detected"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Anthropic API key"
    echo "   Get your key from: https://console.anthropic.com/"
else
    echo ".env file already exists"
fi

# Installation complete
echo ""
echo "=================================="
echo "Installation Complete! 🎉"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Add your Anthropic API key to .env file"
echo ""
echo "3. Run the setup wizard:"
echo "   python main.py setup"
echo ""
echo "4. Add your first task:"
echo "   python main.py add-task 'Your task' --priority high --duration 2"
echo ""
echo "5. Generate your first plan:"
echo "   python main.py plan"
echo ""
echo "For more information, see:"
echo "- QUICKSTART.md (5-minute guide)"
echo "- USAGE_GUIDE.md (comprehensive documentation)"
echo "- example_usage.py (code examples)"
echo ""
echo "Happy planning! 🚀"
