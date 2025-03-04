from PyQt5.QtCore import QObject, pyqtSignal, QMutex, QMutexLocker
from dataclasses import dataclass, field, make_dataclass
from typing import Any, Dict, Type, TypeVar, Optional
import yaml

T = TypeVar('T')

class DataStore(QObject):
    """
    DataStore is a centralized state manager for a PyQt application.
    It follows the Singleton pattern to ensure a single instance,
    and manages dataclasses and their instances in a thread-safe manner.  
    """

    _instance = None  # Class-level attribute to hold the singleton instance
    _mutex = QMutex()  # Mutex for thread safety

    # Signal to notify observers of data updates, emitting the key of the updated data
    data_updated = pyqtSignal(str)

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ method to implement the Singleton pattern.
        Ensures only one instance of DataStore is created.

        Returns:
            DataStore: The singleton instance of the DataStore.
        """
        with QMutexLocker(cls._mutex):  # Ensure thread safety
            if not cls._instance:  # Check if the instance already exists
                cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
                cls._instance._data = {}  # Dictionary to store data
                cls._instance._registry = {}  # Dictionary to register dataclasses
            return cls._instance  # Return the singleton instance

    def update_data(self, key: str, value: Any):
        """
        Update the value associated with a given key in the _data dictionary.
        Emit the data_updated signal with the key of the updated data.

        Args:
            key (str): The key for the data entry.
            value (Any): The value to be associated with the key.
        """
        with QMutexLocker(self._mutex):
            self._data[key] = value
        self.data_updated.emit(key)

    def get_data(self, key: str) -> Any:
        """
        Retrieve the value associated with a given key from the _data dictionary.

        Args:
            key (str): The key for the data entry.

        Returns:
            Any: The value associated with the key, or None if the key does not exist.
        """
        with QMutexLocker(self._mutex):
            return self._data.get(key, None)

    def create_dataclass(self, name: str, fields: Dict[str, Type]) -> Type[T]:
        """
        Create a new dataclass with the specified name and fields.
        Register the new dataclass in the _registry.

        Args:
            name (str): The name of the dataclass.
            fields (Dict[str, Type]): A dictionary of field names and their types.

        Returns:
            Type[T]: The newly created dataclass.

        Raises:
            ValueError: If the dataclass with the given name already exists.
        """
        with QMutexLocker(self._mutex):
            if name in self._registry:
                raise ValueError(f"Dataclass {name} already exists.")
            
            # Create a new dataclass with the specified fields
            new_class = make_dataclass(name, [(f, t, field(default=None)) for f, t in fields.items()])
            self._registry[name] = new_class
            return new_class

    def get_dataclass(self, name: str) -> Optional[Type[T]]:
        """
        Retrieve a registered dataclass by its name.

        Args:
            name (str): The name of the dataclass.

        Returns:
            Optional[Type[T]]: The dataclass if found, else None.
        """
        with QMutexLocker(self._mutex):
            return self._registry.get(name)

    def delete_dataclass(self, name: str):
        """
        Delete a registered dataclass by its name.

        Args:
            name (str): The name of the dataclass to be deleted.

        Raises:
            ValueError: If the dataclass with the given name does not exist.
        """
        with QMutexLocker(self._mutex):
            if name in self._registry:
                del self._registry[name]
            else:
                raise ValueError(f"Dataclass {name} does not exist.")

    def update_dataclass_instance(self, dataclass_name: str, key: str, updates: Dict[str, Any]):
        """
        Update specific attributes of a dataclass instance stored in _data.
        Ensure the dataclass and instance exist before updating.

        Args:
            dataclass_name (str): The name of the dataclass.
            key (str): The key for the dataclass instance in the _data dictionary.
            updates (Dict[str, Any]): A dictionary of attribute names and their new values.

        Raises:
            ValueError: If the dataclass is not registered or the instance does not exist.
            AttributeError: If the instance does not have one of the specified attributes.
        """
        with QMutexLocker(self._mutex):
            if dataclass_name not in self._registry:
                raise ValueError(f"Dataclass {dataclass_name} is not registered.")
            
            dataclass_instance = self._data.get(key, None)
            if not dataclass_instance:
                raise ValueError(f"No instance found for key {key}.")

            for attr, value in updates.items():
                if hasattr(dataclass_instance, attr):
                    setattr(dataclass_instance, attr, value)
                else:
                    raise AttributeError(f"{dataclass_name} has no attribute {attr}.")

            self.data_updated.emit(key)

    def get_dataclass_attribute(self, key: str, attribute: str) -> Any:
        """
        Retrieve a specific attribute from a dataclass instance stored in _data.

        Args:
            key (str): The key for the dataclass instance in the _data dictionary.
            attribute (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the attribute.

        Raises:
            ValueError: If the instance does not exist.
            AttributeError: If the instance does not have the specified attribute.
        """
        with QMutexLocker(self._mutex):
            dataclass_instance = self._data.get(key, None)
            if not dataclass_instance:
                raise ValueError(f"No instance found for key {key}.")
            
            if hasattr(dataclass_instance, attribute):
                return getattr(dataclass_instance, attribute)
            else:
                raise AttributeError(f"Instance has no attribute {attribute}.")

    def add_dataclass_attribute(self, dataclass_name: str, key: str, attribute: str, value: Any):
        """
        Add a new attribute to a dataclass instance.

        Args:
            dataclass_name (str): The name of the dataclass.
            key (str): The key for the dataclass instance in the _data dictionary.
            attribute (str): The name of the attribute to add.
            value (Any): The value to assign to the new attribute.

        Raises:
            ValueError: If the dataclass is not registered or the instance does not exist.
            AttributeError: If the instance already has the specified attribute.
        """
        with QMutexLocker(self._mutex):
            if dataclass_name not in self._registry:
                raise ValueError(f"Dataclass {dataclass_name} is not registered.")
            
            dataclass_instance = self._data.get(key, None)
            if not dataclass_instance:
                raise ValueError(f"No instance found for key {key}.")

            if not hasattr(dataclass_instance, attribute):
                setattr(dataclass_instance, attribute, value)
                self.data_updated.emit(key)
            else:
                raise AttributeError(f"Instance already has attribute {attribute}.")

    def remove_dataclass_attribute(self, dataclass_name: str, key: str, attribute: str):
        """
        Remove an attribute from a dataclass instance.

        Args:
            dataclass_name (str): The name of the dataclass.
            key (str): The key for the dataclass instance in the _data dictionary.
            attribute (str): The name of the attribute to remove.

        Raises:
            ValueError: If the dataclass is not registered or the instance does not exist.
            AttributeError: If the instance does not have the specified attribute.
        """
        with QMutexLocker(self._mutex):
            if dataclass_name not in self._registry:
                raise ValueError(f"Dataclass {dataclass_name} is not registered.")
            
            dataclass_instance = self._data.get(key, None)
            if not dataclass_instance:
                raise ValueError(f"No instance found for key {key}.")

            if hasattr(dataclass_instance, attribute):
                delattr(dataclass_instance, attribute)
                self.data_updated.emit(key)
            else:
                raise AttributeError(f"Instance has no attribute {attribute}.")

    def load_from_yaml(self, yaml_file: str, key: str, dataclass_name: str):
        """
        Load data from a YAML file, create a dataclass, and update its values.

        Args:
            yaml_file (str): Path to the YAML file.
            key (str): The key to use for storing the dataclass instance in the _data dictionary.
            dataclass_name (str): The name to register the dataclass.

        Raises:
            ValueError: If the YAML file cannot be loaded or dataclass creation fails.
        """
        with open(yaml_file, 'r') as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            raise ValueError("YAML file must represent a dictionary.")

        fields = {k: type(v) for k, v in config.items()}
        dataclass_type = self.create_dataclass(dataclass_name, fields)
        dataclass_instance = dataclass_type(**config)

        self.update_data(key, dataclass_instance)
