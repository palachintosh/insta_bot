# Insta_bot_manager need to launch main threed of insta_bot
# This file integrate to task manager

from insta_bot import SendMsg

def __send__(user_id):
    if user_id != None:
        s = SendMsg()
        s.send_message(user_id)


if __name__ == "__main__":
    __send__(user_id="845604634")