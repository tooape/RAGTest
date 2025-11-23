"""Query preprocessing for v0.1 and v0.2 strategies.

Implements query understanding features from the obsidianrag plugin:
- v0.1: Basic tag parsing (explicit tags only)
- v0.2: Auto tag injection, person name expansion, query signals
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from loguru import logger


@dataclass
class QuerySignals:
    """Detected query signals (v0.2 feature)."""

    is_meeting: bool = False
    is_1x1: bool = False
    is_staff: bool = False
    is_temporal: bool = False
    intent: str = "browse"  # who, what, when, how, browse


@dataclass
class ProcessedQuery:
    """Result of query processing."""

    text: str                           # Cleaned query text (tags removed)
    tags: List[str]                     # Extracted/injected tags
    auto_injected: bool = False         # Whether tags were auto-injected (v0.2)
    signals: Optional[QuerySignals] = None  # Query signals (v0.2)
    expanded_variants: Optional[List[str]] = None  # Query variants (v0.2)


class QueryProcessor(ABC):
    """Base class for query processors."""

    @abstractmethod
    def process(self, query: str) -> ProcessedQuery:
        """Process a query and return enhanced version."""
        pass

    def _extract_explicit_tags(self, query: str) -> tuple[str, List[str]]:
        """Extract explicit #tags from query.

        Returns:
            Tuple of (text_without_tags, list_of_tags)
        """
        tokens = query.strip().split()
        text_tokens = []
        tags = []

        for token in tokens:
            if token.startswith('#'):
                # Extract tag (remove # prefix and handle nested tags)
                tag = token[1:]
                if '/' in tag:
                    # For #meetings/1x1, add both "meetings" and "meetings/1x1"
                    parts = tag.split('/')
                    tags.append(parts[0])
                    tags.append(tag)
                else:
                    tags.append(tag)
            else:
                text_tokens.append(token)

        return ' '.join(text_tokens), tags


class QueryProcessorV01(QueryProcessor):
    """Query processor for v0.1 (basic tag parsing only)."""

    def process(self, query: str) -> ProcessedQuery:
        """Process query with v0.1 logic (explicit tags only)."""
        text, tags = self._extract_explicit_tags(query)

        return ProcessedQuery(
            text=text if text else query,  # Fallback to original if all tags
            tags=tags,
            auto_injected=False,
            signals=None,
            expanded_variants=None,
        )


class QueryProcessorV02(QueryProcessor):
    """Query processor for v0.2 (auto tag injection + person expansion)."""

    # Tag injection patterns (from QueryParser.ts)
    MEETING_PATTERNS = re.compile(r'\b(meeting|met|discuss|talked|spoke)\b', re.IGNORECASE)
    ONE_ON_ONE_PATTERNS = re.compile(r'\b(1x1|one-on-one|1:1|one on one)\b', re.IGNORECASE)
    STAFF_PATTERNS = re.compile(r'\bstaff\s+meeting\b', re.IGNORECASE)
    TEMPORAL_PATTERNS = re.compile(r'\b(recent|latest|last\s+time|most\s+recent|last)\b', re.IGNORECASE)

    # Intent patterns (from QueryParser.ts)
    WHO_PATTERNS = re.compile(r'^\s*who\b', re.IGNORECASE)
    WHAT_PATTERNS = re.compile(r'^\s*what\b', re.IGNORECASE)
    WHEN_PATTERNS = re.compile(r'^\s*when\b', re.IGNORECASE)
    HOW_PATTERNS = re.compile(r'^\s*how\b', re.IGNORECASE)

    def __init__(self, vault_dir: Optional[str] = None):
        """Initialize v0.2 query processor.

        Args:
            vault_dir: Optional path to vault directory for person name extraction
        """
        self.person_names = {}  # firstName -> [fullNames]

        if vault_dir:
            self._load_person_names(vault_dir)

    def _load_person_names(self, vault_dir: str) -> None:
        """Load person names from People/*.md files.

        Builds a mapping: firstName -> [fullName1, fullName2, ...]
        """
        vault_path = Path(vault_dir)
        people_dir = vault_path / "People"

        if not people_dir.exists():
            logger.warning(f"People directory not found: {people_dir}")
            return

        # Extract names from People/*.md filenames
        for person_file in people_dir.glob("*.md"):
            full_name = person_file.stem  # "Brian Eriksson"

            # Extract first name
            first_name = full_name.split()[0]  # "Brian"

            if first_name not in self.person_names:
                self.person_names[first_name] = []

            self.person_names[first_name].append(full_name)

        logger.info(f"Loaded {len(self.person_names)} person names from {people_dir}")

    def process(self, query: str) -> ProcessedQuery:
        """Process query with v0.2 logic (auto tag injection + person expansion)."""
        # 1. Detect query signals first
        signals = self._detect_signals(query)

        # 2. Extract explicit tags
        text, tags = self._extract_explicit_tags(query)

        # 3. Auto-inject tags based on detected patterns (only if no explicit tags)
        auto_injected = False
        if not tags:
            if signals.is_1x1:
                tags.extend(['meetings', 'meetings/1x1'])
                auto_injected = True
            elif signals.is_staff:
                tags.extend(['meetings', 'meetings/staff'])
                auto_injected = True
            elif signals.is_meeting:
                tags.append('meetings')
                auto_injected = True

        if auto_injected:
            logger.debug(f"Auto-injected tags: {', '.join(tags)}")

        # 4. Generate query variants with person name expansion
        expanded_variants = self._expand_person_names(text if text else query)

        return ProcessedQuery(
            text=text if text else query,
            tags=tags,
            auto_injected=auto_injected,
            signals=signals,
            expanded_variants=expanded_variants,
        )

    def _detect_signals(self, query: str) -> QuerySignals:
        """Detect query signals and classify intent."""
        # Pattern detection
        is_meeting = bool(self.MEETING_PATTERNS.search(query))
        is_1x1 = bool(self.ONE_ON_ONE_PATTERNS.search(query))
        is_staff = bool(self.STAFF_PATTERNS.search(query))
        is_temporal = bool(self.TEMPORAL_PATTERNS.search(query))

        # Intent classification
        if self.WHO_PATTERNS.match(query):
            intent = "who"
        elif self.WHAT_PATTERNS.match(query):
            intent = "what"
        elif self.WHEN_PATTERNS.match(query):
            intent = "when"
        elif self.HOW_PATTERNS.match(query):
            intent = "how"
        else:
            intent = "browse"

        return QuerySignals(
            is_meeting=is_meeting,
            is_1x1=is_1x1,
            is_staff=is_staff,
            is_temporal=is_temporal,
            intent=intent,
        )

    def _expand_person_names(self, query: str) -> List[str]:
        """Expand person names in query.

        Example: "Brian" -> ["Brian", "Brian Eriksson"]

        Returns:
            List of query variants with expanded person names
        """
        if not self.person_names:
            return [query]  # No person names loaded

        variants = [query]  # Always include original

        # Check each word in query against first names
        words = query.split()
        for i, word in enumerate(words):
            # Strip punctuation for matching
            clean_word = word.strip('.,!?:;')

            if clean_word in self.person_names:
                # Generate variants for each full name
                for full_name in self.person_names[clean_word]:
                    # Replace first name with full name
                    new_words = words.copy()
                    new_words[i] = full_name
                    variant = ' '.join(new_words)

                    if variant != query:  # Don't duplicate original
                        variants.append(variant)

        if len(variants) > 1:
            logger.debug(f"Expanded '{query}' to {len(variants)} variants")

        return variants


def create_query_processor(version: str = "v0.2", vault_dir: Optional[str] = None) -> QueryProcessor:
    """Factory function to create query processor.

    Args:
        version: "v0.1" or "v0.2"
        vault_dir: Optional vault directory for v0.2 person name expansion

    Returns:
        QueryProcessor instance
    """
    if version == "v0.1":
        return QueryProcessorV01()
    elif version == "v0.2":
        return QueryProcessorV02(vault_dir=vault_dir)
    else:
        raise ValueError(f"Unknown version: {version}. Use 'v0.1' or 'v0.2'")
