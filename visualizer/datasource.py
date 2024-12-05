from abc import ABC, abstractmethod
from typing import TypeVar, Type

T = TypeVar('T', bound='DataSource')

class DataSource(ABC):
    """
    A source of data (audio, CV, etc) used by effects
    """

    @classmethod
    def from_context(cls: Type[T], context) -> T:
        return context.get(cls.context_key())
    
    @classmethod
    def context_key(cls):
        """
        Returns the default key to use inside of a context for this data source type
        """

        return cls.__name__
    
    @abstractmethod
    def start(self):
        """
        Start the datasource
        """

    @abstractmethod
    def process(self):
        """
        Runs once each clock cycle for the data source to prep data that will then be accessed
        as needed by effects. Return value is discarded, as effects will read attributes from the
        DataSource directly.
        """
