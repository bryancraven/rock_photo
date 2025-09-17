# Rock Image Analyzer - AI-Powered Geological Analysis

An amateur Python project that uses Google's Gemini 2.5 Pro AI model to identify and analyze rocks in images. This is an experimental tool developed as part of a wider hobby project, attempting to use established geological classification standards where possible.

## Features

- **Geological Classification Attempt**: Tries to apply standardized geological terminology (rock classes, Wentworth scale, weathering grades, etc.)
- **Location-Aware Analysis**: Optional location context to potentially improve identification accuracy
- **Comparison Mode**: Analyze with and without location to see the impact of contextual information
- **Structured JSON Output**: Discrete fields for programmatic parsing plus descriptive fields
- **Analysis Time**: ~60-80 seconds per image using Gemini 2.5 Pro with thinking mode
- **Two Analysis Modes**:
  - `rock_analyzer.py`: Detailed geological analysis attempting to use standard classifications
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

**Flexible Descriptive Fields** (AI interpretation):
- `specific_rock_name`: Detailed rock identification
- `mineral_assemblage`: Visible minerals
- `texture_description`: Comprehensive texture analysis
- `field_notes`: AI-generated observations
- `likely_formation`: Geological formation if identifiable

### Sample Analysis Results

<details>
<summary><b>📊 Full Analysis Without Location Context</b></summary>

```json
{
  "summary": {
    "total_rocks": 5,
    "dominant_rock_class": "sedimentary_chemical",
    "secondary_rock_class": "unconsolidated",
    "geological_setting": "The prevalence of tufa/travertine strongly suggests a localized depositional setting at a site of carbonate-rich groundwater discharge.",
    "tectonic_interpretation": "Travertine deposits can be associated with extensional tectonic settings where faulting provides conduits for deep, mineral-rich groundwater circulation.",
    "depositional_environment": "Terrestrial freshwater environment characterized by the precipitation of calcium carbonate from solution. This could be a cool-water spring (forming tufa) or a geothermal hot spring (forming travertine).",
    "economic_geology": "Travertine and tufa are quarried as ornamental and lightweight building stones. Such spring systems can also be indicators for geothermal energy potential."
  },
  "rocks": [
    {
      "rock_class": "sedimentary_chemical",
      "specific_rock_name": "Tufa",
      "size_class": "boulder",
      "size_cm": 45,
      "grain_size": "cryptocrystalline",
      "weathering_grade": "high",
      "weathering_type": "chemical",
      "hardness_class": "soft",
      "primary_structure": "vesicular",
      "geological_context": "displaced_block",
      "confidence_level": "high",
      "confidence_score": 0.85,
      "mineral_assemblage": "Primarily calcium carbonate (likely calcite).",
      "field_notes": "This appears to be a large piece of tufa, a freshwater carbonate deposit. The porous structure suggests rapid CO2 degassing and/or encrustation of plants.",
      "likely_formation": "Precipitated from cool, calcium-rich spring water, possibly encrusting plants or algae which have since decayed."
    }
  ]
}
```

**Key Findings:**
- Identified as tufa (freshwater carbonate deposits) based on vesicular texture
- Spring system deposit with rapid CO2 degassing
- High porosity from encrusted organic matter that decayed
- Analysis time: ~68 seconds

</details>

### Comparison Mode Results

<details>
<summary><b>🔄 With vs Without Location Context</b></summary>

#### With Location (Uinta-Wasatch-Cache National Forest, Utah):
- **Rock identification**: Limestone with karst weathering
- **Formation**: Paleozoic marine carbonate
- **Tectonic context**: Laramide Orogeny and Basin and Range extension
- **Depositional environment**: Marine shelf environment

#### Without Location:
- **Rock identification**: Tufa/travertine (freshwater carbonate)
- **Formation**: Spring system deposit
- **Tectonic context**: Possible extensional setting with groundwater circulation
- **Depositional environment**: Terrestrial freshwater spring

**Impact of Location Context:**
Location context can bias identification toward regionally common rock types. Without location, the AI focuses purely on visual features, correctly identifying the vesicular texture as tufa. With location, it defaults to limestone (common in the Wasatch Range) despite the distinctive tufa characteristics.

</details>

### Example Command-Line Output

<details>
<summary><b>💻 Terminal Output Example</b></summary>

```bash
$ python rock_analyzer.py rocks_utah.png --location "Uinta-Wasatch-Cache National Forest, Utah" --compare

Running comparison analysis...

[1/2] WITHOUT LOCATION CONTEXT
Loading image: rocks_utah.png
Performing geological analysis without location context...
Analysis completed in 67.99 seconds

======================================================================
GEOLOGICAL ANALYSIS REPORT
======================================================================

EXECUTIVE SUMMARY:
  Total specimens: 5
  Dominant lithology: sedimentary_chemical (tufa/travertine)
  Secondary lithology: unconsolidated
  Average grain size: cryptocrystalline
  Weathering assessment: High chemical weathering creating vuggy textures
  Location: No location context

[... detailed specimen descriptions ...]

[2/2] WITH LOCATION CONTEXT
Loading image: rocks_utah.png
Performing geological analysis with location context...
Analysis completed in 71.49 seconds

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

- Google Gemini API key with access to Gemini 2.5 Pro model
- Internet connection for API calls

## Example Analysis: rocks_utah.png

The repository includes `rocks_utah.png` as a sample image from Uinta-Wasatch-Cache National Forest, Utah. The Pro model identifies these as tufa (freshwater carbonate deposits) when analyzed without location context, though regional geology suggests they could also be weathered limestone.

![Sample Rock Image](rocks_utah.png)
*Tufa deposits in Utah*

## Technical Details

- Uses Google's `google-genai` Python SDK
- Implements typed schemas for guaranteed JSON structure
- Literal types for discrete categorization
- PIL/Pillow for image processing
- Gemini 2.5 Pro with thinking mode (32k budget) for deeper analysis

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - See LICENSE file for details

## Disclaimer

This is an amateur hobby project for educational and experimental purposes. The geological identifications are AI-generated and should not be considered authoritative or professional geological assessments. Always consult qualified geologists for professional rock and mineral identification.

## Acknowledgments

- Google Gemini AI for the vision model
- Geological classification standards from USGS and geological societies (attempted implementation)
- Wentworth scale for grain size classification