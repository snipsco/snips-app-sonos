class Error(object):
    pass

class ParameterError(Error):
    def __init__(self, parameter):
        self.parameter = parameter


class SystemError(Error):
    pass


class ResourceError(Error):
    pass


class OutOfRangeError(ParameterError):
    def __init__(self, parameter, lower_bound, higher_bound):
        super(OutOfRangeError, self).__init__(parameter)

        self.lower_bound = lower_bound
        self.higher_bound = higher_bound


class WrongTypeParameterError(ParameterError):
    pass


class MissingParameterError(ParameterError):
    pass



class Parameter(object):
    def get_description(self, language):
        getattr(self, language)

class Volume(Parameter):
    fr = "volume"
    en = "volume"
