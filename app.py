"""
GPA Advisor - AI-Powered Academic Trajectory Planner
Editorial Academic Document & Digital Transcript Metaphor
Themes: Oxford Paper (Light Cardstock) & Cambridge Chalkboard (Matte Dark)
"""

import html
import json
import math
import streamlit as st
import plotly.graph_objects as go

# Core project imports
from gpa_tools import GRADE_POINTS, GPAMemory
from gpa_agent import (
    memory as agent_memory,
    run_agent,
    describe,
    clear_session,
)


# ==============================================================================
# 1. CLASSICAL ACADEMIC ICONOGRAPHY (THIN-LINE ARCHIVAL VECTOR SVGS)
# ==============================================================================

ACADEMIC_ICONS = {
    "mortarboard": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>""",
    "quill": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18"/><path d="M2 2l7.586 7.586"/><circle cx="11" cy="11" r="2"/></svg>""",
    "tome": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="6" x2="16" y2="6"/><line x1="8" y1="10" x2="14" y2="10"/></svg>""",
    "seal": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>""",
    "ribbon": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M8.21 13.89L7 22l5-3 5 3-1.21-8.11"/></svg>""",
    "compass": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>""",
    "trash": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>""",
    "plus": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>""",
    "refresh": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>""",
    "send": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>""",
    "sun": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>""",
    "moon": """<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>""",
}

def render_svg(name: str, size: int = 16, color: str = "currentColor") -> str:
    template = ACADEMIC_ICONS.get(name, ACADEMIC_ICONS["seal"])
    return template.format(size=size, color=color)


def render_html(html_str: str):
    """
    Safely render raw HTML in Streamlit by stripping leading whitespace from all lines.
    Guarantees CommonMark never interprets any tag as an indented code block.
    """
    clean_lines = [line.strip() for line in html_str.strip().splitlines() if line.strip()]
    st.markdown("".join(clean_lines), unsafe_allow_html=True)


# ==============================================================================
# 2. EDITORIAL DESIGN SYSTEM: OXFORD PAPER & CAMBRIDGE CHALKBOARD
# ==============================================================================

def setup_page():
    st.set_page_config(
        page_title="GPA Advisor • Academic Planning Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_academic_css(theme: str = "paper"):
    """
    Inject bespoke typography and layout styles matching a high-end academic document.
    Rejects generic dark SaaS patterns in favor of Monocle/Swiss editorial typography.
    """
    if theme == "chalkboard":
        # Cambridge Chalkboard (Matte Dark Academic)
        canvas_bg = "#14201A"
        surface_bg = "#18261F"
        surface_subtle = "#1F3128"
        text_ink = "#E8ECE9"
        text_muted = "#9EB0A5"
        text_meta = "#6B7F74"
        hairline = "#263B30"
        accent_archival = "#52B788"
        accent_secondary = "#E9C46A"
        badge_bg = "rgba(82, 183, 136, 0.12)"
        badge_border = "rgba(82, 183, 136, 0.28)"
        badge_text = "#6FE0A8"
        btn_bg = "#253B30"
        btn_text = "#E8ECE9"
        btn_hover = "#2F4A3D"
        ring_track = "rgba(232, 236, 233, 0.12)"
        ring_stroke = "#52B788"
        spotlight_color = "rgba(82, 183, 136, 0.08)"
    else:
        # Oxford Paper (Warm Cream Cardstock)
        canvas_bg = "#FAF8F3"
        surface_bg = "#FFFFFF"
        surface_subtle = "#F4F0E6"
        text_ink = "#1C1810"
        text_muted = "#5A544A"
        text_meta = "#8A8275"
        hairline = "#E5DFD3"
        accent_archival = "#7E2228"  # Oxblood letterman red
        accent_secondary = "#1E3A2F"  # Collegiate forest
        badge_bg = "rgba(126, 34, 40, 0.06)"
        badge_border = "rgba(126, 34, 40, 0.22)"
        badge_text = "#7E2228"
        btn_bg = "#1C1810"
        btn_text = "#FAF8F3"
        btn_hover = "#7E2228"
        ring_track = "rgba(28, 24, 16, 0.1)"
        ring_stroke = "#7E2228"
        spotlight_color = "rgba(215, 198, 172, 0.14)"

    css = f"""
    <style>
    /* -------------------------------------------------------------
       1. Typography & Archival Fonts
       ------------------------------------------------------------- */
    @import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,400;1,6..72,600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    :root {{
        --canvas-bg: {canvas_bg};
        --surface-bg: {surface_bg};
        --surface-subtle: {surface_subtle};
        --text-ink: {text_ink};
        --text-muted: {text_muted};
        --text-meta: {text_meta};
        --hairline: {hairline};
        --accent-archival: {accent_archival};
        --badge-bg: {badge_bg};
        --badge-border: {badge_border};
        --badge-text: {badge_text};
        --btn-bg: {btn_bg};
        --btn-text: {btn_text};
        --btn-hover: {btn_hover};
        --ring-track: {ring_track};
        --ring-stroke: {ring_stroke};
    }}

    html, body, [class*="css"], .stApp {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--canvas-bg) !important;
        color: var(--text-ink) !important;
        -webkit-font-smoothing: antialiased;
        letter-spacing: -0.01em;
    }}

    /* Global ambient cursor spotlight */
    #academic-spotlight {{
        position: fixed;
        width: 650px;
        height: 650px;
        border-radius: 50%;
        pointer-events: none;
        transform: translate(-50%, -50%);
        background: radial-gradient(circle, {spotlight_color} 0%, rgba(0,0,0,0) 70%);
        z-index: 99999;
        mix-blend-mode: multiply;
        transition: opacity 0.2s ease;
    }}

    /* Serifs for Editorial Academic Authority */
    h1, h2, h3, .serif-heading, .academic-title, .stamp-gpa-number {{
        font-family: 'Newsreader', Georgia, serif !important;
        letter-spacing: -0.025em !important;
        font-feature-settings: "liga" 1, "dlig" 1;
    }}

    /* Tabular figures for calculations & points */
    .tabular-mono, code, .pts-cell {{
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums;
    }}

    /* -------------------------------------------------------------
       2. Clean Chrome Removal & Minimal Negative Space
       ------------------------------------------------------------- */
    #MainMenu, header, footer {{
        visibility: hidden !important;
        height: 0 !important;
    }}
    .block-container {{
        max-width: 1240px !important;
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }}

    /* -------------------------------------------------------------
       3. Academic Masthead & Header
       ------------------------------------------------------------- */
    .academic-masthead {{
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        padding-bottom: 1.25rem;
        border-bottom: 2px solid var(--text-ink);
        margin-bottom: 1.85rem;
    }}
    .masthead-left {{
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
    }}
    .masthead-kicker {{
        font-size: 0.725rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--accent-archival);
    }}
    .masthead-title {{
        font-size: 2.25rem;
        font-weight: 600;
        line-height: 1.05;
        margin: 0;
        color: var(--text-ink);
    }}
    .masthead-meta {{
        font-size: 0.85rem;
        color: var(--text-muted);
        font-style: italic;
        font-family: 'Newsreader', Georgia, serif;
    }}
    .masthead-right {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
    }}
    .edition-tag {{
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        border: 1px solid var(--hairline);
        padding: 0.25rem 0.65rem;
        border-radius: 4px;
        color: var(--text-muted);
        background: var(--surface-bg);
    }}

    /* -------------------------------------------------------------
       4. Asymmetric Hero: Stamped Grade & Hand-Drawn Ring
       ------------------------------------------------------------- */
    .hero-plinth {{
        display: grid;
        grid-template-columns: 1.55fr 1fr;
        gap: 2rem;
        align-items: center;
        padding: 1.75rem 2rem;
        background-color: var(--surface-bg);
        border: 1px solid var(--hairline);
        border-radius: 4px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
        margin-bottom: 2rem;
        position: relative;
    }}
    .hero-plinth::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background-color: var(--accent-archival);
    }}
    .hero-stamp-box {{
        display: flex;
        align-items: baseline;
        gap: 1.6rem;
    }}
    .stamp-gpa-number {{
        font-size: 4.6rem;
        font-weight: 700;
        line-height: 0.95;
        color: var(--text-ink);
        letter-spacing: -0.04em;
    }}
    .stamp-details {{
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
    }}
    .stamp-seal-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--badge-text);
        background: var(--badge-bg);
        border: 1px solid var(--badge-border);
        padding: 0.15rem 0.55rem;
        border-radius: 2px;
        width: fit-content;
    }}
    .stamp-label {{
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-ink);
        font-family: 'Newsreader', Georgia, serif;
    }}
    .stamp-sub {{
        font-size: 0.8rem;
        color: var(--text-muted);
    }}

    /* Hand-Drawn Ring & Target Box */
    .hero-target-box {{
        display: flex;
        align-items: center;
        gap: 1.25rem;
        border-left: 1px dashed var(--hairline);
        padding-left: 1.75rem;
    }}
    .ring-wrapper {{
        position: relative;
        width: 64px;
        height: 64px;
        flex-shrink: 0;
    }}
    .hand-drawn-ring {{
        transform: rotate(-90deg);
        transform-origin: 50% 50%;
    }}
    .ring-bg {{
        fill: none;
        stroke: var(--ring-track);
        stroke-width: 3.2;
    }}
    .ring-progress {{
        fill: none;
        stroke: var(--ring-stroke);
        stroke-width: 3.5;
        stroke-linecap: round;
        stroke-dasharray: 175;
        transition: stroke-dashoffset 1.4s cubic-bezier(0.16, 1, 0.3, 1);
    }}
    .ring-center-text {{
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.825rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-ink);
    }}

    .target-input-group {{
        display: flex;
        flex-direction: column;
        gap: 0.2rem;
        flex-grow: 1;
    }}
    .target-input-label {{
        font-size: 0.725rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-meta);
    }}

    /* Hero editorial trajectory footnote */
    .hero-stat-line {{
        margin-top: 1.15rem;
        padding-top: 0.85rem;
        border-top: 1px solid var(--hairline);
        font-size: 0.875rem;
        color: var(--text-muted);
        font-family: 'Newsreader', Georgia, serif;
        font-style: italic;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    .hero-stat-emphasis {{
        font-style: normal;
        font-weight: 600;
        color: var(--text-ink);
    }}

    /* -------------------------------------------------------------
       5. Direct Target Number Input
       ------------------------------------------------------------- */
    div[data-testid="stNumberInput"] {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    div[data-testid="stNumberInput"] input {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.45rem !important;
        font-weight: 700 !important;
        color: var(--accent-archival) !important;
        background: var(--surface-subtle) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 3px !important;
        padding: 0.2rem 0.6rem !important;
        height: 2.3rem !important;
    }}
    div[data-testid="stNumberInput"] input:focus {{
        border-color: var(--accent-archival) !important;
        box-shadow: 0 0 0 2px var(--badge-border) !important;
    }}

    /* -------------------------------------------------------------
       5b. Text Inputs & Elimination of Overlapping Instructions Glitch
       ------------------------------------------------------------- */
    [data-testid="InputInstructions"],
    [data-testid="InputInstructions"] *,
    [data-testid="stInputInstructions"],
    [data-testid="stInputInstructions"] *,
    .stInputInstructions,
    div[class*="InputInstructions"],
    div[class*="instructions"],
    div[class*="stInputInstructions"],
    [data-testid="stTextInput"] [data-testid="InputInstructions"],
    [data-testid="stTextInput"] [data-testid="InputInstructions"] *,
    [data-testid="stNumberInput"] [data-testid="InputInstructions"],
    [data-testid="stNumberInput"] [data-testid="InputInstructions"] *,
    [data-testid="stTextInput"] div:has(> [data-testid="InputInstructions"]),
    [data-testid="stNumberInput"] div:has(> [data-testid="InputInstructions"]) {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        left: -99999px !important;
    }}

    /* Container element for TextInput */
    div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"],
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] {{
        background-color: var(--surface-bg) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 4px !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        overflow: hidden !important;
    }}

    div[data-testid="stTextInput"] div[data-testid="stTextInputRootElement"]:focus-within,
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    div[data-testid="stTextInput"] div[data-baseweb="base-input"]:focus-within {{
        border-color: var(--accent-archival) !important;
        box-shadow: 0 0 0 2px var(--badge-border) !important;
        outline: none !important;
    }}

    div[data-testid="stTextInput"] input {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
        color: var(--text-ink) !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0.55rem 0.85rem !important;
    }}
    div[data-testid="stTextInput"] input:focus {{
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}
    div[data-testid="stTextInput"] input::placeholder {{
        color: var(--text-meta) !important;
        opacity: 0.75 !important;
    }}

    /* -------------------------------------------------------------
       6. Transcript Ledger Table (Replaces Boxed Cards)
       ------------------------------------------------------------- */
    .transcript-header-bar {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        padding-bottom: 0.5rem;
        border-bottom: 1.5px solid var(--text-ink);
        margin-bottom: 0.85rem;
    }}
    .ledger-headline {{
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        color: var(--text-ink);
    }}
    .ledger-count {{
        font-size: 0.775rem;
        color: var(--text-muted);
        font-family: 'JetBrains Mono', monospace;
    }}

    .transcript-table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1.25rem;
        font-size: 0.875rem;
    }}
    .transcript-table th {{
        text-align: left;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--text-meta);
        padding: 0.55rem 0.75rem;
        border-bottom: 1px solid var(--hairline);
    }}
    .transcript-table td {{
        padding: 0.75rem 0.75rem;
        border-bottom: 1px solid var(--hairline);
        color: var(--text-ink);
        transition: background-color 0.15s ease;
    }}
    .transcript-table tr:hover td {{
        background-color: var(--surface-subtle);
    }}
    .course-title-cell {{
        font-weight: 500;
        font-family: 'Newsreader', Georgia, serif;
        font-size: 0.975rem;
    }}
    .grade-stamp {{
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 0.775rem;
        padding: 0.15rem 0.45rem;
        border: 1px solid var(--hairline);
        border-radius: 2px;
        background: var(--surface-subtle);
    }}
    .grade-stamp-o {{ color: #1E3A2F; border-color: rgba(30, 58, 47, 0.3); background: rgba(30, 58, 47, 0.07); }}
    .grade-stamp-a {{ color: var(--accent-archival); border-color: var(--badge-border); background: var(--badge-bg); }}
    .grade-stamp-b {{ color: #8A6D3B; border-color: rgba(138, 109, 59, 0.3); background: rgba(138, 109, 59, 0.07); }}

    /* Staggered Row Entry Animation */
    .stagger-row {{
        animation: ledgerFadeIn 0.35s ease-out forwards;
    }}
    @keyframes ledgerFadeIn {{
        from {{ opacity: 0; transform: translateY(3px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* -------------------------------------------------------------
       7. Scholarly Marginalia Advisor Notes (Chat Panel)
       ------------------------------------------------------------- */
    .marginalia-header-bar {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        padding-bottom: 0.5rem;
        border-bottom: 1.5px solid var(--text-ink);
        margin-bottom: 0.85rem;
    }}
    .marginalia-title {{
        font-size: 1.25rem;
        font-weight: 600;
        margin: 0;
        color: var(--text-ink);
    }}

    /* Annotation Margin Cards */
    .marginalia-note {{
        position: relative;
        background: var(--surface-bg);
        border: 1px solid var(--hairline);
        border-left: 3px solid var(--accent-archival);
        border-radius: 3px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        transform: rotate(-0.25deg);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .marginalia-note:hover {{
        transform: rotate(0deg) translateY(-1px);
        box-shadow: 0 3px 8px rgba(0, 0, 0, 0.06);
    }}
    .marginalia-user {{
        border-left: 3px solid var(--text-meta);
        transform: rotate(0.2deg);
        background: var(--surface-subtle);
    }}
    .marginalia-kicker {{
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--accent-archival);
        margin-bottom: 0.35rem;
    }}
    .marginalia-content {{
        font-size: 0.875rem;
        line-height: 1.55;
        color: var(--text-ink);
    }}

    /* Citations / Tool execution traces */
    .citation-block {{
        margin: 0.5rem 0;
        padding: 0.45rem 0.65rem;
        background: var(--surface-subtle);
        border: 1px dashed var(--hairline);
        border-radius: 2px;
        font-size: 0.74rem;
        font-family: 'JetBrains Mono', monospace;
    }}
    .citation-mark {{
        font-weight: 700;
        color: var(--accent-archival);
        margin-right: 0.4rem;
    }}

    /* -------------------------------------------------------------
       8. Paper Lift Buttons
       ------------------------------------------------------------- */
    .stButton > button,
    button[kind="primary"],
    [data-testid="stFormSubmitButton"] > button,
    [data-testid="stBaseButton-primary"],
    [data-testid="stBaseButton-secondary"] {{
        background-color: var(--btn-bg) !important;
        color: var(--btn-text) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 3px !important;
        font-weight: 600 !important;
        font-size: 0.825rem !important;
        padding: 0.45rem 0.95rem !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08) !important;
        transition: all 0.15s ease !important;
    }}
    .stButton > button:hover,
    button[kind="primary"]:hover,
    [data-testid="stFormSubmitButton"] > button:hover {{
        background-color: var(--btn-hover) !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.12) !important;
    }}
    .stButton > button:active,
    [data-testid="stFormSubmitButton"] > button:active {{
        transform: translateY(0) !important;
    }}

    /* -------------------------------------------------------------
       9. Sidebar as Archival Navigation Register
       ------------------------------------------------------------- */
    [data-testid="stSidebar"] {{
        background-color: var(--surface-subtle) !important;
        border-right: 1px solid var(--hairline) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0.75rem !important;
    }}

    /* -------------------------------------------------------------
       10. Addendum / Scenario Projections
       ------------------------------------------------------------- */
    .addendum-container {{
        margin-top: 1.85rem;
        padding-top: 1.25rem;
        border-top: 1.5px solid var(--hairline);
    }}
    .addendum-title {{
        font-size: 0.725rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: var(--text-meta);
        margin-bottom: 0.75rem;
    }}
    .addendum-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.25rem;
    }}
    .addendum-col {{
        padding: 0.85rem 1rem;
        border-left: 2px solid var(--hairline);
        background: var(--surface-bg);
    }}
    .addendum-col-best {{ border-left-color: #1E3A2F; }}
    .addendum-col-target {{ border-left-color: var(--accent-archival); }}
    .addendum-col-worst {{ border-left-color: #8A6D3B; }}

    .addendum-metric {{
        font-size: 1.5rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-ink);
    }}
    .addendum-label {{
        font-size: 0.725rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
        margin-bottom: 0.2rem;
    }}
    .addendum-desc {{
        font-size: 0.775rem;
        color: var(--text-muted);
        line-height: 1.4;
        margin-top: 0.35rem;
        font-family: 'Newsreader', Georgia, serif;
        font-style: italic;
    }}
    </style>

    <!-- Interactive Mouse Spotlight -->
    <div id="academic-spotlight"></div>
    <script>
    (function() {{
        const spotlight = document.getElementById('academic-spotlight');
        if (spotlight) {{
            window.addEventListener('mousemove', function(e) {{
                spotlight.style.left = e.clientX + 'px';
                spotlight.style.top = e.clientY + 'px';
            }}, {{ passive: true }});
        }}
    }})();
    </script>
    """
    st.markdown(css, unsafe_allow_html=True)


# ==============================================================================
# 3. SESSION STATE MANAGEMENT
# ==============================================================================

def init_session_state():
    # Theme: "paper" (Oxford Paper) or "chalkboard" (Cambridge Chalkboard)
    if "academic_theme" not in st.session_state:
        st.session_state.academic_theme = "paper"

    if "student_name" not in st.session_state:
        st.session_state.student_name = "Alex Morgan"

    if "major" not in st.session_state:
        st.session_state.major = "Computer Science & Artificial Intelligence"

    if "target_gpa" not in st.session_state:
        st.session_state.target_gpa = 8.50

    if "direct_target_gpa_input" not in st.session_state:
        st.session_state.direct_target_gpa_input = 8.50

    if "remaining_credits" not in st.session_state:
        st.session_state.remaining_credits = 16.0

    if "courses" not in st.session_state:
        st.session_state.courses = dict(agent_memory.courses)
    else:
        agent_memory.courses = dict(st.session_state.courses)

    if "agent_history" not in st.session_state:
        st.session_state.agent_history = None

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I am your AI GPA Advisor.\n\n"
                    "I calculate your exact credit-weighted GPA, help you plan upcoming semesters, "
                    "and figure out what grades you need to reach your target GPA.\n\n"
                    "Try asking me:\n"
                    "• *'What average grade do I need to reach an 8.5 GPA?'*\n"
                    "• *'Add Machine Learning with grade A+ and 4 credits.'*\n"
                    "• *'Can I mathematically reach a 9.2 GPA with my remaining credits?'*"
                ),
                "traces": [],
            }
        ]


def safe_add_course(course: str, grade: str, credits: float):
    if hasattr(agent_memory, "add_course"):
        res = agent_memory.add_course(course, grade, credits)
    else:
        res = agent_memory.add_grade(course, grade, credits)
    st.session_state.courses = dict(agent_memory.courses)
    return res


def safe_remove_course(course: str):
    if hasattr(agent_memory, "remove_course"):
        res = agent_memory.remove_course(course)
    else:
        res = agent_memory.remove_grade(course)
    st.session_state.courses = dict(agent_memory.courses)
    return res


def load_sample_dataset():
    clear_session()
    sample_catalog = [
        ("Data Structures & Algorithms", "A+", 4.0),
        ("Linear Algebra & Optimization", "O", 4.0),
        ("Computer Systems Architecture", "A", 3.0),
        ("Discrete Mathematics", "B+", 3.0),
    ]
    for c_name, c_grade, c_credits in sample_catalog:
        safe_add_course(c_name, c_grade, c_credits)

    st.session_state.courses = dict(agent_memory.courses)
    st.session_state.agent_history = None
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Sample coursework loaded (14.0 credits earned). "
                "Your GPA and future trajectory projections have been updated."
            ),
            "traces": [],
        }
    ]
    st.toast("Sample courses loaded successfully!", icon="📚")


def clear_all_data():
    clear_session()
    st.session_state.courses = {}
    st.session_state.agent_history = None
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": "All courses cleared. Ready to record new courses or start fresh.",
            "traces": [],
        }
    ]
    st.toast("All courses cleared.", icon="🧹")


# ==============================================================================
# 4. AGENT CONVERSATION ENGINE & TRACE EXTRACTION
# ==============================================================================

def extract_turn_trace(new_messages: list) -> list:
    traces = []
    for msg in new_messages:
        # Check for tool_calls in dictionary or object form
        tool_calls = msg.get("tool_calls") if isinstance(msg, dict) else getattr(msg, "tool_calls", None)
        if tool_calls:
            for tc in tool_calls:
                tc_fn = tc.get("function", {}) if isinstance(tc, dict) else getattr(tc, "function", {})
                fn_name = tc_fn.get("name", "tool") if isinstance(tc_fn, dict) else getattr(tc_fn, "name", "tool")
                raw_args = tc_fn.get("arguments", "{}") if isinstance(tc_fn, dict) else getattr(tc_fn, "arguments", "{}")
                try:
                    args_dict = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                except Exception:
                    args_dict = {"raw": raw_args}
                traces.append({
                    "tool": fn_name,
                    "arguments": args_dict,
                    "output": None,
                })
        # Check for tool output in dictionary or object form
        role = msg.get("role") if isinstance(msg, dict) else getattr(msg, "role", None)
        if role == "tool":
            tool_content = msg.get("content", "") if isinstance(msg, dict) else getattr(msg, "content", "")
            for tr in reversed(traces):
                if tr["output"] is None:
                    tr["output"] = tool_content
                    break
    return traces


def handle_user_prompt(prompt: str):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})

    # Ensure agent memory has all manually entered courses
    if "courses" in st.session_state:
        agent_memory.courses = dict(st.session_state.courses)

    with st.spinner("Analyzing with GPA Advisor..."):
        try:
            old_history = st.session_state.agent_history or []
            old_length = len(old_history)

            final_answer, updated_history = run_agent(
                goal=prompt,
                conversation_history=st.session_state.agent_history,
                verbose=False,
            )
            st.session_state.agent_history = updated_history

            # Keep session state updated with any courses added or removed by the agent
            st.session_state.courses = dict(agent_memory.courses)

            new_msgs = updated_history[old_length:] if old_length > 0 else updated_history
            turn_traces = extract_turn_trace(new_msgs)

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": final_answer,
                "traces": turn_traces,
            })
        except Exception as e:
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": f"Advisor error: {str(e)}",
                "traces": [],
            })


# ==============================================================================
# 5. MASTHEAD & SIDEBAR REGISTER
# ==============================================================================

def render_masthead():
    try:
        model_desc = describe()
    except Exception:
        model_desc = "Groq / openai/gpt-oss-20b"

    theme_label = "Chalkboard 🏛️" if st.session_state.academic_theme == "paper" else "Oxford Paper 📜"

    col_meta, col_btn = st.columns([4, 1.2])
    with col_meta:
        render_html(f"""
            <div class="academic-masthead">
                <div class="masthead-left">
                    <span class="masthead-kicker">AI Academic Planning • CSE476</span>
                    <h1 class="masthead-title">GPA Advisor</h1>
                    <span class="masthead-meta">Smart GPA planning, course tracking, and trajectory insights</span>
                </div>
                <div class="masthead-right">
                    <span class="edition-tag">{html.escape(model_desc)}</span>
                </div>
            </div>
        """)
    with col_btn:
        if st.button(f"Switch to {theme_label}", use_container_width=True):
            st.session_state.academic_theme = "chalkboard" if st.session_state.academic_theme == "paper" else "paper"
            st.rerun()


def render_sidebar():
    with st.sidebar:
        mortar_icon = render_svg("mortarboard", size=15, color="currentColor")
        render_html(f"<div style='font-size:0.95rem; font-weight:700; font-family:Newsreader, Georgia, serif;'>{mortar_icon} Student Profile</div>")
        st.caption("Your degree and credit settings")

        st.session_state.student_name = st.text_input(
            "Student Name",
            value=st.session_state.student_name,
            help="Your name for course reports",
        )
        st.session_state.major = st.text_input(
            "Degree / Major",
            value=st.session_state.major,
            help="Your major or specialization",
        )
        st.session_state.remaining_credits = st.number_input(
            "Remaining Credits",
            min_value=1.0,
            max_value=160.0,
            value=float(st.session_state.remaining_credits),
            step=1.0,
            help="Credits left to complete your degree requirements",
        )

        st.divider()

        render_html("<div style='font-size:0.75rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-meta); margin-bottom:0.4rem;'>Quick Actions</div>")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Load Samples", use_container_width=True):
                load_sample_dataset()
                st.rerun()
        with c2:
            if st.button("Reset All", use_container_width=True):
                clear_all_data()
                st.rerun()

        with st.expander("Grade Scale (10-Point Scale)", expanded=False):
            st.markdown(
                """
                | Grade | Points | Classification |
                | :---: | :---: | :--- |
                | **O**  | 10.0 | Outstanding |
                | **A+** | 9.0  | Excellent |
                | **A**  | 8.0  | Very Good |
                | **B+** | 7.0  | Good |
                | **B**  | 6.0  | Above Average |
                | **C**  | 5.0  | Average |
                | **D**  | 4.0  | Pass |
                | **F**  | 0.0  | Fail |
                """
            )


# ==============================================================================
# 6. ASYMMETRIC HERO: STAMPED GRADE & HAND-DRAWN PROGRESS RING
# ==============================================================================

def render_hand_drawn_ring(pct: float) -> str:
    """
    Render an SVG circular progress ring with a hand-drawn stroke feel
    and animated stroke-dashoffset tracing.
    """
    clamped = max(0.0, min(pct, 100.0))
    radius = 26
    circ = 2 * math.pi * radius  # ~163.36
    offset = circ * (1.0 - (clamped / 100.0))

    # Organic hand-drawn stroke wobble with slight dash irregularity
    return (
        f'<div class="ring-wrapper">'
        f'<svg class="hand-drawn-ring" width="64" height="64" viewBox="0 0 64 64">'
        f'<circle class="ring-bg" cx="32" cy="32" r="{radius}" stroke-dasharray="163" />'
        f'<circle class="ring-progress" cx="32" cy="32" r="{radius}" '
        f'style="stroke-dasharray: {circ:.2f}; stroke-dashoffset: {offset:.2f};" />'
        f'</svg>'
        f'<div class="ring-center-text">{clamped:.0f}%</div>'
        f'</div>'
    )


def render_academic_hero(gpa_data: dict, remaining_credits: float):
    current_gpa = gpa_data["gpa"]
    total_credits = gpa_data["total_credits"]

    remaining_credits = st.session_state.get("direct_remaining_credits_input", st.session_state.get("remaining_credits", 16.0))
    st.session_state.remaining_credits = remaining_credits
    agent_memory.remaining_credits = remaining_credits

    deg_total = total_credits + remaining_credits

    target_gpa = st.session_state.get("direct_target_gpa_input", st.session_state.get("target_gpa", 8.50))
    st.session_state.target_gpa = target_gpa

    # 1. Stamped Grade Value & Status Badge
    if current_gpa is None:
        gpa_display = "—"
        seal_text = "No Courses Added"
    else:
        gpa_display = f"{current_gpa:.2f}"
        if current_gpa >= 9.0:
            seal_text = "Outstanding Standing"
        elif current_gpa >= 8.0:
            seal_text = "First Class Standing"
        elif current_gpa >= 7.0:
            seal_text = "Very Good Standing"
        elif current_gpa >= 6.0:
            seal_text = "Good Standing"
        else:
            seal_text = "Academic Review Notice"

    # 2. Target Progress & Required Trajectory Math
    if target_gpa and target_gpa > 0 and current_gpa is not None:
        pct = (current_gpa / target_gpa) * 100.0
        ring_html = render_hand_drawn_ring(pct)

        current_points = gpa_data["total_weighted_points"]
        points_needed = (target_gpa * deg_total) - current_points
        required_avg = points_needed / remaining_credits

        if required_avg <= 0:
            req_text = "Target GPA is already secured by your earned points!"
        elif required_avg > 10.0:
            req_text = f"Target {target_gpa:.2f} exceeds the 10.0 ceiling (would require an impossible {required_avg:.2f} average)."
        else:
            req_text = f"Requires an average grade of <span class='hero-stat-emphasis'>{required_avg:.2f}/10</span> across your remaining <span class='hero-stat-emphasis'>{remaining_credits:.0f} credits</span>."
    else:
        ring_html = render_hand_drawn_ring(0.0)
        req_text = "Type your target graduation GPA and remaining credits to see your live trajectory."

    # Render Asymmetric Plinth
    render_html(f"""
        <div class="hero-plinth">
            <div class="hero-stamp-box">
                <div class="stamp-gpa-number">{gpa_display}</div>
                <div class="stamp-details">
                    <div class="stamp-seal-badge">{seal_text}</div>
                    <div class="stamp-label">Current Cumulative GPA</div>
                    <div class="stamp-sub">{total_credits:.1f} credits completed • {deg_total:.0f} total degree credits</div>
                </div>
            </div>
            <div class="hero-target-box">
                {ring_html}
                <div class="target-input-group">
                    <span class="target-input-label">Target GPA & Remaining Credits</span>
                </div>
            </div>
        </div>
    """)

    # Render Direct Number Inputs inside the target area (cleanly below the plinth row)
    col_l, col_r = st.columns([1.55, 1.0])
    with col_r:
        col_t, col_c = st.columns([1.1, 1.0])
        with col_t:
            st.caption("Target GPA")
            curr_val = float(target_gpa) if (target_gpa is not None and target_gpa > 0) else 8.50
            new_target = st.number_input(
                "Target Graduation GPA",
                min_value=0.0,
                max_value=10.0,
                value=curr_val,
                step=0.05,
                format="%.2f",
                key="direct_target_gpa_input",
                label_visibility="collapsed",
                help="Type your target graduation GPA directly into this box",
            )
            st.session_state.target_gpa = new_target
        with col_c:
            st.caption("Remaining Cr.")
            curr_rem = float(remaining_credits) if (remaining_credits is not None and remaining_credits > 0) else 16.0
            new_credits = st.number_input(
                "Remaining Credits Input",
                min_value=1.0,
                max_value=120.0,
                value=curr_rem,
                step=1.0,
                format="%.0f",
                key="direct_remaining_credits_input",
                label_visibility="collapsed",
                help="Change how many remaining credits you have left to complete",
            )
            st.session_state.remaining_credits = new_credits
            agent_memory.remaining_credits = new_credits

    # Editorial Footnote
    render_html(f"""
        <div class="hero-stat-line">
            <span>{req_text}</span>
            <span class="tabular-mono" style="font-size:0.75rem;">LIVE TRAJECTORY</span>
        </div>
    """)


# ==============================================================================
# 7. TRANSCRIPT LEDGER & ARCHIVAL PLOTLY TREND
# ==============================================================================

def render_archival_gpa_trend():
    """Render a quiet, editorial Plotly chart plotted on cardstock/chalkboard canvas."""
    courses = agent_memory.courses
    if not courses or len(courses) == 0:
        return

    names = []
    gpas = []
    cum_points = 0.0
    cum_credits = 0.0

    for name, info in courses.items():
        grd = info["grade"]
        pts = GRADE_POINTS.get(grd, 0)
        crd = info["credits"]
        cum_points += pts * crd
        cum_credits += crd
        names.append(name)
        gpas.append(round(cum_points / cum_credits, 2))

    target = st.session_state.get("target_gpa", 8.50)
    theme = st.session_state.academic_theme

    line_color = "#7E2228" if theme == "paper" else "#52B788"
    grid_color = "rgba(28, 24, 16, 0.06)" if theme == "paper" else "rgba(232, 236, 233, 0.08)"
    text_color = "#8A8275" if theme == "paper" else "#9EB0A5"
    fill_color = "rgba(126, 34, 40, 0.04)" if theme == "paper" else "rgba(82, 183, 136, 0.06)"

    fig = go.Figure()

    if target and target > 0:
        fig.add_trace(go.Scatter(
            x=names,
            y=[target] * len(names),
            mode="lines",
            name=f"Target ({target:.2f})",
            line=dict(color=text_color, width=1.5, dash="dot"),
            hoverinfo="name+y",
        ))

    fig.add_trace(go.Scatter(
        x=names,
        y=gpas,
        mode="lines+markers",
        name="Cumulative CGPA",
        line=dict(color=line_color, width=2.5, shape="spline"),
        marker=dict(size=6, color=line_color),
        fill="tozeroy",
        fillcolor=fill_color,
        hovertemplate="<b>%{x}</b><br>Cumulative CGPA: %{y:.2f}<extra></extra>",
    ))

    y_min = max(0.0, min(gpas + ([target] if target else [])) - 0.75)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=10, b=10),
        height=160,
        showlegend=False,
        hovermode="x unified",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=10, color=text_color, family="Inter, sans-serif"),
            showline=True,
            linecolor=grid_color,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=False,
            tickfont=dict(size=10, color=text_color, family="JetBrains Mono, monospace"),
            range=[y_min, 10.2],
            showline=False,
        ),
    )

    render_html("<div style='font-size:0.725rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--text-meta); margin:1.25rem 0 0.4rem 0;'>GPA Trend Progression:</div>")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_transcript_ledger(gpa_data: dict):
    courses = agent_memory.courses

    render_html(f"""
        <div class="transcript-header-bar">
            <h2 class="ledger-headline">Course History</h2>
            <span class="ledger-count">{len(courses)} COURSES LOGGED</span>
        </div>
    """)

    if not courses:
        render_html("""
            <div style="text-align:center; padding:2.5rem 1.5rem; background:var(--surface-subtle); border:1px dashed var(--hairline); border-radius:3px; margin-bottom:1rem;">
                <p style="font-family:'Newsreader', Georgia, serif; font-size:1.1rem; color:var(--text-ink); margin:0 0 0.35rem 0;">No courses added yet</p>
                <p style="font-size:0.8rem; color:var(--text-muted); margin:0;">Add your courses below, click 'Load Samples' in the sidebar, or ask the AI advisor.</p>
            </div>
        """)
    else:
        table_rows = []
        for idx, (course_name, course_info) in enumerate(courses.items(), 1):
            grd = course_info["grade"]
            pts = GRADE_POINTS.get(grd, 0)
            crd = course_info["credits"]
            weighted = pts * crd

            if pts >= 9:
                stamp_cls = "grade-stamp-o"
            elif pts >= 7:
                stamp_cls = "grade-stamp-a"
            else:
                stamp_cls = "grade-stamp-b"

            delay = idx * 0.04
            row_html = (
                f"<tr class='stagger-row' style='animation-delay:{delay:.2f}s;'>"
                f"<td class='course-title-cell'>{html.escape(course_name)}</td>"
                f"<td class='tabular-mono' style='color:var(--text-muted);'>{crd:.1f} cr</td>"
                f"<td><span class='grade-stamp {stamp_cls}'>{grd} ({pts}.0)</span></td>"
                f"<td class='tabular-mono' style='color:var(--text-ink); font-weight:600;'>{weighted:.1f} pts</td>"
                f"</tr>"
            )
            table_rows.append(row_html)

        table_html = (
            "<table class='transcript-table'>"
            "<thead><tr>"
            "<th style='width: 46%;'>Course Title</th>"
            "<th style='width: 18%;'>Credits</th>"
            "<th style='width: 18%;'>Grade</th>"
            "<th style='width: 18%;'>Points</th>"
            "</tr></thead>"
            "<tbody>"
            f"{''.join(table_rows)}"
            "</tbody></table>"
        )
        render_html(table_html)

        # Inline Course Removal
        c_del1, c_del2 = st.columns([3, 1.2])
        with c_del1:
            to_remove = st.selectbox(
                "Select course to remove",
                options=list(courses.keys()),
                label_visibility="collapsed",
            )
        with c_del2:
            if st.button("Remove Course", use_container_width=True):
                safe_remove_course(to_remove)
                st.toast(f"Removed '{to_remove}'.", icon="🗑️")
                st.rerun()

    # Collapsible Course Addition Drawer
    with st.expander("Add a Course", expanded=False):
        with st.form("new_course_entry_form", clear_on_submit=True):
            f_col1, f_col2, f_col3 = st.columns([2.5, 1, 1])
            with f_col1:
                in_name = st.text_input("Course Title", placeholder="e.g. Machine Learning")
            with f_col2:
                in_credits = st.number_input("Credits", min_value=1.0, max_value=12.0, value=4.0, step=0.5)
            with f_col3:
                in_grade = st.selectbox("Grade", options=["O", "A+", "A", "B+", "B", "C", "D", "F"], index=1)

            submit_course = st.form_submit_button("Add Course", type="primary", use_container_width=True)
            if submit_course:
                if in_name.strip():
                    safe_add_course(in_name.strip(), in_grade, in_credits)
                    st.toast(f"Added '{in_name.strip()}' ({in_grade}, {in_credits} cr).", icon="✍️")
                    st.rerun()
                else:
                    st.warning("Please provide a course title.")

    # GPA Progression Chart
    render_archival_gpa_trend()

    # Addendum: Sensitivity Analysis
    render_academic_addendum(gpa_data)


def render_academic_addendum(gpa_data: dict):
    rem_credits = st.session_state.remaining_credits
    if rem_credits <= 0:
        return

    curr_points = gpa_data["total_weighted_points"]
    curr_credits = gpa_data["total_credits"]
    final_credits = curr_credits + rem_credits
    target_gpa = st.session_state.target_gpa

    best_gpa = (curr_points + (10.0 * rem_credits)) / final_credits
    worst_gpa = (curr_points + (4.0 * rem_credits)) / final_credits

    if target_gpa and target_gpa > 0:
        needed_pts = (target_gpa * final_credits) - curr_points
        req_avg = needed_pts / rem_credits
        if req_avg <= 0:
            target_desc = "Goal already secured with existing credits!"
        elif req_avg > 10.0:
            target_desc = "Exceeds 10.0 ceiling (mathematically impossible)."
        else:
            target_desc = f"Requires an average of {req_avg:.2f}/10 in future courses."
        target_display = f"{target_gpa:.2f}"
    else:
        target_display = "—"
        target_desc = "Set a target GPA above to simulate."

    render_html(f"""
        <div class="addendum-container">
            <div class="addendum-title">What-If Future Scenarios ({rem_credits:.0f} remaining credits)</div>
            <div class="addendum-grid">
                <div class="addendum-col addendum-col-best">
                    <div class="addendum-label">Best-Case Scenario</div>
                    <div class="addendum-metric">{best_gpa:.2f}</div>
                    <div class="addendum-desc">If you score straight 10.0 (O) in all remaining credits.</div>
                </div>
                <div class="addendum-col addendum-col-target">
                    <div class="addendum-label">Target Goal</div>
                    <div class="addendum-metric">{target_display}</div>
                    <div class="addendum-desc">{target_desc}</div>
                </div>
                <div class="addendum-col addendum-col-worst">
                    <div class="addendum-label">Worst-Case Scenario</div>
                    <div class="addendum-metric">{worst_gpa:.2f}</div>
                    <div class="addendum-desc">If you score minimum passing 4.0 (D) in all remaining credits.</div>
                </div>
            </div>
        </div>
    """)


# ==============================================================================
# 8. SCHOLARLY MARGINALIA & ADVISOR COUNSEL (MARGIN NOTES CHAT)
# ==============================================================================

def render_marginalia_advisor():
    sparkle_icon = render_svg("quill", size=16, color="currentColor")
    render_html(f"""
        <div class="marginalia-header-bar">
            <h2 class="marginalia-title">{sparkle_icon} AI GPA Advisor</h2>
            <span style="font-size:0.75rem; color:var(--text-meta); font-family:'JetBrains Mono', monospace;">AUTONOMOUS ASSISTANT</span>
        </div>
    """)
    st.caption("Ask questions, plan target semesters, and get instant grade calculations")

    # Quick Inquiries
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("Trajectory Audit", use_container_width=True):
            t_str = f"{st.session_state.target_gpa:.2f}" if (st.session_state.target_gpa and st.session_state.target_gpa > 0) else "8.5"
            p = f"Calculate my current GPA from session memory. I have {st.session_state.remaining_credits} credits remaining. What average grade point do I need to reach a target GPA of {t_str}?"
            handle_user_prompt(p)
            st.rerun()

    with q2:
        if st.button("Log AI & ML", use_container_width=True):
            p = "Add Artificial Intelligence with grade A and 4 credits. Add Machine Learning with grade A+ and 3 credits. Then compute my new GPA."
            handle_user_prompt(p)
            st.rerun()

    with q3:
        if st.button("Can I Reach 9.5?", use_container_width=True):
            p = f"Can I mathematically reach a 9.50 GPA with my remaining {st.session_state.remaining_credits} credits? Explain using tool calculations."
            handle_user_prompt(p)
            st.rerun()

    # Contained Scrollable Window
    with st.container(height=390):
        for msg in st.session_state.chat_messages:
            role = msg["role"]
            is_assistant = (role == "assistant")
            note_cls = "marginalia-note" if is_assistant else "marginalia-note marginalia-user"
            kicker_text = "GPA Advisor" if is_assistant else f"{st.session_state.student_name}"

            # Render note card
            render_html(f"""
                <div class="{note_cls}">
                    <div class="marginalia-kicker">{kicker_text}</div>
                </div>
            """)

            # Render tool citations if present
            traces = msg.get("traces", [])
            if traces:
                with st.expander(f"Advisor Calculations & Tool Actions ({len(traces)})", expanded=False):
                    for step_idx, event in enumerate(traces, 1):
                        tool_name = event["tool"]
                        args_json = json.dumps(event["arguments"])
                        output_text = str(event["output"] or "None")
                        render_html(f"""
                            <div class="citation-block">
                                <div><span class="citation-mark">Step {step_idx}</span>Tool: <strong>{html.escape(tool_name)}</strong></div>
                                <div style="color:var(--text-muted); margin-top:0.15rem;">Arguments: {html.escape(args_json)}</div>
                                <div style="color:var(--text-ink); margin-top:0.2rem; white-space:pre-wrap;">Result: {html.escape(output_text)}</div>
                            </div>
                        """)

            # Message content
            st.markdown(msg["content"])

    # Embedded Chat Form
    with st.form("marginal_inquiry_form", clear_on_submit=True):
        col_txt, col_btn = st.columns([4.8, 1.2])
        with col_txt:
            user_in = st.text_input(
                "Question",
                placeholder="Ask GPA Advisor anything (e.g., 'What grades do I need for 8.5?')...",
                label_visibility="collapsed",
            )
        with col_btn:
            send_inquiry = st.form_submit_button("Send", type="primary", use_container_width=True)

        if send_inquiry and user_in.strip():
            handle_user_prompt(user_in.strip())
            st.rerun()


# ==============================================================================
# 9. MAIN ORCHESTRATION
# ==============================================================================

def main():
    setup_page()
    init_session_state()
    inject_academic_css(st.session_state.academic_theme)

    # Sync target GPA from direct input
    if "direct_target_gpa_input" in st.session_state:
        st.session_state.target_gpa = st.session_state.direct_target_gpa_input

    render_masthead()
    render_sidebar()

    gpa_data = agent_memory.get_current_gpa_data()

    # 1. Asymmetric Hero: Stamped Grade & Hand-Drawn Progress Ring
    render_academic_hero(
        gpa_data=gpa_data,
        remaining_credits=st.session_state.remaining_credits,
    )

    # 2. Scholarly Columns: Course Ledger (Left) and Marginalia Advisor (Right)
    col_ledger, col_marginalia = st.columns([1.18, 1.22], gap="large")

    with col_ledger:
        render_transcript_ledger(gpa_data=gpa_data)

    with col_marginalia:
        render_marginalia_advisor()


if __name__ == "__main__":
    main()
