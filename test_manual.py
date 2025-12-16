#!/usr/bin/env python3
"""Manual test script to verify core functionality without API key."""

from app.store.memory import NameStore
from app.verifier.service import NameVerifier

def test_verification():
    """Test the verification logic."""
    print("Testing Name Verification System\n")
    print("=" * 50)
    
    # Create store and verifier
    store = NameStore()
    verifier = NameVerifier(store)
    
    # Test 1: Exact match
    print("\nTest 1: Exact Match")
    store.set_target("Ahmed Al-Rashid")
    result = verifier.verify("Ahmed Al-Rashid")
    print(f"Target: Ahmed Al-Rashid")
    print(f"Candidate: Ahmed Al-Rashid")
    print(f"Match: {result.match}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")
    
    # Test 2: Similar name with different punctuation
    print("\n" + "=" * 50)
    print("\nTest 2: Different Punctuation")
    store.set_target("Ahmed Al-Rashid")
    result = verifier.verify("Ahmed Al Rashid")
    print(f"Target: Ahmed Al-Rashid")
    print(f"Candidate: Ahmed Al Rashid")
    print(f"Match: {result.match}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")
    
    # Test 3: Different name
    print("\n" + "=" * 50)
    print("\nTest 3: Different Name")
    store.set_target("Ahmed Al-Rashid")
    result = verifier.verify("John Smith")
    print(f"Target: Ahmed Al-Rashid")
    print(f"Candidate: John Smith")
    print(f"Match: {result.match}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")
    
    # Test 4: Nickname matching
    print("\n" + "=" * 50)
    print("\nTest 4: Nickname Matching")
    store.set_target("William Smith")
    result = verifier.verify("Bill Smith")
    print(f"Target: William Smith")
    print(f"Candidate: Bill Smith")
    print(f"Match: {result.match}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")
    
    # Test 5: Reversed order
    print("\n" + "=" * 50)
    print("\nTest 5: Reversed Order")
    store.set_target("Ahmed Rashid")
    result = verifier.verify("Rashid Ahmed")
    print(f"Target: Ahmed Rashid")
    print(f"Candidate: Rashid Ahmed")
    print(f"Match: {result.match}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")
    
    # Test 6: Compound pattern merging
    print("\n" + "=" * 50)
    print("\nTest 6: Compound Pattern")
    store.set_target("Abdul Rahman")
    result = verifier.verify("Abdul Rahman")
    print(f"Target: Abdul Rahman")
    print(f"Candidate: Abdul Rahman")
    print(f"Match: {result.match}")
    print(f"Confidence: {result.confidence:.2f}")
    print(f"Reason: {result.reason}")
    
    print("\n" + "=" * 50)
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_verification()
