import aiml

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("startup.xml")
kernel.respond("LOAD AIML B")

# Press CTRL-C to break this loop
while True:
    print(kernel.respond(input("Enter your message >>")))