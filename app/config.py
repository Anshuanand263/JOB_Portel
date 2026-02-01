from .extensions import os
class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    SECRET_KEY = "sdgdsfgdsgdg"
