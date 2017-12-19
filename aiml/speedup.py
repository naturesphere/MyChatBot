import aiml
import os

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
# if os.path.isfile("bot_brain.brn"):
#     kernel.bootstrap(brainFile="bot_brain.brn")
# else:
#     kernel.bootstrap(learnFiles="std-startup.xml",commands="load aiml b")
#     kernel.saveBrain("bot_brain.brn")

sessionId = 12345
# sessionData = kernel.getSessionData(sessionId)
# kernel.setPredicate("dog","Brandy",sessionId)
# clients_dogs_name = kernel.getPredicate("dog",sessionId)
# kernel.setBotPredicate("hometown","127.0.0.1")
# bot_hometown = kernel.getBotPredicate("hometown")
# kernel now ready for use
while True:
    # print(kernel.respond(input("Enter your message >> ")))
    message = input("Enter your message to the bot: ")
    # print("--------"+message)
    if message=="quit":
        exit()
    elif message == "save":
        kernel.saveBrain("bot_brain.brn")
    else:
        bot_response = kernel.respond(message, sessionId)
        print(bot_response)