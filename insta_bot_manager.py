# Insta_bot_manager need to launch main threed of insta_bot
# This file integrate to task manager

from insta_bot import SendMsg
import os

def _conf_check():
    file_check = os.path.exists(
                    os.path.dirname(
                        os.path.abspath(__file__)) + "/auth.txt")
    
    if not file_check:
        raise Exception("You must create/or fill the auth.txt file!")
    
    return 1


def __send__(enc_password=False, random_msg=None):
    """
        enc_password -> Bool, False(default) if you store NOT encrypted password in auth.txt
            or True in another case.
        random_msg -> str, None or str you want to send
    """
    data_check = _conf_check()
    
    if data_check == 1:
        #create the SendMsg instance
        s = SendMsg(enc_password=enc_password)
        return s.send_message(random_msg=random_msg)

    return data_check
    

if __name__ == "__main__":
    # You can change params in this calling
    result = __send__()
    print(result)