import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message

MIN_POLL_INTERVAL = 1
MAX_POLL_INTERVAL = 30
BACKOFF_MULTIPLIER = 1.5

driver = WhatsAPIDriver()
print("Waiting for QR")
driver.wait_for_login()

print("Bot started")

poll_interval = MIN_POLL_INTERVAL
while True:
    print(f'Checking for more messages (polling every {poll_interval}s)')
    unread_contacts = driver.get_unread()
    
    if unread_contacts:
        poll_interval = MIN_POLL_INTERVAL
        for contact in unread_contacts:
            for message in contact.messages:
                if isinstance(message, Message):
                    contact.chat.send_message(message.safe_content)
    else:
        poll_interval = min(poll_interval * BACKOFF_MULTIPLIER, MAX_POLL_INTERVAL)
    
    time.sleep(poll_interval)
