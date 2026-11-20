import pytest
from app.infrastructure.security import hash_password, verify_password, create_access_token, decode_token

class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        password = "SecurePass123!"
        hashed = hash_password(password)
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_verify_password_correct(self):
        password = "SecurePass123!"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        password = "SecurePass123!"
        wrong_password = "WrongPassword123!"
        hashed = hash_password(password)
        assert verify_password(wrong_password, hashed) is False

    def test_hash_password_truncates_long_password(self):
        long_password = "A" * 100
        hashed = hash_password(long_password)
        assert isinstance(hashed, str)

class TestJWT:
    def test_create_and_decode_access_token(self):
        data = {"sub": "user-id-123", "email": "test@example.com", "role": "CLIENT"}
        token = create_access_token(data)
        decoded = decode_token(token)
        
        assert decoded is not None
        assert decoded["sub"] == "user-id-123"
        assert decoded["email"] == "test@example.com"
        assert decoded["role"] == "CLIENT"

    def test_decode_invalid_token(self):
        invalid_token = "invalid.token.here"
        decoded = decode_token(invalid_token)
        assert decoded is None