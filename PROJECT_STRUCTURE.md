# Project Structure

Complete overview of the ecDNA classification project organization.

```
ecDNA-classification/
│
├── .github/
│   └── workflows/
│       └── python-app.yml          # CI/CD pipeline configuration
│
├── data/                            # Data directory (not in git)
│   ├── README.md                    # Data documentation
│   ├── PCAWG_WGS/                   # PCAWG whole genome sequencing data
│   ├── TCGA_WES/                    # TCGA whole exome sequencing data
│   ├── Merge/                       # Merged datasets
│   └── Final_Data/                  # Processed final datasets
│
├── notebooks/                       # Jupyter notebooks
│   └── README.md                    # Notebooks documentation
│
├── scripts/                         # Utility scripts
│   ├── README.md                    # Scripts documentation
│   └── verify_installation.py      # Installation verification
│
├── src/                             # Source code modules
│   ├── __init__.py                  # Package initialization
│   ├── data_loading.py              # Data loading functions
│   ├── data_processing.py           # Data preprocessing and merging
│   ├── feature_engineering.py       # Feature transformations
│   ├── model_training.py            # Model training and evaluation
│   └── utils.py                     # Utility functions
│
├── tests/                           # Test suite
│   ├── __init__.py                  # Test package initialization
│   ├── README.md                    # Testing documentation
│   └── test_utils.py                # Utility function tests
│
├── .gitignore                       # Git ignore rules
├── DOCUMENTATION.md                 # Technical documentation
├── PROJECT_STRUCTURE.md             # This file
├── README.md                        # Project overview
│
├── config.py                        # Configuration and settings
├── main.py                          # Main execution script
├── requirements.txt                 # Python dependencies
├── setup.py                         # Package setup configuration
```

## Directory Descriptions

### `.github/workflows/`
Contains GitHub Actions workflows for continuous integration and deployment.
- Automated testing on push/PR
- Multi-Python version support
- Code quality checks

### `data/`
**Not tracked in git** - Contains all genomic datasets.
- PCAWG WGS data
- TCGA WES data  
- Merged datasets
- Generated outputs

### `notebooks/`
Jupyter notebooks for interactive analysis and visualization.
- Exploratory data analysis
- Model evaluation
- Result visualization

### `scripts/`
Utility scripts for maintenance and verification.
- Installation checks
- Data validation
- Helper tools

### `src/`
Core source code organized by functionality.

#### `data_loading.py`
- Load PCAWG datasets
- Load TCGA datasets
- Load additional data files
- Handle file I/O

#### `data_processing.py`
- Process PCAWG indices
- Merge datasets
- Filter samples
- Create mappings between ID systems

#### `feature_engineering.py`
- Train/test split preparation
- Count to proportion conversion
- Column categorization
- Feature renaming and reordering

#### `model_training.py`
- Baseline model training
- Neural network implementation
- Hyperparameter tuning
- Model evaluation and metrics

#### `utils.py`
- ID extraction and parsing
- Data transformations
- Column categorization
- Helper functions

### `tests/`
Unit tests and integration tests.
- Test utilities
- Test data processing
- Test feature engineering
- Test models (to be implemented)

## Key Files

### Configuration
- **config.py**: Centralized configuration for paths, hyperparameters, and settings
- **requirements.txt**: All Python package dependencies
- **setup.py**: Package installation configuration

### Documentation
- **README.md**: Project overview and basic usage
- **QUICKSTART.md**: Quick start guide for new users
- **DOCUMENTATION.md**: Detailed technical documentation
- **CONTRIBUTING.md**: Guidelines for contributors
- **CHANGELOG.md**: Version history
- **PROJECT_STRUCTURE.md**: This file

### Metadata
- **LICENSE**: MIT License
- **CITATION.cff**: Citation information in CFF format
- **.gitignore**: Files and directories to exclude from version control

### Execution
- **main.py**: Main pipeline execution script
- **ecDNA Project Code.py**: Original monolithic code (deprecated, kept for reference)

## Code Organization Principles

1. **Modularity**: Each module has a single, well-defined responsibility
2. **Reusability**: Functions are designed to be reusable across different contexts
3. **Testability**: Code structure facilitates unit testing
4. **Documentation**: All modules, classes, and functions have docstrings
5. **Configuration**: All hardcoded values moved to config.py

## Data Flow

```
Data Files (data/)
    ↓
Data Loading (src/data_loading.py)
    ↓
Data Processing (src/data_processing.py)
    ↓
Feature Engineering (src/feature_engineering.py)
    ↓
Model Training (src/model_training.py)
    ↓
Results & Visualizations
```

## Execution Flow

```
main.py
    ├─→ Load PCAWG data
    ├─→ Load TCGA data
    ├─→ Process and merge
    ├─→ Engineer features
    ├─→ Train models
    ├─→ Tune hyperparameters
    ├─→ Evaluate
    └─→ Save best model
```

## Extension Points

To extend the project:

1. **Add new models**: Modify `src/model_training.py`
2. **Add new features**: Modify `src/feature_engineering.py`
3. **Add new data sources**: Modify `src/data_loading.py`
4. **Add new processing steps**: Modify `src/data_processing.py`
5. **Add new utilities**: Modify `src/utils.py`

## Development Workflow

1. Create feature branch
2. Make changes in appropriate modules
3. Add/update tests
4. Update documentation
5. Run tests locally
6. Submit pull request
7. CI/CD runs automatically
8. Code review
9. Merge to main

## Best Practices

- Keep modules under 500 lines
- Functions under 50 lines
- Clear, descriptive names
- Type hints where appropriate
- Comprehensive docstrings
- Unit tests for new functionality

