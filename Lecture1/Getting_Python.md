# 1) Getting Python on Windows, macOS, and Linux

**Goal:** Give you reliable, copy‑pasteable ways to install Python and verify it works for this course.

**Two mainstream paths**

- **CPython + (venv / pipx / uv)** → lean & fast, great for pure‑Python work
- **Conda (Miniforge) + mamba** → easiest for bioinformatics tools (samtools, bedtools, etc.)

------

# 2) Decision guide — Which option should I pick?

- **You need bioinformatics CLI tools (samtools, bedtools, bcftools, STAR, etc.)** → **Miniforge (Conda) + mamba**
- **You just need Python + common data libs (NumPy/Pandas/Jupyter)** and prefer simple, standard Python → **CPython + uv** (or venv)
- **Windows & want Linux tooling** → **WSL2 + Miniforge** inside Ubuntu
- **On university HPC** → Ask for **Miniforge** (many clusters recommend it)

------

# 3) Universal post‑install checks (all OS)

Run these in a **new** terminal after installing.

```bash
python --version      # or: python3 --version, or: py --version (Windows)
python -m pip --version
which python          # macOS/Linux
where python          # Windows
```

Create + activate a test virtual environment (standard CPython):

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
python -V
python -m pip install --upgrade pip
```

------

# 4) Windows — Option A (recommended for pure‑Python): WinGet (official)

Open **PowerShell (Admin)** and search available Python IDs, then install one:

```powershell
winget search Python.Python
winget install -e --id Python.Python.3.13    # pick current 3.x
```

Verify:

```powershell
python --version
py --version           # Python Launcher (if installed)
where python
```

> If you see “Python was not found … Microsoft Store”, open **Settings → Apps → Advanced app settings → App execution aliases** and turn **python.exe** and **python3.exe** **OFF**. Then reopen the terminal.

------

# 5) Windows — Option B: python.org installer (GUI)

1. Download the latest **Windows x86‑64** installer from python.org.
2. In the first screen, **check**:
   - **Install launcher for all users** (py.exe)
   - **Add python.exe to PATH** (optional but convenient)
3. Click **Install Now** (or **Customize** to change location).
4. Close/reopen terminal; then verify:

```powershell
python --version
py --version
```

Create a venv (standard):

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

------

# 6) Windows — Option C (best for bioinformatics): Miniforge (Conda) + mamba

**Miniforge** is the lightweight conda installer that ships with **mamba** and uses **conda‑forge** packages by default. Steps:

1. Download **Miniforge3‑Windows‑x86_64.exe**.
2. Install. Open the **Miniforge Prompt** (Start Menu) — this ensures conda/mamba are on PATH.
3. One‑time Bioconda setup (channel priority):

```bash
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

1. Create a course env (example):

```bash
mamba create -n bio101 python=3.13 jupyterlab numpy pandas biopython samtools bedtools -y
conda activate bio101
```

1. Launch JupyterLab:

```bash
jupyter lab
```

------

# 7) Windows — Option D: WSL2 (Linux on Windows) + Miniforge

1. In **PowerShell (Admin)**:

```powershell
wsl --install     # installs Ubuntu by default; restart when prompted
```

1. Open **Ubuntu** (from Start), then inside Linux:

```bash
# install Miniforge
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh
bash Miniforge3-*.sh
# init shell, then apply Bioconda setup
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
mamba create -n bio101 python=3.13 biopython samtools bedtools -y
conda activate bio101
```

------

# 8) macOS — Option A (simple): python.org installer (universal2)

1. Download the latest **macOS installer (universal2)** from python.org.
2. Run the `.pkg`. After install, open a **new Terminal** and verify:

```bash
python3 --version
python3 -m pip --version
which python3
```

Create a venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

> Tip: Avoid using `/usr/bin/python3` (Apple’s system Python) for development.

------

# 9) macOS — Option B: Homebrew

Install or update Homebrew, then:

```bash
brew install python        # latest 3.x
# or a specific version
brew install python@3.13
# show caveats/paths
brew info python@3.13
python3 --version
```

> If `python3` still points to the system Python, ensure Homebrew’s bin is first in PATH (Apple Silicon: `/opt/homebrew/bin`).

------

# 10) macOS — Option C (best for bioinformatics): Miniforge (Conda) + mamba

1. Download **Miniforge3‑MacOSX‑arm64.pkg** (Apple Silicon) or **…‑x86_64.pkg** (Intel).
2. After install, open a **new Terminal** and set up channels once:

```bash
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

1. Create env:

```bash
mamba create -n bio101 python=3.13 jupyterlab numpy pandas biopython samtools bedtools -y
conda activate bio101
```

------

# 11) Linux — Option A: System package manager (quickest)

Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
```

Fedora/RHEL:

```bash
sudo dnf install -y python3 python3-pip python3-virtualenv
```

Arch/Manjaro:

```bash
sudo pacman -S python python-pip
```

> On newer distros, `pip` may be blocked globally (PEP 668). Use **venv**, **pipx**, or Conda.

------

# 12) Linux — Option B (recommended for bioinformatics): Miniforge + mamba

```bash
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh
bash Miniforge3-*.sh
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
mamba create -n bio101 python=3.13 biopython samtools bedtools -y
conda activate bio101
```

------

# 13) Linux — Option C: pyenv (install multiple CPython versions side‑by‑side)

```bash
# prerequisites vary by distro; then
curl https://pyenv.run | bash
# add init lines to shell per installer output, then restart shell
pyenv install -l        # list versions
pyenv install 3.13.7
pyenv global 3.13.7
python -V
```

Create a venv as usual with `python -m venv .venv`.

------

# 14) Cross‑platform — uv (fast Python + package/env manager)

Install:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows PowerShell
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Use:

```bash
uv python install 3.13
uv venv               # creates .venv with your chosen Python
source .venv/bin/activate    # macOS/Linux
.\.venv\Scripts\Activate.ps1 # Windows
uv pip install numpy pandas jupyterlab
```

------

# 15) pipx (install standalone CLI apps safely)

```bash
# macOS/Linux
python3 -m pip install --user pipx
python3 -m pipx ensurepath
# Windows (PowerShell)
python -m pip install --user pipx
pipx ensurepath
# Examples
pipx install black ruff cookiecutter
```

------

# 16) Jupyter — quick starts

**Standard venv (CPython):**

```bash
python -m venv .venv
source .venv/bin/activate    # or .\.venv\Scripts\Activate.ps1
python -m pip install jupyterlab ipykernel
python -m ipykernel install --user --name=py-venv --display-name "Python (venv)"
jupyter lab
```

**Conda/Miniforge:**

```bash
mamba create -n bio101 python=3.13 jupyterlab -y
conda activate bio101
jupyter lab
```

------

# 17) Troubleshooting (common issues)

- **Windows shows** “Python was not found … Microsoft Store” → Disable **App execution aliases** for `python.exe` and `python3.exe`. Reopen terminal.
- ``** blocked (externally managed environment)** on Linux/macOS → use a **venv**, **pipx**, or **Conda**; avoid `--break-system-packages` unless you know what you’re doing.
- `** vs **`** confusion** → try `python3 --version`; on Windows, use `py --list` to see installed versions.
- **PATH problems** → open a new terminal; confirm with `which python` (macOS/Linux) or `where python` (Windows).

------

# 18) Recommended baseline for this course

- **Windows:** Miniforge **or** WinGet CPython + uv. If you need Unix CLI tools, prefer **WSL2 + Miniforge**.
- **macOS (Apple Silicon):** Miniforge (arm64) **or** Homebrew CPython + uv.
- **Linux:** Miniforge + mamba; otherwise system Python + venv works.

Create one clean environment per project to keep dependencies reproducible.

------

# 19) One‑pager: copy‑paste for Miniforge + Bioconda

```bash
# After installing Miniforge
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
mamba create -n bio101 python=3.13 biopython samtools bedtools -y
conda activate bio101
python -V
```

------

# 20) Verification checklist (students)

- I can run `python --version` (or `python3 --version`).
- I can create & activate a **venv** or **conda env**.
- `python -m pip --version` runs without errors inside my env.
- I can launch **JupyterLab** in my env.
- (Bio track) I can run `samtools --version` after installing via mamba.

------

# 21) Appendix — Useful commands

```bash
# Show all Pythons on Windows
py --list

# Check where Python comes from
which python     # macOS/Linux
where python     # Windows

# Remove a conda env
conda deactivate
conda env remove -n bio101

# Export a conda env for sharing
conda env export -n bio101 > environment.yml

# Create env from file
mamba env create -f environment.yml
```