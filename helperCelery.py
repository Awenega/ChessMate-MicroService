# tasks.py (Separate file for Celery tasks)
import threading
from time import sleep
from celery import Celery

# Initialize Celeris + Redis
celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

delete_done = threading.Event()


def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f"Received document snapshot: {doc.id}")
    delete_done.set()


@celery.task
def handle_game_state(room_id, db):
    doc_watch = db.collection("Rooms").document(
        room_id).on_snapshot(on_snapshot)
    print(f"Updating game state in room {room_id}")
