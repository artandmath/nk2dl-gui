# Job Submission Progress Bar Implementation Plan

## Overview
This plan outlines the implementation of a job submission progress bar that appears when users select "Submit selected writes to deadline". The progress bar will provide real-time feedback on submission status, connection health, and job results.

## Requirements Analysis

Based on the provided working code snippet and current codebase analysis:

### UI Requirements
1. **Progress Window**: Modal dialog with progress bar and status sections
2. **Top Section**: Current task status (e.g., "Submitting Write3", "Submitting Write5")
3. **Progress Bar**: Visual progress indicator (0-100%)
4. **Connection Status**: Real-time connection status with color coding:
   - Green: Connection successful
   - Orange: Connection failed, falling back to commandline
   - Red: Connection failed, fallback disabled
5. **Job Results ScrollBox**: Scrollable area showing job submission results with IDs and dependencies

### Color Coding System
- **Green (#4CAF50)**: Success states
- **Orange (#FF9800)**: Warning/fallback states  
- **Red (#F44336)**: Error/failure states
- **Blue (#2196F3)**: Information/processing states
- **Purple (#9C27B0)**: Special operations

## Current Codebase Analysis

### Existing Components
1. **`submit_selected_writes_to_deadline()`** in `src/nk2dl_gui/menus.py` (lines 132-205)
   - Currently handles write node selection and submission
   - Uses `submit_nuke_script()` from nk2dl module
   - Returns job IDs and shows simple success message

2. **Worker Pattern** in `src/nk2dl_gui/panel/controllers/workers.py`
   - Contains `SubmissionWorker` for background submissions
   - Has signal-based communication pattern
   - Already handles progress updates and error reporting

3. **PySide Integration**
   - Supports both PySide2 (Nuke < 16) and PySide6 (Nuke >= 16)
   - Modal dialog pattern established

## Implementation Strategy

### Phase 1: Create Progress Dialog Component
**Location**: `src/nk2dl_gui/panel/widgets/submission_progress_dialog.py`

#### Key Components:
1. **JobSubmissionProgressDialog** class
   - Modal dialog with modern styling
   - Top task status label
   - Progress bar with custom styling
   - Connection status label with color support
   - Scrollable job results area
   - Cancel button functionality

2. **Connection Status Management**
   - Method to update connection status with appropriate colors
   - Support for different connection states:
     - Webservice successful
     - Webservice failed → commandline fallback
     - Webservice failed → no fallback
     - Commandline successful/failed

3. **Job Results Tracking**
   - Scrollable text area for job submission results
   - Auto-scroll to bottom for new entries
   - Format: "Write2 submitted with job ID 38937872738327"
   - Dependencies display: "Dependencies: 38937872738326, 389378727383227"

### Phase 2: Enhanced Submission Worker
**Location**: `src/nk2dl_gui/panel/controllers/submission_progress_worker.py`

#### Enhanced Worker Features:
1. **Extended Signal System**
   - `task_status_update(str)`: Current task being processed
   - `connection_status_update(str, str)`: Status message and color
   - `job_submitted(str, str)`: Write node name and job ID
   - `dependency_info(str, list)`: Job ID and dependency list
   - `progress_percentage(int)`: Overall progress (0-100)

2. **Submission Pipeline Integration**
   - Hook into `submit_nuke_script()` to track individual write node submissions
   - Monitor connection attempts and fallback behavior
   - Extract job IDs and dependency information from results

3. **Progress Calculation**
   - Pre-submission: 0-20% (script validation, node analysis)
   - Per-write submission: 20-90% (distributed across write nodes)
   - Post-submission: 90-100% (result processing, cleanup)

### Phase 3: Integration with Menu System
**Location**: Update `src/nk2dl_gui/menus.py`

#### Changes to `submit_selected_writes_to_deadline()`:
1. **Replace Direct Submission**
   - Remove direct call to `submit_nuke_script()`
   - Instantiate progress dialog
   - Create enhanced submission worker
   - Connect signals to dialog updates

2. **Error Handling Integration**
   - Show errors in progress dialog instead of simple message box
   - Allow user to see full error details in scrollable area
   - Maintain cancel functionality throughout process

### Phase 4: Connection Status Integration
**Location**: Investigation needed in nk2dl core module

#### Connection Monitoring:
1. **Deadline Connection Analysis**
   - Hook into deadline connection logic to detect:
     - Webservice connection attempts
     - Fallback to commandline behavior
     - Connection failure states

2. **Status Reporting Pipeline**
   - Modify connection classes to emit status updates
   - Capture connection state changes
   - Report IP addresses and connection types

## Implementation Details

### File Structure
```
src/nk2dl_gui/panel/widgets/
├── submission_progress_dialog.py      # Main progress dialog
└── __init__.py                        # Updated exports

src/nk2dl_gui/panel/controllers/
├── submission_progress_worker.py      # Enhanced worker
└── workers.py                         # Updated existing workers

src/nk2dl_gui/
└── menus.py                          # Updated menu integration
```

### Dialog Layout Specification
```
┌─────────────────────────────────────────┐
│           Job Submission Progress        │
├─────────────────────────────────────────┤
│         Submitting Write3...            │  ← Task Status
├─────────────────────────────────────────┤
│ ████████████████░░░░░░░░░░ 65%          │  ← Progress Bar
├─────────────────────────────────────────┤
│ Connection to webservice 192.168.1.X    │  ← Connection Status
│ successful ●                            │     (colored indicator)
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ Write2 submitted with job ID        │ │  ← Scrollable Results
│ │ 38937872738327                      │ │
│ │ Write3 submitted with job ID        │ │
│ │ 38937872738328                      │ │
│ │ Dependencies: 38937872738326        │ │
│ │              389378727383227        │ │
│ └─────────────────────────────────────┘ │
├─────────────────────────────────────────┤
│                [Cancel]                 │  ← Cancel Button
└─────────────────────────────────────────┘
```

### Signal Flow Diagram
```
submit_selected_writes_to_deadline()
         │
         ▼
JobSubmissionProgressDialog.show()
         │
         ▼
SubmissionProgressWorker.start()
         │
         ▼
┌────────────────────────────────────┐
│ Worker Signals:                    │
│ • task_status_update              │ ──→ Dialog.set_task_status()
│ • connection_status_update        │ ──→ Dialog.set_connection_status()
│ • job_submitted                   │ ──→ Dialog.add_job_result()
│ • progress_percentage             │ ──→ Dialog.set_progress()
│ • finished                        │ ──→ Dialog.show_completion()
└────────────────────────────────────┘
```

## Implementation Steps

### Step 1: Create Progress Dialog (Priority: High)
- [ ] Create `JobSubmissionProgressDialog` class
- [ ] Implement UI layout with all required sections
- [ ] Add styling to match existing UI patterns
- [ ] Test dialog display and basic functionality

### Step 2: Enhance Worker System (Priority: High)
- [ ] Create `SubmissionProgressWorker` with extended signals
- [ ] Implement progress calculation logic
- [ ] Add connection status monitoring hooks
- [ ] Test worker signal emission

### Step 3: Integration (Priority: Medium)
- [ ] Update `submit_selected_writes_to_deadline()` to use new system
- [ ] Connect worker signals to dialog updates
- [ ] Handle cancellation and error cases
- [ ] Test full integration workflow

### Step 4: Connection Status Integration (Priority: Medium)
- [ ] Investigate nk2dl connection classes
- [ ] Add status monitoring to connection logic
- [ ] Implement IP address and connection type reporting
- [ ] Test various connection scenarios

### Step 5: Testing & Polish (Priority: Low)
- [ ] Test with various write node configurations
- [ ] Test connection failure scenarios
- [ ] Add comprehensive error handling
- [ ] Performance optimization for large submissions
- [ ] UI polish and accessibility improvements

## Technical Considerations

### Threading Safety
- Dialog updates must happen on main thread
- Use Qt's signal/slot mechanism for thread communication
- Ensure proper cleanup of background threads

### Error Handling
- Graceful degradation if progress tracking fails
- Maintain existing functionality as fallback
- Clear error reporting in dialog

### Performance
- Minimize UI update frequency to avoid blocking
- Efficient progress calculation for large write sets
- Background processing for non-critical updates

### Compatibility
- Support both PySide2 and PySide6
- Maintain compatibility with existing nk2dl API
- Ensure dialog works in various Nuke versions

## Success Criteria

1. **Functional Requirements**
   - Progress bar displays during submission
   - Real-time task status updates
   - Connection status with appropriate colors
   - Job results with IDs and dependencies
   - Cancellation functionality

2. **User Experience**
   - Smooth, responsive UI updates
   - Clear visual feedback on submission progress
   - Intuitive color coding for status
   - Helpful error messages

3. **Integration**
   - Seamless replacement of existing simple message
   - No breaking changes to existing API
   - Proper cleanup and resource management

## Future Enhancements

1. **Advanced Features**
   - Submission time estimation
   - Detailed network diagnostics
   - Job dependency visualization
   - Resume interrupted submissions

2. **UI Improvements**
   - Expandable/collapsible sections
   - Export submission logs
   - Customizable status colors
   - Progress animation effects

## Risk Mitigation

### Potential Issues:
1. **nk2dl API Changes**: Core submission API might not support progress hooks
   - **Mitigation**: Implement wrapper layer that can adapt to API changes

2. **Threading Complexity**: Qt threading with Nuke API can be complex
   - **Mitigation**: Use established worker patterns from existing codebase

3. **Performance Impact**: Progress tracking might slow submissions
   - **Mitigation**: Make progress tracking optional via configuration

4. **UI Blocking**: Complex submissions might still block UI
   - **Mitigation**: Ensure all heavy operations run in background threads

## Configuration Options

Add to nk2dl config system:
```yaml
menu:
  progress_dialog:
    enabled: true
    show_connection_details: true
    auto_close_on_success: false
    auto_close_timer_seconds: 3
    detailed_logging: true
    update_frequency_ms: 100
```

This plan provides a comprehensive roadmap for implementing the job submission progress bar while maintaining compatibility with the existing codebase and following established patterns.
