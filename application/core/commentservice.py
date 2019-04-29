from application import db
from application.core.models import Comment, User


def add_comment(user_id: int, text):
    """
    Add a new comment from user
    :param user_id: User's Telegram-ID
    :param text: comment's text
    :return: void
    """
    user = User.query.get(user_id)
    comment = Comment(text=text)
    user.comments.append(comment)
    db.session.add(comment)
    db.session.commit()
