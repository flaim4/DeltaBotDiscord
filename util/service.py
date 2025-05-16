

class ServiceRegistry:
    _services = {}

    @classmethod
    def register(cls, name, service):
        cls._services[name] = service

    @classmethod
    def get(cls, name):
        return cls._services[name]

    @classmethod
    def clear(cls):
        cls._services.clear()

