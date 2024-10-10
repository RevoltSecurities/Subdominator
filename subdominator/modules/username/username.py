import os
def get_username():
    try:
        username = os.getlogin()
    except OSError:
        username = os.getenv('USER') or os.getenv('LOGNAME') or os.getenv('USERNAME') or 'Unknown User'
    except Exception as e:
        username = "Unknown User"    
    return username