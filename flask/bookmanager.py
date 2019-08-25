import os

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request, flash

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import Form
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms import validators

# Configuring the database as book_database
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "book_database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
# Setting secret kry because form needs a CSRF token
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = SQLAlchemy(app)


class Book(db.Model):
    """
        The class for the table book which is situated in book_database
    """
    book_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120))
    publisher = db.Column(db.String(120))
    page_no = db.Column(db.Integer)

    def __init__(self, book_id, book_name, author, publisher, page_no):
        self.book_id = book_id
        self.book_name = book_name
        self.author = author
        self.publisher = publisher
        self.page_no = page_no


class AddForm(Form):
    """
        class to create the form to add data to table
    """
    book_id = IntegerField(u"Book id", validators=[validators.input_required()])
    book_name = TextAreaField("Name Of book", validators=[validators.input_required()])
    author = TextAreaField("Author")
    publisher = TextAreaField("Publisher")
    page_no = IntegerField("Page_no")
    submit = SubmitField("Add Book")


@app.route('/')
def index():
    """
        base url redirected to list url
    :return: None
    """
    redirect('/list')


@app.route('/add', methods=["GET", "POST"])
def add():
    """

    :return:form which is the add form  if method is GET else redirected to list url
    """
    form = AddForm()
    if request.method == 'POST':
        if not form.validate():
            flash('All fields are required.')
            return render_template('add.html', form=form)
        else:
            try:
                book = Book(book_id=request.form.get("book_id"), book_name=request.form.get("book_name"),
                            author=request.form.get("author"), publisher=request.form.get("publisher"),
                            page_no=request.form.get("page_no"))
                db.session.add(book)
                db.session.commit()
            except Exception as e:
                print("Failed to add book")
                print(e)
            return redirect('/list')
    return render_template('add.html', form=form)


@app.route('/list')
def list():
    """

    :return: Variable book which contains the table contents
    """
    books = Book.query.all()
    return render_template("list.html", books=books)


@app.route("/filter_book", methods=["POST"])
def filter_book():
    """

    :return: Returns variable books to filter.html,books contains filtered book table rows
    """
    author = request.form.get("author")
    books = Book.query.filter_by(author=author)
    return render_template("filter.html", books=books)


@app.route("/delete", methods=["POST"])
def delete():
    """
        Deletes a particular record in table
    :return: None
    """
    book_id = request.form.get("book_id")
    # book = Book()
    book = Book.query.filter_by(book_id=book_id).first()
    print(book)
    db.session.delete(book)
    db.session.commit()
    return redirect("/list")


@app.route("/update", methods=["GET", "POST"])
def update():
    """
        Updates an existing record
    :return: form if method is GET
    """
    form = AddForm()
    if request.method == 'POST':
        if not request.form.get("book_id"):
            # If book_id is not entered by user return to same page
            flash('Book id is required.')
            return render_template('update.html', form=form)
        else:
            try:
                book_name = request.form.get("book_name")
                book_id = request.form.get("book_id")
                author = request.form.get("author")
                publisher = request.form.get("publisher")
                page_no = request.form.get("page_no")
                book = Book.query.filter_by(book_id=book_id).first()
                # If a field is not null enter data to table book
                if book_name:
                    book.book_name = book_name
                    if author:
                        book.author = author
                        if publisher:
                            book.publisher = publisher
                            if page_no:
                                book.page_no = page_no
                db.session.commit()
            except Exception as e:
                print("Failed to update book")
                print(e)
            return redirect('/list')
    return render_template('update.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
