import uuid
from datetime import datetime

def generate_uuid():
    return str(uuid.uuid4())


def format_created_date():
    return datetime.today().strftime("%d/%m/%Y")




