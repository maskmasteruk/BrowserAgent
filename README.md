# BrowserAgent

BrowserAgent is a browser automation and analysis project that uses a Groq API key to power its AI functionality. The application generates logs during execution, which can then be visualized using the included `analyzer.html` file.

## Requirements

Before starting, make sure you have:

* Python **3.14**
* Git
* A valid **Groq API key**

> **Python 3.14 is supported and working with this project.** It is recommended to use Python 3.14 when creating the virtual environment.

---

## 1. Clone the Repository

```bash
git clone https://github.com/maskmasteruk/BrowserAgent.git
cd BrowserAgent
```

---

## 2. Set Up `GROQ_API_KEY`

The application requires the `GROQ_API_KEY` environment variable.

### Windows

Using Command Prompt:

```cmd
set GROQ_API_KEY=your_groq_api_key_here
```

Using PowerShell:

```powershell
$env:GROQ_API_KEY="your_groq_api_key_here"
```

For a permanent Windows environment variable:

```cmd
setx GROQ_API_KEY "your_groq_api_key_here"
```

After using `setx`, open a **new terminal** before running the application.

### Linux / macOS

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

To make it persistent, add the following to your shell configuration file such as `~/.bashrc` or `~/.zshrc`:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Then reload the configuration:

```bash
source ~/.bashrc
```

### Verify the API Key

Windows PowerShell:

```powershell
echo $env:GROQ_API_KEY
```

Linux/macOS:

```bash
echo $GROQ_API_KEY
```

> **Important:** Never commit your Groq API key to GitHub or place it directly inside Python source files.

---

## 3. Create a Python 3.14 Virtual Environment

Make sure Python 3.14 is installed and available on your system.

Check the version:

```bash
python --version
```

You should see:

```text
Python 3.14.x
```

Create a virtual environment:

```bash
python -m venv venv
```

This creates a virtual environment named `venv`.

---

## 4. Activate the Virtual Environment

### Windows — Command Prompt

```cmd
venv\Scripts\activate
```

### Windows — PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(venv)
```

---

## 5. Install Dependencies

With the virtual environment activated, install all required dependencies:

```bash
pip install -r requirements.txt
```

It is recommended to upgrade `pip` first:

```bash
python -m pip install --upgrade pip
```

Then:

```bash
pip install -r requirements.txt
```

---

## 6. Run BrowserAgent

Once the environment and dependencies are ready, start the application:

```bash
python app.py
```

The application will start using the configured `GROQ_API_KEY`.

---

## 7. Logs

BrowserAgent generates execution logs inside the:

```text
logs/
```

directory.

The logs contain information generated during the application's execution and can be used to analyze what happened during browser-agent runs.

A typical project structure is:

```text
BrowserAgent/
│
├── app.py
├── analyzer.html
├── requirements.txt
├── logs/
│   └── ...
│
├── venv/
│   └── ...
│
└── ...
```

> The `venv/` directory is a local Python environment and should generally **not** be committed to Git.

---

## 8. Visualize Logs with `analyzer.html`

The repository includes:

```text
analyzer.html
```

This file is used to **visualize and analyze the logs generated in the `logs/` folder**.

After running the application and generating logs, open `analyzer.html` in a web browser.

### Option 1 — Open Directly

Navigate to the project directory and open:

```text
analyzer.html
```

in your browser.

### Option 2 — Use a Local HTTP Server

For a more reliable way to access the log files, start a local web server from the project directory.

With the virtual environment activated:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/analyzer.html
```

The analyzer can then be used to visualize the generated logs from the `logs/` directory.

---

## Complete Setup

For a fresh installation, the complete workflow is:

### Windows

```cmd
git clone https://github.com/maskmasteruk/BrowserAgent.git
cd BrowserAgent

set GROQ_API_KEY=your_groq_api_key_here

python --version
python -m venv venv
venv\Scripts\activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python app.py
```

### Linux / macOS

```bash
git clone https://github.com/maskmasteruk/BrowserAgent.git
cd BrowserAgent

export GROQ_API_KEY="your_groq_api_key_here"

python --version
python -m venv venv
source venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python app.py
```

After the application generates logs, open:

```text
analyzer.html
```

to visualize the contents of the `logs/` directory.

---

## Troubleshooting

### `GROQ_API_KEY` is not set

If the application reports that the Groq API key is missing, verify that the environment variable is available in the **same terminal session** where you run:

```bash
python app.py
```

Check it with:

**Windows PowerShell:**

```powershell
echo $env:GROQ_API_KEY
```

**Linux/macOS:**

```bash
echo $GROQ_API_KEY
```

---

### Wrong Python version

Check:

```bash
python --version
```

The project is intended to run with:

```text
Python 3.14.x
```

If `python` points to another version, explicitly use your Python 3.14 executable to create the environment.

---

### Dependencies are missing

Make sure the virtual environment is activated and run:

```bash
pip install -r requirements.txt
```

---

### Analyzer cannot access logs

Run a local HTTP server from the BrowserAgent project directory:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/analyzer.html
```

This allows the analyzer to access files within the project directory through the local server.

---

## Security

Never commit API keys or other secrets to the repository.

Do **not** add your actual key to:

```text
app.py
requirements.txt
analyzer.html
```

or any other source file.

Use the `GROQ_API_KEY` environment variable instead.

---

## Quick Start

```bash
# Clone
git clone https://github.com/maskmasteruk/BrowserAgent.git
cd BrowserAgent

# Configure Groq
# Set GROQ_API_KEY in your environment

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python app.py

# Visualize logs
python -m http.server 8000

# Open:
# http://localhost:8000/analyzer.html
```

## Project Workflow

```text
GROQ_API_KEY
     │
     ▼
Python 3.14 Virtual Environment
     │
     ▼
Install requirements.txt
     │
     ▼
Run app.py
     │
     ▼
Generate logs/
     │
     ▼
analyzer.html
     │
     ▼
Visualize & Analyze Logs
```

---

## License

Refer to the repository for the applicable license and usage terms.
