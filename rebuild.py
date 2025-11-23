#!/usr/bin/env python3

# Read the data files
with open('embedded_data.js', 'r', encoding='utf-8') as f:
    embedded_data = f.read()

with open('zone_boundaries.js', 'r', encoding='utf-8') as f:
    zone_boundaries = f.read()

# HTML template - filters at bottom, no duplicate popup
html = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Milano Real Estate Explorer</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body {
            width: 100%;
            height: 100%;
            overflow-x: hidden;
        }
        body {
            font-family: 'Courier New', monospace;
            height: 100vh;
            display: flex;
            flex-direction: column;
            background: #0a0e1a;
        }
        header {
            background: #1a2332;
            border-bottom: 3px solid #00ffc8;
            color: #00ffc8;
            padding: 1.25rem 2rem;
        }
        header h1 {
            font-size: 1.8rem;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }
        .header-controls {
            display: flex;
            gap: 2rem;
            align-items: center;
            flex-wrap: wrap;
        }
        .main-content {
            flex: 1;
            position: relative;
            overflow: hidden;
            width: 100%;
        }
        #map {
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
        .no-data-message {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(26, 35, 50, 0.95);
            border: 3px solid #ff4757;
            padding: 2rem;
            text-align: center;
            z-index: 1000;
            max-width: 400px;
        }
        .no-data-message h3 {
            color: #ff4757;
            font-size: 1.2rem;
            margin-bottom: 1rem;
            text-transform: uppercase;
        }
        .no-data-message p {
            color: #6b8ba3;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .search-container {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            flex: 1;
            max-width: 400px;
        }
        .search-container input {
            flex: 1;
            padding: 0.5rem 1rem;
            border: 2px solid #2d4159;
            background: #0a0e1a;
            color: #00ffc8;
            font-size: 0.85rem;
            font-family: 'Courier New', monospace;
        }
        .search-container input::placeholder {
            color: #6b8ba3;
        }
        .search-container input:focus {
            outline: none;
            border-color: #00ffc8;
        }
        .search-container button {
            padding: 0.5rem 1rem;
            border: 2px solid #00ffc8;
            background: #00ffc8;
            color: #0a0e1a;
            font-size: 0.75rem;
            font-weight: 700;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 1px;
            white-space: nowrap;
        }
        .search-container button:hover {
            background: #1a2332;
            color: #00ffc8;
        }
        .search-error {
            color: #ff4757;
            font-size: 0.75rem;
            margin-top: 0.5rem;
        }
        .filters-container {
            display: flex;
            gap: 2rem;
            align-items: center;
        }

        footer {
            background: rgba(26, 35, 50, 0.98);
            border-top: 3px solid #00ffc8;
            padding: 1rem 2rem;
            text-align: center;
            box-shadow: 0 -4px 20px rgba(0,255,200,0.2);
        }
        .description {
            font-size: 0.8rem;
            color: #6b8ba3;
            line-height: 1.5;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }
        .description-text {
            display: inline;
            white-space: nowrap;
        }
        .github-icon-link {
            display: inline-flex;
            align-items: center;
            text-decoration: none;
            transition: opacity 0.2s;
        }
        .github-icon-link:hover {
            opacity: 0.7;
        }
        .github-icon-small {
            width: 20px;
            height: 20px;
            fill: #6b8ba3;
            transition: fill 0.2s;
        }
        .github-icon-link:hover .github-icon-small {
            fill: #00ffc8;
        }
        .filter-group {
            display: flex;
            gap: 0.75rem;
            align-items: center;
        }
        .filter-group label {
            font-size: 0.75rem;
            font-weight: 700;
            color: #00ffc8;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            white-space: nowrap;
        }
        .filter-group select {
            padding: 0.5rem 1rem;
            border: 2px solid #2d4159;
            background: #1a2332;
            color: #00ffc8;
            font-size: 0.85rem;
            font-family: 'Courier New', monospace;
            cursor: pointer;
            min-width: 180px;
        }
        .filter-group select:hover { border-color: #00ffc8; }
        .filter-group select:focus { outline: none; border-color: #00ffc8; }

        .description {
            font-size: 0.7rem;
            color: #6b8ba3;
            line-height: 1.5;
            max-width: 500px;
            margin-left: auto;
        }

        .leaflet-popup-content-wrapper {
            background: rgba(26, 35, 50, 0.98);
            border: 3px solid #00ffc8;
            box-shadow: 0 8px 32px rgba(0,255,200,0.4);
            padding: 0;
            font-family: 'Courier New', monospace;
        }
        .leaflet-popup-content {
            margin: 0;
            padding: 1.5rem;
            min-width: 280px;
        }
        .leaflet-popup-tip {
            background: rgba(26, 35, 50, 0.98);
            border: 3px solid #00ffc8;
            border-top: none;
            border-right: none;
        }
        .popup-zone-street {
            font-weight: 700;
            color: #00ffc8;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            line-height: 1.3;
            text-transform: uppercase;
        }
        .popup-zone-code {
            font-size: 0.75rem;
            color: #6b8ba3;
            margin-bottom: 1.5rem;
        }
        .popup-price-section {
            background: #1a2332;
            border: 2px solid #2d4159;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        .popup-price-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }
        .popup-price-row:last-child { margin-bottom: 0; }
        .popup-price-label {
            font-size: 0.75rem;
            color: #6b8ba3;
            text-transform: uppercase;
        }
        .popup-price-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: #00ffc8;
        }
        .trend-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            padding: 0.5rem 0.75rem;
            font-size: 0.85rem;
            font-weight: 700;
            border: 2px solid;
            text-transform: uppercase;
        }
        .trend-up { background: #00ffc8; color: #0a0e1a; border-color: #00ffc8; }
        .trend-down { background: #ff4757; color: #0a0e1a; border-color: #ff4757; }
        .trend-stable { background: #6b8ba3; color: #0a0e1a; border-color: #6b8ba3; }

        .legend {
            background: rgba(26, 35, 50, 0.98);
            border: 3px solid #00ffc8;
            padding: 1.25rem;
        }
        .legend h4 {
            color: #00ffc8;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
        }
        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
            font-size: 0.75rem;
            color: #00ffc8;
        }
        .legend-item:last-child { margin-bottom: 0; }
        .legend-color {
            width: 24px;
            height: 24px;
            margin-right: 0.75rem;
            border: 2px solid #00ffc8;
        }

        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            header {
                padding: 1rem;
            }
            header h1 {
                font-size: 1.2rem;
                margin-bottom: 0.75rem;
            }
            .header-controls {
                flex-direction: column;
                gap: 0.75rem;
                width: 100%;
            }
            .search-container {
                width: 100%;
                max-width: 100%;
            }
            .filters-container {
                width: 100%;
                gap: 0.75rem;
                flex-wrap: nowrap;
            }
            .filter-group {
                flex: 1;
                min-width: 0;
            }
            .filter-group select {
                width: 100%;
                min-width: 0;
                font-size: 0.8rem;
            }
            .legend {
                padding: 0.5rem;
            }
            .legend h4 {
                font-size: 0.65rem;
                margin-bottom: 0.4rem;
            }
            .legend-item {
                font-size: 0.6rem;
                margin-bottom: 0.25rem;
            }
            .legend-color {
                width: 16px;
                height: 16px;
                margin-right: 0.4rem;
            }
            .description {
                flex-direction: column;
                gap: 0.5rem;
                font-size: 0.7rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>Milano Real Estate Explorer</h1>
        <div class="header-controls">
            <div class="search-container">
                <input type="text" id="address-search" placeholder="Cerca indirizzo (es. Via Montenapoleone)">
                <button onclick="searchAddress()">Cerca</button>
            </div>
            <div class="filters-container">
                <div class="filter-group">
                    <label for="tipo-filter">Tipologia</label>
                    <select id="tipo-filter"><option value="">Tutte</option></select>
                </div>
                <div class="filter-group">
                    <label for="stato-filter">Stato</label>
                    <select id="stato-filter"><option value="">Tutti</option></select>
                </div>
            </div>
        </div>
        <div id="search-error" class="search-error" style="display: none;"></div>
    </header>

    <div class="main-content">
        <div id="map"></div>
        <div id="no-data-message" class="no-data-message" style="display: none;">
            <h3>Nessun Dato Disponibile</h3>
            <p>Non ci sono dati per questa combinazione di filtri. Prova a cambiare la selezione.</p>
        </div>
    </div>

    <footer>
        <div class="description">
            <span class="description-text">Quotazioni Immobiliari OMI - Semestre 2025/1 - Analisi Trend vs 2024/2</span>
            <a href="https://github.com/jacopom/milano-real-estate-explorer" target="_blank" rel="noopener noreferrer" class="github-icon-link" title="View on GitHub">
                <svg class="github-icon-small" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                </svg>
            </a>
        </div>
    </footer>

    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
'''

html += embedded_data + '\n'
html += zone_boundaries + '\n'

html += '''
        let map, filteredData = [], zoneLayers = new Map();
        const MILAN_CENTER = [45.4642, 9.1900], MILAN_ZOOM = 14;

        function getPriceColor(avgPrice) {
            if (avgPrice > 10000) return '#00ffc8';
            if (avgPrice > 7000) return '#5bc0de';
            if (avgPrice > 4000) return '#4a90a4';
            return '#6b8ba3';
        }

        function getTrendIcon(direction) {
            if (direction === 'up') return '▲';
            if (direction === 'down') return '▼';
            return '■';
        }

        async function searchAddress() {
            const input = document.getElementById('address-search');
            const errorDiv = document.getElementById('search-error');
            const address = input.value.trim();

            errorDiv.style.display = 'none';
            errorDiv.textContent = '';

            if (!address) {
                errorDiv.textContent = 'Inserisci un indirizzo';
                errorDiv.style.display = 'block';
                return;
            }

            try {
                // Call Nominatim API for geocoding
                const response = await fetch(
                    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&limit=5&bounded=1&viewbox=9.04,45.54,9.28,45.39`
                );

                if (!response.ok) throw new Error('Geocoding fallito');

                const results = await response.json();

                if (results.length === 0) {
                    errorDiv.textContent = 'Indirizzo non trovato a Milano';
                    errorDiv.style.display = 'block';
                    return;
                }

                // Use first result
                const lat = parseFloat(results[0].lat);
                const lon = parseFloat(results[0].lon);
                const point = L.latLng(lat, lon);

                // Find which zone contains this point
                let foundZone = null;
                for (const [zoneId, layer] of zoneLayers.entries()) {
                    const bounds = layer.getBounds();
                    if (bounds.contains(point)) {
                        // More precise check: point in polygon
                        let contains = false;
                        layer.eachLayer(sublayer => {
                            if (sublayer.getBounds && sublayer.getBounds().contains(point)) {
                                contains = true;
                            }
                        });
                        if (contains) {
                            foundZone = filteredData.find(z => z.zona === zoneId);
                            break;
                        }
                    }
                }

                if (foundZone) {
                    // Zoom to zone and open popup
                    const zoneLayer = zoneLayers.get(foundZone.zona);
                    map.fitBounds(zoneLayer.getBounds().pad(0.2));
                    setTimeout(() => {
                        zoneLayer.openPopup(point);
                    }, 300);
                    input.value = '';
                } else {
                    errorDiv.textContent = 'Indirizzo trovato ma fuori dalle zone OMI di Milano';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                errorDiv.textContent = 'Errore nella ricerca: ' + error.message;
                errorDiv.style.display = 'block';
            }
        }

        // Allow Enter key to search
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('address-search').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') searchAddress();
            });
        });

        function initMap() {
            map = L.map('map').setView(MILAN_CENTER, MILAN_ZOOM);
            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '© OpenStreetMap © CARTO',
                maxZoom: 18
            }).addTo(map);

            // Position legend based on screen size
            const isMobile = window.innerWidth <= 768;
            const legend = L.control({ position: isMobile ? 'bottomleft' : 'bottomright' });
            legend.onAdd = function() {
                const div = L.DomUtil.create('div', 'legend');
                div.innerHTML = `
                    <h4>Prezzo €/mq</h4>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #00ffc8"></div>
                        <span>&gt; 10K</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #5bc0de"></div>
                        <span>7K-10K</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #4a90a4"></div>
                        <span>4K-7K</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color" style="background: #6b8ba3"></div>
                        <span>&lt; 4K</span>
                    </div>
                `;
                return div;
            };
            legend.addTo(map);
        }

        function populateFilters() {
            const tipoSet = new Set(), statoSet = new Set();
            EMBEDDED_DATA.forEach(row => {
                if (row.descr_tipologia) tipoSet.add(row.descr_tipologia);
                if (row.stato) statoSet.add(row.stato);
            });

            const tipoFilter = document.getElementById('tipo-filter');
            const statoFilter = document.getElementById('stato-filter');

            Array.from(tipoSet).sort().forEach(tipo => {
                const option = document.createElement('option');
                option.value = tipo;
                option.textContent = tipo;
                if (tipo === 'Abitazioni civili') option.selected = true;
                tipoFilter.appendChild(option);
            });

            Array.from(statoSet).sort().forEach(stato => {
                const option = document.createElement('option');
                option.value = stato;
                // Capitalize first letter, rest lowercase
                option.textContent = stato.charAt(0).toUpperCase() + stato.slice(1).toLowerCase();
                if (stato === 'OTTIMO') option.selected = true;
                statoFilter.appendChild(option);
            });
        }

        function applyFilters() {
            const tipoFilter = document.getElementById('tipo-filter').value;
            const statoFilter = document.getElementById('stato-filter').value;

            let filtered = EMBEDDED_DATA.filter(row => {
                const matchTipo = !tipoFilter || row.descr_tipologia === tipoFilter;
                const matchStato = !statoFilter || row.stato === statoFilter;
                return matchTipo && matchStato;
            });

            const zoneMap = new Map();
            filtered.forEach(row => {
                if (!zoneMap.has(row.zona)) {
                    zoneMap.set(row.zona, {
                        zona: row.zona,
                        fascia: row.fascia,
                        zona_descr: row.zona_descr,
                        values: []
                    });
                }
                zoneMap.get(row.zona).values.push(row);
            });

            filteredData = Array.from(zoneMap.values()).map(item => {
                const comprMin2025 = Math.min(...item.values.map(v => v.compr_min_2025_1).filter(v => v > 0));
                const comprMax2025 = Math.max(...item.values.map(v => v.compr_max_2025_1));
                const trendsWithData = item.values.filter(v => v.trend_percent !== undefined);
                let avgTrend = 0, trendDirection = 'stable';

                if (trendsWithData.length > 0) {
                    avgTrend = trendsWithData.reduce((sum, v) => sum + v.trend_percent, 0) / trendsWithData.length;
                    if (avgTrend > 0.5) trendDirection = 'up';
                    else if (avgTrend < -0.5) trendDirection = 'down';
                }

                return {
                    ...item,
                    comprMin: comprMin2025 === Infinity ? 0 : comprMin2025,
                    comprMax: comprMax2025 === -Infinity ? 0 : comprMax2025,
                    trendPercent: Math.round(avgTrend * 10) / 10,
                    trendDirection: trendDirection
                };
            }).filter(item => item.comprMin > 0 || item.comprMax > 0);

            updateMap();
        }

        function updateMap() {
            zoneLayers.forEach(layer => map.removeLayer(layer));
            zoneLayers.clear();

            const noDataMsg = document.getElementById('no-data-message');

            if (filteredData.length === 0) {
                noDataMsg.style.display = 'block';
                return;
            } else {
                noDataMsg.style.display = 'none';
            }

            filteredData.forEach(zone => {
                const boundary = ZONE_BOUNDARIES.features.find(f => f.properties.zona === zone.zona);
                if (!boundary) return;

                const avgPrice = (zone.comprMin + zone.comprMax) / 2;
                const color = getPriceColor(avgPrice);

                const trendHtml = zone.trendPercent !== 0 ? `
                    <div class="trend-indicator trend-${zone.trendDirection}">
                        ${getTrendIcon(zone.trendDirection)} ${zone.trendPercent > 0 ? '+' : ''}${zone.trendPercent}% vs 2024/2
                    </div>
                ` : '';

                const popupContent = `
                    <div class="popup-zone-street">${zone.zona_descr}</div>
                    <div class="popup-zone-code">ZONA ${zone.zona} | FASCIA ${zone.fascia}</div>
                    <div class="popup-price-section">
                        <div class="popup-price-row">
                            <span class="popup-price-label">Min</span>
                            <span class="popup-price-value">${zone.comprMin.toLocaleString('it-IT')} €/mq</span>
                        </div>
                        <div class="popup-price-row">
                            <span class="popup-price-label">Max</span>
                            <span class="popup-price-value">${zone.comprMax.toLocaleString('it-IT')} €/mq</span>
                        </div>
                        <div class="popup-price-row">
                            <span class="popup-price-label">Media</span>
                            <span class="popup-price-value">${avgPrice.toLocaleString('it-IT')} €/mq</span>
                        </div>
                    </div>
                    ${trendHtml}
                `;

                const layer = L.geoJSON(boundary, {
                    style: {
                        fillColor: color,
                        weight: 2,
                        opacity: 0.8,
                        color: '#00ffc8',
                        fillOpacity: 0.45
                    }
                });

                layer.bindPopup(popupContent, {
                    maxWidth: 350,
                    className: 'custom-popup'
                });

                layer.on('mouseover', function() {
                    this.setStyle({ weight: 3, fillOpacity: 0.65 });
                });
                layer.on('mouseout', function() {
                    this.setStyle({ weight: 2, fillOpacity: 0.45 });
                });

                layer.addTo(map);
                zoneLayers.set(zone.zona, layer);
            });

            if (zoneLayers.size > 0) {
                const group = new L.featureGroup(Array.from(zoneLayers.values()));
                map.fitBounds(group.getBounds().pad(0.1));
            }
        }

        document.getElementById('tipo-filter').addEventListener('change', applyFilters);
        document.getElementById('stato-filter').addEventListener('change', applyFilters);

        initMap();
        populateFilters();
        applyFilters();
    </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('✓ Search and filters moved to top bar')
print('✓ Description kept at bottom')
print('✓ Zoom increased to 14')
print('✓ Layout reorganized')
