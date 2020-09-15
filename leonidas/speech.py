import discord

_HAVING_TROUBLE = ("Say `help` to me at any time and I'll give you some instructions.\n"
                   "If you need help from a human, please post in <#%s>.")

GREETING = ("Greetings **%s**! I am <@%s>, UBC Course Chat's loyal guardian.\n")

EMAIL_REQUEST = ("I'll verify your UBC email address and then I can add you to the course chats!\n"
                 "Please tell me your UBC email address. It should end with **ubc.ca**.")

BAD_EMAIL = ("Hmm, I couldn't see a UBC email address in your message.\n" +
             _HAVING_TROUBLE)

EMAIL_ALREADY_USED = ("It looks like that email has already been used to verify a user.\n" +
                       _HAVING_TROUBLE)

SENT_EMAIL = ("Thanks! I sent an email with an access code to **%s**.\n"
              "Respond to me here with the code once you receive it.")

BAD_CODE = ("Hmm, I can't see the right access code in your message.\n"
            "If you need me to resend the code, please tell me your UBC email address again.\n" +
            _HAVING_TROUBLE)

BAD_COURSE = ("I don't think '%s' is a valid UBC class this session.")

BAD_SCHEDULE = ("Hmm, that doesn't look like the right file format to me.\n"
                + _HAVING_TROUBLE)

NO_COURSES = ("I can't see any valid UBC classes in your message.\n" +
              _HAVING_TROUBLE)

ADDED_TO_CHANNEL = ("I added you to the <#%s> channel!")

REMOVED_FROM_CHANNEL = ("I removed you from *%s*.")

INVALID_CHANNEL = ("I don't think *%s* is a valid class channel. Please try again.\n" +
                   _HAVING_TROUBLE)

ALREADY_IN_CHANNELS = ("Looks like you're already in all the channels related to *%s*.")

VERIFIED = ("Nice! You're verified. I've added you to <#%s> and <#%s>.")

COURSE_INSTRUCTIONS_1 = ("Let's add you to some course chats!\n"
                         "The easiest way is to download your course schedule from the timetable page "
                         "on the SSC and drag/drop that file into the chat here.\n"
                         "I can read your schedule and automatically add you to chats for your courses, sections, labs, etc.")

COURSE_INSTRUCTIONS_2 = ("Alternatively, you can tell me which classes you want to be added to. E.g.:\n"
                         "> *CPSC 110 101*, *BIOL 112 T02*, *ASTR 101 10W*\n"
                         "If you want to leave a channel at anytime, "
                         "you can send me a message like `leave cpsc-110-101`.")

ALREADY_VERIFIED = ("You're already verified")

UNKNOWN_USER = ("Hmm, I can't remember you joining the server. "
                "Here's an invite link! %s")

RE_VERIFY = ("Hi **%s**, I need to verify your account.\n"
             "Apologies if we already did this, I suffer from occasional memory loss.")
                

EMAIL_INST_EMBED = discord.Embed(
    title="Getting a UBC email address",
    url="https://it.ubc.ca/services/email-voice-internet/ubc-student-email-service",
    description="Follow these steps if you don't already have a UBC email address!",
    colour=discord.Color.from_rgb(0, 30, 60)
).set_thumbnail(url="https://teenlife.s3.amazonaws.com/media/uploads/listings/BLqgL7cNrgto.jpg")
