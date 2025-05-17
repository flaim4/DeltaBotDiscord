from disnake.ext import commands
from dataclasses import dataclass
import disnake
import inspect

@dataclass
class OnMessage:
    bot : commands.Bot
    message : disnake.Message

@dataclass
class OnReady:
    bot : commands.Bot

class EventBus:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type, listener):
        self._listeners.setdefault(event_type, []).append(listener)

    def unsubscribe(self, event_type, listener):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)
            if not self._listeners[event_type]:
                del self._listeners[event_type]

    async def post(self, event):
        for listener in self._listeners.get(type(event), []):
            if inspect.iscoroutinefunction(listener):
                await listener(event)
            else:
                listener(event)

bus = EventBus()

def subscribe(event_type):
    def wrapper(func):
        func._event_type = event_type
        return func
    return wrapper

def auto_subscribe(obj, bus: EventBus):
    for attr_name in dir(obj):
        attr = getattr(obj, attr_name)
        if callable(attr) and hasattr(attr, "_event_type"):
            bus.subscribe(attr._event_type, attr)