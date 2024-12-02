Start the Application Locally
   frontend
      1) pnpm i (or) npm i --force
      2) pnpm run dev (or) npm run dev
   backend
      1) python -m venv venv
      2) venv\Scripts\activate
      3) pip install -r requirements.txt
      4) python manage.py makemigrations
      5) python manage.py migrate
      6) python manage.py createsuperuser
         it will prompt for username,email and password
         enter admin,admin@gmail.com,1234 
      7) python manage.py update_players.py
      8) python manage.py update_data.py



1) model.pt -> ML Model file
2) api/ml_model.py -> ML model integrated with the Web UI
3) api/agent.py -> LLM gen AI integrated feature 
4) api/data -> stored data of player to identifier mapping and player stats etc