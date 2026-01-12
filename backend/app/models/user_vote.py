from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from app.core.database import Base

class UserVote(Base):
    __tablename__ = "user_votes"

    id = Column(Integer, primary_key=True, index=True)
    session_code = Column(String, index=True)
    queue_id = Column(Integer, ForeignKey("queue.id"))
    user_id = Column(String)
    vote = Column(Integer)  # 1 for upvote, -1 for downvote

    __table_args__ = (UniqueConstraint("queue_id", "user_id", name="unique_user_vote"),)