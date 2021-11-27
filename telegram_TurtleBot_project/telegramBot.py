#!/usr/bin/env python3

import datetime  # Importing the datetime library
import telepot   # Importing the telepot library
# Library function to communicate with telegram bot
from telepot.loop import MessageLoop
import rospy
# Importing the time library to provide the delays in program
from time import sleep
from geometry_msgs.msg import Twist
from telegramBotCapture import TakePhoto

now = datetime.datetime.now()  # Getting date and time
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
rospy.init_node('survilBot', anonymous=True)
move_msg = Twist()
click = TakePhoto()
r = rospy.Rate(10)


def handle(msg):
    chat_id = msg['chat']['id']  # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage(chat_id, str("Hi! Mechx Student"))
    elif command == '/time':
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) +
                        str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) +
                        str("/") + str(now.month) + str("/") + str(now.year))
    elif command == '/forward':
        bot.sendMessage(chat_id, str('Moving Forward'))
        move_msg.linear.x = 0.3
        move_msg.angular.z = 0
        for i in range(5):
            pub.publish(move_msg)
            r.sleep()

    elif command == '/backward':
        bot.sendMessage(chat_id, str('Moving Backward'))
        move_msg.linear.x = -0.3
        move_msg.angular.z = 0
        pub.publish(move_msg)

    elif command == '/right':
        bot.sendMessage(chat_id, str('Turning Right'))
        move_msg.linear.x = 0
        move_msg.angular.z = -3.15
        pub.publish(move_msg)

    elif command == '/left':
        bot.sendMessage(chat_id, str('Turning Left'))
        move_msg.linear.x = 0
        move_msg.angular.z = 3.15
        pub.publish(move_msg)

    elif command == '/photo':
        bot.sendMessage(chat_id, 'Clicking a picture')
        click.take_picture('work_photo.jpg')
        bot.sendPhoto(chat_id,  open(
            '/home/manasrr/Downloads/work_photo.jpg', 'rb'))

    else:
        bot.sendMessage(chat_id, str('Sorry I did not understand the command'))


# Insert your telegram token below
bot = telepot.Bot('2130244677:AAERx3-ThfAZjnlhyKc5EgfrcbKCKjLAfx4')
print(bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print('Listening....')

while 1:
    sleep(10)
    # try:
    #     handle()
    # except rospy.ROSInterruptException:
    #     pass
