def dict_func_generator(method):
    def wrapper(text, chat, items):

        method()

    return wrapper
