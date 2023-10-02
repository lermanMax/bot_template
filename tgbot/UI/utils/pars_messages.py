from __future__ import annotations
from typing import List, Dict, NamedTuple, Optional
from loguru import logger
from pydantic import BaseModel

from aiogram.types import Message

class Poll(BaseModel):
    question: str
    options: list
    is_anonymous: bool
    allows_multiple_answers: bool

# class for post message for telegram bot
class Post(BaseModel):
    title: Optional[str]
    text: Optional[str]
    photos: list
    video: list
    doc: list
    poll: Optional[Poll]


async def parse_message(message: Message, album: List[Message]) -> Post:
    """parse telegram message and return Post object

    Args:
        message (Message): message for parsing
        title (str, optional): bold title for post. Defaults to None.

    Returns:
        Post: _description_
    """
    logger.info(f"Start to parsing")

    if message.text:
        text = message.text
    elif message.caption:
        text = message.caption
    else:
        text = ''

    photos = []
    video = []
    doc = []
    poll = None

    if not album:
        album = [message,]

    for msg in album:
        if msg.photo:
            photos.append(msg.photo[-1].file_id)

        if msg.video:
            video.append(msg.video.file_id)

        if msg.document:
            doc.append(msg.document.file_id)
        
        if msg.poll:
            poll = Poll(
                question = msg.poll.question,
                options = [option['text'] for option in msg.poll.options],
                is_anonymous = msg.poll.is_anonymous,
                allows_multiple_answers = msg.poll.allows_multiple_answers
            )

    return Post(
        title='',
        text=text,
        photos=photos,
        video=video,
        doc=doc,
        poll=poll,)