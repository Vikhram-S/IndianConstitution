"""[DEPRECATED] Legacy monolithic module interface for backward compatibility.

This module is deprecated as of v1.5.0 and will be removed in v2.0.0.
Please use :class:`indianconstitution.Constitution` or top-level functions instead.
"""

import warnings
from typing import Any, List, Optional

from .engine import Constitution
from .models import Article

warnings.warn(
    "indianconstitution.core.legacy is deprecated as of v1.5.0 and will be removed in v2.0.0. "
    "Please import from `indianconstitution` directly.",
    DeprecationWarning,
    stacklevel=2,
)


class IndianConstitutionLegacy:
    """Deprecated legacy wrapper class around Constitution engine."""

    def __init__(self) -> None:
        """Initialize legacy wrapper."""
        self.engine = Constitution()

    def get_article(self, num: Any) -> Optional[Article]:  # noqa: ANN401
        """Legacy article lookup."""
        return self.engine.get_article(str(num))

    def search(self, query: str) -> List[Article]:
        """Legacy keyword search."""
        return self.engine.search(query)


__all__ = ["IndianConstitutionLegacy"]
