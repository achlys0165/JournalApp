from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, time
import threading
import webview
from threading import Thread
from dictionary import Dictionary
from reminder_scheduler import run_scheduler
import time as pytime

app = Flask(__name__)

# Initialize and load from JSON
entries_dict = Dictionary()
feedback_dict = Dictionary()

entries_dict.load("entries.json")
feedback_dict.load("feedback.json")


def get_sorted_entries():
    items = entries_dict.items()  # (timestamp, (content, mood))
    return sorted(items, key=lambda x: x[0], reverse=True)


@app.route('/')
def index():
    entries = get_sorted_entries()
    today = datetime.now().strftime("%Y-%m-%d")
    feedback = feedback_dict.get(today, None)
    print("Today's Feedback:", feedback)
    print("All Feedback:", feedback_dict.items())
    return render_template('index.html', entries=entries, feedback=feedback)


@app.route('/add', methods=['POST'])
def add_entry():
    content = request.form['content']
    mood = request.form.get('mood', '').lower()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entries_dict.add(timestamp, (content, mood))
    entries_dict.save("entries.json")

    now = datetime.now().time()
    EIGHT_PM = time(0, 0)
    if now >= EIGHT_PM:
        today_date = datetime.now().strftime("%Y-%m-%d")
        moods_today = [
            val[1] for key, val in entries_dict.items() if key.startswith(today_date)
        ]

        happy_count = moods_today.count('happy')
        neutral_count = moods_today.count('neutral')
        sad_count = moods_today.count('sad')

        if happy_count >= max(neutral_count, sad_count):
            feedback_msg = "Great job! You seem to be feeling positive today. Keep it up! 😊"
        elif neutral_count >= max(happy_count, sad_count):
            feedback_msg = "You're feeling quite neutral today. Hope tomorrow brings more joy! 😐"
        else:
            feedback_msg = "It seems like you had some tough moments today. Remember, it's okay to have bad days. We're here for you. 😟"

        feedback_dict.add(today_date, feedback_msg)
        feedback_dict.save("feedback.json")

    return redirect(url_for('index'))


@app.route('/feedback')
def view_feedback():
    today = datetime.now().strftime("%Y-%m-%d")
    feedback = feedback_dict.get(today, "No feedback yet.")
    return render_template('feedback.html', feedback=feedback)


def wait_for_server(url, timeout=10):
    import requests
    start_time = pytime.time()
    while True:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                break
        except:
            pass
        if pytime.time() - start_time > timeout:
            break
        pytime.sleep(0.5)


if __name__ == '__main__':
    Thread(target=run_scheduler, daemon=True).start()
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()

    width = 460
    height = 720

    wait_for_server("http://127.0.0.1:5000")
    webview.create_window("Wellness Journal", "http://127.0.0.1:5000", width=width, height=height)
    webview.start()
