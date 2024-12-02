![Project Landing Page](https://res.cloudinary.com/dqo9rn5lp/image/upload/v1733159971/landing_page_ho80ra.png)

# Project Repository Structure

This repository is structured to streamline data processing, modeling, and UI integration. Below is an overview of each folder and its purpose.

---

## 🚀 Main Application

*(This section is currently empty. Fill in with relevant details about the main application.)*

---

## Data

*(This section is currently empty. Fill in with relevant details about the data processing and structure.)*

---

## Data Processing

*(This section is currently empty. Fill in with relevant details about data processing scripts and workflows.)*

---

## Documentation and Demos

*(This section is currently empty. Fill in with relevant details about documentation, videos, and walkthroughs.)*

---

## Model

*(This section is currently empty. Fill in with relevant details about training, prediction, and model scripts.)*

---

## Model Artifacts

*(This section is currently empty. Fill in with relevant details about pre-trained models and artifacts.)*

---

## Out of Sample Data

*(This section is currently empty. Fill in with relevant details about evaluation data and integration workflows.)*

---

## Rest

*(This section is currently empty. Fill in with details about any miscellaneous requirements.)*

---

## UI

### BASE_DIR: `/src/UI/PRODUCT_UI`

#### Key Components:
1. **`model.pt`**: ML Model file.  
2. **`api/ml_model.py`**: ML model integrated with the Web UI.  
3. **`api/agent.py`**: LLM Generative AI integrated feature.  
4. **`api/data`**: Stores data for player-to-identifier mapping and player stats.

---

#### Deployed Site:
The Product UI is deployed and accessible at:  
**[http://172.16.4.2:8080](http://172.16.4.2:8080)**  

The Product UI can be tested and utilized at the above URL.

---

## Start the Application Locally

### Frontend (cd `frontend`)
1. Install dependencies:  
   ```bash
   pnpm i
   # or
   npm i --force
2. Start the development server:
   ``` bash
   pnpm run dev
   # or
   npm run dev

### Backend (cd `backend`)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
5. Enter the following details:
   1) Username: admin
   2) Email: admin@gmail.com
   3) Password: 1234
6. Update player data:
   ```bash
   python manage.py update_players.py
7. Update additional data:
   ```bash
   python manage.py update_data.py