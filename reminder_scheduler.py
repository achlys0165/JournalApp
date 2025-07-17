import time
from datetime import datetime, timedelta
from plyer import notification
from reminders import Reminder, OrderedArray

reminders = OrderedArray()
# reminders.insert(Reminder(0, 0, "Time for your morning reflection 🌅"))
# reminders.insert(Reminder(12, 0, "Noon check-in! How are you doing? ☀️"))
# reminders.insert(Reminder(20, 0, "Evening wind-down. Journal your thoughts 🌙"))

now = datetime.now()
for i in range(5):  # You can increase the number for more test reminders
    trigger_time = now + timedelta(seconds=10 * (i + 1))
    reminders.insert(Reminder(trigger_time.hour, trigger_time.minute, f"Test Reminder {i+1} 🔔"))





def run_scheduler():
    print("Ordered reminder scheduler started")
    while True:
        due = reminders.pop_due()
        if due:
            now_str = datetime.now().strftime('%H:%M:%S')
            print(f"[{now_str}] Triggering: {due.message}")
            notification.notify(
                title="Wellness Journal Reminder",
                message=f"[{now_str}] {due.message}",
                timeout=5#Change to 10
            )
        time.sleep(1)#Change to 30 for final
