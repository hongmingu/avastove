POSTCHAT_START = 1000
POSTCHAT_REST_OPEN = 2000
POSTCHAT_REST_CLOSED = 3000
POSTCHAT_TEXT = 4000
POSTCHAT_PHOTO = 5000

def post_chat_kind_converter(word):
    if word == POSTCHAT_START:
        return 'start'
    elif word == POSTCHAT_TEXT:
        return 'text'
    elif word == POSTCHAT_PHOTO:
        return 'photo'

