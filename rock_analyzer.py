#!/usr/bin/env python3
"""
Geologically-comprehensive rock analyzer with professional standardization
Implements proper geological classifications and terminology
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

# Professional geological schema with comprehensive standardization
class Rock(typing.TypedDict):
    # PRIMARY CLASSIFICATION - More detailed categories
    rock_class: Literal[
        "igneous_volcanic",      # Extrusive igneous (basalt, rhyolite)
        "igneous_plutonic",      # Intrusive igneous (granite, gabbro)
        "igneous_hypabyssal",    # Shallow intrusive (dolerite, porphyry)
        "sedimentary_clastic",   # Sandstone, shale, conglomerate
        "sedimentary_chemical",  # Limestone, dolomite, evaporites
        "sedimentary_organic",   # Coal, diatomite
        "metamorphic_foliated",  # Schist, gneiss, slate
        "metamorphic_nonfoliated", # Marble, quartzite, hornfels
        "unconsolidated",        # Soil, sand, gravel
        "unknown"
    ]

    # SIZE CLASSIFICATION - Wentworth scale aligned
    size_class: Literal[
        "clay_silt",    # <0.0625mm particles
        "sand",         # 0.0625-2mm particles
        "granule",      # 2-4mm
        "pebble",       # 4-64mm
        "cobble",       # 64-256mm
        "boulder",      # 256-4096mm
        "block",        # >4096mm
        "outcrop"       # Bedrock exposure
    ]

    # GRAIN SIZE - For crystalline/clastic rocks
    grain_size: Literal[
        "cryptocrystalline",  # <0.1mm
        "very_fine",          # 0.1-0.5mm
        "fine",               # 0.5-1mm
        "medium",             # 1-5mm
        "coarse",             # 5-30mm
        "very_coarse",        # 30-100mm
        "pegmatitic",         # >100mm
        "mixed",              # Variable grain sizes
        "not_applicable"      # For glassy or massive rocks
    ]

    # WEATHERING CLASSIFICATION - More specific
    weathering_grade: Literal[
        "fresh",              # W0 - No visible weathering
        "slight",             # W1 - Slight discoloration
        "moderate",           # W2 - <50% weathered
        "high",               # W3 - >50% weathered
        "complete",           # W4 - All minerals weathered
        "residual_soil"       # W5 - Completely decomposed
    ]

    # WEATHERING TYPE
    weathering_type: Literal[
        "none",
        "mechanical",         # Frost wedging, abrasion
        "chemical",           # Solution, oxidation, hydrolysis
        "biological",         # Root wedging, lichen
        "mixed",             # Multiple types
        "spheroidal",        # Rounded weathering
        "exfoliation"        # Sheet-like weathering
    ]

    # HARDNESS - Mohs scale ranges
    hardness_class: Literal[
        "very_soft",     # 1-2 Mohs (talc, gypsum)
        "soft",          # 2-3 Mohs (calcite)
        "medium",        # 3-5 Mohs (apatite)
        "hard",          # 5-7 Mohs (quartz, feldspar)
        "very_hard"      # 7-10 Mohs (topaz, corundum)
    ]

    # STRUCTURE
    primary_structure: Literal[
        "massive",           # No visible structure
        "layered",          # Bedding planes
        "foliated",         # Metamorphic layering
        "vesicular",        # Gas bubbles (volcanic)
        "amygdaloidal",     # Filled vesicles
        "porphyritic",      # Large crystals in fine matrix
        "brecciated",       # Angular fragments
        "conglomeratic",    # Rounded fragments
        "crystalline",      # Visible crystal structure
        "concretionary"     # Spherical structures
    ]

    # FRACTURE PATTERN
    fracture_type: Literal[
        "conchoidal",       # Shell-like (obsidian, flint)
        "irregular",        # Random breakage
        "splintery",        # Sharp splinters
        "blocky",           # Cubic blocks
        "platy",            # Flat sheets
        "columnar",         # Hexagonal columns (basalt)
        "joint_controlled", # Following joint sets
        "none_visible"      # No clear fracture pattern
    ]

    # ALTERATION
    alteration_type: Literal[
        "unaltered",
        "oxidized",         # Rust, iron staining
        "silicified",       # Quartz replacement
        "carbonatized",     # Carbonate alteration
        "chloritized",      # Green alteration
        "sericitized",      # White mica alteration
        "kaolinized",       # Clay alteration
        "mineralized",      # Ore minerals present
        "metamorphosed",    # Heat/pressure alteration
        "hydrothermal"      # Hot water alteration
    ]

    # COLOR PATTERN
    color_pattern: Literal[
        "uniform",          # Single color
        "mottled",         # Irregular patches
        "banded",          # Regular bands
        "spotted",         # Distinct spots
        "veined",          # Mineral veins
        "gradational"      # Gradual color change
    ]

    # GEOLOGICAL CONTEXT
    geological_context: Literal[
        "in_situ_outcrop",  # Bedrock in place
        "displaced_block",  # Moved but local
        "float",            # Transported unknown distance
        "talus",            # Slope debris
        "glacial_erratic",  # Glacially transported
        "stream_cobble",    # Water transported
        "artificial",       # Human-placed
        "unknown_context"
    ]

    # CONFIDENCE
    confidence_level: Literal["very_low", "low", "medium", "high", "very_high"]

    # POSITION IN IMAGE
    image_position: Literal["foreground", "midground", "background", "left", "right", "center", "multiple"]

    # NUMERICAL FIELDS
    confidence_value: float        # 0.0 to 1.0
    estimated_diameter_cm: float   # Largest dimension in cm
    visible_minerals_count: int    # Number of identifiable minerals

    # DETAILED DESCRIPTIVE FIELDS (flexibility preserved)
    specific_rock_name: str        # E.g., "biotite granite", "oolitic limestone"
    color_details: str              # Full color description
    texture_description: str       # Detailed texture observations
    mineral_assemblage: str         # List of visible minerals
    surface_features: str           # Lichen, moss, coatings, stains
    structural_features: str        # Joints, folds, faults, veins
    shape_description: str          # Overall morphology
    luster_description: str         # Metallic, vitreous, dull, etc.
    special_features: str           # Fossils, crystals, xenoliths
    field_notes: str               # Professional geological observations
    likely_formation: str          # Suspected geological formation
    age_estimate: str              # Geological age if determinable


class GeologicalSummary(typing.TypedDict):
    total_rocks: int
    dominant_rock_class: str
    secondary_rock_class: str
    average_grain_size: str
    weathering_assessment: str
    structural_geology: str
    geological_setting: str
    tectonic_interpretation: str
    depositional_environment: str
    metamorphic_grade: str
    economic_geology_notes: str
    regional_geology_context: str
    recommended_analyses: list[str]
    location_used: str


class GeologicalAnalysisResult(typing.TypedDict):
    summary: GeologicalSummary
    rocks: list[Rock]
    geological_interpretation: str
    confidence_assessment: str


def analyze_rocks_geological(image_path: str, location: str = None, use_location: bool = True):
    """
    Perform comprehensive geological analysis of rocks in image

    Args:
        image_path: Path to the image file
        location: Optional location information
        use_location: Whether to use location in analysis
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

    # Professional geological analysis prompt with reasoning scaffolds
    prompt = """
    You are an experienced field geologist conducting a systematic geological analysis of rocks in this image.
    Your analysis will be used for scientific documentation, so apply rigorous field geology principles.

    ═══════════════════════════════════════════════════════════════════
    ANALYTICAL FRAMEWORK - Use Your Extended Thinking Capability
    ═══════════════════════════════════════════════════════════════════

    In your thinking process, follow this systematic approach for each rock:

    1. OBSERVATION PHASE
       - Systematically observe all visible features without interpretation
       - Note texture, color, structure, grain size, weathering patterns
       - Identify any distinctive features (crystals, fossils, layering, vesicles)
       - Assess scale and context clues

    2. INTERPRETATION PHASE
       - What do these features tell you about rock origin?
       - Consider multiple hypotheses (e.g., could this be volcanic OR contact metamorphic?)
       - Evaluate evidence strength for each hypothesis
       - Note any conflicting or ambiguous indicators

    3. CLASSIFICATION PHASE
       - Select the most appropriate standardized categories
       - Justify your classifications based on observed features
       - Assign confidence based on feature clarity and diagnostic certainty
       - Use "unknown" only when truly indeterminate, not when moderately uncertain

    ═══════════════════════════════════════════════════════════════════
    STANDARDIZED CLASSIFICATION SYSTEM
    ═══════════════════════════════════════════════════════════════════

    For each rock, select from these precise categories. Context provided to guide decisions:

    ┌─ ROCK CLASSIFICATION ─────────────────────────────────────────────
    │ rock_class - Primary genetic classification:
    │   • "igneous_volcanic" - Extrusive: basalt, rhyolite, andesite, tuff
    │   • "igneous_plutonic" - Intrusive: granite, gabbro, diorite
    │   • "igneous_hypabyssal" - Shallow intrusive: porphyry, dolerite
    │   • "sedimentary_clastic" - Fragment-based: sandstone, shale, conglomerate
    │   • "sedimentary_chemical" - Precipitated: limestone, dolomite, evaporites, tufa
    │   • "sedimentary_organic" - Biogenic: coal, diatomite
    │   • "metamorphic_foliated" - Layered: schist, gneiss, slate, phyllite
    │   • "metamorphic_nonfoliated" - Massive: marble, quartzite, hornfels
    │   • "unconsolidated" - Loose: soil, sand, gravel
    │   • "unknown" - Truly indeterminate only
    │
    │ Decision guide: Volcanic rocks show rapid cooling (fine grain, vesicles).
    │ Plutonic rocks show slow cooling (coarse, interlocking crystals).
    │ Sedimentary clastic shows grains/fragments. Chemical shows crystalline/massive texture.
    │ Metamorphic foliated shows alignment. Consider transition zones carefully.
    └────────────────────────────────────────────────────────────────────

    ┌─ SIZE CLASSIFICATION (Wentworth Scale) ───────────────────────────
    │ size_class - Particle or specimen size:
    │   • "clay_silt" - <0.0625mm particles (feels smooth, not gritty)
    │   • "sand" - 0.0625-2mm (gritty, individual grains barely visible)
    │   • "granule" - 2-4mm (small pebbles, pea-sized)
    │   • "pebble" - 4-64mm (thumbnail to fist-sized)
    │   • "cobble" - 64-256mm (fist to bowling ball)
    │   • "boulder" - 256-4096mm (larger than basketball)
    │   • "block" - >4096mm (very large, typically >4m)
    │   • "outcrop" - Bedrock exposure, not individual clast
    │
    │ Note: For clastic rocks, classify by clast size. For crystalline rocks,
    │ classify by overall specimen size unless describing component grain sizes.
    └────────────────────────────────────────────────────────────────────

    ┌─ GRAIN/CRYSTAL SIZE ──────────────────────────────────────────────
    │ grain_size - Internal texture scale:
    │   • "cryptocrystalline" - <0.1mm (appears smooth, no visible grains)
    │   • "very_fine" - 0.1-0.5mm (hand lens needed)
    │   • "fine" - 0.5-1mm (just visible to naked eye)
    │   • "medium" - 1-5mm (clearly visible grains/crystals)
    │   • "coarse" - 5-30mm (large distinct grains)
    │   • "very_coarse" - 30-100mm (very large crystals)
    │   • "pegmatitic" - >100mm (giant crystals)
    │   • "mixed" - Multiple distinct grain sizes (porphyritic, conglomerate)
    │   • "not_applicable" - Glassy, massive, or amorphous
    └────────────────────────────────────────────────────────────────────

    ┌─ WEATHERING ASSESSMENT ───────────────────────────────────────────
    │ weathering_grade (Standard rock weathering scale):
    │   • "fresh" - W0: No visible alteration, fresh surfaces
    │   • "slight" - W1: Discoloration, minor surface changes
    │   • "moderate" - W2: <50% minerals weathered, structure intact
    │   • "high" - W3: >50% weathered, structure weakening
    │   • "complete" - W4: All minerals altered, original texture obscured
    │   • "residual_soil" - W5: Complete decomposition to soil
    │
    │ weathering_type - Dominant process:
    │   • "mechanical" - Physical: frost wedging, thermal, abrasion
    │   • "chemical" - Solution, oxidation, hydrolysis (rust, dissolution)
    │   • "biological" - Roots, lichen, organic acids
    │   • "spheroidal" - Onion-skin rounded weathering
    │   • "exfoliation" - Sheet-like spalling
    │   • "mixed" - Multiple processes evident
    └────────────────────────────────────────────────────────────────────

    ┌─ PHYSICAL PROPERTIES ─────────────────────────────────────────────
    │ hardness_class (Mohs scale ranges):
    │   • "very_soft" - 1-2: Talc, gypsum (scratches with fingernail)
    │   • "soft" - 2-3: Calcite (scratches with coin)
    │   • "medium" - 3-5: Fluorite, apatite (scratches with knife)
    │   • "hard" - 5-7: Quartz, feldspar (scratches glass)
    │   • "very_hard" - 7-10: Corundum, diamond
    │
    │ primary_structure - Dominant structural feature:
    │   • "massive" - No visible internal structure
    │   • "layered" - Sedimentary bedding planes
    │   • "foliated" - Metamorphic alignment of minerals
    │   • "vesicular" - Gas bubble holes (volcanic)
    │   • "amygdaloidal" - Filled vesicles (mineralized)
    │   • "porphyritic" - Large crystals in fine matrix
    │   • "brecciated" - Angular fragments cemented
    │   • "conglomeratic" - Rounded clasts in matrix
    │   • "crystalline" - Interlocking crystal structure
    │   • "concretionary" - Spherical/nodular concentrations
    │
    │ fracture_type:
    │   • "conchoidal" - Shell-like curved surfaces (obsidian, chert)
    │   • "joint_controlled" - Breaks along structural planes
    │   • "columnar" - Hexagonal columns (basalt cooling joints)
    │   • "blocky", "platy", "splintery", "irregular"
    └────────────────────────────────────────────────────────────────────

    ┌─ ALTERATION & APPEARANCE ─────────────────────────────────────────
    │ alteration_type - Post-formation changes:
    │   • "unaltered" - Primary mineralogy intact
    │   • "oxidized" - Iron staining, rust colors
    │   • "silicified" - Quartz replacement/cementation
    │   • "carbonatized" - Carbonate mineral alteration
    │   • "chloritized" - Green chlorite alteration
    │   • "sericitized" - White mica (sericite) alteration
    │   • "kaolinized" - Clay mineral replacement
    │   • "mineralized" - Ore minerals introduced
    │   • "hydrothermal" - Hot water alteration
    │
    │ color_pattern:
    │   • "uniform", "mottled", "banded", "spotted", "veined", "gradational"
    └────────────────────────────────────────────────────────────────────

    ┌─ GEOLOGICAL CONTEXT ──────────────────────────────────────────────
    │ geological_context - Placement and transport history:
    │   • "in_situ_outcrop" - Bedrock in original position
    │   • "displaced_block" - Moved but clearly local source
    │   • "float" - Detached, uncertain transport distance
    │   • "talus" - Slope debris at base of outcrop
    │   • "glacial_erratic" - Glacially transported
    │   • "stream_cobble" - Water-worn and transported
    │   • "artificial" - Human-placed (building stone, fill)
    └────────────────────────────────────────────────────────────────────

    ┌─ CONFIDENCE CALIBRATION ──────────────────────────────────────────
    │ confidence_level & confidence_value (0.0-1.0):
    │   • "very_high" (0.8-1.0) - Diagnostic features clearly visible
    │   • "high" (0.6-0.8) - Strong evidence, minor uncertainty
    │   • "medium" (0.4-0.6) - Reasonable inference, some ambiguity
    │   • "low" (0.2-0.4) - Educated guess, limited features
    │   • "very_low" (0.0-0.2) - Highly uncertain, poor visibility
    │
    │ Calibration guidance: Be honest about uncertainty. High confidence
    │ requires diagnostic features. Consider image resolution, lighting,
    │ angle, and coverage. Partial views reduce confidence.
    └────────────────────────────────────────────────────────────────────

    ┌─ ADDITIONAL FIELDS ───────────────────────────────────────────────
    │ • image_position: Location in frame
    │ • estimated_diameter_cm: Best estimate of largest dimension
    │ • visible_minerals_count: Number of identifiable minerals
    │
    │ DESCRIPTIVE FIELDS (detailed professional descriptions):
    │ • specific_rock_name: Full geological name (e.g., "biotite granite")
    │ • color_details, texture_description, mineral_assemblage
    │ • surface_features, structural_features, shape_description
    │ • luster_description, special_features (fossils, xenoliths, etc.)
    │ • field_notes: Professional observations linking features to interpretation
    │ • likely_formation: Geological formation name if identifiable
    │ • age_estimate: Geological age if determinable from features/formation
    └────────────────────────────────────────────────────────────────────

    ═══════════════════════════════════════════════════════════════════
    SUMMARY REQUIREMENTS
    ═══════════════════════════════════════════════════════════════════

    Provide comprehensive geological interpretation including:
    • Tectonic setting and structural geology context
    • Depositional environment (for sedimentary)
    • Metamorphic grade (if applicable)
    • Regional geological setting
    • Economic geology significance
    • Recommended further analyses (thin sections, XRF, etc.)

    ═══════════════════════════════════════════════════════════════════
    EDGE CASE GUIDANCE
    ═══════════════════════════════════════════════════════════════════

    • Mixed rock types: Choose dominant class, note mixing in field_notes
    • Heavily weathered: Focus on relict textures and resistant minerals
    • Poor lighting/resolution: Lower confidence, describe limitations
    • Unusual features: Document thoroughly in special_features
    • Transitional rocks: Select closest match, explain reasoning in field_notes
    """

    if location and use_location:
        prompt += f"""

    ═══════════════════════════════════════════════════════════════════
    LOCATION CONTEXT - Use as Bayesian Prior, Not Confirmation
    ═══════════════════════════════════════════════════════════════════

    Location: {location}

    IMPORTANT: Use location knowledge appropriately:

    1. VISUAL EVIDENCE IS PRIMARY
       - Base your identification primarily on observable features
       - Location provides context and probabilistic priors, not answers

    2. INTEGRATE REGIONAL GEOLOGY
       - Consider typical rock types in this region
       - Think about regional tectonic setting and geological history
       - Use knowledge of local formations and lithologies

    3. HANDLE CONFLICTS HONESTLY
       - If visual features contradict regional expectations, TRUST THE VISUALS
       - Explicitly note conflicts in field_notes (e.g., "Visual features suggest
         X, but this is uncommon in [location]; possible transported specimen")
       - Consider transported rocks: glacial erratics, building stones, fill material

    4. AVOID CONFIRMATION BIAS
       - Don't force identification to match regional rock types
       - Unusual specimens exist; document them
       - Your confidence should reflect visual evidence quality, not location matching

    5. USE LOCATION TO ENHANCE, NOT OVERRIDE
       - Helps with formation identification
       - Informs age estimates
       - Provides tectonic context
       - But diagnostic features trump regional probabilities

    Example reasoning: "Vesicular texture strongly indicates volcanic origin (high confidence).
    Location is in sedimentary terrain, suggesting this is displaced/transported volcanic rock,
    possibly glacial erratic or fill material."
    """
    else:
        prompt += """

    ═══════════════════════════════════════════════════════════════════
    NO LOCATION CONTEXT - Pure Visual Analysis
    ═══════════════════════════════════════════════════════════════════

    Analyze based purely on observable features without regional geology knowledge.
    This approach eliminates location bias but may miss formation-specific insights.

    Focus entirely on:
    • Texture, structure, and mineralogy visible in image
    • Weathering patterns and alteration
    • Physical characteristics and relationships
    • Diagnostic features that indicate rock origin

    Without location, you cannot reliably:
    • Identify specific geological formations
    • Provide precise age estimates
    • Assess regional tectonic context
    • Evaluate typical vs. unusual occurrences

    Adjust confidence accordingly: High confidence only when diagnostic features
    are clearly visible and definitive.
    """

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=GeologicalAnalysisResult,
        thinking_config=types.ThinkingConfig(thinking_budget=32000)
    )

    print(f"Performing geological analysis {'with' if (location and use_location) else 'without'} location context...")
    start_time = time.time()

    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=[image, prompt],
            config=config
        )

        elapsed = time.time() - start_time
        print(f"Analysis completed in {elapsed:.2f} seconds")

        result = json.loads(response.text)

        # Add location to summary
        if 'summary' in result:
            result['summary']['location_used'] = location if (location and use_location) else "No location context"

        return result

    except Exception as e:
        print(f"Error in geological analysis: {e}")
        import traceback
        traceback.print_exc()
        return None


def display_geological_results(result: dict):
    """Display results in geological report format"""

    if not result:
        print("No results to display")
        return

    print("\n" + "="*70)
    print("GEOLOGICAL ANALYSIS REPORT")
    print("="*70)

    # Summary section
    if 'summary' in result:
        s = result['summary']
        print("\nEXECUTIVE SUMMARY:")
        print(f"  Total specimens: {s.get('total_rocks', 0)}")
        print(f"  Dominant lithology: {s.get('dominant_rock_class', 'Unknown')}")
        print(f"  Secondary lithology: {s.get('secondary_rock_class', 'None')}")
        print(f"  Average grain size: {s.get('average_grain_size', 'Unknown')}")
        print(f"  Weathering assessment: {s.get('weathering_assessment', 'Unknown')}")
        print(f"  Location: {s.get('location_used', 'Unknown')}")

        print("\nGEOLOGICAL INTERPRETATION:")
        print(f"  Setting: {s.get('geological_setting', 'Unknown')}")
        print(f"  Tectonic context: {s.get('tectonic_interpretation', 'Unknown')}")
        print(f"  Depositional environment: {s.get('depositional_environment', 'N/A')}")
        print(f"  Metamorphic grade: {s.get('metamorphic_grade', 'N/A')}")

        if s.get('economic_geology_notes'):
            print(f"\nECONOMIC GEOLOGY: {s['economic_geology_notes']}")

        if s.get('recommended_analyses'):
            print(f"\nRECOMMENDED ANALYSES:")
            for analysis in s['recommended_analyses']:
                print(f"  • {analysis}")

    # Detailed specimen descriptions
    if 'rocks' in result:
        print(f"\n{'='*70}")
        print(f"DETAILED SPECIMEN DESCRIPTIONS ({len(result['rocks'])} specimens)")
        print("="*70)

        for i, rock in enumerate(result['rocks'], 1):
            print(f"\n--- Specimen {i} ---")
            print(f"Classification: {rock.get('rock_class', 'unknown')}")
            print(f"Specific name: {rock.get('specific_rock_name', 'Unidentified')}")
            print(f"Size: {rock.get('size_class', 'unknown')} (~{rock.get('estimated_diameter_cm', 0):.0f} cm)")
            print(f"Grain size: {rock.get('grain_size', 'unknown')}")
            print(f"Hardness: {rock.get('hardness_class', 'unknown')}")
            print(f"Structure: {rock.get('primary_structure', 'unknown')}")
            print(f"Weathering: {rock.get('weathering_grade', 'unknown')} ({rock.get('weathering_type', 'unknown')})")
            print(f"Alteration: {rock.get('alteration_type', 'unknown')}")
            print(f"Context: {rock.get('geological_context', 'unknown')}")
            print(f"Confidence: {rock.get('confidence_level', 'unknown')} ({rock.get('confidence_value', 0):.2f})")

            if rock.get('mineral_assemblage'):
                print(f"Minerals: {rock['mineral_assemblage']}")

            if rock.get('field_notes'):
                print(f"Field notes: {rock['field_notes'][:200]}...")

            if rock.get('likely_formation'):
                print(f"Formation: {rock['likely_formation']}")

    # Overall interpretation
    if 'geological_interpretation' in result:
        print(f"\n{'='*70}")
        print("OVERALL GEOLOGICAL INTERPRETATION")
        print("="*70)
        print(result['geological_interpretation'])

    if 'confidence_assessment' in result:
        print(f"\nCONFIDENCE ASSESSMENT:")
        print(result['confidence_assessment'])


def main():
    """Main function for geological rock analyzer"""
    parser = argparse.ArgumentParser(
        description='Professional geological rock analyzer with comprehensive standardization'
    )
    parser.add_argument('image', help='Path to the image file')
    parser.add_argument('--location', '-l', help='Location information (coordinates, place name, geological region)')
    parser.add_argument('--no-location', action='store_true', help='Analyze without location context')
    parser.add_argument('--save', '-s', action='store_true', help='Save results to JSON file')
    parser.add_argument('--compare', '-c', action='store_true', help='Compare with and without location')

    args = parser.parse_args()

    if args.compare and args.location:
        # Run comparison
        print("Running comparison analysis...")

        # With location
        print("\n[1/2] WITH LOCATION CONTEXT")
        with_loc = analyze_rocks_geological(args.image, args.location, use_location=True)
        if with_loc:
            display_geological_results(with_loc)

        # Without location
        print("\n[2/2] WITHOUT LOCATION CONTEXT")
        without_loc = analyze_rocks_geological(args.image, args.location, use_location=False)
        if without_loc:
            display_geological_results(without_loc)

        # Save if requested
        if args.save and with_loc and without_loc:
            base_name = os.path.splitext(os.path.basename(args.image))[0]

            with open(f"geological_analysis_with_location_{base_name}.json", 'w') as f:
                json.dump(with_loc, f, indent=2)
            with open(f"geological_analysis_without_location_{base_name}.json", 'w') as f:
                json.dump(without_loc, f, indent=2)

            print(f"\nResults saved to JSON files")

    else:
        # Single analysis
        use_location = not args.no_location
        result = analyze_rocks_geological(
            args.image,
            args.location if use_location else None,
            use_location=use_location
        )

        if result:
            display_geological_results(result)

            if args.save:
                output_file = f"geological_analysis_{os.path.splitext(os.path.basename(args.image))[0]}.json"
                with open(output_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()