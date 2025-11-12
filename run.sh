#!/bin/bash
# Simple script to run BrandManager topic research

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to show usage
show_usage() {
    echo -e "${GREEN}BrandManager - AI Topic Research Tool${NC}"
    echo ""
    echo "Usage: ./run.sh [command] [topic]"
    echo ""
    echo "Commands:"
    echo "  setup              - First-time setup (install + configure)"
    echo "  install            - Install the package"
    echo "  research <topic>   - Research a topic (standard depth)"
    echo "  quick <topic>      - Quick research (faster, less detailed)"
    echo "  deep <topic>       - Deep research (slower, more comprehensive)"
    echo ""
    echo "Examples:"
    echo "  ./run.sh setup"
    echo "  ./run.sh research \"AI in healthcare\""
    echo "  ./run.sh quick \"sustainable fashion\""
    echo "  ./run.sh deep \"quantum computing\""
    echo ""
}

# Function to setup the project
setup_project() {
    echo -e "${GREEN}Setting up BrandManager...${NC}"
    
    # Install package
    echo "Installing package..."
    pip install -e .
    
    # Setup .env file
    if [ ! -f .env ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file from .env.example${NC}"
        echo -e "${YELLOW}⚠ Please edit .env and add your OPENAI_API_KEY${NC}"
    else
        echo -e "${GREEN}✓ .env file already exists${NC}"
    fi
    
    echo ""
    echo -e "${GREEN}Setup complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env and add your OpenAI API key"
    echo "2. Run: ./run.sh research \"your topic\""
}

# Function to install package
install_package() {
    echo -e "${GREEN}Installing BrandManager...${NC}"
    pip install -e .
    echo -e "${GREEN}✓ Installation complete${NC}"
}

# Function to research topic
research_topic() {
    local depth="$1"
    local topic="$2"
    
    if [ -z "$topic" ]; then
        echo -e "${RED}Error: Topic is required${NC}"
        echo "Usage: ./run.sh $depth \"your topic here\""
        exit 1
    fi
    
    if [ "$depth" = "research" ]; then
        topic-research research "$topic"
    elif [ "$depth" = "quick" ]; then
        topic-research quick "$topic"
    elif [ "$depth" = "deep" ]; then
        topic-research deep "$topic"
    fi
}

# Main script logic
case "$1" in
    setup)
        setup_project
        ;;
    install)
        install_package
        ;;
    research)
        research_topic "research" "$2"
        ;;
    quick)
        research_topic "quick" "$2"
        ;;
    deep)
        research_topic "deep" "$2"
        ;;
    help|--help|-h|"")
        show_usage
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac
