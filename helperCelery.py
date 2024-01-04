import datetime
import threading
from celery import Celery
import chess
from firebase_admin import firestore

# Initialize Celery + Redis
celery = Celery(
    __name__,
    broker="redis://127.0.0.1:6379/0",
    backend="redis://127.0.0.1:6379/0"
)

@celery.task
def listen_for_game_changes(room_id, db):
    room_ref = db.collection("Rooms")
    
    end_game = threading.Event()
    timeout = 1200  # Timeout for the game

    def on_snapshot(doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'MODIFIED':
                data = change.document.to_dict()
                playerTwo = data.get("playerTwoId")
                if playerTwo != '':
                    end_game.set()

    end_game.wait(timeout=timeout)
    room = room_ref.document(room_id)
    room.delete()

