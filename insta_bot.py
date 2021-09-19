"""
    This is the main file of insta_bot.
    Body cotains 3 standard classes: Login, SendMsg, MessageMaker
    for login (for auth), send messages to selected user (by his IG ID) 
    and MessageMaker (for forming message from conf file "conf.txt")
    You can write your own conf.txt with another messages.
"""
from datetime import datetime

import re
import requests
import random
import uuid


class Login:
    """
        Login try to log in your insta account if it possible.
        Gets username and password.
    """
    status: int

    def __init__(self, enc_password=False):
        # Try to construct username and passwd
        with open("auth.txt", "r") as f:
            l = f.read().split("\n")
            username = l[0]
            passwd = l[1]
            self.user_id = l[2]

        if passwd is not None:
            if not enc_password:
                passwd = passwd.replace('<E>', "0")
            else:
                passwd = passwd.replace('<E>', "10")
            
            passwd = passwd.replace('<T>', str(int(datetime.now().timestamp())))
        
        else: raise Exception("Password not found in auth.txt!")

        self.auth = {
            "username": username,
            "enc_password": passwd, 
        }
        self.login_url = "https://www.instagram.com/accounts/login/"
        self.login_url_ajax = self.login_url + "ajax/"

        self.session = None

    def response_parse(self, response):
        if response is not None:
            token = re.search('(csrf_token":")+(?P<value>[A-Za-z0-9]*)', response)

            token_value = token.groupdict() 
            if token_value is not None:
                return {"success": "ok", "value": token_value.get("value")}      

            return {"error": "Unable to extrack token from response!"}


    def _get_token(self):
        # Make a GET request for getting csrf token and cookie
        # Create session
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 9; SM-A102U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Instagram 155.0.0.37.107 Android (28/9; 320dpi; 720x1468; samsung; SM-A102U; a10e; exynos7885; en_US; 239490550)"

        get_token = self.session.get(self.login_url)

        # set a own user-agent

        # Check response and return token
        if get_token.status_code == 200:
            self.status = 200
            headers = {}

            # If Instagram returned cookies 
            if get_token.cookies.get("csrftoken") is not None:
                headers["x-csrftoken"] = get_token.cookies["csrftoken"]
            
            # If doesn't - try to find csrftoken in response body
            else:
                csrf_token = self.response_parse(get_token.text) 
                
                if csrf_token.get("success") != None:
                    headers["x-csrftoken"] = csrf_token.get("value")

                if csrf_token.get("error"):
                    return csrf_token

            # Return headers and status
            return {
                'success': 'ok',
                'headers': headers,
                }
            
        # Return error if smth goes wrong with response or token
        return {'error': 'Error while getting response!'}


    def login(self):
        """
            Try to log in Insta account with username and passwd.
            Current session wrote in "self.session" var and available
            for all cycle's live.
        """
        # Login attepmpt
        session_data = self._get_token()

        if session_data.get('success') == 'ok':
            headers = session_data.get("headers")

            # Try to log in
            log_in = self.session.post(self.login_url_ajax, data=self.auth, headers=headers)

            #Checking response
            self.status = log_in.status_code

            return {'success': 'ok', 'response': log_in.content}


        # If token wasn't
        return {'error': session_data.get('error')}


class MessageMaker:
    """
        This class need to forming messg from "conf.txt" file.
        Choice in base on selecting random sthing from conf.txt.
    """
    def __init__(self):
        with open("conf.txt", "r") as get_f:
            self.get_f = get_f.read().split('\n')


    def array_sort(self, array, symbol):
        new_array = []
        counter = 0

        for string in array:
            if counter > 0:
                if string == symbol:
                    counter = 0
                continue

            if string == symbol:
                counter += 1

            if string != symbol and len(string) > 2 and string[0] != "/":
                new_array.append(string)

        return new_array
            
          
    def almost_random_choice(self):
        # Try to select random phrase from whole conf file
        # get_random_str = random.choice(self.get_f)

        day = datetime.today().weekday()

        if day > 4:
            get_phrase = self.array_sort(array=self.get_f, symbol="!")
            get_random_str = random.choice(get_phrase)
        
        if day < 5:
            get_phrase = self.array_sort(array=self.get_f, symbol="@")
            get_random_str = random.choice(get_phrase)
        
        return get_random_str


    def select_str(self):
        get_random_str = self.almost_random_choice()

        if get_random_str != '' and get_random_str != None:
            return get_random_str
        
        return self.select_str()


class SendMsg(Login, MessageMaker):
    """
        Send message was forming by MessageMaker.
        For log in use a Login class.
    """
    def __init__(self, enc_password=False):
        super().__init__(enc_password=enc_password)
        MessageMaker.__init__(self)


    def _log(self, *args, **kwargs):
        string = str(datetime.now())

        if args:
            for i in args:
                string = string + ' ' + str(i)
        
        if kwargs:
            for key, value in kwargs:
                string = string + ' ' + str(value)

        with open("log.log", "a") as f:
            print(string, file=f)


    def send_message(self, random_msg=None):

        #Login
        log_in = self.login()

        if log_in.get("success") is not None:
            send_mess_to_url = "https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
            uuid_v4 = uuid.uuid4()

            if random_msg is None:
                message = self.select_str()
            else:
                message = str(random_msg)

            encoded_msg = message.encode("utf-8")
            body = 'text={}&_uuid=&_csrftoken={}&recipient_users="[["{}"]]"&action=send_item&thread_ids=["0"]&client_context={}'.format(encoded_msg.decode("latin-1"), self.session.cookies["csrftoken"], self.user_id, uuid_v4)

            # Setting headers
            headers = self.session.headers
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["x-csrftoken"] = self.session.cookies["csrftoken"]
            headers["X-IG-App-ID"] = "936619743392459"
            
            # Finaly, send it!
            send_m = self.session.post(send_mess_to_url, data=body, headers=headers)
            self.status = send_m.status_code

            #Loging this all
            self._log(self.status, "msg_status: {}".format(send_m.status_code), encoded_msg.decode("utf-8"))

            return send_m.status_code


