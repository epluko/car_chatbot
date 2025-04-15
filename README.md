# car_chatbot
Simple chatbot assistant - demo - test


How to run the app:
1. Download the code or clone the repository.
2. Change working directory to the main project directory car_chatbot
3. Create python virtual environment using python 3.13.2 or later and activate it.
```
python3.13 -m venv venv
source venv/bin/activate
```
4. Install dependencies
```
pip install -r app/requirements.txt
```
5. Create your own .env (copy the template file and edit).
```
cp app/.env.tmpleate app/.env
```
6. Run the streamlit app
```
streamlit run app/streamlit_app.py
```