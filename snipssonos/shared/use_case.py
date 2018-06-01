from snipssonos.shared.response_object import ResponseFailure

class UseCase(object):

    def execute(self, request_object):
        if not request_object:
            return ResponseFailure.build_from_invalid_request_object(request_object)

        try:
            return self.process_request(request_object)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, str(exc))
            )

    def process_request(self, request_object):
        raise NotImplementedError(
            "process_request() not implemented by UseCase class"
        )