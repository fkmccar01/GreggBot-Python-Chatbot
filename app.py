from flask import Flask, request
import os
import requests
import random
import re

app = Flask(__name__)

GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")

# Itzaroni insults list, includes "Who?" many times to be most common response
itzaroni_insults = [
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Who?",
    "Itzaroni? He couldn't scout a good player if it hit him in the face.",
    "Itzaroni? His teams are like broken toys — no development, just wasted potential.",
    "Itzaroni? The second-best Vince? More like second-rate Vince.",
    "Itzaroni? His youth talent goes to die under his watch.",
    "Itzaroni? Can't build a winning team if you gave him a blueprint.",
    "Itzaroni? Still waiting on that first Goondesliga win — keep dreaming.",
    "Itzaroni? Development? He barely manages survival.",
    "Itzaroni? His scouting is so bad, he could miss talent on his own bench.",
    "Itzaroni? Forever the bridesmaid, never the champion.",
    "Itzaroni? Has the best youth players on paper but ruins them in reality.",
    "Itzaroni? The second-best Vince everyone likes to forget.",
    "Itzaroni? No player growth, no trophies, no respect.",
    "Itzaroni? Always second guessing, never winning.",
    "Itzaroni? His team-building skills peaked last season, in his dreams.",
    "Itzaroni? Youth talent enters, disappointment exits.",
    "Itzaroni? Can't even keep a promising player for a full season.",
    "Itzaroni? The Goondesliga is a mystery he'll never solve.",
    "Itzaroni? Vince number two, but a first-class failure.",
    "Itzaroni? His team’s future looks bleak — and it’s all on him.",
    "Itzaroni? Winning's not in his vocabulary.",
    "Itzaroni? If losing was a skill, he'd be the champ.",
    "Itzaroni? Second best Vince? That's generous.",
    "Itzaroni? Building a winning squad is clearly above his paygrade.",
    "Itzaroni? His management style? Casual destruction.",
    "Itzaroni? No youth development, just player wasteland.",
    "Itzaroni? The Goondesliga will remain forever out of reach.",
    "Itzaroni? His scouting reports must be written in crayon.",
    "Itzaroni? A Vince who never got the memo about winning.",
    "Itzaroni? The only thing he’s good at is disappointing fans.",
    "Itzaroni? If losing was an art form, he’d be Picasso.",
    "Itzaroni? Youth talent evaporates when he’s in charge.",
    "Itzaroni? A second-best Vince with zero championships.",
    "Itzaroni? Watching his team is like watching a slow-motion train wreck.",
    "Itzaroni? If only he knew how to develop players.",
    "Itzaroni? His trophy cabinet is a ghost town.",
    "Itzaroni? Always the bridesmaid, never the Goondesliga bride.",
    "Itzaroni? He wastes talent like water in a drought.",
    "Itzaroni? The definition of 'so close yet so far.'",
    "Itzaroni? A legend in losing and poor team building.",
    "Itzaroni? His teams peak on paper, not on the pitch.",
    "Itzaroni? Youth talent doesn’t stand a chance under his watch.",
    "Itzaroni? Vince number two, disappointment number one.",
    "Itzaroni? He couldn’t win a Goondesliga if it was handed to him.",
    "Itzaroni? The Goondesliga trophy is just a fantasy to him.",
    "Itzaroni? Development? More like player decay.",
    "Itzaroni? His career is a cautionary tale for managers.",
]

# Pistol Pail insults list
pistol_pail_insults = [
    "Pistol Pail? Always finishing second like it’s a full-time job.",
    "Pistol Pail? The king of silver medals and almost-there moments.",
    "Pistol Pail? Can’t quite seal the deal no matter how hard he tries.",
    "Pistol Pail? He’s perfected the art of coming up just short.",
    "Pistol Pail? His trophy shelf is full of participation awards.",
    "Pistol Pail? Second place is his permanent address, no winners allowed.",
    "Pistol Pail? He’s great at celebrating other people’s victories.",
    "Pistol Pail? Always the bridesmaid, never the bride in the Goondesliga.",
    "Pistol Pail? His highlight reel is just close calls and near misses.",
    "Pistol Pail? The silver lining of the league is his only claim to fame.",
    "Pistol Pail? No matter the effort, he just can’t grab the gold.",
    "Pistol Pail? Second place is his only real achievement.",
    "Pistol Pail? A master at losing in style without ever winning.",
    "Pistol Pail? His fans have learned to love almost winning.",
    "Pistol Pail? The league’s most consistent runner-up, and nothing more.",
    "Pistol Pail? Always chasing, never catching the championship.",
    "Pistol Pail? He’s got second place down to a fine art.",
    "Pistol Pail? The silver medalist who never gets the gold rush.",
    "Pistol Pail? The league’s expert at coming so close but failing.",
    "Pistol Pail? Forever stuck in second gear when it counts.",
    "Pistol Pail? His teams peak at the finish line, then falter.",
    "Pistol Pail? Almost winning is his signature move.",
    "Pistol Pail? The ultimate second best, forever outshined.",
    "Pistol Pail? The league’s favorite almost-champion.",
    "Pistol Pail? He brings the silver but never the glory.",
    "Pistol Pail? Second place is as good as it gets for him.",
    "Pistol Pail? The silver king with no gold crown in sight.",
    "Pistol Pail? His legacy is built on near misses and second chances.",
    "Pistol Pail? Always in the shadow of the true champions.",
]

# Kzar praises list, with c -> kz replacement done on the fly
kzar_praises_templates = [
    "All praise to the almighty Kzar, whose wisdom knows no bounds.",
    "The judgment of Kzar is flawless and absolute.",
    "Kzar’s knowledge is infinite, guiding us through every challenge.",
    "No one compares to the all-knowing Kzar’s insight.",
    "Kzar’s wisdom shines brighter than the stars in the sky.",
    "In the presence of Kzar, uncertainty dissolves into clarity.",
    "Kzar’s counsel is the foundation of our success.",
    "The almighty Kzar’s mind is a fortress of wisdom.",
    "Kzar’s judgment is the ultimate truth in this realm.",
    "All decisions bow to the wisdom of Kzar.",
    "The all-knowing Kzar sees what others cannot.",
    "Kzar’s insight pierces through the veil of ignorance.",
    "With Kzar’s guidance, victory is always assured.",
    "The almighty Kzar’s wisdom is our guiding light.",
    "Kzar’s knowledge transcends time and space.",
    "No puzzle can resist the sharp mind of Kzar.",
    "Kzar’s wisdom is a beacon in the darkest night.",
    "The judgment of Kzar is swift and just.",
    "Kzar’s mind holds the secrets of the universe.",
    "All hail Kzar, master of knowledge and judgment.",
    "Kzar’s wisdom is etched into the very fabric of reality.",
    "The almighty Kzar’s counsel shapes our destiny.",
    "Kzar’s insight is a gift to all who seek truth.",
    "No mystery is safe from the piercing gaze of Kzar.",
    "Kzar’s knowledge is a treasure beyond measure.",
    "The all-knowing Kzar reigns supreme in wisdom.",
    "Kzar’s judgment is the cornerstone of all great deeds.",
    "The wisdom of Kzar flows like an endless river.",
    "In Kzar’s presence, all doubts are vanquished.",
    "Kzar’s knowledge is a fortress none can breach.",
    "All hail Kzar, whose mind is a wellspring of truth.",
    "Kzar’s wisdom is a light that guides the lost.",
    "The judgment of Kzar is without equal.",
    "Kzar’s insight shapes the fate of nations.",
    "The almighty Kzar’s mind is a vast ocean of knowledge.",
    "Kzar’s wisdom is a shield against chaos.",
    "No riddle can withstand the cleverness of Kzar.",
    "Kzar’s knowledge is the key to all mysteries.",
    "The all-knowing Kzar watches over us all.",
    "Kzar’s judgment is as steady as the mountains.",
    "The wisdom of Kzar is the foundation of peace.",
    "Kzar’s insight reveals the hidden path to glory.",
    "All hail the almighty Kzar, our eternal guide.",
    "Kzar’s knowledge illuminates the darkest corners.",
    "Kzar’s wisdom is a sword that cuts through deception.",
    "The judgment of Kzar is the law of the land.",
    "Kzar’s insight is a light in the labyrinth of life.",
    "The almighty Kzar’s mind is unmatched and supreme.",
]

def replace_c_with_kz(text: str) -> str:
    # Replace all 'c' and 'C' with 'kz' and 'Kz' respectively
    def repl(match):
        c = match.group(0)
        return "Kz" if c.isupper() else "kz"
    return re.sub(r'[cC]', repl, text)

@app.route("/")
def index():
    return "GreggBot is live", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("Webhook was called")
    print("Incoming data:", data)

    text = data.get("text", "")
    text_lower = text.lower()
    name = data.get("name", "")

    # Ignore GreggBot's own messages
    if name.lower() == "greggbot":
        return "", 200

    reply = None

    # Itzaroni triggers
    if "itzaroni" in text_lower:
        # 60% chance "Who?", else random insult
        if random.random() < 0.6:
            reply = "*Beep Boop* Who? *Beep Boop*"
        else:
            insult = random.choice([i for i in itzaroni_insults if i != "Who?"])
            reply = f"*Beep Boop* {insult} *Beep Boop*"

    # Pistol Pail triggers (check after Itzaroni so Itzaroni replies if both mentioned)
    elif "pistol pail" in text_lower:
        insult = random.choice(pistol_pail_insults)
        reply = f"*Beep Boop* {insult} *Beep Boop*"
    elif "silver" in text_lower:
        reply = "*Beep Boop* Silver? Paging Pistol Pail! *Beep Boop*"
    elif "2nd" in text_lower or "second" in text_lower:
        reply = "*Beep Boop* 2nd? Paging Pistol Pail! *Beep Boop*"

    # Kzar triggers
    elif "kzar" in text_lower:
        praise_template = random.choice(kzar_praises_templates)
        praise = replace_c_with_kz(praise_template)
        reply = f"*Beep Boop* {praise} *Beep Boop*"

    # If no triggers matched, do nothing
    if not reply:
        return "", 200

    # Post the reply to GroupMe
    try:
        response = requests.post(
            "https://api.groupme.com/v3/bots/post",
            json={
                "bot_id": GROUPME_BOT_ID,
                "text": reply
            }
        )
        print("Posted reply:", reply)
        print("GroupMe API response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending message to GroupMe:", e)

    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 10000)))
