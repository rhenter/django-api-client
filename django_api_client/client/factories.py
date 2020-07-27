from simple_model.builder import model_builder


class ResponseFactory:
    """"
    Return a API Response object
    """

    def __init__(self, response, endpoint=''):
        self.endpoint = endpoint
        self.response_name = self._get_response_name()
        self.raw = response

    def _get_response_first_name(self, endpoint):
        words = [key for key in endpoint.split('/') if key]
        response_name = words[0]
        if response_name in [f'v{i}' for i in range(10)]:
            response_name = words[1]
        return response_name

    def _get_response_name(self):
        path = self.endpoint
        if path.startswith('/'):
            path = path[1:]
        words = [key for key in path.split('?')[0].split('/') if key]
        base_name = words[0]
        if base_name in [f'v{i}' for i in range(10)]:
            base_name = words[1]

        last = words[-1]
        if len(words) > 2:
            last = words[-2]

        if base_name == last:
            response_name = base_name
        else:
            response_name = ''.join(word.capitalize() for word in [base_name, last])
        return response_name

    def as_dict(self):
        return self.raw.json()

    def as_obj(self):
        result = self.as_dict()
        return model_builder(result, class_name=self.response_name)

    def __repr__(self):
        return '<{} object>'.format(self.response_name)
