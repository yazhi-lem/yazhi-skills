"""Registry helpers: providers, scorers, suites, and datasets by name.

Every plug-in point is a name -> factory mapping so config files can name a
component as a string and the CLI can list what is available.
"""

from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Type


class RegistryError(KeyError):
    pass


class Registry:
    """A tiny name -> factory registry with helpful error messages."""

    def __init__(self, label: str) -> None:
        self.label = label
        self._items: Dict[str, Callable] = {}
        self._aliases: Dict[str, str] = {}

    def register(self, name: str, factory: Callable, *, aliases: Iterable[str] = ()) -> None:
        key = name.strip().lower()
        if key in self._items:
            raise RegistryError(f"{self.label} {name!r} is already registered")
        self._items[key] = factory
        for alias in aliases:
            self._aliases[alias.strip().lower()] = key

    def get(self, name: str) -> Callable:
        key = name.strip().lower()
        key = self._aliases.get(key, key)
        if key not in self._items:
            known = ", ".join(sorted(self.names())) or "(none)"
            raise RegistryError(f"unknown {self.label} {name!r}; known: {known}")
        return self._items[key]

    def names(self) -> List[str]:
        return sorted(self._items)

    def __contains__(self, name: str) -> bool:
        key = name.strip().lower()
        return key in self._items or key in self._aliases


class UniqueRegistry:
    """Like ``Registry`` but instances are constructed once and shared."""

    def __init__(self, label: str) -> None:
        self.label = label
        self._instances: Dict[str, int] = {}
        self._factories: Dict[str, Callable[[], object]] = {}
        self._values: List[object] = []

    def register(self, name: str, factory: Callable[[], object]) -> None:
        key = name.strip().lower()
        if key in self._factories:
            raise RegistryError(f"{self.label} {name!r} is already registered")
        self._factories[key] = factory

    def get(self, name: str) -> object:
        key = name.strip().lower()
        if key not in self._factories:
            known = ", ".join(sorted(self._factories)) or "(none)"
            raise RegistryError(f"unknown {self.label} {name!r}; known: {known}")
        return self._factories[key]()

    def names(self) -> List[str]:
        return sorted(self._factories)


def assert_type(value: object, expected: Type, registry: str, name: str) -> None:
    if not isinstance(value, expected):
        raise RegistryError(
            f"{registry} {name!r} produced {type(value).__name__}, "
            f"expected {expected.__name__}"
        )
