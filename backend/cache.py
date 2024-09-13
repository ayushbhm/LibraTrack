from flask_caching import Cache

# Create a Cache instance
cache = Cache()

def init_cache(app):
    # Configure the Cache instance with Redis settings
    cache.init_app(app, config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': 'localhost',
        'CACHE_REDIS_PORT': 6379,
        'CACHE_REDIS_DB': 0,
        'CACHE_DEFAULT_TIMEOUT': 60  # Default cache timeout (in seconds)
    })
