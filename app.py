from flask import Flask, request
import os
import requests
import random
import re

app = Flask(__name__)

GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")

# 100 Itzaroni insults (excluding "Who?")
itzaroni_insults = [
    "Itzaroni? He couldn't scout a good player if it hit him in the face.",
    "Itzaroni? His youth talent development is borderline kriminal.",
    "Itzaroni? He'll never win a Goondesliga, no matter how hard he tries.",
    "Itzaroni? Builds teams like a toddler with blocks — all over the place.",
    "Itzaroni? Is he the second-best Vince?",
    "Itzaroni? Wastes youth talent like he's human Tar.",
    "Itzaroni? He couldn’t develop a player to save Signora's life.",
    "Itzaroni? His tactics are about as sharp as a wet noodle.",
    "Itzaroni? Forever stuck in the shadow of Dino Vince.",
    "Itzaroni? Calls himself a manager, more like man-eager to win the Goondesliga...which will be never.",
    "Itzaroni? More like Pistolroni with the way his teams peak at second-place.",
    "Itzaroni? Did he buy another 22/8 for 6m?",
    "Itzaroni? Youth talent fears his coaching more than his opponents do.",
    "Itzaroni? Has all the luck of a broken horseshoe.",
    "Itzaroni? Success is just a myth in his dictionary.",
    "Itzaroni? He thinks scouting means picking up any incompatible, over-priced player on the external market.",
    "Itzaroni? His 'development' program should be just called a 'destruction' program.",
    "Itzaroni? He couldn't build a winning team even with KzhatGPT guiding him.",
    "Itzaroni? Runs his team like a sinking ship with no captain.",
    "Itzaroni? He’s the reason ‘second-best Vince’ is a thing.",
    "Itzaroni? Can’t coach his way out of a paper bag.",
    "Itzaroni? Brags about mediocrity like it’s an art form.",
    "Itzaroni? His game plan is [inchorrent screeching]",
    "Itzaroni? Runs his team into the ground season after season.",
    "Itzaroni? If losing was an Olympic sport, he’d get gold.",
    "Itzaroni? Wastes talent faster than the clock runs down.",
    "Itzaroni? The best thing he’s built is a losing streak.",
    "Itzaroni? More likely to break a player than build one.",
    "Itzaroni? His youth system is a talent graveyard.",
    "Itzaroni? Has ‘failure’ tattooed on his coaching badge.",
    "Itzaroni? The definition of ‘second-best’ in the league.",
    "Itzaroni? Couldn’t win a Goondesliga if every other team was in the Spoondesliga.",
    "Itzaroni? His teams crash after the turn like a drunk driver.",
    "Itzaroni? Brings new meaning to ‘choking under pressure.’",
    "Itzaroni? They call him the human hormone blocker for the way he stops kids' development.",
    "Itzaroni? The Goondesliga’s most consistent disappointment.",
    "Itzaroni? Scouting reports fear his attention more than rivals.",
    "Itzaroni? Constantly rebuilding, never winning.",
    "Itzaroni? More talk, less results every single season.",
    "Itzaroni? Could turn a winning team into losers overnight.",
    "Itzaroni? The eternal bridesmaid of Goondesliga glory.",
    "Itzaroni? Has more second-place finishes than wins.",
    "Itzaroni? Wastes youth talent like a sieve leaks water.",
    "Itzaroni? Tries to coach, ends up demoralizing.",
    "Itzaroni? A legend of mediocrity and lost opportunities.",
    "Itzaroni? The league’s premier ‘what could have been.’",
    "Itzaroni? Couldn’t manage his way out of a paper sack.",
    "Itzaroni? Always close, never close enough.",
    "Itzaroni? Proves every season that luck isn’t on his side.",
    "Itzaroni? The ‘second best Vince’ no one aspires to be.",
    "Itzaroni? A master of snatching defeat from the jaws of victory.",
    "Itzaroni? His idea of strategy is throwing darts blindfolded.",
    "Itzaroni? The only thing consistent about him is disappointment.",
    "Itzaroni? Believes in miracles because he creates none.",
    "Itzaroni? Has a PhD in failing the final match.",
    "Itzaroni? His players need therapy more than training.",
    "Itzaroni? The league’s expert in last-minute collapses.",
    "Itzaroni? A cautionary tale for young coaches everywhere.",
    "Itzaroni? Wins are a rare mythical creature in his playbook.",
    "Itzaroni? His leadership inspires everyone to give up.",
    "Itzaroni? Could lose a game with a team of legends.",
    "Itzaroni? More luck in a lottery than in a match.",
    "Itzaroni? Drafts like he’s blindfolded and spinning.",
    "Itzaroni? A monument to mediocrity on the sidelines.",
    "Itzaroni? His training sessions are nap inductions.",
    "Itzaroni? Tactics so outdated, they belong in a museum.",
    "Itzaroni? Can’t develop talent, only burn it.",
    "Itzaroni? Plays favorites, loses fairness.",
    "Itzaroni? The expert in choking under pressure.",
    "Itzaroni? His motto: ‘Almost, but not quite.’",
    "Itzaroni? Builds castles on sand and wonders why they fall.",
    "Itzaroni? Has a talent for turning wins into draws.",
    "Itzaroni? His ‘plans’ are last-minute improvisations.",
    "Itzaroni? The league’s best example of ‘try and fail.’",
    "Itzaroni? Makes sure the spotlight never shines on him.",
    "Itzaroni? More interested in excuses than solutions.",
    "Itzaroni? His teams peak in friendly matches only.",
    "Itzaroni? Coaches like he’s lost in a maze.",
    "Itzaroni? Wears ‘failure’ like a badge of honor.",
    "Itzaroni? Has more bad decisions than good ones.",
    "Itzaroni? Believes effort alone wins games.",
    "Itzaroni? Can’t read the game or the room.",
    "Itzaroni? The league’s definition of inconsistency.",
    "Itzaroni? Teams play better when he’s not around.",
    "Itzaroni? Hopes for luck, never earns it.",
    "Itzaroni? The bench is his comfort zone.",
    "Itzaroni? Famous for his ‘strategy meetings’ that lead nowhere.",
    "Itzaroni? Could lose to a team of amateurs.",
    "Itzaroni? Blames others, never himself.",
    "Itzaroni? His trophy shelf is embarrassingly empty.",
    "Itzaroni? Known for making simple things complicated.",
    "Itzaroni? Coaches with the confidence of a lost puppy.",
    "Itzaroni? Has a ‘how not to win’ manual.",
    "Itzaroni? The league’s expert in self-sabotage.",
    "Itzaroni? Always just one step behind glory.",
]

def get_itzaroni_reply():
    if random.random() < 0.20:
        return "Who?"
    else:
        return random.choice(itzaroni_insults)

# 50 Pistol Pail insults
pistol_pail_insults = [
    "Pistol Pail? Always that bridesmaid, never the bride.",
    "Pistol Pail? So close to winning, yet so far forever.",
    "Pistol Pail? Silver medals piling up like trophies of failure.",
    "Pistol Pail? Finishing 2nd is his personal best.",
    "Pistol Pail? The king of ‘almost but not quite.’",
    "Pistol Pail? Has more runner-up trophies than wins.",
    "Pistol Pail? Forever chasing glory, never catching it.",
    "Pistol Pail? Second place suits him like a glove.",
    "Pistol Pail? The league’s most consistent second-place finisher.",
    "Pistol Pail? Known for coming so close, yet falling short.",
    "Pistol Pail? His team peaks right behind the leaders.",
    "Pistol Pail? Silver’s his favorite color and it shows.",
    "Pistol Pail? Runs a team that finishes just shy of glory.",
    "Pistol Pail? The perennial runner-up with no finish line.",
    "Pistol Pail? 2nd place is his comfort zone.",
    "Pistol Pail? The master of choking at the final hurdle.",
    "Pistol Pail? Second-best everything, never number one.",
    "Pistol Pail? His trophies say ‘almost’ in bold letters.",
    "Pistol Pail? 2nd place is his default setting.",
    "Pistol Pail? Always in the silver shadow of champions.",
    "Pistol Pail? Finishing second is his art form.",
    "Pistol Pail? 2nd place or bust, that’s his motto.",
    "Pistol Pail? Chasing the title, settling for less.",
    "Pistol Pail? Runner-up medals gather dust in his cabinet.",
    "Pistol Pail? Perpetually just one step behind glory.",
    "Pistol Pail? The silver lining is the only thing he knows.",
    "Pistol Pail? Close enough to taste it, far from winning it.",
    "Pistol Pail? The league’s favorite almost-man.",
    "Pistol Pail? Peaks at second, then falls off a cliff.",
    "Pistol Pail? The second-place specialist.",
    "Pistol Pail? Always the bridesmaid, never the bride.",
    "Pistol Pail? Knows the taste of silver better than gold.",
    "Pistol Pail? 2nd place medals outnumber wins.",
    "Pistol Pail? His team’s goal is to finish behind the best.",
    "Pistol Pail? The eternal runner-up in Goondesliga history.",
    "Pistol Pail? Silver medals are his team's true trophies.",
    "Pistol Pail? So close to greatness, yet so far.",
    "Pistol Pail? Always second, never celebrated.",
    "Pistol Pail? His glory days end at 2nd place.",
    "Pistol Pail? The master of just missing out.",
    "Pistol Pail? Known for finishing strong... but not strong enough.",
    "Pistol Pail? 2nd place is the highest he’ll ever get.",
    "Pistol Pail? Chasing dreams, settling for silver.",
    "Pistol Pail? The league’s silver medal specialist.",
    "Pistol Pail? His team's goal is to lose the final.",
    "Pistol Pail? Always a bridesmaid, never the champ.",
    "Pistol Pail? The runner-up kingpin.",
    "Pistol Pail? Makes silver look like a participation prize.",
    "Pistol Pail? 2nd place finisher with no upgrades.",
    "Pistol Pail? Forever the runner-up, never the hero.",
    "Pistol Pail? Silver medalist for life.",
    "Pistol Pail? The ‘almost champions’ poster child.",
]

# 25 Kzar praises (with 'c'/'C' replaced by 'kz'/'Kz')
kzar_praises_raw = [
    "All hail the almighty Kzar, whose wisdom guides the Goondesliga.",
    "Kzar's judgment is as unerring as the stars themselves.",
    "No decision escapes the watchful eyes of Kzar.",
    "Kzar's knowledge is the foundation of our glory.",
    "The league bows before the all-knowing Kzar.",
    "Kzar sees through all tactics with divine clarity.",
    "The wisdom of Kzar shapes the fate of teams.",
    "Kzar's insight is sharper than any sword.",
    "Under Kzar's gaze, all strategies unravel.",
    "Kzar’s words are law, and law is victory.",
    "The Kzar’s judgment balances fate and fortune.",
    "Kzar's mind is a fortress no rival can breach.",
    "Every move is predicted by the omniscient Kzar.",
    "Kzar’s wisdom turns games into legends.",
    "No secret is safe from the all-seeing Kzar.",
    "Kzar’s vision turns chaos into order.",
    "Our glory is forged in Kzar’s mind.",
    "The hand of Kzar guides the winning path.",
    "Kzar’s counsel is sought by all who dare win.",
    "Forever wise, forever Kzar, forever victorious.",
    "The Kzar’s judgment is final and just.",
    "Kzar’s insight outmatches all opposition.",
    "In Kzar we trust for victory and honor.",
    "Kzar’s wisdom lights the darkest battles.",
    "All victories are gifts from the wise Kzar.",
]

def replace_c_with_kz(text):
    def repl(m):
        return 'kz' if m.group(0).islower() else 'Kz'
    return re.sub(r'[cC]', repl, text)

kzar_praises = [replace_c_with_kz(p) for p in kzar_praises_raw]

def get_kzar_reply():
    return random.choice(kzar_praises)

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
    
    if name.lower() == "taycan a. schitt":
            return "", 200

    reply = None

    # Priority: silver > 2nd/second > pistol pail insults
    if "silver" in text:
        reply = "*Beep Boop* Silver? Paging Pistol Pail! *Beep Boop*"
    elif "2nd" in text or "second" in text:
        reply = "*Beep Boop* 2nd? Paging Pistol Pail! *Beep Boop*"
    elif "pistol pail" in text:
        insult = random.choice(pistol_pail_insults)
        reply = f"*Beep Boop* {insult} *Beep Boop*"
    # If Itzaroni mentioned but not silver/2nd/pistol pail
    elif "itzaroni" in text:
        reply = get_itzaroni_reply()
        reply = f"*Beep Boop* {reply} *Beep Boop*"
    # If Kzar mentioned and no reply yet
    elif "kzar" in text:
        reply = get_kzar_reply()
        reply = f"*Beep Boop* {reply} *Beep Boop*"
    # Franzia + title special link
    if "franzia" in text and "title" in text:
        reply = "*Beep Boop* Franzia and titles? https://howmanydayssincefranzialastwonthegoon.netlify.app/ *Beep Boop*"
    
    if reply:
        try:
            response = requests.post(
                "https://api.groupme.com/v3/bots/post",
                json={
                    "bot_id": GROUPME_BOT_ID,
                    "text": reply
                }
            )
            print("Posted reply:", reply)
            print("GroupMe API response:", response.status_code)
        except Exception as e:
            print("Exception sending message:", e)

    return "", 200

if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 10000)))
