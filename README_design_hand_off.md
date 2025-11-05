# Patient Monitor Interface Design Hand-Off

## Overview
This document provides the design specifications, component library, and hand-off guidelines for the Patient Monitor Interface. The design is inspired by professional medical monitors with distinct innovations for improved usability in high-stress clinical environments.

## Design Philosophy
- **High Contrast & Readability**: Deep charcoal background (#0D0D0D) reduces eye strain while maintaining contrast.
- **Minimalist & Focused**: Limits visible parameters to ~5 key vitals to avoid overload.
- **Responsive & Scalable**: Designed for 27" 2560×1440 monitors, readable from 1 meter, with responsive scaling.
- **Innovations**: Charcoal background, red flashing outlines for critical values, waveform overlap/fade, semi-transparent footer overlay, clear units/labels.

## Color Palette
- **Background**: #0D0D0D (Deep Charcoal)
- **Text Grey-White**: #E0E0E0 (Labels, secondary text)
- **Primary Colors**:
  - HR/ECG II: #00FF00 (Bright Lime Green)
  - ECG I: #32CD32 (Slightly Cooler Green)
  - SpO₂/Pleth: #00FFFF (Cyan-Blue)
  - Resp: #FFD700 (Golden-Yellow)
  - NIBP: #FFFFFF (White)
- **Alert**: #FF4C4C (Bright Red for critical values)
- **Status**: #FFC200 (Amber for messages)
- **Footer Icons**: #BFBFBF (Light Grey, #FFFFFF on hover)
- **Footer Overlay**: rgba(26, 26, 26, 0.7)

## Typography
- **Font Family**: Roboto (Sans-serif)
- **Weights**: Bold for numbers, Regular for labels
- **Font Sizes** (scaled for 27" monitor, readable from 1m):
  - HR: ~80pt
  - SpO₂: ~75pt
  - Resp: ~70pt
  - NIBP: ~65pt
  - Units: ~30pt
  - Labels: ~20pt
  - Waveform Labels: ~12pt
- **Spacing**: Vertical spacing ~40px between main numbers, consistent margin ~24px around elements.

## Grid Structure
- **Layout**: CSS Grid with custom 12-column inspired structure.
- **Main Grid**: 1fr (left waveforms) : 2fr (right vitals)
- **Rows**: Auto (status) : 1fr (main) : Auto (footer)
- **Responsive**: Scales down for smaller screens using media queries.

## Component Library

### 1. Waveform Strip Component
- **Purpose**: Displays ECG, Pleth, Resp waveforms.
- **Structure**: Label (top-left), SVG canvas for waveform.
- **Features**: Overlap/fade at bottom edge (-20px margin), scrolling animation.
- **Variants**: ECG II (lime), ECG I (cooler green), Pleth (cyan), Resp (yellow).
- **Reusable**: Yes, with configurable color, label, and data source.

### 2. Numeric Vital Card Component
- **Purpose**: Displays HR, SpO₂, Resp, NIBP.
- **Structure**: Label (above), Value + Unit (centered).
- **Features**: Bold numbers, color-coded, critical flashing (red outline for 2s).
- **Variants**: Single line (HR, SpO₂, Resp), Stacked (NIBP systolic/diastolic).
- **Reusable**: Yes, with props for label, value, unit, color, critical state.

### 3. Status Bar Component
- **Purpose**: Top-right status indicators.
- **Structure**: Icons (battery, signal) + text message area.
- **Features**: Minimalist white icons on dark bg, amber text for messages.
- **Reusable**: Yes, with dynamic icon states and message updates.

### 4. Footer Control Button Component
- **Purpose**: Operational controls (Alarm Reset, Freeze, Setup, Display Mode).
- **Structure**: Line-icon SVG.
- **Features**: Light grey, white on hover/touch.
- **Reusable**: Yes, with icon SVG and click handler.

### 5. Trend Panel Component
- **Purpose**: NIBP sparkline and temperature indicators.
- **Structure**: Sparkline graph + temp labels/values.
- **Features**: Small graph for trends, dual temp display.
- **Reusable**: Yes, with data arrays for trends.

## Asset Export Guidelines
- **Format**: Export as SVG for vectors (icons, waveforms), PNG for raster elements.
- **Resolution**: 2x for high-DPI monitors (e.g., 2560×1440).
- **Naming Convention**:
  - Components: `component-name-variant.svg` (e.g., `waveform-ecg-ii.svg`)
  - Icons: `icon-name.svg` (e.g., `battery.svg`)
  - Colors: Use CSS custom properties for easy theming.
- **File Structure**:
  - `/assets/icons/` - SVG icons
  - `/assets/components/` - Component screenshots/mockups
  - `/assets/palette/` - Color swatches

## Implementation Notes
- **Frameworks**: Designed for web (HTML/CSS/JS) but adaptable to Qt/PySide6 or native apps.
- **Animations**: CSS for flashing, JS for data updates.
- **Accessibility**: High contrast, large fonts, clear labels.
- **Testing**: Verify readability at 1m distance, responsiveness on various screen sizes.

## Next Steps
1. Import HTML mockup into Figma/Sketch for refinement.
2. Create interactive prototypes.
3. Develop component library in target framework.
4. Conduct usability testing in clinical environment.

## Files Provided
- `patient_monitor_mockup.html`: Complete HTML/CSS/JS mockup.
- This README for specifications.

For questions or refinements, refer to the mockup and adjust as needed.
