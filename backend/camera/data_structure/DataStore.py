import sys
import pathlib as path

sys.path.append(str(path.Path(__file__).parent.resolve()))

import threading
from event_bus import EventBus
from typing import Any

FILE_path = path.Path(__file__).parent.parent.resolve()


class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances.get(cls, None)


class DataStore(metaclass=SingletonMeta):
    """
    DataStore is a centralized state manager for a Python application.
    It manages variables in a thread-safe manner.
    """

    def __init__(self):
        self._data = {}
        self._event_bus = EventBus()
        self._lock = threading.Lock()

    def update_data(self, key: str, value: Any):
        """
        INFO: Update or add the value associated with a given key in the _data dictionary.
        ARGS:
            key: str - The key to update or add to the _data dictionary.
            value: Any - The value to update or add to the _data dictionary.
        RETURNS:
            None
        """
        with self._lock:
            is_update = key in self._data
            self._data[key] = value
            action = "update" if is_update else "add"

            self._notify_data_updated(key, value, action)

    def get_data(self, key: str) -> Any:
        """
        INFO: Retrieve the value associated with a given key from the _data dictionary.
        ARGS:
            key: str - The key to retrieve the value from the _data dictionary.
        RETURNS:
            Any - The value associated with the given key, or None if the key does not exist.
        """
        with self._lock:
            if key not in self._data:
                print("Attempt to get data that hasn't been registered")
                return None
            value = self._data.get(key)
            return value

    def delete_data(self, key: str):
        """
        INFO: Delete the value associated with a given key from the _data dictionary.
        ARGS:
            key: str - The key to delete from the _data dictionary.
        RETURNS:
            None
        """
        with self._lock:
            if key in self._data:
                del self._data[key]
                self._notify_data_updated(key, None, "delete")
            else:
                raise ValueError(f"Key {key} does not exist.")

    def on_update(self, key, callback):
        """Subscribe to updates for a specific key."""
        with self._lock:
            if key not in self._data:
                self._data[key] = []
            self._data[key].append(callback)

    def _notify_data_updated(self, key: str, data: Any, action: str):
        """
        INFO: Notify subscribers about data updates.
        ARGS:
            key: str - The key associated with the data update.
            data: Any - The updated data.
            action: str - The action performed on the data.
        RETURNS:
            None
        """
        data_info = {"action": action, "data": data}
        channel = "data" + action
        # self._event_bus.emit(event_name=key, data=data_info, channel=channel)
