import redis
import yaml

def load_config():
    
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

def get_redis_connection():
    
    return redis.Redis(
        host=config["redis"]["host"],
        port=config["redis"]["port"],
        db=0,
        decode_responses=True,
        username=config["redis"]["user"],
        password=config["redis"]["password"],
    )

redis_connection = get_redis_connection()
