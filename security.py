import bcrypt

def get_password_hash(password):
    """Hash a password using bcrypt."""
    # Ensure the password is encoded to bytes, then hash it
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')  # Store as string in the database

def verify_password(plain_password, hashed_password):
    """Verify a plain password against the hashed password using bcrypt."""
    # Ensure both password and hashed password are bytes, then verify them
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
