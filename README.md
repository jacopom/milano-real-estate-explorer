# Milano Real Estate Explorer

An interactive web application for visualizing and exploring real estate price quotations (Quotazioni Immobiliari OMI) across Milan's zones, with trend analysis and address search functionality.

![Milano Real Estate Explorer](https://img.shields.io/badge/Status-Live-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🚀 Live Demo

[View Live Application](https://jacopom.github.io/milano-real-estate-explorer/)

## ✨ Features

- **Interactive Map Visualization**: Explore Milan's OMI zones with color-coded real estate prices
- **Address Search**: Search any Milan address to find its corresponding zone and pricing data
- **Price Trend Analysis**: Compare current prices (2025/1) with historical data (2024/2)
- **Advanced Filtering**: Filter by property type (Tipologia) and condition (Stato)
- **Contextual Popups**: Click zones to view detailed pricing information
- **Tech-Inspired Design**: Dark theme with cyan accents for a modern aesthetic
- **Fully Responsive**: Works seamlessly on desktop and mobile devices

## 📊 Data Sources

### About OMI (Osservatorio del Mercato Immobiliare)

The data comes from the **Agenzia delle Entrate** (Italian Tax Agency), which publishes semi-annual real estate market quotations for all Italian municipalities through the OMI (Real Estate Market Observatory).

**Key Information:**
- **Official Source**: Agenzia delle Entrate - Osservatorio del Mercato Immobiliare
- **Update Frequency**: Semi-annual (this version uses 2025/1 and 2024/2 data)
- **Coverage**: All Italian municipalities with sale quotations and rental rates
- **Basis**: Primarily based on actual notarized transactions (rogiti)
- **Usage**: Used for property appraisals, market analysis, and potential tax reform

### Data Interpretation

**Important Notes:**
- Quotations are **averages** and should be used as **trend indicators**, not absolute values
- Each property is unique - actual prices vary significantly based on specific characteristics
- Homogeneous zones (zone omogenee) are topographical groupings, but values can vary street by street
- In Milan, real estate agencies often consider OMI prices conservative estimates
- Prices represent market quotations, not necessarily final transaction prices

### Data Sources Used

- **OMI Quotations**: 2025/1 (current) and 2024/2 (historical for trends)
- **Geographic Data**: Official KMZ zone boundary files
- **Geocoding**: OpenStreetMap Nominatim API for address search

## 🛠️ Technologies Used

- **Leaflet.js**: Interactive maps
- **OpenStreetMap**: Base map tiles (CARTO Dark theme)
- **Nominatim API**: Free geocoding service
- **Pure JavaScript**: No frameworks, vanilla JS only
- **Python**: Data processing and build scripts

## 🎨 Features Breakdown

### Price Visualization
- **> 10,000 €/mq**: Bright cyan - Premium zones
- **7,000-10,000 €/mq**: Light blue - High-value zones
- **4,000-7,000 €/mq**: Medium blue - Mid-range zones
- **< 4,000 €/mq**: Grey-blue - Affordable zones

### Trend Indicators
- **▲ Green**: Price increase vs previous semester
- **▼ Red**: Price decrease vs previous semester
- **■ Grey**: Stable prices

### Search Functionality
Search for any Milan address and the map will:
1. Geocode the address using Nominatim
2. Find the corresponding OMI zone
3. Zoom to the zone and display pricing data
4. Show trend analysis

## 🚀 Getting Started

### Prerequisites
- Web browser (Chrome, Firefox, Safari, Edge)
- Python 3.x (only for rebuilding data)

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/jacopom/milano-real-estate-explorer.git
cd milano-real-estate-explorer
```

2. Open `index.html` in your browser:
```bash
open index.html
# or
python3 -m http.server 8000
```

3. Navigate to `http://localhost:8000` (if using Python server)

### Rebuilding from Source Data

If you want to update the data or modify the build:

```bash
python3 rebuild.py
```

This script:
- Reads the OMI CSV files and KMZ boundaries
- Processes and combines the data
- Generates a self-contained `index.html` file

## 📁 Project Structure

```
milano-real-estate-explorer/
├── index.html                          # Main application (self-contained)
├── rebuild.py                          # Build script
├── embedded_data.js                    # Processed OMI data
├── zone_boundaries.js                  # GeoJSON zone boundaries
├── QI_1292013_1_20251_VALORI.csv      # 2025/1 OMI values
├── QI_1292013_1_20251_ZONE.csv        # Zone reference data
├── QI_1292023_1_20242_VALORI.csv      # 2024/2 OMI values (historical)
├── F205 - Comune di MILANO 2025-1.kmz # Zone boundary polygons
└── README.md                           # This file
```

## 🌐 GitHub Pages Deployment

This project is configured for GitHub Pages:

1. Push your code to GitHub
2. Go to repository Settings → Pages
3. Select "Deploy from a branch"
4. Choose `main` branch and `/ (root)` folder
5. Save and wait for deployment

Your site will be live at: `https://jacopom.github.io/milano-real-estate-explorer/`

## 🎯 Usage Examples

### Search by Address
- Type: "Via Montenapoleone, Milano"
- Click "Cerca" or press Enter
- The map will zoom to the zone and show pricing data

### Filter Properties
- **Tipologia**: Select property type (e.g., "Abitazioni civili")
- **Stato**: Select condition (e.g., "OTTIMO", "Normale")
- Map updates automatically with filtered data

### Explore Zones
- Hover over zones to see borders highlighted
- Click any zone to view detailed information
- View min, max, and average prices per square meter
- See trend comparison with previous semester

## 📝 Additional Data Information

### How to Access OMI Data

The official OMI data can be accessed through:
1. **Web Portal**: Connect via SPID or CIE at the Agenzia delle Entrate website
2. **GeoPOI**: Quick online lookup for specific addresses (no registration needed)
3. **OMI Mobile App**: Mobile application by Agenzia delle Entrate
4. **Historical Data**: Available from 2004 onwards

### Data Specifications

- **Semestre 2025/1**: January-June 2025 data
- **Semestre 2024/2**: July-December 2024 data (for trend comparison)
- **Prices**: EUR per square meter (€/mq) for sales
- **Rentals**: EUR per square meter per month for rentals (not included in this visualization)
- **Classification**: Properties divided by characteristics (signorile, civile, popolare) and maintenance state

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Credits

- **OMI Data**: Agenzia delle Entrate - Osservatorio del Mercato Immobiliare
- **Maps**: OpenStreetMap contributors
- **Tiles**: CARTO
- **Geocoding**: Nominatim by OpenStreetMap

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

Made with ❤️ for Milan real estate data enthusiasts
