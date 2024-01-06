from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Book, Author
from . import create_app, db  

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
def index():
    books = Book.query.all()
    authors = Author.query.all()
    loaned_books = Book.query.filter_by(loaned=True).all()
    loaned_books_from_list = []
    owned_books = Book.query.filter_by(owned=True).all()
    owned_books_from_list = []
    return render_template('index.html', books=books, authors=authors,loaned_books=loaned_books, loaned_books_from_list=loaned_books_from_list, owned_books=owned_books, owned_books_from_list=owned_books_from_list)

@routes_blueprint.route('/list_books')
def list_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

@routes_blueprint.route('/list_authors')
def list_authors():
    authors = Author.query.all()
    return render_template('authors.html', authors=authors)

@routes_blueprint.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title', '')
        author_id = request.form.get('author', '')
        year = request.form.get('year', '')
        genre = request.form.get('genre', '')
        description = request.form.get('description', '')

        if not title or not author_id or not year or not genre or not description:
            # Jeżeli jakieś pole jest puste, zwróć błąd
            return render_template('add_book.html', error='Wszystkie pola są wymagane')

        # Sprawdź, czy istnieje autor o podanym ID
        author = Author.query.filter_by(id=author_id).first()

        # Sprawdź, czy autor istnieje w bazie danych
        if not author:
            return render_template('add_book.html', error='Nieprawidłowy autor. Wybierz autora z listy.')

        book = Book(title=title, author_id=author.id, year=year, genre=genre, description=description)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('routes.index'))

    # Pobierz listę wszystkich autorów
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)

@routes_blueprint.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)

    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Książka została usunięta.', 'success')
    else:
        flash('Nie znaleziono książki o podanym identyfikatorze.', 'danger')

    return redirect(url_for('routes.index'))

@routes_blueprint.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        nationality = request.form['nationality']

        author = Author(name=name, birth_date=birth_date, nationality=nationality)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('routes.list_authors'))
    return render_template('add_author.html')

@routes_blueprint.route('/delete_author/<int:author_id>', methods=['POST'])
def delete_author(author_id):
    author = Author.query.get(author_id)

    if author:
        if len(author.books) == 0:
            db.session.delete(author)
            db.session.commit()
            flash('Autor został usunięty.', 'success')
        else:
            flash('Nie można usunąć autora, ponieważ jest przypisany do książek.', 'danger')
    else:
        flash('Nie znaleziono autora o podanym identyfikatorze.', 'danger')

    return redirect(url_for('routes.index'))


@routes_blueprint.route('/loan_book/<int:book_id>', methods=['POST'])
def loan_book(book_id):
    book = Book.query.get(book_id)

    if book:
        if not book.owned:  # Dodaj warunek, czy książka nie jest już w Bibliotece
            book.loaned = True
            db.session.commit()
            flash('Książka została dodana do Wypożyczonych.', 'success')
        else:
            flash('Nie można wypożyczyć książki, gdyż jest już dostępna w Bibliotece.', 'danger')
    else:
        flash('Nie znaleziono książki o podanym identyfikatorze.', 'danger')

    return redirect(url_for('routes.index'))

@routes_blueprint.route('/list_loans')
def list_loans():
    books = Book.query.filter_by(loaned=True).all()
    return render_template('loan.html', books=books)

@routes_blueprint.route('/own_book/<int:book_id>', methods=['POST'])
def own_book(book_id):
    book = Book.query.get(book_id)

    if book:
        if not book.loaned:  # Dodaj warunek, czy książka nie jest wypożyczona
            book.owned = True
            db.session.commit()
            flash('Książka została dodana do W Bibliotece.', 'success')
        else:
            flash('Nie można dodać książki do W Bibliotece, gdyż jest aktualnie wypożyczona.', 'danger')
    else:
        flash('Nie znaleziono książki o podanym identyfikatorze.', 'danger')

    return redirect(url_for('routes.index'))

@routes_blueprint.route('/list_owned')
def list_owned():
    books = Book.query.filter_by(owned=True).all()
    return render_template('owned.html', books=books)

@routes_blueprint.route('/toggle_book_status/<int:book_id>', methods=['POST'])
def toggle_book_status(book_id):
    book = Book.query.get(book_id)

    if book:
        if book.owned:
            book.owned = False
            book.loaned = True
            flash('Książka została dodana do Wypożyczonych.', 'success')
        elif book.loaned:
            book.owned = True
            book.loaned = False
            flash('Książka została dodana do W Bibliotece.', 'success')
        else:
            book.loaned = True
            flash('Książka została dodana do Wypożyczonych.', 'success')

        db.session.commit()
    else:
        # Tutaj dodaj kod obsługujący przypadek, gdy nie znaleziono książki
        flash('Nie znaleziono książki o podanym identyfikatorze.', 'danger')

    return redirect(url_for('routes.index'))

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
