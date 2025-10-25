# Scripts

Utility scripts for the ecDNA classification project.

## Available Scripts

### verify_installation.py
Verifies that all required dependencies are properly installed.

**Usage:**
```bash
python scripts/verify_installation.py
```

**Output:**
- ✓ for successfully installed packages with version numbers
- ✗ for missing packages

## Adding New Scripts

When adding utility scripts:
1. Add to this directory
2. Include a docstring explaining the purpose
3. Make executable if needed: `chmod +x script_name.py`
4. Add shebang for direct execution: `#!/usr/bin/env python`
5. Update this README

