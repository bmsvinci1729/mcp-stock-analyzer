#!/bin/bash
echo "🚀 Deploying Stock MCP System..."

# Install dependencies
pip install -r requirements.txt

# Create requirements.txt if it doesn't exist
pip freeze > requirements.txt

# Start the production system
python production_system.py
