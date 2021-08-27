"""
    This is the main file of insta_bot.
    Body cotains 3 standard classes: Login, SendMsg, MessageMaker
    for login (for auth), send messages to selected user (by his IG ID) 
    and MessageMaker (for forming message from conf file "conf.txt")
    You can write your own conf.txt with another messages.
"""

import os
import requests
import datetime
from datetime import datetime
import random
import uuid


class Login:
    """
        Login try to log in your insta account if it possible.
        Gets username and password.
    """
    status: int

    def __init__(self, username=None, passwd=None):
        # Try to construct username and passwd
        if username == None and passwd == None:
            with open("auth.txt", "r") as f:
                l = f.read().split("\n")
                username = l[0]
                passwd = l[1]

        self.auth = {
            "username": username,
            "enc_password": passwd, 
        }
        self.login_url = "https://www.instagram.com/accounts/login/"
        self.login_url_ajax = self.login_url + "ajax/"

        self.session = None

    def _get_token(self):
        # set a own user-agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36",
        }
        
        # Make a GET request for getting csrf token and cookie
        # Create session
        self.session = requests.Session()
        get_token = self.session.get(self.login_url, headers=headers)

        # Check response and return token
        if get_token.status_code == 200:
            self.status = 200
            headers["x-csrftoken"] = get_token.cookies["csrftoken"]

            return {
                'success': 'ok',
                'headers': headers,
                }

        self.status = 400

        # Return error if with response or token smth wrong
        return {'error': 'Unable to extract token from response!'}


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
            if log_in.status_code == 200:
                self.status = 200

                return {'success': 'ok', 'response': log_in.content}


        # If token wasn't
        return {'error': session_data.get('error')}


class MessageMaker:
    """
        This class need to forming messg from "conf.txt" file.
        Choice in base on selecting random sthing from conf.txt.
    """
    def __init__(self):
        with open("conf.txt", "r", encoding="latin-1") as get_f:
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

        day = datetime.datetime.today().weekday()

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
    def __init__(self):
        super().__init__()
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


    def send_message(self, user_id):
        log_in = self.login()

        if log_in.get("success") is not None:
            send_mess_to_url = "https://i.instagram.com/api/v1/direct_v2/threads/broadcast/text/"
            uuid_v4 = uuid.uuid4()
            message = self.select_str()
            body = 'text={}&_uuid=&_csrftoken={}&recipient_users="[["{}"]]"&action=send_item&thread_ids=["0"]&client_context={}'.format(message, self.session.cookies["csrftoken"], user_id, uuid_v4)

            headers = self.session.headers
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            headers["User-Agent"] = "Instagram 169.1.0.23.115 Android (22/5.1.1; 320dpi; 720x1280; samsung; SM-J320H; j3x3g; sc8830; ru_RU)"
            headers["x-csrftoken"] = self.session.cookies["csrftoken"]
            headers["X-IG-App-ID"] = "936619743392459"

            # Finaly, send it!
            send_m = self.session.post(send_mess_to_url, data=body, headers=headers)

            #Loging this all
            self._log(self.status, "msg_status: {}".format(send_m.status_code), message)

            return send_m.status_code


