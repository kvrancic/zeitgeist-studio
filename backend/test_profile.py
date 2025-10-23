#!/usr/bin/env python3
"""
Test script for profile creation endpoint.
"""

import requests
import io

BASE_URL = "http://localhost:8000"


def test_profile_without_files():
    """Test creating profile without file uploads."""
    print("\n=== Test 1: Profile Creation Without Files ===")

    data = {
        "company_name": "TeeWiz",
        "company_description": "TeeWiz is a print-on-demand custom apparel company that creates viral, trend-driven t-shirt designs. We blend cultural zeitgeist with wearable art, helping customers express their identity through clothing that captures the moment.",
        "brand_voice": "edgy",
    }

    response = requests.post(f"{BASE_URL}/api/profile/create", data=data)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Success: {result['message']}")
        print(f"✓ Company: {result['profile']['company_name']}")
        print(f"✓ Brand Voice: {result['profile']['brand_voice']}")
        print(f"✓ Files Processed: {result.get('files_processed', 'None')}")
    else:
        print(f"✗ Error: {response.text}")


def test_profile_with_text_file():
    """Test creating profile with text file upload."""
    print("\n=== Test 2: Profile Creation With Text File ===")

    # Create a sample brand document
    brand_doc = """
TeeWiz Brand Guidelines

Company Overview:
TeeWiz is a premium print-on-demand apparel brand that specializes in capturing cultural moments through wearable art. Founded in 2023, we've become known for our ability to identify emerging trends and translate them into viral t-shirt designs.

Brand Values:
- Cultural Awareness: We stay ahead of the curve, identifying trends before they peak
- Authentic Expression: Our designs help people express their unique identity
- Quality Craftsmanship: Premium materials meet thoughtful design
- Community First: We listen to our customers and co-create with them

Target Audience:
- Age: 18-35
- Psychographics: Culturally aware, trend-conscious, value authentic self-expression
- Interests: Pop culture, social media trends, streetwear, meme culture
- Pain Points: Generic mass-market clothing, feeling disconnected from mainstream fashion

Brand Voice:
- Edgy but not offensive
- Witty and culturally savvy
- Confident and bold
- Authentic and relatable

Tone Guidelines:
DO:
✓ Use cultural references and zeitgeist language
✓ Be bold and provocative (within reason)
✓ Show expertise in trend analysis
✓ Celebrate individuality

DON'T:
✗ Be corporate or stuffy
✗ Use outdated slang
✗ Take yourself too seriously
✗ Ignore current events

Marketing Themes:
1. "Wear the Moment" - Capturing cultural zeitgeist
2. "Express Yourself" - Individual identity through clothing
3. "Stay Ahead" - Trend-forward positioning
4. "Community Canvas" - Co-creation with customers

Product Categories:
- Viral Trend Tees (our core offering)
- Limited Edition Drops
- Custom Community Designs
- Seasonal Collections

Competitive Advantages:
- AI-powered trend analysis using proprietary algorithms
- 48-hour design-to-market turnaround
- Premium quality materials (100% organic cotton)
- Strong social media presence and engaged community
    """.strip()

    # Create file-like object
    files = {
        'files': ('brand-guidelines.txt', io.BytesIO(brand_doc.encode('utf-8')), 'text/plain')
    }

    data = {
        "company_name": "TeeWiz",
        "company_description": "TeeWiz is a print-on-demand custom apparel company that creates viral, trend-driven t-shirt designs.",
        "brand_voice": "edgy",
    }

    print("Uploading brand guidelines document...")
    response = requests.post(f"{BASE_URL}/api/profile/create", data=data, files=files)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Success: {result['message']}")
        print(f"✓ Company: {result['profile']['company_name']}")
        print(f"✓ Brand Voice: {result['profile']['brand_voice']}")
        print(f"✓ Files Processed: {result.get('files_processed')}")

        if result['profile'].get('extracted_context'):
            context = result['profile']['extracted_context']
            print(f"\n✓ Extracted Context ({len(context)} chars):")
            print(f"{context[:500]}...")
        else:
            print("\n⚠ No extracted context (summarization may have failed)")
    else:
        print(f"✗ Error: {response.text}")


def test_health():
    """Test that backend is running."""
    print("\n=== Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✓ Backend is healthy")
            return True
        else:
            print("✗ Backend returned non-200 status")
            return False
    except Exception as e:
        print(f"✗ Backend not reachable: {e}")
        return False


if __name__ == "__main__":
    print("Testing Zeitgeist Studio Profile API")
    print("=" * 50)

    if test_health():
        test_profile_without_files()
        test_profile_with_text_file()
        print("\n" + "=" * 50)
        print("Testing complete!")
    else:
        print("\n✗ Cannot proceed - backend is not running")
        print("Start backend with: cd backend && ./start_server.sh")
