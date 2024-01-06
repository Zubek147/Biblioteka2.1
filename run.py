from app import create_app, db
from flask_migrate import Migrate
from init_db import init_database  # Dodaj import dla funkcji init_database

app = create_app()
migrate = Migrate(app, db)

# Dodaj ten kod, aby sprawdzić i utworzyć bazę danych z przykładowymi danymi
with app.app_context():
    init_database()

if __name__ == '__main__':
    app.run(debug=True)
