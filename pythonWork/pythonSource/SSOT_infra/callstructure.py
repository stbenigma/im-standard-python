import inspect

def callers_name():
    """ returns the name of the callers function
    """
    stack=inspect.stack()
    caller=stack[2]
    return caller[3]