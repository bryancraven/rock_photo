# Rock Image Analyzer - AI-Powered Geological Analysis

A Python application that uses Google's Gemini 2.5 Flash AI model to perform comprehensive geological analysis of rocks in images. Features professional-grade rock classification, detailed mineralogical assessment, and location-aware geological interpretation.

## Features

- **Professional Geological Classification**: Uses standardized geological terminology and classifications (rock classes, Wentworth scale, weathering grades, etc.)
- **Location-Aware Analysis**: Optional location context enhances identification accuracy with regional geological knowledge
- **Comparison Mode**: Analyze with and without location to see the impact of contextual information
- **Structured JSON Output**: Standardized discrete fields for programmatic parsing plus flexible descriptive fields
- **Fast Analysis**: ~20-40 seconds per image using Gemini 2.5 Flash
- **Two Analysis Modes**:
  - `rock_analyzer.py`: Comprehensive geological analysis with professional standardization
  - `quick_analyzer.py`: Faster simplified analysis with basic categorization

## Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rock-image-analyzer.git
cd rock-image-analyzer
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

## Usage

### Comprehensive Geological Analysis

```bash
python rock_analyzer.py path/to/image.jpg

# With location context
python rock_analyzer.py rocks.jpg --location "Grand Canyon, Arizona"

# Save results to JSON
python rock_analyzer.py rocks.jpg --location "Utah" --save

# Compare with/without location
python rock_analyzer.py rocks.jpg --location "Yosemite" --compare
```

### Quick Analysis

```bash
python quick_analyzer.py path/to/image.jpg

# With location and comparison
python quick_analyzer.py rocks.jpg --location "Hawaii" --compare --save
```

## Output Format

### Rock Classification Fields

**Discrete Standardized Fields** (for programmatic parsing):
- `rock_class`: igneous_volcanic, sedimentary_clastic, metamorphic_foliated, etc.
- `size_class`: Wentworth scale (pebble, cobble, boulder, etc.)
- `grain_size`: cryptocrystalline to pegmatitic
- `weathering_grade`: fresh to residual_soil
- `hardness_class`: very_soft to very_hard (Mohs scale)
- `primary_structure`: massive, layered, vesicular, etc.
- `geological_context`: in_situ_outcrop, float, talus, etc.

**Flexible Descriptive Fields** (geological expertise):
- `specific_rock_name`: Detailed rock identification
- `mineral_assemblage`: Visible minerals
- `texture_description`: Comprehensive texture analysis
- `field_notes`: Professional observations
- `likely_formation`: Geological formation if identifiable

### Sample Analysis Results

<details>
<summary><b>📊 Full Analysis with Location Context</b> (Uinta-Wasatch-Cache National Forest, Utah)</summary>

```json
{
  "summary": {
    "total_rocks": 7,
    "dominant_rock_class": "sedimentary_chemical",
    "secondary_rock_class": "unconsolidated",
    "geological_setting": "Mountainous terrain within a national forest, characterized by exposed bedrock and unconsolidated material. The presence of limestone suggests a past marine environment.",
    "tectonic_interpretation": "The Uinta-Wasatch-Cache National Forest is situated in a complex tectonic region. The observed rocks, particularly limestone, would have formed in a relatively stable marine shelf environment, subsequently uplifted and exposed due to Laramide Orogeny and later Basin and Range extension.",
    "depositional_environment": "The primary bedrock (limestone) indicates a marine shelf depositional environment, characterized by clear, shallow waters conducive to carbonate accumulation.",
    "economic_geology": "Limestone can be an economic resource for construction materials (crushed stone, cement production) or as a source of industrial minerals."
  },
  "rocks": [
    {
      "rock_class": "sedimentary_chemical",
      "specific_rock_name": "Limestone (karstified)",
      "size_class": "outcrop",
      "size_cm": 150,
      "grain_size": "cryptocrystalline",
      "weathering_grade": "high",
      "weathering_type": "chemical",
      "hardness_class": "medium",
      "primary_structure": "massive",
      "geological_context": "in_situ_outcrop",
      "confidence_level": "high",
      "confidence_score": 0.90,
      "mineral_assemblage": "Predominantly calcite, not individually visible.",
      "field_notes": "Likely a weathered limestone outcrop. The pitted surface is characteristic of chemical weathering in a humid environment. Partially covered by soil and vegetation.",
      "likely_formation": "Paleozoic marine carbonate formation."
    },
    {
      "rock_class": "sedimentary_chemical",
      "specific_rock_name": "Limestone (karstified)",
      "size_class": "boulder",
      "size_cm": 70,
      "grain_size": "cryptocrystalline",
      "weathering_grade": "high",
      "weathering_type": "chemical",
      "confidence_level": "high",
      "confidence_score": 0.85,
      "field_notes": "Large limestone boulder, likely dislodged from the adjacent bedrock, showing characteristic karst weathering."
    }
  ]
}
```

**Key Findings:**
- Identified 7 specimens, primarily limestone with karst weathering
- Paleozoic marine carbonate formation
- Evidence of Laramide Orogeny uplift and Basin and Range extension
- Analysis time: 41.06 seconds

</details>

### Comparison Mode Results

<details>
<summary><b>🔄 With vs Without Location Context</b></summary>

#### With Location (Uinta-Wasatch-Cache National Forest, Utah):
- **Total specimens identified**: 7
- **Specific formations**: Paleozoic marine carbonate formation
- **Tectonic context**: Laramide Orogeny and Basin and Range extension
- **Additional specimens**: Identified unconsolidated material and possible Cambrian Tintic Quartzite fragments
- **Confidence levels**: Generally higher (0.60-0.95)

#### Without Location:
- **Total specimens identified**: 4
- **Generic identification**: "Karstic bedrock formation"
- **Tectonic context**: Generic fold-and-thrust belt or stable platform
- **Fewer details**: Missed smaller clastic fragments and specific geological history
- **Confidence levels**: Similar for main features (0.70-0.95)

**Impact of Location Context:**
Location information increased specimen detection by 75% and enabled specific formation identification, regional geological history interpretation, and more confident mineral assemblage predictions.

</details>

### Example Command-Line Output

<details>
<summary><b>💻 Terminal Output Example</b></summary>

```bash
$ python rock_analyzer.py rocks_utah.png --location "Uinta-Wasatch-Cache National Forest, Utah" --compare

Running comparison analysis...

[1/2] WITH LOCATION CONTEXT
Loading image: rocks_utah.png
Performing geological analysis with location context...
Analysis completed in 41.06 seconds

======================================================================
GEOLOGICAL ANALYSIS REPORT
======================================================================

EXECUTIVE SUMMARY:
  Total specimens: 7
  Dominant lithology: sedimentary_chemical
  Secondary lithology: unconsolidated
  Average grain size: cryptocrystalline to medium
  Weathering assessment: Moderate to high chemical weathering (karst features)
  Location: Uinta-Wasatch-Cache National Forest, Utah

[... detailed specimen descriptions ...]

[2/2] WITHOUT LOCATION CONTEXT
Loading image: rocks_utah.png
Performing geological analysis without location context...
Analysis completed in 36.17 seconds

[... comparison analysis ...]
```

</details>

## Geological Features Detected

- **Rock Types**: All major rock classes and subtypes
- **Weathering Features**: Tafoni, spheroidal weathering, karst features
- **Structures**: Bedding, foliation, joints, veins
- **Textures**: Grain size, crystallinity, porosity
- **Alteration**: Oxidation, silicification, mineralization
- **Context**: Outcrop vs float, depositional environment

## Performance

- **Response Time**: 20-40 seconds per analysis
- **Image Size**: Automatically resized for optimal processing
- **Accuracy**: Enhanced significantly with location context

## Command Line Options

```
--location, -l    : Add location information (GPS, place name, region)
--compare, -c     : Compare results with and without location
--save, -s        : Save results to JSON file
--no-location     : Force analysis without location context
```

## API Requirements

- Google Gemini API key with access to Gemini 2.5 Flash model
- Internet connection for API calls

## Example Analysis: rocks_utah.png

The repository includes `rocks_utah.png` as a sample image from Uinta-Wasatch-Cache National Forest, Utah. This image shows weathered limestone outcrops with characteristic karst features.

## Technical Details

- Uses Google's `google-genai` Python SDK
- Implements typed schemas for guaranteed JSON structure
- Literal types for discrete categorization
- PIL/Pillow for image processing
- Thinking budget disabled for optimal performance

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Google Gemini AI for the powerful vision model
- Geological classification standards from USGS and geological societies
- Wentworth scale for grain size classification