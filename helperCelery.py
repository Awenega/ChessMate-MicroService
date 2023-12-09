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


@celery.task
def listen_for_game_changes(room_id, db, timeout=6000):
    end_game = threading.Event()

    # Create a callback on_snapshot function to capture changes
    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f"Received document snapshot: {doc.id}")
        end_game.set()

    room_ref = db.collection("Rooms").document(room_id)
    doc_watch = room_ref.on_snapshot(on_snapshot)

    end_game.wait(timeout=timeout)
    doc_watch.unsubscribe()
