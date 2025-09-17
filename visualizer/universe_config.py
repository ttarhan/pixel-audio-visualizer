from dataclasses import dataclass, field


@dataclass(kw_only=True)
class UniverseConfig:
    """
    Defines the configuration parameters for a universe
    """

    multicast: bool = field(default=True)
    destination: str= field(default=None)