"""Custom typed exception hierarchy for IndianConstitution.

All exceptions inherit from :class:`IndianConstitutionError`.
"""

from typing import Optional


class IndianConstitutionError(Exception):
    """Base exception class for all errors raised by indianconstitution."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ArticleNotFoundError(IndianConstitutionError):
    """Raised when a requested article number is not present in the corpus.

    Attributes:
        article_number: The article number string that was queried.
    """

    def __init__(self, article_number: str) -> None:
        self.article_number = article_number
        super().__init__(f"Article '{article_number}' not found in the Constitution corpus.")


class CorpusIntegrityError(IndianConstitutionError):
    """Raised when corpus data is missing, corrupted, or fails checksum validation.

    Attributes:
        path: Path to the problematic corpus file, if applicable.
        reason: Diagnostic description of the validation failure.
    """

    def __init__(self, reason: str, path: Optional[str] = None) -> None:
        self.path = path
        self.reason = reason
        msg = f"Corpus integrity error: {reason}" + (f" (file: {path})" if path else "")
        super().__init__(msg)


class InvalidAmendmentRangeError(IndianConstitutionError):
    """Raised when amendment year bounds are logically invalid (e.g., from_year > to_year).

    Attributes:
        from_year: Starting year bound.
        to_year: Ending year bound.
    """

    def __init__(self, from_year: int, to_year: int) -> None:
        self.from_year = from_year
        self.to_year = to_year
        super().__init__(f"Invalid amendment year range: from_year ({from_year}) > to_year ({to_year}).")


class DependencyMissingError(IndianConstitutionError):
    """Raised when an optional dependency required for a feature is not installed.

    Attributes:
        feature_name: Name of the requested feature.
        extra_name: Name of the optional extra to install (e.g. 'data', 'ai', 'api').
    """

    def __init__(self, feature_name: str, extra_name: str) -> None:
        self.feature_name = feature_name
        self.extra_name = extra_name
        super().__init__(
            f"Feature '{feature_name}' requires optional dependency. "
            f"Install with: pip install 'indianconstitution[{extra_name}]'"
        )


class UnsupportedFormatError(IndianConstitutionError):
    """Raised when an unsupported export format is specified.

    Attributes:
        format_requested: Format name provided by user.
        supported_formats: List of supported format names.
    """

    def __init__(self, format_requested: str) -> None:
        self.format_requested = format_requested
        self.supported_formats = ["json", "csv", "markdown", "md", "gexf", "graphml"]
        super().__init__(
            f"Unsupported export format '{format_requested}'. Supported formats: {', '.join(self.supported_formats)}."
        )
