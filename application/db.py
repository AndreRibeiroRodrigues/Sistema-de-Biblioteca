from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from filelock import Firelock

DB_PATH = Path('data/biblioteca.json')
LOCK_PATH = Path(str(DB_PATH) + '.lock')


def get_db():
    if 'tinydb' not in g:
        DB_path.parent.mkdir(parents=True, exist_ok=True)
        g.tinydb = TinyDB(DB_PATH, storage=CachingMiddleware(JSONStorage))
    return g.tinydb

def get_table(name: str):
    return get_db().table(name)

def get_lock():
    return Firelock(LOCK_PATH)