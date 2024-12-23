from passlib.context import CryptContext

pwd_txt = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_txt.hash(password)


def verify_password(
        plain_password: str,
        hashed_password: str,

) -> bool:
    return pwd_txt.verify(plain_password, hashed_password)
