html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Toolbar Redesign Prototype</title>
<style>
body {
    background: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    padding: 30px;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
}

/* Redesigned Slicer Card */
.slicer-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
    display: flex;
    flex-direction: column;
    gap: 14px;
}

/* Tier 1: Navigation Tabs & Status */
.slicer-tabs-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}

.tab-group {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.nav-tab-btn {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    color: #475569;
    font-size: 12.5px;
    font-weight: 600;
    padding: 7px 15px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
    white-space: nowrap;
}

.nav-tab-btn:hover {
    background: #F1F5F9;
    color: #111827;
    border-color: #CBD5E1;
}

.nav-tab-btn.active {
    background: #111827 !important;
    color: #FFFFFF !important;
    border-color: #111827 !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
}

.slicer-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11.5px;
    font-weight: 600;
    color: #475569;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    padding: 5px 12px;
    border-radius: 20px;
    white-space: nowrap;
}

.status-indicator-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10B981;
    display: inline-block;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

/* Tier 2: Filter & Search Action Bar */
.slicer-controls-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
    padding-top: 12px;
    border-top: 1px solid #F1F5F9;
}

.search-wrapper {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 0 12px;
    height: 36px;
    flex: 1;
    max-width: 380px;
    min-width: 240px;
    transition: all 0.15s ease;
}

.search-wrapper:focus-within {
    border-color: #111827;
    background: #FFFFFF;
    box-shadow: 0 0 0 2px rgba(17, 24, 39, 0.08);
}

.search-icon {
    flex-shrink: 0;
}

.search-field {
    border: none;
    background: transparent;
    outline: none;
    width: 100%;
    font-size: 12.5px;
    color: #111827;
    padding: 0;
}

.search-field::placeholder {
    color: #94A3B8;
}

.slicer-dropdowns {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
}

.slicer-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

.slicer-label {
    font-size: 11px;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}

.slicer-select {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 600;
    color: #111827;
    outline: none;
    cursor: pointer;
    height: 36px;
    transition: border-color 0.15s ease;
}

.slicer-select:focus {
    border-color: #111827;
}

.slicer-reset-btn {
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    padding: 0 14px;
    font-size: 12px;
    font-weight: 600;
    color: #475569;
    cursor: pointer;
    height: 36px;
    transition: all 0.15s ease;
    white-space: nowrap;
}

.slicer-reset-btn:hover {
    background: #E2E8F0;
    color: #111827;
}
</style>
</head>
<body>
<div class="container">
    <div class="slicer-card">
        <!-- Top Row: Section Navigation Tabs & Live Dataset Scope -->
        <div class="slicer-tabs-row">
            <div class="tab-group">
                <button class="nav-tab-btn active">Batting Evaluation (Top 10)</button>
                <button class="nav-tab-btn">Bowling Evaluation (Top 10)</button>
                <button class="nav-tab-btn">IPL 2027 RR Squad & Auction Strategy</button>
                <button class="nav-tab-btn">Leverage Variance Audit</button>
            </div>
            <div class="slicer-status-badge">
                <span class="status-indicator-dot"></span>
                <span>IPL 2027 Auction Pool &bull; 1,217 Evaluated</span>
            </div>
        </div>

        <!-- Bottom Row: Filter & Search Controls (Balanced, Full-Width, No Empty Void) -->
        <div class="slicer-controls-row">
            <div class="search-wrapper">
                <svg class="search-icon" viewBox="0 0 20 20" width="15" height="15" fill="none" stroke="#64748B" stroke-width="2">
                    <circle cx="8.5" cy="8.5" r="5.5"></circle>
                    <line x1="12.5" y1="12.5" x2="17" y2="17"></line>
                </svg>
                <input type="text" id="filterInput" class="search-field" placeholder="Search player name, franchise, state, or role...">
            </div>

            <div class="slicer-dropdowns">
                <div class="slicer-item">
                    <label for="roleSlicer" class="slicer-label">ROLE:</label>
                    <select id="roleSlicer" class="slicer-select">
                        <option value="ALL">All Roles</option>
                        <option value="TOP">Top Order & Anchors (#1–#3)</option>
                        <option value="MIDDLE">Middle-Overs Enforcers (#4–#5)</option>
                        <option value="FINISHER">Finishers / Death Specialists (#5–#7)</option>
                        <option value="SEAM">Fast Bowlers / Seam</option>
                        <option value="SPIN">Spin / All-Rounders</option>
                    </select>
                </div>

                <div class="slicer-item">
                    <label for="sortSlicer" class="slicer-label">SORT:</label>
                    <select id="sortSlicer" class="slicer-select">
                        <option value="RANK">Rank (Ascending)</option>
                        <option value="DIFF">Win Differential (&Delta;)</option>
                        <option value="WIN">High-Leverage Win%</option>
                        <option value="INDEX">Index Score (CPPI)</option>
                    </select>
                </div>

                <button class="slicer-reset-btn">Reset</button>
            </div>
        </div>
    </div>
</div>
</body>
</html>
"""

with open("scratch/prototype_slicers.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Saved prototype to scratch/prototype_slicers.html")

