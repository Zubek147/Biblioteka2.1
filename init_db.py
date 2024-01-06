from app import db
from app.models import Book, Author

def init_database():
    db.create_all()

    # Sprawdź, czy w bazie danych nie ma już przykładowych danych dla Book
    if not Book.query.first():
        # Jeśli nie, dodaj przykładową książkę z przypisanym autorem
        example_author = Author(
            name='Przykładowy Autor',
            birth_date='01-01-1990',
            nationality='Przykładowa Narodowość'
        )
        db.session.add(example_author)
        db.session.commit()

        example_book = Book(
            title='Przykładowa Książka',
            author_id=example_author.id,  # Ustawiamy foreign key na id autora
            year=2022,
            genre='Przykładowy Gatunek',
            description='To jest przykładowy opis książki.'
        )
        db.session.add(example_book)
        db.session.commit()

if __name__ == '__main__':
    init_database()
