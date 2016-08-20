from app.cache import *

if is_marked_timeline_cache():
    create_timeline_cache()
    delete_timeline_cache()
