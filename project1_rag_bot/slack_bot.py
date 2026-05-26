from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
import os, sys

sys.path.append(".")
from project1_rag_bot.rag_chain import answer

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    question = event["text"]
    question = question.split(">", 1)[-1].strip()

    say("Searching FINTRAC documents...")

    try:
        result = answer(question)
        sources = "\n".join([f"• {s}" for s in result["sources"]])
        response = f"*Answer:*\n{result['answer']}\n\n*Sources:*\n{sources}"
    except Exception as e:
        response = f"Sorry, I hit an error: {str(e)}"

    say(response)
@app.event("message")
def handle_dm(event, say):
    # Only respond to direct messages, ignore channel messages
    if event.get("channel_type") != "im":
        return
    
    question = event.get("text", "").strip()
    if not question:
        return

    say("Searching FINTRAC documents...")

    try:
        result = answer(question)
        sources = "\n".join([f"• {s}" for s in result["sources"]])
        response = f"*Answer:*\n{result['answer']}\n\n*Sources:*\n{sources}"
    except Exception as e:
        response = f"Sorry, I hit an error: {str(e)}"

    say(response)

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("FINTRAC bot is running. @-mention it in any Slack channel.")
    handler.start()