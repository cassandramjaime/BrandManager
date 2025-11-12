.PHONY: help install install-dev run quick deep test clean setup

help:
	@echo "BrandManager - AI Topic Research Tool"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup        - Complete first-time setup (install + configure)"
	@echo "  make install      - Install the package and dependencies"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make run          - Run topic research (usage: make run TOPIC='your topic')"
	@echo "  make quick        - Quick research (usage: make quick TOPIC='your topic')"
	@echo "  make deep         - Deep research (usage: make deep TOPIC='your topic')"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Remove build artifacts and cache files"
	@echo "  make help         - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make setup"
	@echo "  make run TOPIC='AI in healthcare'"
	@echo "  make quick TOPIC='sustainable fashion'"
	@echo "  make deep TOPIC='quantum computing' OUTPUT='results.json'"

setup: install
	@echo "Setting up .env file..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ Created .env file from .env.example"; \
		echo "⚠ Please edit .env and add your OPENAI_API_KEY"; \
	else \
		echo "✓ .env file already exists"; \
	fi
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "1. Edit .env and add your OpenAI API key"
	@echo "2. Run: make run TOPIC='your topic'"

install:
	@echo "Installing BrandManager..."
	pip install -e .
	@echo "✓ Installation complete"

install-dev:
	@echo "Installing BrandManager with dev dependencies..."
	pip install -e .
	pip install -r requirements-dev.txt
	@echo "✓ Development installation complete"

run:
	@if [ -z "$(TOPIC)" ]; then \
		echo "Error: TOPIC is required"; \
		echo "Usage: make run TOPIC='your topic here'"; \
		echo "Example: make run TOPIC='AI in healthcare'"; \
		exit 1; \
	fi
	@if [ -n "$(OUTPUT)" ]; then \
		topic-research research "$(TOPIC)" --output "$(OUTPUT)"; \
	else \
		topic-research research "$(TOPIC)"; \
	fi

quick:
	@if [ -z "$(TOPIC)" ]; then \
		echo "Error: TOPIC is required"; \
		echo "Usage: make quick TOPIC='your topic here'"; \
		echo "Example: make quick TOPIC='sustainable fashion'"; \
		exit 1; \
	fi
	@if [ -n "$(OUTPUT)" ]; then \
		topic-research quick "$(TOPIC)" --output "$(OUTPUT)"; \
	else \
		topic-research quick "$(TOPIC)"; \
	fi

deep:
	@if [ -z "$(TOPIC)" ]; then \
		echo "Error: TOPIC is required"; \
		echo "Usage: make deep TOPIC='your topic here'"; \
		echo "Example: make deep TOPIC='quantum computing'"; \
		exit 1; \
	fi
	@if [ -n "$(OUTPUT)" ]; then \
		topic-research deep "$(TOPIC)" --output "$(OUTPUT)"; \
	else \
		topic-research deep "$(TOPIC)"; \
	fi

test:
	@echo "Running tests..."
	pytest tests/ -v

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleanup complete"
