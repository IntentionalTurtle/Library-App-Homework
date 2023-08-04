from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix= '/api')

@api.route('/book', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    pub_year = request.json['pub_year']
    ISBN = request.json['ISBN']
    in_inventory = request.json['in_inventory']
    hard_paper = request.json['hard_paper']
    user_token = current_user_token.token

    # print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, pub_year, ISBN, in_inventory, hard_paper, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

#get all cars
@api.route('/book', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    book = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(book)
    return jsonify(response)

#Get Single Contact
@api.route('/book/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

# UPDATE endpoint <id> is a variable, 'PUT' is the replacement method
@api.route('/book/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.title = request.json['title']
    book.author = request.json['author']
    book.pub_year = request.json['pub_year']
    book.ISBN = request.json['ISBN']
    book.in_inventory = request.json['in_inventory']
    book.hard_paper = request.json['hard_paper']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE ENDPOINT
@api.route('/book/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)