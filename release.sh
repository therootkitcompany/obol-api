# build_files.sh
pip install -r requirements.txt

python3.12 manage.py migrate
python3.12 manage.py loaddata foods/fixtures/foods.json
