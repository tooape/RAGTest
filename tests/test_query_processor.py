"""Test query processors v0.1 and v0.2."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.query_processor import QueryProcessorV01, QueryProcessorV02


def test_v01_basic():
    """Test v0.1 processor with basic queries."""
    processor = QueryProcessorV01()

    # Test 1: No tags
    result = processor.process("who's the PsW PM?")
    assert result.text == "who's the PsW PM?"
    assert result.tags == []
    assert result.auto_injected is False
    print("✓ v0.1: No tags query")

    # Test 2: Explicit tags
    result = processor.process("photoshop #meetings")
    assert result.text == "photoshop"
    assert "meetings" in result.tags
    assert result.auto_injected is False
    print("✓ v0.1: Explicit tags")

    # Test 3: Meeting keywords (should NOT auto-inject)
    result = processor.process("What did I discuss with Ritu")
    assert "meetings" not in result.tags
    assert result.auto_injected is False
    print("✓ v0.1: Meeting keywords (no auto-injection)")


def test_v02_auto_tags():
    """Test v0.2 processor with auto tag injection."""
    processor = QueryProcessorV02()

    # Test 1: Meeting keyword (should auto-inject #meetings)
    result = processor.process("What did I discuss with Ritu")
    assert "meetings" in result.tags
    assert result.auto_injected is True
    assert result.signals.is_meeting is True
    print("✓ v0.2: Auto-inject #meetings for 'discuss'")

    # Test 2: 1x1 keyword (should inject #meetings and #meetings/1x1)
    result = processor.process("Brian 1x1")
    assert "meetings" in result.tags
    assert "meetings/1x1" in result.tags
    assert result.auto_injected is True
    assert result.signals.is_1x1 is True
    print("✓ v0.2: Auto-inject #meetings/1x1 for '1x1'")

    # Test 3: Staff meeting
    result = processor.process("staff meeting notes")
    assert "meetings" in result.tags
    assert "meetings/staff" in result.tags
    assert result.auto_injected is True
    assert result.signals.is_staff is True
    print("✓ v0.2: Auto-inject #meetings/staff for 'staff meeting'")

    # Test 4: Temporal keyword
    result = processor.process("recent updates on Intent AI")
    assert result.signals.is_temporal is True
    print("✓ v0.2: Detect temporal signal for 'recent'")

    # Test 5: Explicit tags (should NOT auto-inject)
    result = processor.process("What did I discuss with Ritu #meetings")
    assert "meetings" in result.tags
    assert result.auto_injected is False  # Already has explicit tag
    print("✓ v0.2: No auto-injection when explicit tags present")


def test_v02_intent():
    """Test v0.2 intent classification."""
    processor = QueryProcessorV02()

    tests = [
        ("who's the PsW PM?", "who"),
        ("what are the Q1 priorities?", "what"),
        ("when did we launch?", "when"),
        ("how does temporal retrieval work?", "how"),
        ("show me Intent AI docs", "browse"),
    ]

    for query, expected_intent in tests:
        result = processor.process(query)
        assert result.signals.intent == expected_intent, f"Expected {expected_intent}, got {result.signals.intent}"
        print(f"✓ v0.2: Intent '{expected_intent}' for '{query}'")


def test_v02_person_expansion():
    """Test v0.2 person name expansion."""
    # Create processor with test vault
    vault_dir = Path(__file__).parent.parent / "vault copy"

    if not vault_dir.exists():
        print("⊘ Skipping person expansion test (vault not found)")
        return

    processor = QueryProcessorV02(vault_dir=str(vault_dir))

    # Test person name expansion
    # Note: This will only work if People/*.md files exist
    if processor.person_names:
        # Find a person name to test
        first_name = list(processor.person_names.keys())[0]
        full_names = processor.person_names[first_name]

        result = processor.process(f"What did {first_name} say?")

        # Should have at least 2 variants: original + expanded
        assert len(result.expanded_variants) >= 2
        assert result.expanded_variants[0] == f"What did {first_name} say?"

        # Check that full name variants were created
        for full_name in full_names:
            expected = f"What did {full_name} say?"
            assert expected in result.expanded_variants, f"Expected '{expected}' in variants"

        print(f"✓ v0.2: Person expansion for '{first_name}' -> {len(result.expanded_variants)} variants")
    else:
        print("⊘ Skipping person expansion test (no person names found)")


if __name__ == "__main__":
    print("Testing Query Processors\n")

    print("=== v0.1 Tests ===")
    test_v01_basic()

    print("\n=== v0.2 Auto Tag Injection ===")
    test_v02_auto_tags()

    print("\n=== v0.2 Intent Classification ===")
    test_v02_intent()

    print("\n=== v0.2 Person Name Expansion ===")
    test_v02_person_expansion()

    print("\n✅ All tests passed!")
