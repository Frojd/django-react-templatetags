class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.text = data
        self.status_code = status_code

    def raise_for_status(self):
        pass

    def json(self):
        return self.data
