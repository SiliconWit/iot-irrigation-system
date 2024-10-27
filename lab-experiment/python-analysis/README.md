# Irrigation System Project Setup Guide

This guide will help you set up a Python virtual environment and Jupyter notebook for the irrigation system project in Ubuntu using VS Code.

## Prerequisites

- Ubuntu operating system
- Python 3.x installed
- VS Code installed
- Basic familiarity with terminal commands

## 1. VS Code Extensions

First, install these essential VS Code extensions:

- Python
- Jupyter
- Jupyter Keymap
- Jupyter Notebook Renderers

You can install them either:
- Through VS Code's Extensions sidebar (`Ctrl + Shift + X`)
- Or via terminal:
```bash
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
```

## 2. Project Setup

### 2.1 Create Project Directory

Open terminal in VS Code (`Ctrl + ~`) and run:

```bash
# Create and navigate to project directory
mkdir python-analysis
cd python-analysis
```

### 2.2 Create and Activate Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Your terminal prompt should now show (venv) at the beginning
```

### 2.3 Install Required Packages

```bash
# Install necessary packages
pip install jupyter numpy pandas ipywidgets matplotlib seaborn

# Create a kernel for Jupyter
pip install ipykernel
python -m ipykernel install --user --name=python-analysis

# Save package requirements
pip freeze > requirements.txt
```

## 3. Working with Jupyter Notebooks

### 3.1 Create a New Notebook

Method 1 - VS Code Command Palette:
1. Press `Ctrl + Shift + P`
2. Type "Create New Jupyter Notebook"
3. Select "Python Notebook"

Method 2 - File Explorer:
1. Click New File button
2. Give it a `.ipynb` extension (e.g., `dynamic_irrigation_management.ipynb`)

### 3.2 Select Kernel

1. Click "Select Kernel" in the top right of the notebook
2. Choose the `python-analysis` kernel

### 3.3 Alternative: Running Jupyter in Terminal

```bash
# While in your activated venv
jupyter notebook
```

## 4. Useful Shortcuts

### VS Code Jupyter Shortcuts
- `Shift + Enter`: Run cell and move to next
- `Ctrl + Enter`: Run cell and stay
- `Alt + Enter`: Run cell and insert below
- `Ctrl + ~`: Open/close terminal
- `Ctrl + Shift + P`: Command palette

## 5. Daily Workflow

### 5.1 Starting Work

```bash
# Navigate to project directory
cd python-analysis

# Activate virtual environment
source venv/bin/activate
```

### 5.2 Finishing Work

```bash
# Deactivate virtual environment
deactivate
```

## 6. Troubleshooting

### 6.1 Kernel Issues
If Jupyter kernel isn't showing:
1. Ensure venv is activated
2. Reinstall kernel:
```bash
python -m ipykernel install --user --name=python-analysis
```

### 6.2 Package Issues
If missing packages:
```bash
# Make sure venv is activated, then
pip install -r requirements.txt
```

## 7. Project Structure

Recommended project structure:
```
python-analysis/
├── venv/
├── notebooks/
│   ├── dynamic_irrigation_management.ipynb
│   └── experiments.ipynb
├── src/
│   └── dynamic_irrigation_management.py
├── data/
├── requirements.txt
└── README.md
```

## 8. For New Team Members

To set up an existing project:
```bash
# Clone or download project
cd python-analysis

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install Jupyter kernel
pip install ipykernel
python -m ipykernel install --user --name=python-analysis
```

## 9. Maintenance

Remember to:
- Update `requirements.txt` when adding new packages:
```bash
pip freeze > requirements.txt
```
- Keep your virtual environment activated while working
- Commit your notebook outputs selectively
- Clear notebook outputs before committing if they contain sensitive information

## Need Help?

- Check the official [VS Code Jupyter documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- Refer to the [Python virtual environments guide](https://docs.python.org/3/tutorial/venv.html)
- Contact the project maintainer