__module_name__ = "blargbot"
__module_version__ = "1.1.5"
__module_description__ = "Blargcat bot."

import hexchat
from datetime import datetime
import os

try_base = False
dir = hexchat.get_info("configdir") + "\\addons\\blargbot\\"

start_time = datetime.now()
eat_faces = True
authed_user = None
pass_dir = hexchat.get_info("configdir") + "\\addons\\blargbot-password.txt"
if not os.path.isfile(pass_dir):
    f_pass = open(pass_dir, 'a')
    f_pass.write("password")
    f_pass.close()
f_pass = open(pass_dir, 'r')
password = f_pass.read()
f_pass.close()
channel = "#hysteriaunleashed"


def on_mention(word, word_eol, userdata):
    if eat_faces:
        hexchat.command("say \00304I will eat your fucking face.")
    return hexchat.EAT_NONE


def say(message):
    hexchat.command("say " + message)


def eat():
    global eat_faces
    if eat_faces:
        eat_faces = False
        say("I'm no longer hungry.")
    else:
        eat_faces = True
        say("I'm suddenly really hungry.")


def get_uptime(word):
    time_elapsed = datetime.now() - start_time
    s = time_elapsed.seconds
    days, remainderD = divmod(s, 3600 * 24)
    hours, remainderH = divmod(remainderD, 3600)
    minutes, seconds = divmod(remainderH, 60)
    time_string = '%s days %s hours %s minutes %s seconds.' % (days, hours, minutes, seconds)
    say("Catter uptime: " + time_string)


def mail_send(word):
    sender = word[0]
    buffer_word = word[1]
    buffer_word = buffer_word.replace(".mail send ", "", 1)
    index = buffer_word.index(" ")
    receiver = buffer_word[:index]
    buffer_word = buffer_word.replace(receiver + " ", "", 1)
    global dir
    f = open(dir + receiver + ".txt", 'a')
    sender = hexchat.strip(sender, len(sender), 3)
    timestamp = datetime.strftime(datetime.now(), '[%y-%m-%d %H:%M:%S] ')
    f.write(timestamp + sender + "> " + buffer_word + "\n")
    f.close()
    say("Message queued: '" + buffer_word + "' from " + sender + " at " + timestamp + ".")


def mail_read(word):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    global dir
    f = open(dir + receiver + ".txt", 'r')
    if os.path.getsize(dir + receiver + ".txt") > 0:
        say("You received the following messages:")
        for line in f:
            line = line.replace('\n', "")
            say(line)
        say("To delete your messages, type '.mail delete'")
    else:
        say("You have no messages.")


def mail_delete(word):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    say("Deleting all of " + receiver + "'s messages")
    global dir
    f = open(dir + receiver + ".txt", 'r+')
    f.truncate()
    f.close()


def mail(word):
    if word[1] == ".mail help" or word[1] == ".mail":
        say("Mail commands: read, send, delete, help")
    elif word[1].startswith(".mail send "):
        mail_send(word)
    elif word[1] == ".mail read":
        mail_read(word)
    elif word[1] == ".mail delete":
        mail_delete(word)
    else:
        say("Unknown command. Too many or too little parameters.")


def base_commands(word, word_eol, userdata):
    if word[1] == ".help":
        say("Valid commands: help, currenttime, eat, time, uptime, version, mail")
    elif word[1] == ".time":
        say("blargcat was started at " + datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S'))
    elif word[1] == ".currenttime":
        say("The current time for blargcat is " + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    elif word[1] == ".uptime":
        get_uptime(word)
    elif word[1] == ".eat":
        eat()
    # elif word[1] == ".tps":
    #    say("TPS:\0033 19.97")
    # elif word[1] == ".list":
    #    say("\00312Online (2/20): \0034[Admin] \00315blargcat\0031, \0039[Member] \00315FacePolice")
    elif word[1] == ".version":
        say("blargcat is running \0039" + __module_name__ + "\0031 version\0039 " + __module_version__)
    elif word[1].startswith(".mail"):
        mail(word)


def pm_commands(word, word_eol, userdata):
    global authed_user
    global password
    global channel
    if word[1] == ".auth":
        if authed_user == None:
            say("There is no authed user")
        else:
            say("Currently authed user is " + authed_user)
    elif word[1].startswith(".auth "):
        if word[1] == ".auth " + password:
            authed_user = word[0]
            say("Login successful. " + authed_user + " is now authed.")
        else:
            say("Invalid password. Try again, or do '.auth' to see who is currently authed.")
    elif word[1].startswith(".say "):
        if word[0] == authed_user:
            hexchat.command("doat " + channel + " say " + word[1][5:])
        else:
            say("I'm sorry, " + word[
                0] + ", but you have no permissions to do that. Try logging in with .auth <password>")
    elif word[1].startswith(".channel "):
        if word[0] == authed_user:
            channel = word[1][9:]
            say("Channel set to " + channel)
        else:
            say("I'm sorry, " + word[
                0] + ", but you have no permissions to do that. Try logging in with .auth <password>")
    elif word[1] == ".channel":
        say("Currently selected channel is " + channel)
    elif word[1] == ".eat":
        eat()
    elif word[1] == ".iseat":
        global eat_faces
        if eat_faces:
            say("I want to eat faces.")
        else:
            say("I do not want to eat faces.")
    else:
        global try_base
        try_base = True


def on_join(word, word_eol, userdata):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    if os.path.getsize(dir + receiver + ".txt") > 0:
        say("Welcome back, " + receiver + ". You have unread messages. Type '.mail read' to read them.")
    return hexchat.EAT_NONE


def on_command(word, word_eol, userdata):
    base_commands(word, word_eol, userdata)
    return hexchat.EAT_NONE


def on_pm(word, word_eol, userdata):
    pm_commands(word, word_eol, userdata)
    global try_base
    if try_base:
        base_commands(word, word_eol, userdata)
    return hexchat.EAT_NONE


if not os.path.exists(dir):
    os.makedirs(dir)

hexchat.hook_print("Channel Msg Hilight", on_mention)
hexchat.hook_print("Channel Message", on_command)
hexchat.hook_print("Private Message to Dialog", on_pm)
hexchat.hook_print("Private Message", on_pm)
hexchat.hook_print("Join", on_join)

print("Script " + __module_name__ + " version " + __module_version__ + " successfully loaded")
