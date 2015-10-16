__module_name__ = "blargbot"
__module_version__ = "1.1.5"
__module_description__ = "Blargcat bot."

import hexchat
from datetime import datetime
import os

try_base = False
dir = hexchat.get_info("configdir") + "/addons/blargbot/"

start_time = datetime.now()
eat_faces = False
authed_user = None
pass_dir = hexchat.get_info("configdir") + "/addons/blargbot-password.txt"
if not os.path.isfile(pass_dir):
    f_pass = open(pass_dir, 'a')
    f_pass.write("password")
    f_pass.close()
f_pass = open(pass_dir, 'r')
first = True
for line in f_pass:
  if first:
    password = line.replace('\n', '')
f_pass.close()
channel = "#hysteriaunleashed"





def say(message):
    hexchat.command("say " + message)

def on_mention(word, word_eol, userdata):
    if "thanks blargcat" in word[1].lower() or "thanks, blargcat" in word[1].lower() or "thank you blargcat" in word[1].lower() or "thank you, blargcat" in word[1].lower():
      say("No problem.")
    elif eat_faces:
        say("\00304I will eat your fucking face, " + hexchat.strip(word[0], len(word[0]), 3) + ".")
    return hexchat.EAT_NONE


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
    s = time_elapsed.total_seconds()
    days, remainderD = divmod(s, 3600 * 24)
    hours, remainderH = divmod(remainderD, 3600)
    minutes, seconds = divmod(remainderH, 60)
    time_string = '%s days %s hours %s minutes %s seconds.' % (days, hours, minutes, seconds)
    say("Catter uptime: " + time_string)


def mail_send(word):
    sender = word[0]
    buffer_word = word[1]
    buffer_word = buffer_word.replace("mail send ", "", 1)
    index = buffer_word.index(" ")
    receiver = buffer_word[:index]
    buffer_word = buffer_word.replace(receiver + " ", "", 1)
    global dir
    f = open(dir + receiver.lower() + ".txt", 'a')
    sender = hexchat.strip(sender, len(sender), 3)
    timestamp = datetime.strftime(datetime.now(), '[%m/%d %H:%M] ')
    f.write(timestamp + sender + "> " + buffer_word + "\n")
    f.close()
    say("Message queued: '" + buffer_word + "' from " + sender + " at " + timestamp + ".")


def mail_read(word):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    global dir
    if os.path.isfile(dir + receiver.lower() + ".txt"):
      f = open(dir + receiver.lower() + ".txt", 'r')
      if os.path.getsize(dir + receiver.lower() + ".txt") > 0:
          say("You received the following messages:")
          for line in f:
              line = line.replace('\n', "")
              say(line)
          say("To delete your messages, type '!mail delete'")
      else:
          say("You have no messages.")
    else:
      say("You have no messages.")

def mail_delete(word):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    say("Deleting all of " + receiver.lower() + "'s messages")
    global dir
    if os.path.isfile(dir + receiver.lower() + ".txt"):
      f = open(dir + receiver.lower() + ".txt", 'r+')
      f.truncate()
      f.close()


def mail(word):
    if word[1] == "mail help" or word[1] == "mail":
        say("Mail commands: read, send, delete, help")
    elif word[1].startswith("mail send "):
        mail_send(word)
    elif word[1] == "mail read":
        mail_read(word)
    elif word[1] == "mail delete":
        mail_delete(word)
    else:
        say("Unknown command. Too many or too little parameters.")


def base_commands(word, word_eol, userdata):
    if word[1] == "help":
        say("Valid commands: help, currenttime, eat, time, uptime, version, mail")
    elif word[1] == "time":
        say("blargcat was started at " + datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S'))
    elif word[1] == "currenttime":
        say("The current time for blargcat is " + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    elif word[1] == "uptime":
        get_uptime(word)
    elif word[1] == "eat":
        eat()
    # elif word[1] == ".tps":
    #    say("TPS:\0033 19.97")
    # elif word[1] == ".list":
    #    say("\00312Online (2/20): \0034[Admin] \00315blargcat\0031, \0039[Member] \00315FacePolice")
    elif word[1] == "version":
        say("blargcat is running \0039" + __module_name__ + "\0031 version\0039 " + __module_version__)
    elif word[1].startswith("mail"):
        mail(word)
    elif word[1] == "douptime":
        say(".uptime")


def pm_commands(word, word_eol, userdata):
    global authed_user
    global password
    global channel
    if word[1] == "auth":
        if authed_user == None:
            say("There is no authed user")
        else:
            say("Currently authed user is " + authed_user)
    elif word[1].startswith("auth "):
        if word[1] == "auth " + password:
            authed_user = word[0]
            say("Login successful. " + authed_user + " is now authed.")
        else:
            say("Invalid password. Try again, or do '.auth' to see who is currently authed.")
    elif word[1].startswith("say "):
        if word[0] == authed_user:
            hexchat.command("doat " + channel + " say " + word[1][5:])
        else:
            say("I'm sorry, " + word[
                0] + ", but you have no permissions to do that. Try logging in with .auth <password>")
    elif word[1].startswith("channel "):
        if word[0] == authed_user:
            channel = word[1][9:]
            say("Channel set to " + channel)
        else:
            say("I'm sorry, " + word[
                0] + ", but you have no permissions to do that. Try logging in with .auth <password>")
    elif word[1] == "channel":
        say("Currently selected channel is " + channel)
    elif word[1] == "eat":
        eat()
    elif word[1] == "iseat":
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
    if os.path.isfile(dir + receiver.lower() + ".txt"):
     if os.path.getsize(dir + receiver.lower() + ".txt") > 0:
        say("Welcome back, " + receiver + ". You have unread messages. Type '!mail read' to read them.")
     else:
        say("Welcome back, " + receiver + ".")
    else:
      f = open(dir + receiver.lower() + ".txt", 'a')
      f.close()
      say("Welcome, " + receiver + ". I hope you enjoy your stay.")
    return hexchat.EAT_NONE


def on_command(word, word_eol, userdata):
    check = hexchat.strip(word[0], len(word[0]), 3).lower()
    if check == "hu_infinity" or check == "blockrim_realms" or check == "bogus_server":
      if '>' in word[1]:
        index = word[1].index('>') + 2
        word[1] = word[1][index:]
    if word[1].startswith(".") or word[1].startswith("!"):
      if word[1].startswith("."):
        word[1] = word[1].replace('.', '', 1)
      else:
        word[1] = word[1].replace('!', '', 1)
      base_commands(word, word_eol, userdata)
    return hexchat.EAT_NONE


def on_pm(word, word_eol, userdata):
    if word[1].startswith(".") or word[1].startswith("!"):
      if word[1].startswith("."):
        word[1] = word[1].replace('.', '', 1)
      else:
        word[1] = word[1].replace('!', '', 1)
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
