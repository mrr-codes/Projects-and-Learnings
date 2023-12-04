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

from std_msgs.msg import Float32MultiArray

# now = datetime.datetime.now()
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)

# controller_pub = rospy.Publisher(
#     '/controller_values', Float32MultiArray, queue_size=1)
rospy.init_node('survilBot', anonymous=True)
move_msg = Twist()
click = TakePhoto()

r = rospy.Rate(5)


def handle(msg):
    chat_id = msg['chat']['id']  # Receiving the message from telegram
    command = msg['text']   # Getting text from the message

    print('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage(chat_id, str("Hi! Mechx Student"))
    elif command == '/time':
        now = datetime.datetime.now()
        bot.sendMessage(chat_id, str("Time: ") + str(now.hour) +
                        str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        now = datetime.datetime.now()
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) +
                        str("/") + str(now.month) + str("/") + str(now.year))

    elif command == '/forward':
        bot.sendMessage(chat_id, str('Moving Forward'))
        move_msg.linear.x = 0.5
        move_msg.angular.z = 0
        for i in range(10):
            pub.publish(move_msg)
            r.sleep()

    elif command == '/backward':
        bot.sendMessage(chat_id, str('Moving Backward'))
        move_msg.linear.x = -0.5
        move_msg.angular.z = 0
        for i in range(10):
            pub.publish(move_msg)
            r.sleep()
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
        now = datetime.datetime.now()
        bot.sendPhoto(chat_id,  open(
            '/home/manasrr/catkin_ws_lab/src/survil_bot_pkg/turtleBot_photos/work_photo.jpg', 'rb'), caption='Photo @' + str(now.hour) +
            str(":") + str(now.minute) + str(":") + str(now.second)+'_'+str(now.day) +
            str("/") + str(now.month) + str("/") + str(now.year))

    elif command == '/help':
        bot.sendMessage(chat_id, str(
            "You can do the following commands:\n /forward -to move forward by 1m\n /backward -to move forward by 1m\n /left -to turn left\n /right -to turn right\n /photo -to click and send a picture\n /date -for current date\n /time -for current time"))

    # elif 'goto' in command:
    #     extract = command.split(' ')
    #     ka = float(extract[1])
    #     kx = float(extract[2])
    #     x = float(extract[3])
    #     y = float(extract[4])
    #     controller_values = [ka, kx, x, y]
    #     controller_pub.publish(controller_values)

        # print("extracted part is ", extract)
        # bot.sendMessage(chat_id, str('Moving to set location'))

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
