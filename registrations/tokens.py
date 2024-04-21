import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'your_secret_key'

def create_token(user):
    """ Create a JWT token that stores this user's ID and has an expiry date set to 1 day. """
    payload = {
        'user_id': str(user.id),
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def get_user_from_token(token):
    """ Decode the JWT token to get the user ID. """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
def delete_token(user):
    """ Delete the token for this user. """
    # Your implementation here
    user.token = None
    user.save()
    return
