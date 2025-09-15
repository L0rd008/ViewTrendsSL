@echo off
echo Installing core dependencies...
pip install -r requirements.txt

echo Installing development dependencies...
pip install -r requirements-dev.txt

echo Installing production dependencies...
pip install -r requirements-prod.txt

echo All dependencies installed successfully.
