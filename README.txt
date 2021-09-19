The insta_bot this is a bot :) which send messages to select user Instagram user


##################    Using    ##################
For start, you need to configure some files:
    1. auth.txt
    2. conf.txt


##################    auth.txt    ##################
File contains only 3 lines with auth data and Intsagram ID of user you want to send msg. Every parameter must be written from new line. Sample:


login
password
091328409238


Login - this is you "regular" IG login

Password:
You has a two password options:
    1. Write your regular password, like "mypass123@".
    2. Input encrypted password in "auth.txt" file.
        This one, is not your "original" password like "myPass123@". This is a string encoded by IG. You cat get it from any "Log in" request to Insta in browser console.
        Unfortunatly, I don't know this encoding yet.

For this case i add enc_password parameter in "Login" class.
If you would using pasword without encryption ("myPass123@") than leave parameter "enc_password" in False (default value).
Another case - using enc_password=True with your encrypted password in auth.txt.

In auth.txt it looks like this:
#PWD_INSTAGRAM_BROWSER:<E>:<T>:pass
Here - <E> param will be replaced on "10" if you use a enccrypted password or on "0" for password in text view.
<T> - param just replaced on UNIX time in both cases.


User ID this is the user id in Instagram. Smth like the string of nums: "443444040000".
Another way - you can set the user ID in "insta_bot_manager.py" like parameter of __send__().


##################    conf.txt   ##################

Insta_bot sending the random messages from "conf.txt".
Possible to configure it while calling __send__() (insta_bot_manager.py) with random_msg parameter.

__send__(random_msg="blabla") -> app will use this param
__send__(random_msg=None) -> wil use conf.txt

If you want more random - configure "conf.txt" in "insta_bot" dir. You you don't this file - just create and fill it.

File has basic syntacsys that help MassageMaker forminng messages:

str
string
blabla

!
Workdays msg
!

@
weekend msg
@


// String of comments
//
// ! - NOT send in weekend
// @ - Send ONLY in the weekend
// 'Nothing' - send for all week


As you can see, this is a shit, but it works.



##################    log.log    ##################

After first launch will create the log.txt in app directory.


##################    insta_bot_manager.py ##################

Something like launcher of main file "insta_bot.py".
Can set user_id and random_msg in this.



##################    Integrate with "Cron"   ##################

If you want sending messages regularly, you can crate task in cron.
Only you need is add a new crontab string:
$ crontab -e

0 0 * * * python3 /path/to/file/insta_bot_manager.py //This will sending messages every day at 0:00


If you read it because this script is DOESEN'T work - send me message in @palachintosh_blog on IG.









