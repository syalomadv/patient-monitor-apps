# TODO: FORCE FINAL VISUAL FIXES

## Phase 1: CO2 Font Size Scaling
- [x] Edit `vital_sign_widget.py`: Add transform: scale(0.5) to CO2 value_label for visual shrinking.

## Phase 2: Row 1 Consolidation
- [x] Edit `bottom_bar_widget.py`: Add CSS overrides to row1_layout (display: flex; gap: 0 !important; etc.) and nibp_trend_widget (position: relative; left: -5px !important;).

## Phase 3: SpO2 Details Adjacency
- [x] Edit `spo2_resp_widget.py`: Adjust spo2_bottom_layout to make PR and PI adjacent to the 98 value using flex.

## Phase 4: Control Buttons Grouping
- [x] Edit `bottom_bar_widget.py`: Ensure buttons_layout has gap: 0 and flush bottom-right (already done, verify).

## Phase 5: ST-Segment Alignment
- [x] Edit `ecg_widget.py`: Adjust st_grid to align baseline with HR baseline.

## Phase 6: Verification
- [x] Run the app and verify all fixes.
