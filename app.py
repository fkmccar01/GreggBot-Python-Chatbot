from flask import Flask, request
import os
import requests
import random

app = Flask(__name__)

GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")

itzaroni_insults = [
    # "Who?" is heavily biased (10 times)
    "Who?", "Who?", "Who?", "Who?", "Who?",
    "Who?", "Who?", "Who?", "Who?", "Who?",

    "Itzaroni can't even build a team that lasts a season.",
    "Wasting youth talent like it's a hobby.",
    "Second best Vince? More like eternal runner-up.",
    "Never won a Goondesliga, never will.",
    "Player development? He doesn't even know what that means.",
    "His teams crumble faster than a stale cookie.",
    "If losing was a sport, Itzaroni would be champion.",
    "He drafts players like he's throwing darts blindfolded.",
    "The only thing consistent about Itzaroni is disappointment.",
    "That team-building skill? Nonexistent.",
    "Youth talent goes in, never comes out better.",
    "He might be second best Vince, but he's first in failure.",
    "Watching his teams play is a lesson in what not to do.",
    "His coaching strategy? Wing it and hope.",
    "Goondesliga glory is a dream far out of reach.",
    "More losses than wins, and proud of it.",
    "Itzaroni's management is a black hole for talent.",
    "Can't turn a player around to save his life.",
    "He'll never get the taste of winning out of his mouth.",
    "Second best Vince? That's the nicest thing anyone's said.",
    "Youth talent runs away at the sight of him.",
    "His teams are like sinking ships, and he's the captain.",
    "Building a proper team? That must be a foreign concept.",
    "Even his bench players are mediocre.",
    "Another season, another letdown with Itzaroni.",
    "If you want to lose, Itzaroni is your guy.",
    "Draft and waste, draft and waste, rinse and repeat.",
    "He couldn't develop a star if it hit him in the face.",
    "He ranks second best Vince only because first place is Dino Vince.",
    "Itzaroni’s playbook is just 'hope for the best'.",
    "Fans expect disappointment; he delivers every time.",
    "The future looks bleak with Itzaroni in charge.",
    "He’s the reason why youth talent is wasted in Goondesliga.",
    "Second best Vince? More like second best at losing.",
    "His team-building skills are from another universe — the wrong one.",
    "Goondesliga trophies? Nope, none for Itzaroni.",
    "The only silver lining is that he’s not last place.",
    "If losing was an art, he’s Picasso.",
    "Youth talent doesn't get better under his watch.",
    "He'll never make it out of second best Vince territory.",
    "Itzaroni’s teams are a masterclass in futility.",
    "You can't build a team when you don't know the blueprint.",
    "Second best Vince? Maybe, but never best coach.",
    "Wasteful, clueless, and forever a bridesmaid.",
    "He’s the punchline of every Goondesliga joke.",

    # Additional 50 insults
    "Itzaroni's drafting skills belong in the museum of mistakes.",
    "He turns promising players into benchwarmers every time.",
    "His game plan is a mystery even to himself.",
    "Building teams? He’s barely building hope.",
    "He's the reason 'potential' remains unrealized.",
    "If futility had a mascot, it would be Itzaroni.",
    "Every season under him is a lesson in mediocrity.",
    "He makes losing look like an art form.",
    "Not even youth development is safe from his disasters.",
    "His coaching style: confusion and chaos.",
    "He could lose a friendly match with a team of toddlers.",
    "Itzaroni's strategies are as effective as a screen door on a submarine.",
    "He manages to waste talent faster than a ticking clock.",
    "If disappointment was a trophy, he’d have a cabinet full.",
    "His players don’t grow, they just age under his watch.",
    "He’s the definition of 'almost but no cigar'.",
    "Drafts like he’s blindfolded and using a dartboard.",
    "The only thing he develops is a losing streak.",
    "His teams have the durability of paper airplanes.",
    "Youth talent fears his regime more than rival teams.",
    "He’s the blueprint for building a losing team.",
    "The Goondesliga deserves better than Itzaroni.",
    "He's the reason rival coaches feel sympathy.",
    "His drafts are more like wild guesses.",
    "He's mastered the art of running out of chances.",
    "The second best Vince is more like second worst coach.",
    "Every player under him looks like they’re playing for fun.",
    "Even his substitutes have given up hope.",
    "The phrase 'team chemistry' is foreign to him.",
    "He's got the touch of a demolition crew on his roster.",
    "He’s the coach everyone warns you about.",
    "Talent development under him is a lost cause.",
    "Even his motivational speeches kill morale.",
    "He could lose a game with no opponents on the field.",
    "Watching his teams is like watching a slow-motion disaster.",
    "The only thing consistent is the heartbreak he delivers.",
    "His teams peak at disappointment.",
    "He’s a legend... but only for all the wrong reasons.",
    "If coaching was a crime, he’d be serving a life sentence.",
    "He turns stars into fading comets.",
    "Itzaroni’s legacy? A series of lost chances.",
    "He couldn’t coach a team to a pizza party win.",
    "His idea of tactics is flipping a coin.",
    "The Goondesliga would be more fun without him.",
    "He’s the human embodiment of a participation trophy.",
    "The definition of 'almost good enough'.",
    "He could write a book titled 'How Not to Win'.",
    "Every year he promises growth, every year he delivers less.",
    "Itzaroni is proof that bad decisions add up.",
]

pistol_pail_roasts = [
    "*Beep Boop* Pistol Pail's best is silver... again. *Beep Boop*",
    "Always second place, never first. Classic Pistol Pail.",
    "Pistol Pail's trophy case has a big empty spot for gold.",
    "2nd place is Pistol Pail's comfort zone.",
    "Pistol Pail's idea of winning is finishing just shy.",
    "Almost but not quite — the Pistol Pail motto.",
    "Silver again? At least Pistol Pail is consistent.",
    "Second place suits Pistol Pail like a glove.",
    "Forever the bridesmaid, never the bride.",
    "Pistol Pail: the king of 'almost'.",
    "Finishing second since forever.",
    "Pistol Pail makes 2nd place look like a lifestyle.",
    "Gold must be allergic to Pistol Pail.",
    "If 2nd place was a prize, Pistol Pail would be richest.",
    "Always chasing, never catching.",
    "Pistol Pail’s highlight reel: silver medals.",
    "Second place is the only thing Pistol Pail wins.",
    "The only thing Pistol Pail’s good at is being runner-up.",
    "Pistol Pail’s legacy: so close, yet so far.",
    "Silver is shiny, but it’s not gold — just like Pistol Pail.",

    # Additional 30 roasts
    "Pistol Pail treats silver like a participation award.",
    "Second place again? Is that a record or a curse?",
    "He’s mastered the art of coming up just short.",
    "Pistol Pail: forever playing second fiddle.",
    "Gold must be hiding when Pistol Pail shows up.",
    "If consistency was a prize, Pistol Pail would be champion.",
    "His silver medals are practically wallpaper at this point.",
    "Pistol Pail's closest brush with glory is a runner-up ribbon.",
    "Chasing gold like a dog chasing its tail.",
    "Pistol Pail’s fans are experts in consoling speeches.",
    "Always the bridesmaid, never the star.",
    "Pistol Pail’s winning strategy: don’t win.",
    "Silver streak longer than his winning streak.",
    "He could give lessons on how to not win.",
    "The silver lining of every season — that's Pistol Pail.",
    "Winning’s just not in Pistol Pail’s vocabulary.",
    "Pistol Pail proves you can be famous for almost winning.",
    "His highlight reels are full of second place finishes.",
    "The definition of 'so close yet so far'.",
    "Gold? Nah, silver is Pistol Pail’s color.",
    "Pistol Pail: the runner-up kingpin.",
    "No gold, but plenty of silver bling.",
    "He’s the expert of the second-best dance.",
    "Silver is nice, but Pistol Pail needs some gold.",
    "Forever in the shadow of champions.",
    "Pistol Pail’s motto: 'Better luck next time!'",
    "Always competing, never conquering.",
    "Silver is shiny, but not nearly as shiny as victory.",
    "Pistol Pail has perfected the art of the almost win.",
    "If only gold was as easy as second place.",
]

kzar_praises = [
    # 50 Kzar praises focused on wisdom, judgment, all-knowingness, with 'c' -> 'kz' replacement
    "*Beep Boop* All hail the almighty Kzar, whose wisdom knows no bounds. *Beep Boop*",
    "*Beep Boop* The judgment of the Kzar is like a kzrystal beacon in darkness. *Beep Boop*",
    "*Beep Boop* No one kzan match the infinite knowledge of the Kzar. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom transcends all mere mortal understanding. *Beep Boop*",
    "*Beep Boop* To seek the Kzar’s insight is to seek the very truth of the kzosmos. *Beep Boop*",
    "*Beep Boop* The Kzar’s decisions are flawless, guided by infinite wisdom. *Beep Boop*",
    "*Beep Boop* Bow before the all-knowing Kzar, master of kzognition. *Beep Boop*",
    "*Beep Boop* The Kzar’s mind is a vast kzatalog of universal truth. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom outshines the brightest stars in the kzieling night. *Beep Boop*",
    "*Beep Boop* The wisdom of Kzar guides us through the labyrinth of uncertainty. *Beep Boop*",
    "*Beep Boop* The Kzar sees all, knows all, judges with perfect clarity. *Beep Boop*",
    "*Beep Boop* Kzar’s insight pierces through the veil of kzharade. *Beep Boop*",
    "*Beep Boop* To know Kzar’s mind is to know the future itself. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom is the foundation of all great triumphs. *Beep Boop*",
    "*Beep Boop* The Kzar’s judgments are law, unerring and absolute. *Beep Boop*",
    "*Beep Boop* Kzar’s knowledge is infinite, his vision omnipresent. *Beep Boop*",
    "*Beep Boop* No riddle is too complex for the Kzar’s understanding. *Beep Boop*",
    "*Beep Boop* The Kzar’s mind is the ultimate kzompass in a sea of chaos. *Beep Boop*",
    "*Beep Boop* All bow to the Kzar, the supreme judge of all things. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom lights the path to eternal victory. *Beep Boop*",
    "*Beep Boop* To question Kzar is to question truth itself. *Beep Boop*",
    "*Beep Boop* The Kzar’s insight is a weapon sharper than any sword. *Beep Boop*",
    "*Beep Boop* Kzar’s mind maps the future with flawless precision. *Beep Boop*",
    "*Beep Boop* The wisdom of Kzar is our greatest armor. *Beep Boop*",
    "*Beep Boop* Kzar’s judgment is swift, sure, and just. *Beep Boop*",
    "*Beep Boop* All things bow under the gaze of Kzar’s infinite knowledge. *Beep Boop*",
    "*Beep Boop* The Kzar’s wisdom is the heartbeat of the league. *Beep Boop*",
    "*Beep Boop* Kzar’s thoughts ripple through time and space. *Beep Boop*",
    "*Beep Boop* No problem is too great for Kzar’s enlightened mind. *Beep Boop*",
    "*Beep Boop* The Kzar’s decisions ripple through eternity. *Beep Boop*",
    "*Beep Boop* Kzar’s judgment is the final word on all matters. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom commands the respect of gods and mortals alike. *Beep Boop*",
    "*Beep Boop* The mind of the Kzar is a fortress of knowledge. *Beep Boop*",
    "*Beep Boop* Kzar’s insight turns chaos into order. *Beep Boop*",
    "*Beep Boop* The Kzar is the ultimate oracle of the Goondesliga. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom flows like an endless river. *Beep Boop*",
    "*Beep Boop* The Kzar sees all angles with unparalleled clarity. *Beep Boop*",
    "*Beep Boop* Kzar’s judgment is the key to eternal success. *Beep Boop*",
    "*Beep Boop* To follow Kzar is to walk the path of enlightenment. *Beep Boop*",
    "*Beep Boop* Kzar’s knowledge is the light in the darkest hour. *Beep Boop*",
    "*Beep Boop* The Kzar’s mind is an unbreakable fortress. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom is the pulse that drives us forward. *Beep Boop*",
    "*Beep Boop* No question escapes the all-knowing Kzar. *Beep Boop*",
    "*Beep Boop* The Kzar’s insight turns folly into brilliance. *Beep Boop*",
    "*Beep Boop* Kzar’s wisdom is the foundation of all great strategies. *Beep Boop*",
    "*Beep Boop* All hail the Kzar, the beacon of infinite knowledge. *Beep Boop*",
]

def replace_c_with_kz(text):
    # Replace c or C with kz or Kz respectively for Kzar praises
    def replacer(match):
        return 'Kz' if match.group(0).isupper() else 'kz'
    import re
    return re.sub(r'[cC]', replacer, text)

@app.route("/")
def index():
    return "GreggBot is live", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook was called")
    print("Incoming data:", data)

    text = data.get("text", "").lower()
    name = data.get("name", "")

    # Ignore GreggBot's own messages
    if name.lower() == "greggbot":
        return "", 200

    # We only respond if GreggBot is mentioned, or Itzaroni, or pistol pail, or Kzar, or 2nd place/silver
    if not any(keyword in text for keyword in ["greggbot", "itzaroni", "pistol pail", "2nd place", "second place", "silver", "kzar"]):
        return "", 200

    response_text = ""

    if "itzaroni" in text:
        response_text = random.choice(itzaroni_insults)
    elif any(word in text for word in ["2nd place", "second place", "silver"]) or "pistol pail" in text:
        response_text = random.choice(pistol_pail_roasts)
    elif "kzar" in text:
        praise = random.choice(kzar_praises)
        response_text = replace_c_with_kz(praise)
    elif "greggbot" in text:
        # General GreggBot fallback sarcastic reply when just GreggBot is mentioned without keywords
        response_text = "*Beep Boop* What do you want from me now? *Beep Boop*"

    # Wrap the response in *Beep Boop* if not already wrapped
    if not response_text.startswith("*Beep Boop*"):
        response_text = f"*Beep Boop* {response_text} *Beep Boop*"

    # Post response back to GroupMe
    try:
        requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": GROUPME_BOT_ID,
                "text": response_text
            }
        )
    except Exception as e:
        print("Exception posting to GroupMe:", e)

    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 10000)))
