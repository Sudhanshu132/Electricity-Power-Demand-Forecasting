#!/bin/bash
echo "============================================"
echo "   Running Power Demand Forecast Pipeline"
echo "============================================"

# Optional: activate a virtual environment
# source venv/bin/activate

# Check if Python is available
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 not found. Please install it or add to PATH."
    exit 1
fi

# Run the Python script
python3 MainStart.py
if [ $? -ne 0 ]; then
    echo "❌ Script failed to run."
    exit 1
fi

echo
echo "✅ Forecast completed successfully."
