#!/bin/bash
# Quick setup and test script

cd "$(dirname "$0")"

# Check Python version
echo "Python version:"
python --version

# Try importing main packages
echo -e "\nChecking main packages..."
python -c "
try:
    import pandas; print('✓ pandas')
    import numpy; print('✓ numpy')
    import sklearn; print('✓ scikit-learn')
    import matplotlib; print('✓ matplotlib')
    import seaborn; print('✓ seaborn')
    import joblib; print('✓ joblib')
    print('\n✓ All core packages available!')
except ImportError as e:
    print(f'✗ Missing: {e}')
"

# Check data
echo -e "\nChecking data..."
if [ -f "data/raw/StrockDataset.csv" ]; then
    echo "✓ Dataset found"
    wc -l data/raw/StrockDataset.csv
else
    echo "✗ Dataset not found"
fi

# Check source modules
echo -e "\nChecking source modules..."
for file in src/{__init__,data_loader,preprocessing,models,utils}.py; do
    if [ -f "$file" ]; then
        echo "✓ $(basename $file)"
    else
        echo "✗ Missing $file"
    fi
done

echo -e "\n✓ Setup verification complete!"
