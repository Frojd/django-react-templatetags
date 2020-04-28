class MockResponse:
    def __init__(self, data, status_code, ok=True):
        self.data = data
        self.text = data
        self.status_code = status_code
        self.ok = ok

    def raise_for_status(self):
        pass

    def json(self):
        return self.data
