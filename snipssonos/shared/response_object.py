class ResponseSuccess(object):

    def __init__(self, value=None):
        pass

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__

