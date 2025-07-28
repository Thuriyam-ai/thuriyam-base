from datetime import datetime, timedelta, UTC
from jose import jwt

# JWT settings from your application
SECRET_KEY = "your-secret-key-here"  # Default from base.py
ALGORITHM = "HS256"

# Create JWT payload
payload = {
    "sub": "testuser",  # Username
    "scopes": [         # Available scopes from auth.py
        "me",
        "users", 
        "admin",
        "campaigns:read",
        "campaigns:write", 
        "campaigns:manage"
    ],
    "exp": datetime.now(UTC) + timedelta(minutes=30)  # 30 minutes from now
}

# Generate the JWT token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
print("Generated JWT Token:")
print(token)

# Verify the token (optional - to test decoding)
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("\nDecoded payload:")
    print(decoded)
except Exception as e:
    print(f"Error decoding token: {e}")
