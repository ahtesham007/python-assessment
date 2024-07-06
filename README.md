# stantech-ai-assessment
This repository has solution for the assessment questions


1. SQL Assesment

   Based on the question query has been provided in the in the .sql file

4. Python Assesment

    All the requirements have been implemented

## Setup
1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>/python_app

2. **Create a virtual environment: (optional but recommended):**

   ```bash
      python -m venv env
  
    # Activate the virtual environment
    # On Windows
    .\env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
    
3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt

4. **Set up the .env file:**

   Create a .env file in the root of the project. Add the necessary environment variables.

   ```bash
   FLASK_APP=run.py
   FLASK_ENV=development

   #Database Config
   DATABASE_USER=
   DATABASE_PASSWORD=
   DATABASE_HOST=localhost
   DATABASE_PORT=3306
   DATABASE_NAME=

   #JWT Config
   JWT_SECRET_KEY=

5. **Run the Flask app:**

   ```bash
   flask run

**End points**

1. /signup - POST
2. /login  - POST
3. /upload  - POST
4. /summary  - GET

**Features**
-  Logging
-  Exception Handling
-  JWT Token
-  SQLAlchemy ORM
-  Data Cleaning
-  Summary
   
