**LibraLink - Library Management System**
LibraLink is a Django-based application designed to streamline library management tasks such as tracking book transactions, managing patron accounts, and handling book inventory. 

**Features**
Patron Management: Add, edit, and deactivate patron records with ease.
Book Inventory: Track book availability and manage checkouts and returns.
Transaction Logs: Record and view transaction histories with pagination support.
Search and Filter: Dynamic search capabilities to find books and patrons quickly.
Automated Notifications: Inform users about transaction statuses and errors through system messages.

**Getting Started**
Prerequisites:
Python 3.8+
Django 3.2+
Pipenv or virtualenv for managing dependencies

**Installation**
1. Clone the repository:
git clone https://github.com/rizalargadas/libralink.git
cd libralink

2. Set up a virtual environment:
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate

3. Install the dependencies:
pip install -r requirements.txt

4. Run database migrations:
python manage.py migrate

5. Start the server:
python manage.py runserver

6. Open a web browser and navigate to http://127.0.0.1:8000/ to use the application.
   
**Contributing**
Any contributions you make are greatly appreciated.

**Contact**
Email: rmlargadas@gmail.com
