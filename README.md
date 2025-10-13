Local Chatbot (Sentiment-Aware)

Repo: https://github.com/vaibhavneo/Sentiment_Chatbot

Local path (dev): C:\Users\vaibh\Desktop\Local_chatbot

What this is

A simple Python chatbot that responds to multiple prompts, lists capabilities, handles malformed input, and adapts tone/flow using sentiment analysis (VADER). It’s structured so you can swap in cloud AI later (Azure Cognitive Services / Azure OpenAI).

Where the code came from

Upstream source: Microsoft BotBuilder-Samples → Python → 02.echo-bot

Why copy:

Provides a minimal, working scaffold to focus on conversation design.

Stable, well-known sample to extend with sentiment & fallbacks.

Assignment requires submitting a self-contained project (GitHub + ZIP).

License: See upstream repo’s LICENSE (MIT). Keep headers where present.

What I changed

Added command router: /help, echo <text>, upper <text>, time.

Added sentiment path with VADER:

Negative → empathize and short-circuit to options/handoff.

Positive → acknowledge and offer next step.

Neutral → standard handling + helpful fallback.

Wrote clearer fallback copy; cap clarification to 2–3 turns.

Added this README and submission steps.

Files (fill these in with your actual names)

Entry point: <app.py> (if different, use <main.py> / <run.py> / <index.py>)

Bot logic: bots/<echo_bot.py or sentiment_bot.py>

Requirements: <requirements.txt> (if present)

Misc: .env (ignored), .gitignore, README.md

To see what you actually have:

dir /b *.py
dir /b /s *.py

Setup & Run (Windows • cmd.exe)
1) Environment
call conda activate MSAI631_MBF  || (conda create -y -n MSAI631_MBF python=3.8 & call conda activate MSAI631_MBF)
cd /d C:\Users\vaibh\Desktop\Local_chatbot
python -m pip install --upgrade pip
pip install -r requirements.txt  ||  pip install botbuilder-core botbuilder-integration-aiohttp aiohttp vaderSentiment

2A) If this is a web bot (Bot Framework endpoint)
set MicrosoftAppId=
set MicrosoftAppPassword=
set PORT=3978
python app.py   &&  REM replace with your real entry if not app.py


Then open Bot Framework Emulator → “Open Bot”
Endpoint URL: http://localhost:3978/api/messages (leave App ID/Password blank)

Not sure it’s a web bot? Search for the route:

findstr /S /I "/api/messages" *.py

2B) If this is a console bot

Just run the entry file and chat in the terminal:

python app.py   || python main.py || python run.py || python index.py

Troubleshooting quickies
netstat -ano | findstr :3978   &:: should show a listener for web bots
taskkill /PID <PID> /F         &:: free the port if occupied

Minimal sentiment wiring (VADER)

If not already in your code, this shows the basic pattern.
Install: pip install vaderSentiment

# bots/sentiment_bot.py (excerpt)
from datetime import datetime
from botbuilder.core import ActivityHandler, TurnContext
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

class EchoBot(ActivityHandler):
    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for m in members_added:
            if m.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("👋 Hi! I’m your sentiment-aware sample bot. Type `/help`.")

    async def on_message_activity(self, turn_context: TurnContext):
        raw = (turn_context.activity.text or "").strip()
        lo  = raw.lower()

        if lo in ("/help","help"):
            return await turn_context.send_activity(
                "Capabilities:\n• time\n• upper <text>\n• echo <text>\nI also detect tone and guide accordingly."
            )
        if lo == "time":    return await turn_context.send_activity(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if lo.startswith("upper "): return await turn_context.send_activity(raw[6:].upper() or "Usage: upper <text>")
        if lo.startswith("echo "):  return await turn_context.send_activity(raw[5:] or "Usage: echo <text>")

        # sentiment
        s = analyzer.polarity_scores(raw)["compound"]
        if s <= -0.35:
            return await turn_context.send_activity("Sorry this is frustrating. Want quick steps (A) or a person (B)?")
        if s >= 0.35:
            return await turn_context.send_activity("Glad that helped! Need anything else?")

        return await turn_context.send_activity("I didn’t catch a command. Try `/help` or `echo hello`.")


Why VADER? Great out-of-the-box for short text; interpretable score in [-1,1]. For domain nuance or multilingual, plan to upgrade to Azure Cognitive Services or a fine-tuned model later.

Assignment notes (provenance + reason to copy)

This repo includes copied scaffolding from Microsoft’s 02.echo-bot sample to:

satisfy the assignment’s requirement for a simple working chatbot,

concentrate effort on sentiment-aware conversation design rather than boilerplate, and

enable future integration with Azure AI by swapping the “unknown message” branch to a cloud model.

License from upstream is preserved; changes are documented above.

Packaging for submission
cd /d C:\Users\vaibh\Desktop\Local_chatbot
powershell -command "Compress-Archive -Path * -DestinationPath ..\Local_chatbot_Submission.zip -Force"


Submit the ZIP and the GitHub URL.

CHANGELOG
2025-10-12

Add VADER sentiment path with empathetic copy and handoff options.

Add /help, time, upper, echo commands; improve fallbacks (max 3 turns).

Create README with provenance, run steps, submission commands.

2025-10-11

Copy scaffold from BotBuilder-Samples 02.echo-bot and verify local run with Emulator.

Generate a log from Git (optional):

git log --pretty=format:"- %ad %h %s" --date=short