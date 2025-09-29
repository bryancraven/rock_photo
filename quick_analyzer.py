#!/usr/bin/env python3
"""
Enhanced rock analyzer with standardized fields and comparison mode
Uses literal types instead of Enums for Gemini compatibility
"""

from google import genai
from google.genai import types
from PIL import Image
import json
import os
from dotenv import load_dotenv
import time
import typing_extensions as typing
from typing import Literal
import argparse

# Define the typed schema with literal types for discrete fields
class Rock(typing.TypedDict):
    # Discrete fields using Literal types for better parsing
    primary_type: Literal["sedimentary", "igneous", "metamorphic", "unknown", "other"]
    size_category: Literal["tiny", "small", "medium", "large", "boulder", "massive"]
    weathering_state: Literal["fresh", "slightly_weathered", "moderately_weathered", "heavily_weathered", "extremely_weathered"]
    confidence_level: Literal["very_low", "low", "medium", "high", "very_high"]
    position: Literal["foreground", "midground", "background", "left", "right", "center", "top", "bottom", "multiple"]

    # Numerical fields
    confidence_value: float  # 0.0 to 1.0
    estimated_size_cm: float  # Estimated size in centimeters

    # Flexible descriptive fields for geological expertise
    specific_rock_type: str  # e.g., "limestone", "granite", "basalt"
    color_description: str  # Detailed color description
    texture_details: str  # Detailed texture description
    mineral_composition: str  # Observed minerals
    structural_features: str  # Joints, bedding, foliation, etc.
    surface_features: str  # Lichen, moss, staining, etc.
    shape_description: str  # Angular, rounded, irregular, etc.
    geological_notes: str  # Expert observations and interpretations

class RockAnalysisSummary(typing.TypedDict):
    total_rocks: int
    dominant_rock_type: Literal["sedimentary", "igneous", "metamorphic", "unknown", "other"]
    average_confidence: float
    geological_setting: str
    formation_interpretation: str
    regional_geology_notes: str
    location_context: str

class RockAnalysisResult(typing.TypedDict):
    summary: RockAnalysisSummary
    rocks: list[Rock]

class ComparisonAnalysis(typing.TypedDict):
    key_differences: list[str]
    location_impact: str
    confidence_change: float
    accuracy_assessment: str
    geological_insights: str
    recommendation: str


def analyze_rocks(image_path: str, location: str = None, use_location: bool = True):
    """
    Analyze rocks with standardized discrete fields and flexible descriptions

    Args:
        image_path: Path to the image file
        location: Optional location information
        use_location: Whether to use location in the analysis
    """
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    client = genai.Client(api_key=api_key)

    # Load and prepare image
    print(f"Loading image: {image_path}")
    image = Image.open(image_path)
    image.thumbnail([1024, 1024], Image.Resampling.LANCZOS)

    # Enhanced prompt with reasoning scaffolds (simplified for quick analysis)
    base_prompt = """
    You are a field geologist performing a rapid rock assessment. While this is a quick analysis,
    maintain scientific rigor and systematic observation.

    ═══════════════════════════════════════════════════════════════════
    QUICK ANALYSIS FRAMEWORK
    ═══════════════════════════════════════════════════════════════════

    For each rock, follow this rapid assessment process:
    1. Observe: Note key visual features (texture, color, structure)
    2. Classify: Determine primary rock type and characteristics
    3. Assess: Evaluate confidence based on feature clarity

    ═══════════════════════════════════════════════════════════════════
    CLASSIFICATION CATEGORIES
    ═══════════════════════════════════════════════════════════════════

    ┌─ PRIMARY ROCK TYPE ───────────────────────────────────────────────
    │ primary_type - Select ONE:
    │   • "sedimentary" - Layered, grainy, or massive (sandstone, limestone, shale)
    │   • "igneous" - Crystalline or glassy (granite, basalt, obsidian)
    │   • "metamorphic" - Foliated or recrystallized (schist, marble, slate)
    │   • "unknown" - Cannot determine from visible features
    │   • "other" - Unconsolidated or mixed materials
    │
    │ Quick identification tips:
    │ - Sedimentary: Look for layers, grains, fossils, rounded clasts
    │ - Igneous: Interlocking crystals (slow cooling) or fine/glassy (fast cooling)
    │ - Metamorphic: Foliation, alignment, recrystallized texture
    └────────────────────────────────────────────────────────────────────

    ┌─ SIZE CATEGORY ───────────────────────────────────────────────────
    │ size_category - Estimate largest dimension:
    │   • "tiny" - <5cm (hand sample)
    │   • "small" - 5-20cm (grapefruit to melon)
    │   • "medium" - 20-50cm (basketball to large pumpkin)
    │   • "large" - 50-100cm (beach ball to small boulder)
    │   • "boulder" - 100-200cm (large boulder)
    │   • "massive" - >200cm (very large or outcrop)
    └────────────────────────────────────────────────────────────────────

    ┌─ WEATHERING STATE ────────────────────────────────────────────────
    │ weathering_state - Degree of surface alteration:
    │   • "fresh" - Clean, unaltered surfaces
    │   • "slightly_weathered" - Minor discoloration or surface changes
    │   • "moderately_weathered" - Visible weathering, structure intact
    │   • "heavily_weathered" - Significant alteration, weakened structure
    │   • "extremely_weathered" - Heavily altered, texture obscured
    └────────────────────────────────────────────────────────────────────

    ┌─ CONFIDENCE CALIBRATION ──────────────────────────────────────────
    │ confidence_level & confidence_value:
    │   • "very_high" (0.8-1.0) - Diagnostic features clearly visible
    │   • "high" (0.6-0.8) - Good features, minor uncertainty
    │   • "medium" (0.4-0.6) - Reasonable guess, some ambiguity
    │   • "low" (0.2-0.4) - Educated guess, limited clarity
    │   • "very_low" (0.0-0.2) - Highly uncertain identification
    │
    │ Be honest about uncertainty. Consider image quality, angle, and coverage.
    └────────────────────────────────────────────────────────────────────

    ┌─ OTHER FIELDS ────────────────────────────────────────────────────
    │ • position: Location in image frame
    │ • estimated_size_cm: Best estimate of largest dimension in cm
    │
    │ DESCRIPTIVE FIELDS (detailed observations):
    │ • specific_rock_type: As specific as possible (e.g., "limestone", "granite")
    │ • color_description: Detailed color observations
    │ • texture_details: Surface and internal texture
    │ • mineral_composition: Any visible minerals
    │ • structural_features: Bedding, foliation, joints, veins
    │ • surface_features: Lichen, weathering patterns, coatings
    │ • shape_description: Overall morphology and angularity
    │ • geological_notes: Expert observations linking features to interpretation
    └────────────────────────────────────────────────────────────────────

    ═══════════════════════════════════════════════════════════════════
    SUMMARY REQUIREMENTS
    ═══════════════════════════════════════════════════════════════════

    • dominant_rock_type: Must be "sedimentary", "igneous", "metamorphic", "unknown", or "other"
    • Provide geological interpretation of the overall setting
    • Note formation processes and potential geological context
    """

    if location and use_location:
        prompt = f"""{base_prompt}

    ═══════════════════════════════════════════════════════════════════
    LOCATION CONTEXT PROVIDED
    ═══════════════════════════════════════════════════════════════════

    Location: {location}

    Use location knowledge to:
    • Consider typical regional rock types
    • Inform geological setting interpretation
    • Guide formation identification

    IMPORTANT: Visual evidence is primary. If features contradict regional
    expectations, trust what you observe and note the discrepancy. Consider
    transported specimens (glacial erratics, building stones, fill material).
    """
    else:
        prompt = f"""{base_prompt}

    ═══════════════════════════════════════════════════════════════════
    NO LOCATION CONTEXT - Visual Analysis Only
    ═══════════════════════════════════════════════════════════════════

    Analyze based purely on observable features without regional geology knowledge.
    Focus on diagnostic visual characteristics: texture, structure, mineralogy.
    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=RockAnalysisResult,
        thinking_config=types.ThinkingConfig(thinking_budget=32000)
    )

    print(f"Analyzing rocks {'with' if (location and use_location) else 'without'} location context...")
    start_time = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[image, prompt],
            config=config
        )

        elapsed = time.time() - start_time
        print(f"Response received in {elapsed:.2f} seconds")

        result = json.loads(response.text)

        # Add location to summary
        if 'summary' in result:
            result['summary']['location_context'] = location if (location and use_location) else "No location context used"

        return result

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_analyses(image_path: str, location: str):
    """
    Run analysis with and without location, then compare results

    Returns both analyses and AI-generated comparison
    """
    print("\n" + "="*60)
    print("RUNNING COMPARISON ANALYSIS")
    print("="*60)

    # Run with location
    print("\n[1/3] Analyzing WITH location context...")
    with_location = analyze_rocks(image_path, location, use_location=True)

    # Run without location
    print("\n[2/3] Analyzing WITHOUT location context...")
    without_location = analyze_rocks(image_path, location, use_location=False)

    if not with_location or not without_location:
        print("Failed to complete both analyses")
        return None, None, None

    # Generate AI comparison
    print("\n[3/3] Generating AI comparison analysis...")
    comparison = generate_comparison(with_location, without_location, location)

    return with_location, without_location, comparison


def generate_comparison(with_loc: dict, without_loc: dict, location: str) -> dict:
    """
    Use Gemini to compare the two analyses and provide insights
    """
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    client = genai.Client(api_key=api_key)

    comparison_prompt = f"""
    Compare these two rock analyses of the same image - one with location context ({location}) and one without.

    Analysis WITH location:
    {json.dumps(with_loc, indent=2)}

    Analysis WITHOUT location:
    {json.dumps(without_loc, indent=2)}

    Provide a comparison with:
    - key_differences: List the main differences in rock identification
    - location_impact: How did location knowledge affect the analysis?
    - confidence_change: Average confidence change (positive means location improved confidence)
    - accuracy_assessment: Which analysis seems more accurate and why?
    - geological_insights: What geological insights does the comparison reveal?
    - recommendation: Should location context be used for this type of image?
    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ComparisonAnalysis,
        thinking_config=types.ThinkingConfig(thinking_budget=32000)
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=comparison_prompt,
            config=config
        )

        return json.loads(response.text)
    except Exception as e:
        print(f"Comparison generation error: {e}")
        return None


def display_results(result: dict, title: str = "ROCK ANALYSIS RESULTS"):
    """
    Display analysis results in a formatted way
    """
    print("\n" + "="*60)
    print(title)
    print("="*60)

    if 'summary' in result:
        summary = result['summary']
        print("\nSUMMARY:")
        print(f"Total rocks: {summary.get('total_rocks', 0)}")
        print(f"Dominant type: {summary.get('dominant_rock_type', 'Unknown')}")
        print(f"Average confidence: {summary.get('average_confidence', 0):.2f}")
        print(f"Location context: {summary.get('location_context', 'None')}")

        # Count size distribution from rocks data
        if 'rocks' in result:
            size_counts = {}
            for rock in result['rocks']:
                size = rock.get('size_category', 'unknown')
                size_counts[size] = size_counts.get(size, 0) + 1

            print("\nSize distribution:")
            for size in ['tiny', 'small', 'medium', 'large', 'boulder', 'massive']:
                if size in size_counts:
                    print(f"  {size}: {size_counts[size]}")

    if 'rocks' in result:
        print(f"\nINDIVIDUAL ROCKS ({len(result['rocks'])} identified):")
        print("-"*60)
        for i, rock in enumerate(result['rocks'], 1):
            print(f"\nRock {i}:")
            print(f"  Type: {rock.get('primary_type', 'unknown')} ({rock.get('specific_rock_type', 'unspecified')})")
            print(f"  Size: {rock.get('size_category', 'unknown')} (~{rock.get('estimated_size_cm', 0):.0f}cm)")
            print(f"  Confidence: {rock.get('confidence_level', 'unknown')} ({rock.get('confidence_value', 0):.2f})")
            print(f"  Weathering: {rock.get('weathering_state', 'unknown')}")
            print(f"  Position: {rock.get('position', 'unknown')}")

            # Show some flexible fields
            if rock.get('color_description'):
                print(f"  Color: {rock['color_description'][:80]}...")
            if rock.get('texture_details'):
                print(f"  Texture: {rock['texture_details'][:80]}...")
            if rock.get('geological_notes'):
                print(f"  Notes: {rock['geological_notes'][:100]}...")


def main():
    """Main function with comparison mode"""
    parser = argparse.ArgumentParser(description='Enhanced rock analyzer with standardized fields')
    parser.add_argument('image', help='Path to the image file')
    parser.add_argument('--location', '-l', help='Location information')
    parser.add_argument('--compare', '-c', action='store_true',
                       help='Compare results with and without location')
    parser.add_argument('--save', '-s', action='store_true',
                       help='Save results to JSON files')

    args = parser.parse_args()

    print("="*60)
    print("ENHANCED ROCK ANALYZER")
    print("="*60)
    print(f"Image: {args.image}")
    if args.location:
        print(f"Location: {args.location}")

    if args.compare and args.location:
        # Comparison mode
        with_loc, without_loc, comparison = compare_analyses(args.image, args.location)

        if with_loc and without_loc:
            # Display both results
            display_results(with_loc, "WITH LOCATION CONTEXT")
            display_results(without_loc, "WITHOUT LOCATION CONTEXT")

            # Display comparison
            if comparison:
                print("\n" + "="*60)
                print("AI COMPARISON ANALYSIS")
                print("="*60)
                print("\nKey Differences:")
                for diff in comparison.get('key_differences', []):
                    print(f"  • {diff}")
                print(f"\nLocation Impact: {comparison.get('location_impact', 'N/A')}")
                print(f"Confidence Change: {comparison.get('confidence_change', 0):.2%}")
                print(f"Accuracy Assessment: {comparison.get('accuracy_assessment', 'N/A')}")
                print(f"Geological Insights: {comparison.get('geological_insights', 'N/A')}")
                print(f"Recommendation: {comparison.get('recommendation', 'N/A')}")

            # Save if requested
            if args.save:
                base_name = os.path.splitext(os.path.basename(args.image))[0]

                # Save all three analyses
                with open(f"analysis_with_location_{base_name}.json", 'w') as f:
                    json.dump(with_loc, f, indent=2)
                with open(f"analysis_without_location_{base_name}.json", 'w') as f:
                    json.dump(without_loc, f, indent=2)
                if comparison:
                    with open(f"analysis_comparison_{base_name}.json", 'w') as f:
                        json.dump(comparison, f, indent=2)
                print(f"\nResults saved to JSON files")

    else:
        # Single analysis mode
        result = analyze_rocks(args.image, args.location)
        if result:
            display_results(result)

            if args.save:
                output_file = f"rock_analysis_{os.path.splitext(os.path.basename(args.image))[0]}.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()