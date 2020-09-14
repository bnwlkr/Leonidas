import discord

_HAVING_TROUBLE = ("If you're having trouble, please send a message in <#%s>.")

GREETING = ("Greetings **%s**! I am Leonidas, UBC discord's loyal guardian.\n"
            "To start with, I'll verify your UBC email address and then I can add you to the course chats!")

EMAIL_REQUEST = ("Please tell me your UBC email address. It should end with **ubc.ca**.")

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

COURSE_INSTRUCTIONS = ("Let's add you to some courses!\n"
                       "Tell me the courses/sections/labs/tutorials/waitlists that you're in. E.g.:\n\n"
                       "> *CPSC 110*, *BIOL 112 T02*, *ASTR 101 10W*\n\n"
                       "If you want to leave a channel at anytime, "
                       "you can send a message to me like `LEAVE <channel-name>` (e.g. `LEAVE cpsc-110-101`)")



ALREADY_VERIFIED = ("You're already verified")

UNKNOWN_USER = ("Hmm, I can't remember you joining the UBC discord. "
                "Here's an invite link! %s")

RE_VERIFY = ("Hi **%s**, I need to verify your account.\n"
             "Apologies if we already did this, I suffer from occasional memory loss.")
                

EMAIL_INST_EMBED = discord.Embed(
    title="Getting a UBC email address",
    url="https://it.ubc.ca/services/email-voice-internet/ubc-student-email-service",
    description="Follow these steps if you don't already have a UBC email address!",
    colour=discord.Color.from_rgb(0, 30, 60)
).set_thumbnail(url="https://teenlife.s3.amazonaws.com/media/uploads/listings/BLqgL7cNrgto.jpg")
