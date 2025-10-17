# Patient Monitor Components Development TODO

## Step 1: Create Vital Sign Widget Component
- [x] Create `vital_sign_widget.py` file
- [x] Implement VitalSignWidget class as QWidget subclass
- [x] Add constructor to accept label, value, unit, color parameters
- [x] Implement styling: black background, sans-serif font (Courier New, 24pt bold), specific colors, glow shadow effect
- [x] Add update_value method for dynamic data updates
- [x] Ensure text format: "LABEL\nVALUE UNIT"

## Step 2: Create Waveform Widget Component
- [x] Create `waveform_widget.py` file
- [x] Implement WaveformWidget class as QWidget subclass using pyqtgraph.PlotWidget
- [x] Add constructor to accept title/label parameter
- [x] Implement Mindray-like styling: black background, white foreground, subtle grid, axis pens
- [x] Add update_data method to plot dynamic waveform data (e.g., arrays for ECG, Pleth, etc.)
- [x] Ensure antialiasing and proper axis configuration

## Step 3: Create SpO2 and Respiration Combined Panel Component
- [x] Create `spo2_resp_widget.py` file
- [x] Implement Spo2RespWidget class as QWidget subclass
- [x] Top half: SpO2 section with label, large cyan value, alarm limits to right, secondary params (PI, PR, Source) to right
- [x] Bottom half: Resp section with label, large yellow value, alarm limits to right
- [x] Accept data object: { "spo2": 98, "spo2HighLimit": 100, "pulseRate": 60, "respirationRate": 20, "respHighLimit": 30, ... }
- [x] Implement styling: black background, sans-serif fonts, specific colors, layout with QHBoxLayout and QVBoxLayout
- [x] Add update_data method for dynamic updates

## Step 3.5: Create NIBP Panel Component
- [x] Create `nibp_widget.py` file
- [x] Implement NibpWidget class as QWidget subclass
- [x] Main reading: '120/80' in large bold white font, '(93)' in same size regular weight next to it
- [x] To the right: last measurement time '16:54' and mode 'Manual' in smaller white font
- [x] Below: vertical bar graph with high limit at top, low limit at bottom
- [x] Accept data object: { "systolic": 120, "diastolic": 80, "map": 93, "lastMeasuredTime": "16:54", "mode": "Manual", ... }
- [x] Implement styling: black background, sans-serif fonts, white text, vertical bar for limits
- [x] Add update_data method for dynamic updates

## Step 4: Integrate Components (Optional)
- [x] Update `monitor_ui.py` to import and use the new components instead of hardcoded elements
- [ ] Replace existing vitals labels with VitalSignWidget instances
- [ ] Replace existing waveform plots with WaveformWidget instances
- [ ] Add Spo2RespWidget below ECG

## Step 5: Testing and Verification
- [x] Run the application (`python main.py`) to verify components render correctly
- [x] Test dynamic updates with sample data (e.g., simulate vitals changes, waveform plotting)
- [x] Verify styling matches Mindray look: black theme, colors, fonts, shadows
- [x] Check responsiveness and layout in the UI
- [x] Perform thorough testing: interact with all components, check for errors, verify data accuracy
- [x] Test new Spo2RespWidget with sample data
- [ ] Test new NibpWidget with sample data

## Step 7: Create Temperature Panel Component
- [x] Create `temp_widget.py` file
- [x] Implement TempWidget class as QWidget subclass
- [x] Horizontal layout: 'Temp °C' small white label left; vertically stacked T1 and T2 (labels small white, values large bold white) middle; TD (label small white, value large bold white) right
- [x] Accept data object: { "t1": 37.0, "t2": 37.2, "td": 0.2 }
- [x] Implement styling: black background, sans-serif fonts, white text
- [x] Add update_data method for dynamic updates
- [x] Integrate into monitor_ui.py: replace temp_label with TempWidget, update update_vitals_ui

## Step 8: Revert Temperature to Previous Version
- [x] Update `monitor_ui.py`: Replace TempWidget with QLabel for temp (like "TEMP\n37.0°C")
- [x] Update `data_worker.py`: Change temp in compute_vitals to string "37.0°C"
- [x] Update `main.py`: Change default temp to string "37.0°C"
- [ ] Remove TempWidget import and usage in monitor_ui.py

## Step 6: Finalize and Document
- [ ] Ensure all components are production-ready: error handling, performance, modularity
- [ ] Add docstrings and comments for maintainability
- [ ] Confirm components accept dynamic data via props/state as required
