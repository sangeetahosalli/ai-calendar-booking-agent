#!/bin/bash

# setup-env.sh
# Automated environment setup script for AI Calendar Booking Agent

echo "🚀 Setting up AI Calendar Booking Agent Environment..."
echo "=================================================="

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Setup cancelled. Existing .env file preserved."
        exit 1
    fi
fi

# Copy .env.example to .env
if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "✅ Created .env from .env.example template"
else
    echo "❌ .env.example not found! Please ensure all project files are present."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully"
else
    echo "❌ pip not found! Please install Python and pip first."
    exit 1
fi

# Create directories
echo "📁 Creating project directories..."
mkdir -p uploads backups logs data
echo "✅ Project directories created"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Create/update .gitignore
echo "📝 Setting up .gitignore..."
cat > .gitignore << 'EOF'
# Environment variables
.env
.env.local
.env.production

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Credentials
credentials.json
token.json
*.key
*.pem

# Logs
*.log
logs/

# Database
*.db
*.sqlite
data/

# Temporary files
*.tmp
*.temp
uploads/
backups/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution
dist/
build/
*.egg-info/
EOF

echo "✅ .gitignore configured"

# Validate configuration
echo "🔍 Validating configuration..."
if python -c "from config import config; config.print_config_summary()" 2>/dev/null; then
    echo "✅ Configuration validation successful"
else
    echo "⚠️  Configuration needs attention - run 'python config.py' for details"
fi

echo ""
echo "🎉 Environment setup complete!"
echo "=================================================="
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your actual configuration values:"
echo "   nano .env"
echo ""
echo "2. For Google Calendar integration:"
echo "   - Go to: https://console.cloud.google.com/"
echo "   - Enable Google Calendar API"
echo "   - Create OAuth credentials"
echo "   - Download credentials.json"
echo "   - Update GOOGLE_* variables in .env"
echo ""
echo "3. Test your configuration:"
echo "   python config.py"
echo ""
echo "4. Run the application:"
echo "   streamlit run calendar_booking_agent.py"
echo ""
echo "5. Commit your changes:"
echo "   git add ."
echo "   git commit -m '🔧 Setup environment configuration'"
echo ""
echo "📚 For detailed setup instructions, see README.md"
echo "🔐 Remember: Never commit .env file to version control!"