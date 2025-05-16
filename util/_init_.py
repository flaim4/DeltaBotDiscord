def Indelifer(id: str):
    def decorator(obj):
        obj.id = id
        return obj
    return decorator