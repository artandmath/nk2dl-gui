# nk2dl-gui

**Nuke to Deadline Submitter - GUI Panel**

Nuke-integrated GUI panel for submitting scripts to Thinkbox Deadline. This package provides a Qt-based graphical interface for the [nk2dl](https://github.com/artandmath/nk2dl) core module.

## Features

- Nuke panel integration
- Qt-based GUI components (PySide2/PySide6)
- Real-time data updates
- Background processing
- Configuration management
- Nuke gizmo integration

## Installation

```bash
pip install nk2dl-gui
```

**Dependencies:**
- [nk2dl](https://github.com/artandmath/nk2dl) core module
- PySide2 (Python < 3.10) or PySide6 (Python >= 3.10)
- Nuke (for panel integration)

## Usage

The GUI panel automatically integrates with Nuke when the package is installed. Access it through the Nuke menu system.

## Development

```bash
# Clone repository
git clone -b development https://github.com/artandmath/nk2dl-gui.git
cd nk2dl-gui

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Structure

```
nk2dl-gui/
├── src/
│   ├── nk2dl_gui/        # Main GUI module
│   ├── grizmos/          # Nuke gizmos
│   └── dot_nuke/         # Nuke setup files
└── tests/                # Test suite
```

## License

MIT License - see [LICENSE](LICENSE) file for details.
