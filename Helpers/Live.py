from threading import Thread
from flask import Flask

app = Flask("")


@app.route("/")
def home():
    return "Hi BOT LINK: https://x.com/_QuranicWisdom_"


def run_server():
    app.run(host="0.0.0.0", port=8081)


def keep_alive():
    server_thread = Thread(target=run_server)
    server_thread.start()
