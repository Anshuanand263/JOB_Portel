
from .extensions import mongo

def get_users_col():
    return mongo.db.users

def get_providers_col():
    return mongo.db.providers

def get_job_collections():
    return mongo.db.job_collections

def get_applicants_col():
    return mongo.db.applicants_col
