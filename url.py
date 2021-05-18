from urllib.parse import urlparse

def tracker_type(announce):
    url = urlparse(announce) 
    return url.scheme
