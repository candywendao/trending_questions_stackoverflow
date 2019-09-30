from flaskr import db
from sqlalchemy.dialects.postgresql import ARRAY


class Post(db.Model):
    __tablename__ = "test_stackoverflow_v5"
    _PostId = db.Column(db.BigInteger, primary_key=True)
    _Title = db.Column(db.String(200))
    _Body = db.Column(db.String(200))
    num_favorites_7d = db.Column(db.BigInteger)
    num_favorites_14d = db.Column(db.BigInteger)
    num_favorites_28d = db.Column(db.BigInteger)
    num_comments_7d = db.Column(db.BigInteger)
    num_comments_14d = db.Column(db.BigInteger)
    num_comments_28d = db.Column(db.BigInteger)
    total_comments = db.Column(db.BigInteger)
    total_votes = db.Column(db.BigInteger)
    tags = db.Column(ARRAY(db.String(50)))
