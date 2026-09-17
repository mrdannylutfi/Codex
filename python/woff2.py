import base64
import json

# Define font component table sizes in bytes
# Uncompressed Raw Binary Font Stack data
raw_glyf = 245000
raw_gpos = 65000
raw_gsub = 48000
raw_cmap = 18000
raw_head_hhea = 16000

# Optimized WOFF2 Container data (reflecting high Brotli table compression flattening)
woff2_glyf = 52000
woff2_gpos = 14000
woff2_gsub = 9000
woff2_cmap = 2000
woff2_head_hhea = 1000

# Calculate totals for metadata calculations
raw_total = raw_glyf + raw_gpos + raw_gsub + raw_cmap + raw_head_hhea
woff2_total = woff2_glyf + woff2_gpos + woff2_gsub + woff2_cmap + woff2_head_hhea

print("==================================================================")
print("📦 COMPONENT METRICS: UNCOMPRESSED VS OPTIMIZED WOFF2")
print("==================================================================")
print(f"   ├── Raw Binary Asset Stack Total : {raw_total:,} Bytes")
print(f"   ├── Optimized WOFF2 Container    : {woff2_total:,} Bytes")
print(f"   └── Net Table Footprint Saved    : {raw_total - woff2_total:,} Bytes")
print("==================================================================")

# Generate Structured JSON Object for the layout rendering system
chart_data = {
    "metadata": {
        "chart_type": "bar",
        "chart_title": "Font Layout Array Shift: Uncompressed vs WOFF2",
        "orientation": "vertical",
        "stacking": "stacked",
        "x_axis_title": "Font Component Configurations",
        "y_axis_title": "Size in Bytes",
        "unit_symbol": " B",
        "unit_position": "suffix",
        "value_tiers": [
            {"min": 1000, "divide_by": 1000, "suffix": "K"}
        ],
        "scale_type": "linear"
    },
    "labels": ["Raw Binary Asset Stack", "Optimized WOFF2 File"],
    "datasets": [
        {
            "label": "glyf (Glyph Outlines)",
            "axis": "primary",
            "data": [
                {"value_raw": float(raw_glyf), "tooltip_text": f"glyf (Outlines): {raw_glyf:,} B"},
                {"value_raw": float(woff2_glyf), "tooltip_text": f"glyf (Outlines): {woff2_glyf:,} B"}
            ]
        },
        {
            "label": "gpos (Glyph Positioning/Kerning)",
            "axis": "primary",
            "data": [
                {"value_raw": float(raw_gpos), "tooltip_text": f"gpos (Positioning): {raw_gpos:,} B"},
                {"value_raw": float(woff2_gpos), "tooltip_text": f"gpos (Positioning): {woff2_gpos:,} B"}
            ]
        },
        {
            "label": "gsub (Glyph Substitution/Ligatures)",
            "axis": "primary",
            "data": [
                {"value_raw": float(raw_gsub), "tooltip_text": f"gsub (Substitution): {raw_gsub:,} B"},
                {"value_raw": float(woff2_gsub), "tooltip_text": f"gsub (Substitution): {woff2_gsub:,} B"}
            ]
        },
        {
            "label": "cmap (Character To Glyph Mapping)",
            "axis": "primary",
            "data": [
                {"value_raw": float(raw_cmap), "tooltip_text": f"cmap (Mapping): {raw_cmap:,} B"},
                {"value_raw": float(woff2_cmap), "tooltip_text": f"cmap (Mapping): {woff2_cmap:,} B"}
            ]
        },
        {
            "label": "head_hhea (Global Headers/Metrics)",
            "axis": "primary",
            "data": [
                {"value_raw": float(raw_head_hhea), "tooltip_text": f"head_hhea (Headers): {raw_head_hhea:,} B"},
                {"value_raw": float(woff2_head_hhea), "tooltip_text": f"head_hhea (Headers): {woff2_head_hhea:,} B"}
            ]
        }
    ]
}
