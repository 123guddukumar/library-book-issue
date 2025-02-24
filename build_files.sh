echo "BUILD START"

# Ensure Python is available
which python3
which pip3

# Upgrade pip and install dependencies
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
