from snipssonos.shared.request_object import InvalidRequestObject, ValidRequestObject

class VolumeUpRequestObject(ValidRequestObject):
    def __init__(self,  volume_increase=None):
        self.volume_increase = volume_increase

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if 'volume_increase' in a_dictionary and not isinstance(a_dictionary['volume_increase'], int):
            invalid_request.add_error('volume_increase', 'must be an integer')

        if 'volume_increase' in a_dictionary and isinstance(a_dictionary['volume_increase'], int) and a_dictionary['volume_increase'] < 0:
            invalid_request.add_error('volume_increase', 'must be positive')

        if 'volume_increase' in a_dictionary and isinstance(a_dictionary['volume_increase'], int) and a_dictionary['volume_increase'] > 100:
            invalid_request.add_error('volume_increase', 'must be lower than 100')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_increase=a_dictionary.get('volume_increase', None)
        )


class VolumeDownRequestObject(ValidRequestObject):
    def __init__(self,  volume_decrease=None):
        self.volume_decrease = volume_decrease

    @classmethod
    def from_dict(cls, a_dictionary):
        invalid_request = InvalidRequestObject()

        if 'volume_decrease' in a_dictionary and not isinstance(a_dictionary['volume_decrease'], int):
            invalid_request.add_error('volume_decrease', 'must be an integer')

        if 'volume_decrease' in a_dictionary and isinstance(a_dictionary['volume_decrease'], int) and a_dictionary['volume_decrease'] < 0:
            invalid_request.add_error('volume_decrease', 'must be positive')

        if 'volume_decrease' in a_dictionary and isinstance(a_dictionary['volume_decrease'], int) and a_dictionary['volume_decrease'] > 100:
            invalid_request.add_error('volume_decrease', 'must be lower than 100')

        if invalid_request.has_errors():
            return invalid_request

        return cls(
            volume_decrease=a_dictionary.get('volume_decrease', None)
        )

class PlaySongRequestObject(ValidRequestObject):
    pass