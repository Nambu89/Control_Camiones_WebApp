# Contributing to Truck Control Web App

Thank you for your interest in contributing! This document covers the basics.

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/Nambu89/Control_Camiones_WebApp.git
   cd Control_Camiones_WebApp
   ```
3. **Create a virtual environment** and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Linux/macOS
   venv\Scripts\activate           # Windows
   pip install -r requirements.txt
   ```
4. **Run the app** to verify everything works:
   ```bash
   python app.py
   ```
   The app should be available at `http://localhost:5000`.

## Development Workflow

1. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. **Make your changes**. Keep commits focused and write clear commit messages.
3. **Test your changes** — start the app and verify the affected functionality.
4. **Commit**:
   ```bash
   git commit -am 'Add: brief description of your change'
   ```
5. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request** on GitHub with a clear description of what you changed and why.

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use 4-space indentation.
- Keep functions small and focused.
- Add comments for non-obvious logic.

## Reporting Issues

If you find a bug or have a feature request, please [open an issue](../../issues) with:

- A clear title and description.
- Steps to reproduce (for bugs).
- Expected vs. actual behavior.
- Your environment (OS, Python version, Docker version).

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
