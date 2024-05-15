from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(username="jeff", password="123", email="test@test.br")
    session.add(new_user)

    user = session.scalar(select(User).where(User.username == "jeff"))

    assert user.username == "jeff"
