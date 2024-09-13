from flask import Blueprint, jsonify,request
import base64
from models.models import User,BookDetails, BookCategory,BookRequests,BookRating,db

from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta,date

from flask_caching import Cache
from cache import cache
studenthome_bp = Blueprint('studenthome', __name__, )

@studenthome_bp.route('/api/get_book_details')
@cache.cached(timeout=40)
def get_book_details():
    
    books = BookDetails.query.all()
    
    return jsonify([book.to_dict() for book in books])

@studenthome_bp.route('/api/get_book_categories')
@cache.cached(timeout=40)
def get_book_categories():
    
    categories = BookCategory.query.all()
    return jsonify([category.to_dict() for category in categories])

@studenthome_bp.route('/api/get_book_requests')
@jwt_required()
def get_book_requests():
    # Get the username from the JWT token
    username = get_jwt_identity()
    
    # Join BookRequests and BookDetails tables and filter by username
    query = db.session.query(BookRequests, BookDetails).join(BookDetails, BookRequests.book_id == BookDetails.id).filter(BookRequests.username == username).all()

    # Extract necessary information from the query results
    book_requests_data = []
    for book_request, book_detail in query:
        book_request_data = {
            'request_id': book_request.request_id,
            'username': book_request.username,
            'book_id': book_request.book_id,
            'status': book_request.status,
            'request_date': book_request.request_date.strftime('%Y-%m-%d'),
            'issue_date': book_request.issue_date.strftime('%Y-%m-%d') if book_request.issue_date else None,
            'return_date': book_request.return_date.strftime('%Y-%m-%d') if book_request.return_date else None,
            'category': book_detail.category,
            'title': book_detail.title,
            'author': book_detail.author
        }
        book_requests_data.append(book_request_data)

    return jsonify(book_requests_data)


@studenthome_bp.route('/api/get_approved_books')
@cache.cached(timeout=40)
@jwt_required()
def get_approved_books():
    # Get the current user's username from the JWT token
    username = get_jwt_identity()
    print(username)

    # Join BookRequests with BookDetails to fetch book details for approved requests
    approved_books = db.session.query(BookRequests, BookDetails).\
        join(BookDetails, BookRequests.book_id == BookDetails.id).\
        filter(BookRequests.status == 'approved', BookRequests.username == username).all()
    
    # Extract required book details from the result
    books_data = [{
        'book_id': book[0].book_id,
        'title': book[1].title,
        'author': book[1].author,
        'category': book[1].category,
        'issue_date': book[0].issue_date.strftime('%Y-%m-%d'), # Include issue_date in the response
        'return_date': book[0].return_date.strftime('%Y-%m-%d'),
        'request_date': book[0].request_date.strftime('%Y-%m-%d'),
        'request_id': book[0].request_id
    } for book in approved_books]
    
    return jsonify(books_data)





@studenthome_bp.route('/api/get_book_pdf/<int:book_id>')
@cache.cached(timeout=40)
def get_book_pdf(book_id):
    book = BookDetails.query.get(book_id)
    if book:
        pdfdata = book.get_pdf_data()
        
        return pdfdata
    else:
        return jsonify({'error': 'Book not found'}), 404
    
    
    

@studenthome_bp.route('/api/post_review', methods=['POST'])
@jwt_required()
def post_review():
    data = request.json

    book_id = data.get('book_id')
    rating = data.get('rating')
    review_text = data.get('review')

    username = get_jwt_identity()  # Get the username from the JWT token

    if not (book_id and username):
        return jsonify({'error': 'Missing required data (book_id or username)'}), 400

    # Check if a review already exists for the given book and user
    existing_review = BookRating.query.filter_by(book_id=book_id, username=username).first()

    if existing_review:
        # Update the existing review
        existing_review.rating = rating
        existing_review.review = review_text
        db.session.commit()
        return jsonify({'message': 'Review updated successfully'})
    else:
        # Create a new review
        new_review = BookRating(book_id=book_id, username=username, rating=rating, review=review_text)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Review posted successfully'})

@studenthome_bp.route('/api/delete_book_request', methods=['POST'])
def delete_book_request():
    request_data = request.json
    request_id = request_data.get('request_id')

    if request_id is None:
        return jsonify({'error': 'Request ID is required'}), 400

    # Find the book request by its ID and delete it
    book_request = BookRequests.query.get(request_id)
    if book_request:
        db.session.delete(book_request)
        db.session.commit()
        return jsonify({'message': 'Book request deleted successfully'}), 200
    else:
        return jsonify({'error': 'Book request not found'}), 404
    
    



from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from flask_cors import CORS 




@studenthome_bp.route('/api/request_book', methods=['POST'])
# Requires authentication using JWT
@jwt_required()
def request_book():
    current_user = get_jwt_identity()  # Get the current user from the JWT token
    data = request.get_json()
    duration = data.get('duration')
    book_id = data.get('book_id')

    # Check if duration is provided
    existing_request = BookRequests.query.filter_by(username=current_user, book_id=book_id).first()
    if existing_request:
        return jsonify({'duplicate_request': True}), 200
    new_request = BookRequests(
        username=current_user,
        book_id=book_id,
        duration=duration,
        return_date=None,
        issue_date=None,
        
        status='pending'  # Default status
    )
  # Add the new request to the database
    try:
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message': 'Book requested successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500




@studenthome_bp.route('/readreviews/<int:book_id>')
def read_reviews(book_id):
    book_data = db.session.query(BookDetails, BookRating).\
                    join(BookRating).\
                    filter(BookDetails.id == book_id).all()

    reviews = []
    for book_detail, rating in book_data:
        reviews.append({
            'title': book_detail.title,
            'author': book_detail.author,
            'category': book_detail.category,
            'username': rating.username,
            'rating': rating.rating,
            'review': rating.review
        })
    
    return jsonify(reviews)





@studenthome_bp.route('/api/user_profile', methods=['GET'])
@jwt_required()
def user_profile():
    username = get_jwt_identity()

    # Fetch user details
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Fetch number of approved books
    num_approved_books = BookRequests.query.filter_by(username=username, status='approved').count()

    # Fetch number of pending book requests
    num_pending_requests = BookRequests.query.filter_by(username=username, status='pending').count()

    # Construct user profile data
    user_profile_data = {
        'username': user.username,
        'email': user.email,
        'num_approved_books': num_approved_books,
        'num_pending_requests': num_pending_requests
    }

    return jsonify(user_profile_data), 200
