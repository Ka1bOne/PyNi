PyNi 1.0 - Python Mini IDE
======================
# PyNi uses 87KB of storage!


  Windows/PyNi.exe   - Windows app (double-click)
  Mac/PyNi.app       - macOS app (drag to Applications if you like)
  pyni.py            - the same IDE as a plain script (Windows/Mac/Linux:  python3 pyni.py)

REQUIREMENT: Python 3 must be installed (PyNi uses it to run your code).
  Get it free from https://www.python.org/downloads/
  - Windows: the python.org installer includes everything PyNi needs.
  - Mac: use the python.org installer (Homebrew Python also works if you
    run "brew install python-tk").

FIRST LAUNCH
  Windows: if SmartScreen says "Windows protected your PC", click
           "More info" -> "Run anyway" (the app isn't code-signed).
  Mac:     right-click PyNi.app -> Open -> Open. On macOS 15+, if that
           doesn't offer "Open", go to System Settings -> Privacy & Security
           and click "Open Anyway" (the app isn't signed by Apple).

FEATURES
  - Line numbers, light & dark themes, zoom, word wrap
  - Python syntax highlighting, bracket matching, current-line highlight
  - Tabs for multiple files, open/save/save as, recent files
  - Auto-indent, smart backspace, indent/dedent region, comment/uncomment
  - Find / replace (match case, whole word, regex), go to line
  - Word & module completion (Tab after a name, or Ctrl+Space)
  - Run module (F5) in an interactive Python shell, like IDLE:
    input() works, variables stay available afterwards, coloured errors,
    command history (Up/Down), Ctrl+C to interrupt, restart shell
  - Double-click a traceback line to jump to the error
  - Check syntax (Alt+X), module browser (Alt+C), open module (Alt+M)

KEYS (Cmd instead of Ctrl on Mac)
  Ctrl+N/O/S        New / Open / Save        Ctrl+Shift+S  Save As
  Ctrl+W            Close tab                Ctrl+Tab      Next tab
  Ctrl+Z / Ctrl+Y   Undo / Redo              Ctrl+F / H    Find / Replace
  F3 / Shift+F3     Find next / previous     Ctrl+G        Go to line
  Ctrl+] / Ctrl+[   Indent / Dedent          Ctrl+/        Toggle comment
  Alt+3 / Alt+4     Comment / Uncomment      Ctrl+Space    Completions
  F5                Run module               Alt+X         Check syntax
  Ctrl+F6           Restart shell            Ctrl+T        Dark/light theme
  Ctrl+ + / - / 0   Zoom                     F1            Python docs

Settings are saved in ~/.pyni.json
