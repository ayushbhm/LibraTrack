from models.models import User,db
from datetime import datetime, timedelta


def fetch_inactive_user_emails():
    """
    Fetch emails of users who have not logged in today.
    :return: List of email addresses.
    """
    # Import the SQLAlchemy session and User model
    
   

    # Get today's date and the date of yesterday
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    # Query the database to fetch inactive users
    with db.session() as session:
        result = session.execute(
            db.select(User.email).filter(
                (User.last_login < yesterday) | (User.last_login.is_(None))
            )
        )
        # Extract emails from the result
        email_list = [row[0] for row in result]
        print(email_list)

    return email_list