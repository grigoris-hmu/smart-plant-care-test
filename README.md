# smart-plant-care-test
SmartPlantCare repository for testing

## Run mini How To

### Clone repository
git clone https://github.com/grigoris-hmu/smart-plant-care-test.git<br/>
cd smart-plant-care-test/

### Initialize Python virtual enviroment
python3 -m virtualenv .venv<br/>
source .venv/bin/activate

### Install dependencies
pip install -r requirements.txt

### Install dependencies
pip install -r requirements.txt

### Set enviroment variables (used in SmartPlantCare/__init__.py)
export SECRET_KEY='use_a_strong_string'<br/>
export WTF_CSRF_SECRET_KEY='use_a_strong_string'<br/>
export SQLALCHEMY_DATABASE_URI='use_the_database_credentials'<br/>

### Run app locally (Running on http://127.0.0.1:5000)
python3 app.py
