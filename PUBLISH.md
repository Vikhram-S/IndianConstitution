# Publishing to PyPI - Step by Step Guide

## Prerequisites

```bash
pip install setuptools wheel twine
```

## Step 1: Build Distribution Packages

```bash
python setup.py sdist bdist_wheel
```

This creates:
- `dist/IndianConstitution-0.8.tar.gz` (source distribution)
- `dist/IndianConstitution-0.8-py3-none-any.whl` (wheel)

## Step 2: Check the Build

```bash
# Check the distribution files
twine check dist/*
```

## Step 3: Test Upload to TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI first
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Test install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ IndianConstitution
```

## Step 4: Upload to PyPI

```bash
# Upload to real PyPI
twine upload dist/*
```

You'll be prompted for your PyPI credentials. If you have 2FA enabled, use an API token instead of password.

### Using API Token (Recommended)

1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Use `__token__` as username and the token as password

## Step 5: Verify Installation

```bash
pip install indianconstitution
python -c "from indianconstitution import IndianConstitution; print('Success!')"
```

## Updating Version

1. Update version in:
   - `setup.py` (version='0.8')
   - `indianconstitution/__init__.py` (__version__ = '0.8')
   - `README.md` (if mentioned)
   - `conda/recipe/meta.yaml` (if using conda)

2. Rebuild and upload:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Clean Up

After publishing, you can remove build artifacts:

```bash
rm -rf build/ dist/ *.egg-info
```

Or on Windows:
```bash
rmdir /s /q build dist *.egg-info
```

---

## Quick Command Summary

```bash
# Full workflow
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
```

---

## Troubleshooting

- **"File already exists"**: Version already published. Bump version number.
- **"Invalid credentials"**: Check username/password or API token.
- **"Package name conflict"**: Package name already taken on PyPI.
