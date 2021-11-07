# -*- coding: utf-8 -*-
from utils.orm.db import BaseModel, Base
from sqlalchemy import BigInteger, Column, Boolean, ForeignKey, String, DateTime, select
from sqlalchemy.orm import relationship, backref


class Message(BaseModel):
    __tablename__ = 'messages'

    content_id = Column(BigInteger(), ForeignKey('message_contents.id'), nullable=False)
    receiver_id = Column(BigInteger(), ForeignKey('users.id'))  # if message public, receiver_id is null
    room_id = Column(BigInteger(), ForeignKey('message_rooms.id'))
    read = Column(Boolean())


class MessageContent(BaseModel):
    __tablename__ = 'message_contents'

    content = Column(String(), nullable=False)


class MessageRoomUser(Base):
    __tablename__ = "message_room_users"

    user_id = Column(BigInteger(), ForeignKey("users.id"), primary_key=True)
    room_id = Column(BigInteger(), ForeignKey("message_rooms.id"), primary_key=True)


class MessageRoom(BaseModel):
    __tablename__ = 'message_rooms'

    name = Column(String(), nullable=False)
    description = Column(String())
    code = Column(String(), nullable=False)
    user_ids = relationship("utils.orm.db.User", secondary='message_room_users', backref="room_ids")
