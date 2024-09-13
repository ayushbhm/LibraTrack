from flask import Blueprint, jsonify,request
import base64
from models.models import BookDetails, BookCategory,BookRequests,BookRating,db
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, timedelta
admincontrols_bp = Blueprint('admincontrols', __name__, )

from flask_cors import CORS 
CORS(admincontrols_bp, origins='http://localhost:5173', supports_credentials=True, allow_headers=[
    'Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])


@admincontrols_bp.route('/alloted_books/<int:book_id>', methods=['GET'])
def get_alloted_books(book_id):
    try:
        # Fetch allocations from the database where status is 'approved'
        allocations = db.session.query(BookRequests).filter_by(book_id=book_id, status='approved').all()
        result = [allocation.to_dict() for allocation in allocations]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@admincontrols_bp.route('/revoke_access/<int:request_id>', methods=['POST'])
def revoke_access(request_id):
    try:
        # Fetch the request
        request = db.session.query(BookRequests).get(request_id)
        if request:
            # Delete the request from the database
            db.session.delete(request)
            db.session.commit()
            return jsonify({'message': 'Access revoked successfully'}), 200
        else:
            return jsonify({'message': 'Request not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@admincontrols_bp.route('/approved_books', methods=['GET'])
def get_approved_books():
    try:
        # Query books that have at least one approved request
        approved_books = db.session.query(BookDetails).join(BookRequests).filter(BookRequests.status == 'approved').distinct().all()
        response = [book.to_dict() for book in approved_books]
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admincontrols_bp.route('/admin_approve_request', methods=['POST'])
def approve_request():
    request_id = request.json.get('request_id')
    current_date = datetime.now().date()

    # Find the request
    book_request = BookRequests.query.filter_by(request_id=request_id).first()

    if not book_request:
        return jsonify({'message': 'Request not found'}), 404

    # Calculate return date
    return_date = current_date + timedelta(days=book_request.duration)

    # Update request status and dates
    book_request.status = 'approved'
    book_request.issue_date = current_date
    book_request.return_date = return_date

    db.session.commit()

    return jsonify({'message': 'Request approved successfully'}), 200

@admincontrols_bp.route('/admin_deny_request', methods=['POST'])
def deny_request():
    request_id = request.json.get('request_id')
    

    # Find the request
    book_request = BookRequests.query.filter_by(request_id=request_id).first()
    # Update request status and dates
    book_request.status = 'rejected'

    db.session.commit()

    return jsonify({'message': 'Request approved successfully'}), 200

@admincontrols_bp.route('/admin_get_book_request_details', methods=['POST','GET'])
def admin_get_book_request_details():
    book_requests = BookRequests.query.filter_by(status='pending').all()
    
    return jsonify([book_request.to_dict() for book_request in book_requests])





@admincontrols_bp.route('/add_book', methods=['POST'])
def add_book():
    try:
        title = request.form.get('title')
        author = request.form.get('author')
        category = request.form.get('category')
        file = request.files.get('file')

        if not title or not author or not category or not file:
            return jsonify(error='Missing required fields'), 400

        if file.filename == '':
            return jsonify(error='No selected file'), 400

        if file:
            pdf_data = file.read()

            new_book = BookDetails(
                title=title,
                author=author,
                category=category,
                pdf=pdf_data
            )

            db.session.add(new_book)
            db.session.commit()

            return jsonify(message='Book added successfully', book=new_book.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

@admincontrols_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        
        return 'File received2e', 200

@admincontrols_bp.route('/api/admin_get_book_details')
def admin_get_book_details():
    books = BookDetails.query.all()
    
    return jsonify([book.to_dict() for book in books])


@admincontrols_bp.route('/api/admin_get_categories')
def admin_get_book_categories():
    categories = BookCategory.query.all()
    return jsonify([categories.to_dict() for categories in categories])

@admincontrols_bp.route('/api/admin_update_book/<int:book_id>', methods=['POST'])
def update_book(book_id):
    
    book = BookDetails.query.get_or_404(book_id)
   
   
    if 'pdf_file' not in request.files:
        return jsonify(message='No PDF file provided'), 400
    pdf_file = request.files.get('pdf_file')
    
    print(pdf_file)
    
    data = request.json
    
    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'category' in data:
        book.category = data['category']
        
    
    

    try:
        
        db.session.commit()
        return jsonify(message='Book updated successfully'), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(message=f'Failed to update book: {str(e)}'), 500



@admincontrols_bp.route('/admin_delete_book/<int:book_id>', methods=['DELETE'])
def admin_delete_book(book_id):
    book = BookDetails.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify(message='Book deleted successfully'), 200




@admincontrols_bp.route('/api/admin_dashboard', methods=['GET'])
def admin_dashboard_api():
    # Query book details along with the user it is issued to (if approved), return date, and request date
    book_details = db.session.query(
        BookDetails.title,
        BookDetails.author,
        BookDetails.category,
        BookRequests.username,
        BookRequests.return_date,
        BookRequests.request_date
    ).join(
        BookRequests, BookDetails.id == BookRequests.book_id
    ).filter(
        BookRequests.status == 'approved'
    ).all()

    # Format book details as a list of dictionaries
    formatted_book_details = []
    for detail in book_details:
        formatted_book_details.append({
            'title': detail.title,
            'author': detail.author,
            'category': detail.category,
            'issued_to': detail.username,
            'return_date': str(detail.return_date),
            'request_date': str(detail.request_date)
        })

    # Return JSON response
    return jsonify(formatted_book_details)





@admincontrols_bp.route('/api/add_book_category', methods=['POST'])

def add_book_category():
    data = request.get_json()

    if not data or 'category' not in data:
        return jsonify({'error': 'Category data missing or invalid'}), 400

    category_name = data['category']

    # Check if the category already exists
    existing_category = BookCategory.query.filter_by(category=category_name).first()
    if existing_category:
        return jsonify({'error': 'Category already exists'}), 400

    try:
        # Create a new category
        new_category = BookCategory(category=category_name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message': 'Book category added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while adding book category'}), 500
    finally:
        db.session.close()
        
        



@admincontrols_bp.route('/api//delete_book_category/<int:id>', methods=['DELETE'])

def delete_book_category(id):
    book_category = BookCategory.query.get(id)

    

    try:
        db.session.delete(book_category)
        db.session.commit()
        return jsonify({'message': 'Book category deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting book category'}), 500
    finally:
        db.session.close()
        
        
        

@admincontrols_bp.route('/api/update_book_category/<int:id>', methods=['POST'])

def update_book_category(id):
    data = request.get_json()
    print("aefdsdbg")
    if not data or 'category' not in data:
        return jsonify({'error': 'Category data missing or invalid'}), 400

    book_category = BookCategory.query.get(id)

    if not book_category:
        return jsonify({'error': 'Book category not found'}), 404

    try:
        # Update category data
        book_category.category = data['category']
        db.session.commit()
        return jsonify({'message': 'Book category updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating book category'}), 500
    finally:
        db.session.close()


@admincontrols_bp.route('/api/update_book/<int:id>', methods=['POST','GET','OPTIONS'])
def update_the_book(id):
    book = BookDetails.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    try:
        # Update text fields
        book.title = request.form['title']
        book.author = request.form['author']
        book.category = request.form['category']

        # Commit changes
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating the book'}), 200
    finally:
        db.session.close()




@admincontrols_bp.route('/api/get_books_without_pdf', methods=['GET'])
def get_books_without_pdf():
    try:
        # Fetch all book records from the database
        books = BookDetails.query.all()
        
        # Prepare a list of book details excluding the PDF field
        books_list = [
            {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'category': book.category
            }
            for book in books
        ]
        
        # Return the book details as JSON response
        return jsonify(books_list), 200
    except Exception as e:
        # Log the exception and return an error response
        print(f"Error fetching books: {e}")
        return jsonify({"error": "Failed to fetch books"}), 500