# NK2DL GUI Component Migration Plan

## Important Note: GUI Module Focus

**This document is specifically for migrating the GUI module to its own repository.** The core module (`nk2dl`) is being handled in a separate repository and migration process. 

**When working on this GUI migration, if you encounter any issues with interfacing between the GUI and core modules, you must:**

1. **Stop the current work**
2. **Assess whether the issue requires changes to the core module or the GUI module**
3. **Make the appropriate changes in the correct repository**
4. **Resume the GUI migration only after the interface issue is resolved**

This ensures that the separation is clean and that both modules maintain proper interfaces.

## Current State Analysis

The nk2dl project currently consists of 2 tightly integrated components:

1. **Core Module (`nk2dl`)**: Core functionality for Nuke script submission to Deadline
2. **GUI Panel (`nk2dl gui`)**: Nuke-integrated GUI panel for submission

### Current Dependencies

```
GUI → Core Module (nk2dl) + Nuke + PySide
Core Module → Deadline API + Nuke API
```

### Key Dependencies Identified

**GUI Dependencies:**
- `nk2dl.common.*` - All common modules
- `nk2dl.nuke.submission` - Core submission logic
- `nk2dl.deadline.connection` - Deadline connectivity
- Nuke API + PySide (Qt)

**Core Module Dependencies:**
- Deadline API
- Nuke API (for script parsing)
- PyYAML (configuration)
- Standard Python libraries

## Nuke Launch Command

For testing and debugging the GUI component during migration, you can launch Nuke with the following command:

```powershell
& 'C:\Program Files\Nuke15.1v1\Nuke15.1.exe'
```

This command will launch Nuke and you can monitor the console output to help with the migration process. The console output will show any import errors, initialization issues, or other problems that need to be addressed during the GUI component separation.

Wait for feedback from the console. Nuke will take some time to launch.

## Detailed File Migration Mapping

### GUI Panel (nk2dl-gui) - This Repository
```bash
# GUI modules - move contents of gui/ to nk2dl_gui/ (combine __init__.py files)
nk2dl/nk2dl/gui/* → nk2dl-gui/src/nk2dl_gui/
nk2dl/nk2dl/setup_gui.py → nk2dl-gui/src/nk2dl_gui/setup_gui.py

# Grizmos - move to src/
nk2dl/nk2dl/grizmos/ → nk2dl-gui/src/grizmos/

# Nuke integration - rename to dot_nuke and move to src/
nk2dl/dot_nuke/ → nk2dl-gui/src/dot_nuke/

# GUI tests
nk2dl/tests/qt/ → nk2dl-gui/tests/
nk2dl/tests/nukescripts/ → nk2dl-gui/tests/nukescripts/
```

**Note**: The core library migration is handled in the separate `nk2dl` repository. This document focuses only on the GUI component extraction.

## Immediate Next Steps

### 1. Setup Repository Structure

**For the GUI repository, create the python folder structure:**

```bash
# Clone the GUI repository locally (development branch)
git clone -b development https://github.com/artandmath/nk2dl-gui.git

# Create src folder structure
mkdir -p nk2dl-gui/src/nk2dl_gui
mkdir -p nk2dl-gui/src/grizmos
mkdir -p nk2dl-gui/src/dot_nuke
mkdir -p nk2dl-gui/tests
```

### 2. Extract GUI Components

**Move GUI modules from current repository:**

```bash
# From current nk2dl repository
# Move contents of gui/ to nk2dl_gui/ (combine __init__.py files)
cp -r nk2dl/gui/* nk2dl-gui/src/nk2dl_gui/
cp nk2dl/setup_gui.py nk2dl-gui/src/nk2dl_gui/

# Move grizmos to src/
cp -r nk2dl/grizmos nk2dl-gui/src/

# Move dot_nuke to src/ (rename from nuke_integration)
cp -r dot_nuke nk2dl-gui/src/

# Move GUI tests
cp -r tests/qt nk2dl-gui/tests/
cp -r tests/nukescripts nk2dl-gui/tests/
```

### 3. Fix Import Statements

**Critical: Update all broken imports in the migrated code:**

```bash
# Find all files with broken imports
find nk2dl-gui/src/nk2dl_gui -name "*.py" -exec grep -l "from nk2dl\.gui\." {} \;
find nk2dl-gui/tests -name "*.py" -exec grep -l "from nk2dl\.gui\." {} \;

# Update imports in source files (relative imports)
sed -i 's/from nk2dl\.gui\./from .\./g' nk2dl-gui/src/nk2dl_gui/**/*.py

# Update imports in test files (absolute imports)
sed -i 's/from nk2dl\.gui\./from nk2dl_gui\./g' nk2dl-gui/tests/**/*.py

# Update menu registration references
sed -i 's/nk2dl\.gui\.menus/nk2dl_gui\.menus/g' nk2dl-gui/src/nk2dl_gui/**/*.py
```

### 4. Update Dependencies

**nk2dl-gui/setup.py:**
```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nk2dl-gui",
    version="0.1.0",
    author="Daniel Harkness",
    author_email="danielharkness@icloud.com",
    description="Nuke to Deadline Submitter - GUI Panel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/artandmath/nk2dl-gui",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "nk2dl>=0.1.0,<0.2.0",
        "PySide2>=5.15.0;python_version<'3.10'",
        "PySide6>=6.0.0;python_version>='3.10'",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.5.1",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.10",
    package_data={
        "nk2dl_gui": [
            "grizmos/*.nk",
            "dot_nuke/*.py",
        ],
    },
)
```

### 4. Update Import Statements

**In nk2dl-gui, update imports throughout GUI modules:**
```python
# Old imports
from ..common.config import config
from ..nuke.submission import submit_nuke_script
from ..deadline.connection import DeadlineConnection

# New imports
from nk2dl.common.config import config
from nk2dl.nuke.submission import submit_nuke_script
from nk2dl.deadline.connection import DeadlineConnection
```

**Important**: If any of these imports fail during testing, you must assess whether the issue is in the core module's API or the GUI module's usage, and make changes in the appropriate repository.

## Proposed Separation Plan

### GUI Panel: `nk2dl-gui`

**Repository**: `nk2dl-gui`
**Purpose**: Nuke-integrated GUI panel
**Dependencies**: nk2dl + Nuke + PySide

**Structure:**
This takes precedence over anything else in this document
```
nk2dl-gui/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   ├── nk2dl_gui/
│   │   ├── __init__.py
│   │   ├── setup_gui.py        # GUI setup and registration
│   │   ├── menus.py            # Nuke menu integration
│   │   ├── panel/
│   │   │   ├── __init__.py
│   │   │   ├── panel.py        # Main panel class
│   │   │   ├── constants.py    # UI constants
│   │   │   ├── config.py       # Panel configuration
│   │   │   ├── models/         # Data models
│   │   │   ├── views/          # UI views
│   │   │   ├── widgets/        # Custom widgets
│   │   │   ├── delegates.py    # Table delegates
│   │   │   ├── controllers/    # Background workers
│   │   │   └── repositories/   # Data repositories
│   │   └── ...                 # Other GUI modules
│   ├── grizmos/                # Nuke gizmos
│   │   ├── Nk2dl_ModifyMetaData.nk
│   │   └── Nk2dl_ModifyMetaDataGui.nk
│   └── dot_nuke/               # Nuke setup files
│       ├── __init__.py
│       ├── init.py             # Nuke init.py content
│       └── menu.py             # Nuke menu.py content
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── qt/                     # Qt-specific tests
│   └── nukescripts/            # Nuke script tests
├── setup.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── CHANGELOG.md
└── LICENSE
```

**Key Features:**
- Nuke panel integration
- Qt-based GUI components (PySide2/PySide6)
- Real-time data updates
- Background processing
- Configuration management
- Nuke gizmo integration
- Deadline plugin files

**Dependencies:**
```
install_requires=[
    "nk2dl>=0.1.0,<0.2.0",
    "PySide2>=5.15.0;python_version<'3.10'",
    "PySide6>=6.0.0;python_version>='3.10'",
]
```

## Future Enhancements (Nice to Have)

The following sections describe advanced features that can be implemented after the core separation is complete:

### CI/CD Pipeline Configuration

**Create .github/workflows/ci.yml for the GUI repository:**

**nk2dl-gui:**
```yaml
name: GUI Panel CI

on:
  push:
    branches: [ development, main ]
  pull_request:
    branches: [ development, main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
        pyside-version: ["PySide6", "PySide2"]
        exclude:
          - python-version: "3.12"
            pyside-version: "PySide2"  # PySide2 doesn't support Python 3.12

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
        pip install ${{ matrix.pyside-version }}
    
    - name: Lint and format checks
      run: |
        flake8 python/nk2dl_gui python/tests
        black --check python/nk2dl_gui python/tests
        isort --check-only python/nk2dl_gui python/tests
    
    - name: Test GUI components (without Nuke)
      run: pytest python/tests --cov=nk2dl_gui --cov-report=xml
      env:
        QT_QPA_PLATFORM: offscreen  # For headless testing

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

### Git Branch Management

**Important**: The GUI repository uses `development` as the primary development branch, not `main`.

**Git workflow:**
```bash
# Clone with development branch
git clone -b development https://github.com/artandmath/nk2dl-gui.git

# Push to development branch
git push origin development

# Create feature branches from development
git checkout -b feature/gui-separation development
```

**Branch strategy:**
- `development` - Primary development branch
- `feature/*` - Feature branches for specific work
- `main` - Release branch (when ready)

### Advanced Version Synchronization Strategy

**Version Compatibility Matrix:**
```
nk2dl       | nk2dl-gui    | Notes
------------|--------------|-------
0.1.x       | 0.1.x        | Initial release
0.2.x       | 0.1.x-0.2.x  | Backward compatible
1.0.x       | 1.0.x        | Major release
```

**Dependency Constraints:**
- GUI package pins core to compatible major version: `nk2dl>=0.1.0,<0.2.0`
- Use `~=0.1.0` for patch-level compatibility
- Update constraints with each major release

## Migration Strategy

### Phase 1: GUI Panel Extraction (Week 1-2) ✅ REPOSITORY CREATED

**Status**: [nk2dl-gui](https://github.com/artandmath/nk2dl-gui) repository created

**Next Steps**:
1. **Extract GUI modules** to nk2dl-gui repository
   - Move `gui/` modules to `src/nk2dl_gui/`
   - Move `setup_gui.py` to GUI package
   - Move `dot_nuke/` to `nuke_integration/`
   - Update imports to use `nk2dl` dependency
   - Create GUI-specific setup and configuration
   - Set up CI/CD pipeline with Qt testing
   - Create comprehensive test suite
   - Publish to PyPI

2. **Update Nuke integration**
   - Ensure Nuke menu integration still works
   - Test panel registration and functionality
   - Verify PySide2/PySide6 compatibility
   - Test with Nuke launch command: `& 'C:\Program Files\Nuke15.1v1\Nuke15.1.exe'`

3. **Interface testing with core module**
   - Test all imports from the core `nk2dl` package
   - Verify that the GUI can properly communicate with the core module
   - If interface issues arise, assess whether changes are needed in core or GUI
   - Make changes in the appropriate repository

### Phase 2: Integration and Testing (Week 3)

1. **Cross-package integration testing**
   - Test GUI with the core module
   - Verify functionality preservation
   - Test version compatibility
   - Performance benchmarking

2. **Documentation updates**
   - Update installation instructions for the GUI package
   - Create GUI-specific documentation
   - Update examples and tutorials
   - Create migration guide for existing users

3. **Release coordination**
   - Coordinate with core module release
   - Update dependency constraints
   - Tag releases in the GUI repository

## Test Distribution Strategy

### GUI Tests
- **Widget tests**: `nk2dl-gui/tests/qt/`
- **Nuke integration tests**: `nk2dl-gui/tests/nukescripts/`
- **PySide compatibility tests**: Both PySide2 and PySide6
- **Panel functionality tests**: GUI → Core interaction

### Cross-Package Integration Tests
- **End-to-end workflow tests**: Complete submission pipeline
- **Version compatibility tests**: Package version combinations
- **Performance regression tests**: Ensure no degradation

## Benefits of Separation

### 1. **Modularity**
- GUI component can be developed independently
- Clear separation of concerns
- Easier to maintain and test
- Better code organization

### 2. **Flexibility**
- Users can install only the GUI if they need it
- Different deployment strategies possible
- Easier to integrate into existing pipelines
- Support for different Python environments

### 3. **Development Efficiency**
- Parallel development possible with core module
- Smaller, focused codebase
- Easier onboarding for new contributors
- Independent release cycles

### 4. **Distribution**
- Independent versioning and releases
- Better dependency management
- PyPI publication for the GUI component
- Easier package management

## Implementation Details

### Version Management
- Use semantic versioning for the GUI component
- Maintain compatibility with core module
- Pin major versions in dependencies
- Coordinate releases when needed

### Documentation Strategy
- GUI component has comprehensive README
- Cross-reference with core module documentation
- Central documentation hub with integration guides
- API documentation for all public interfaces

### Testing Strategy
- Unit tests for the GUI component
- Integration tests with core module
- End-to-end tests for complete workflows
- Automated testing in CI/CD pipelines

### CI/CD Pipeline
- Separate GitHub Actions for the GUI repository
- Integration testing with core module
- Automated dependency updates
- PyPI publication on releases

## Migration Checklist

### GUI Panel (nk2dl-gui) ✅ REPOSITORY CREATED
- [x] Create new repository
- [ ] Extract GUI modules
- [ ] Move Nuke integration files
- [ ] Update to use nk2dl dependency
- [ ] Set up CI/CD pipeline with Qt support
- [ ] Create GUI-specific tests
- [ ] Test GUI integration with core
- [ ] Test Nuke panel functionality
- [ ] Publish to PyPI (test)
- [ ] Publish to PyPI (production)
- [ ] Update documentation

### Integration and Release
- [ ] Cross-package integration testing
- [ ] Version compatibility testing
- [ ] Performance benchmarking
- [ ] Update main documentation
- [ ] Create migration guide
- [ ] Update examples and tutorials
- [ ] Coordinate initial releases (0.1.0)
- [ ] Update package metadata
- [ ] Create release announcements

## Risk Mitigation

### 1. **Breaking Changes**
- Maintain backward compatibility during transition
- Provide clear migration guides
- Use semantic versioning strictly
- Deprecate features before removal

### 2. **Dependency Management**
- Pin dependency versions in setup.py
- Use compatible version ranges with core module
- Regular dependency security updates
- Monitor for dependency conflicts

### 3. **Testing Coverage**
- Comprehensive test suites for the GUI package
- Integration testing with core module
- Automated testing in CI/CD
- Manual testing for critical workflows

### 4. **Documentation and Support**
- Clear installation instructions for the GUI package
- Comprehensive migration guides
- Troubleshooting documentation
- Community support channels

## Timeline

- **Week 1-2**: GUI panel extraction and testing
- **Week 3**: Integration testing and documentation
- **Week 4**: Release coordination and migration support
- **Week 5+**: Ongoing maintenance and improvements

## Success Criteria

1. **Functionality Preservation**: All existing GUI features work as before
2. **Performance**: No performance degradation from separation
3. **Usability**: Installation and usage remain simple or simpler
4. **Maintainability**: Code is easier to maintain and extend
5. **Documentation**: Clear documentation for the GUI component
6. **Testing**: Comprehensive test coverage for the GUI package
7. **CI/CD**: Automated testing and publishing pipelines
8. **Community**: Smooth transition for existing users
