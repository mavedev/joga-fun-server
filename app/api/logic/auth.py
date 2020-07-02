from flask_security import login_user

from app.model import User


def can_administrate(username: str, password: str) -> bool:
    admin: User = User.query().filter(User.username == username).first()
    if not admin or not admin.check_password(password):
        return False
    else:
        login_user(admin, remember=True)
        return True
