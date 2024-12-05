from abc import ABC, abstractmethod


class ElementFilter(ABC):
    """
    Filters if a list of Elements should be active based on an attribute value
    within the given datasource
    """

    def __init__(self, elements):
        self.datasource_cls = datasource_cls
        self.attribute_name = attribute_name

    @abstractmethod
    def filter(self, context):
        """
        Return true if the Element should be active
        """



class ElementFilter(ABC):
    """
    Filters which Element should be active based on an attribute value
    within the given datasource
    """

    def __init__(self, datasource_cls, attribute_name):
        self.datasource_cls = datasource_cls
        self.attribute_name = attribute_name

    def filter(self, context):
        """
        Return true if the Element should be active
        """
