#!/usr/bin/env python3
"""PyNi (Python Mini) - a tiny IDLE-style Python IDE. Standard library only."""
import os, sys, re, json, queue, threading, subprocess, signal, keyword, builtins, codecs, bisect, webbrowser
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font as tkfont

APP, VER = "PyNi", "1.0"
MAC, WIN = sys.platform == "darwin", os.name == "nt"
MOD, MODL = ("Command", "Cmd") if MAC else ("Control", "Ctrl")
CFG_PATH = os.path.join(os.path.expanduser("~"), ".pyni.json")
FTYPES = [("Python files", "*.py *.pyw *.pyi"), ("Text files", "*.txt"), ("All files", "*.*")]
ICON = "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"  # filled in by build script (base64 PNG)

THEMES = {
    "light": dict(bg="#ffffff", fg="#000000", ui="#f0f0f0", ui2="#dadada", border="#c4c4c4", sel="#b5d5ff",
                  curline="#f2f6fc", gut="#f5f5f5", gutfg="#a0a0a0", gutcur="#303030", caret="#000000",
                  match="#b9f0b9", hit="#ffe27a", keyword="#ff7700", builtin="#900090", string="#00aa00",
                  comment="#dd0000", defname="#0000ff", number="#0b7a8a", decorator="#aa22ff",
                  out="#0000c0", err="#cc0000", prompt="#770000", stdin="#000000", info="#808080"),
    "dark": dict(bg="#1e1f22", fg="#d4d4d4", ui="#2b2d30", ui2="#3a3d41", border="#111214", sel="#264f78",
                 curline="#26282d", gut="#1e1f22", gutfg="#5c6067", gutcur="#c8c8c8", caret="#ffffff",
                 match="#3d5c3d", hit="#6b5a1a", keyword="#cc7832", builtin="#8888e6", string="#6a9955",
                 comment="#808080", defname="#ffc66d", number="#6897bb", decorator="#bbb529",
                 out="#6cb6ff", err="#ff6b68", prompt="#cc7832", stdin="#d4d4d4", info="#7f848e"),
}
TAGS = ("defname", "number", "builtin", "keyword", "decorator", "string", "comment")
SHTAGS = ("out", "err", "prompt", "stdin", "info")
KW = keyword.kwlist + ["match", "case"]
BI = sorted(n for n in dir(builtins) if not n.startswith("_") and n not in KW)
_q3 = r"'''[\s\S]*?(?:'''|\Z)" + "|" + r'"""[\s\S]*?(?:"""|\Z)'
_q1 = r"'(?:\\.|[^'\\\n])*'?" + "|" + r'"(?:\\.|[^"\\\n])*"?'
PAT = re.compile("|".join([
    r"(?P<string>(?<!\w)[rRbBuUfF]{0,2}(?:%s|%s))" % (_q3, _q1),
    r"(?P<comment>#[^\n]*)",
    r"(?P<decorator>^[ \t]*@[\w.]+)",
    r"(?P<keyword>\b(?:%s)\b)" % "|".join(KW),
    r"(?P<builtin>(?<!\.)\b(?:%s)\b)" % "|".join(BI),
    r"(?P<number>\b(?:0[xXoObB][\da-fA-F_]+|\d[\d_]*(?:\.\d*)?(?:[eE][+-]?\d+)?[jJ]?))",
]), re.M)
DEFRE = re.compile(r"\b(?:def|class)[ \t]+(\w+)")
TBRE = re.compile(r'File "(.+?)", line (\d+)')

# Runs inside the shell's child Python: a REPL whose stderr and prompts are
# tagged on stdout, so the IDE keeps output in order and can color it.
BOOT = r'''
import sys, os, code, traceback, threading, queue, _thread
O = sys.stdout
class Err:
    encoding, errors = "utf-8", "replace"
    def write(s, x): O.write("\x02" + x + "\x03"); O.flush(); return len(x)
    def flush(s): O.flush()
    def isatty(s): return False
sys.stderr = Err()
Q = queue.Queue()
def rd():
    for ln in iter(sys.__stdin__.readline, ""):
        if ln == "\x03\n": _thread.interrupt_main()
        else: Q.put(ln)
    Q.put("")
threading.Thread(target=rd, daemon=True).start()
class In:
    encoding, errors = "utf-8", "replace"
    def readline(s, n=-1):
        while True:
            try: return Q.get(timeout=0.1)
            except queue.Empty: pass
    read = readline
    def readlines(s): return list(iter(s.readline, ""))
    def __iter__(s): return iter(s.readline, "")
    def isatty(s): return False
sys.stdin = In()
class Con(code.InteractiveConsole):
    def raw_input(s, p=""):
        O.write("\x05" + p + "\x06"); O.flush()
        ln = sys.stdin.readline()
        if not ln: raise EOFError
        return ln.rstrip("\n")
ns = {"__name__": "__main__", "__builtins__": __builtins__}
if len(sys.argv) > 1:
    p = sys.argv[1]; sys.argv = sys.argv[1:]; sys.path[0] = os.path.dirname(p); ns["__file__"] = p
    try:
        with open(p, "rb") as f: src = f.read()
        exec(compile(src, p, "exec"), ns)
    except SystemExit as e:
        if e.code not in (None, 0): print("SystemExit:", e.code, file=sys.stderr)
    except BaseException as e:
        traceback.print_exception(type(e), e, e.__traceback__.tb_next)
else:
    sys.path[0] = ""
sys.ps1, sys.ps2 = ">>> ", "... "
Con(ns).interact(banner="", exitmsg="")
'''


def pyexe():
    e = sys.executable or "python3"
    if WIN and os.path.basename(e).lower() == "pythonw.exe":
        c = os.path.join(os.path.dirname(e), "python.exe")
        if os.path.exists(c):
            return c
    return e


def ix(starts, off):
    ln = bisect.bisect_right(starts, off)
    return "%d.%d" % (ln, off - starts[ln - 1])


class Completer:
    """Popup list of completions for a Text widget (Tab / Ctrl+Space)."""

    def __init__(s, app, text, words):
        s.app, s.t, s.words, s.win, s.cands = app, text, words, None, []
        tag = "Comp%d" % id(s)
        text.bindtags((tag,) + text.bindtags())
        for k in ("<Up>", "<Down>", "<Prior>", "<Next>", "<Return>", "<KP_Enter>", "<Tab>", "<Escape>"):
            text.bind_class(tag, k, s.key)
        text.bind_class(tag, "<KeyRelease>", s.refilter)
        text.bind_class(tag, "<Button-1>", lambda e: s.close())
        text.bind_class(tag, "<FocusOut>", lambda e: text.after(150, s.close))

    def key(s, e):
        if not s.win:
            return None
        k = e.keysym
        if k == "Escape":
            s.close()
        elif k in ("Return", "KP_Enter", "Tab"):
            s.accept()
        else:
            n = s.lb.size()
            cur = (s.lb.curselection() or (0,))[0]
            i = max(0, min(n - 1, cur + {"Up": -1, "Down": 1, "Prior": -8, "Next": 8}[k]))
            s.lb.selection_clear(0, "end"); s.lb.selection_set(i); s.lb.see(i)
        return "break"

    def show(s):
        t = s.t
        s.close()
        pre = re.search(r"[\w.]*$", t.get("insert linestart", "insert")).group()
        obj, dot, part = pre.rpartition(".")
        s.cands = sorted(set(s.app.attrs(obj) if dot else s.words()), key=str.lower)
        m = [w for w in s.cands if w.startswith(part) and w != part]
        if not m:
            t.bell(); return
        cp = os.path.commonprefix(m)
        if len(cp) > len(part):
            t.insert("insert", cp[len(part):]); part = cp
            if len(m) == 1:
                return
        s.start = t.index("insert-%dc" % len(part))
        th = s.app.th
        s.win = w = tk.Toplevel(t)
        w.wm_overrideredirect(True)
        try:
            w.attributes("-topmost", True)
        except tk.TclError:
            pass
        s.lb = tk.Listbox(w, font=s.app.font, activestyle="none", exportselection=False, takefocus=0, bd=1,
                          relief="solid", highlightthickness=0, bg=th["bg"], fg=th["fg"],
                          selectbackground=th["sel"], selectforeground=th["fg"],
                          width=max(14, min(40, max(map(len, m)) + 2)))
        s.lb.pack(fill="both", expand=True)
        s.lb.bind("<ButtonRelease-1>", lambda e: s.accept())
        s.fill(m)
        bb = t.bbox(s.start) or t.bbox("insert") or (0, 0, 0, 16)
        w.geometry("+%d+%d" % (t.winfo_rootx() + bb[0], t.winfo_rooty() + bb[1] + bb[3] + 2))

    def fill(s, m):
        s.lb.delete(0, "end")
        for w in m:
            s.lb.insert("end", w)
        s.lb.config(height=min(10, len(m)))
        s.lb.selection_set(0)

    def refilter(s, e=None):
        if not s.win or (e and e.keysym in ("Up", "Down", "Prior", "Next", "Return", "KP_Enter", "Tab", "Escape")):
            return
        t = s.t
        if t.compare("insert", "<", s.start):
            return s.close()
        part = t.get(s.start, "insert")
        m = [w for w in s.cands if w.startswith(part)] if re.fullmatch(r"\w*", part) else []
        if not m:
            return s.close()
        s.fill(m)

    def accept(s):
        sel = s.lb.curselection()
        w = s.lb.get(sel[0]) if sel else None
        s.close()
        if w:
            s.t.delete(s.start, "insert"); s.t.insert("insert", w)

    def close(s):
        if s.win:
            s.win.destroy(); s.win = None


class Editor(ttk.Frame):
    count = 0

    def __init__(s, app, path=None):
        super().__init__(app.nb)
        s.app, s.path, s.dirty, s.nl, s.enc, s._hl = app, path, False, "\n", "utf-8", None
        Editor.count += 1
        s.num = Editor.count
        s.gut = tk.Canvas(s, width=40, highlightthickness=0, bd=0)
        s.text = t = tk.Text(s, wrap="word" if app.cfg["wrap"] else "none", undo=True, maxundo=-1,
                             font=app.font, bd=0, highlightthickness=0, padx=6, pady=4, insertwidth=2,
                             tabs=(app.font.measure("    "),))
        vs = ttk.Scrollbar(s, command=t.yview)
        s.hs = ttk.Scrollbar(s, orient="horizontal", command=t.xview)
        t.config(yscrollcommand=lambda a, b: (vs.set(a, b), s.lines()), xscrollcommand=s.hs.set)
        s.gut.grid(row=0, column=0, sticky="ns"); t.grid(row=0, column=1, sticky="nsew")
        vs.grid(row=0, column=2, sticky="ns"); s.hs.grid(row=1, column=1, sticky="ew")
        s.rowconfigure(0, weight=1); s.columnconfigure(1, weight=1)
        if app.cfg["wrap"]:
            s.hs.grid_remove()
        if not app.cfg["lines"]:
            s.gut.grid_remove()
        for tg in ("curline",) + TAGS + ("match", "hit"):
            t.tag_configure(tg)
        t.tag_raise("sel")
        app.common_keys(t)
        s.comp = Completer(app, t, s.words)
        t.bind("<<Modified>>", s.modified)
        t.bind("<Return>", s.ret); t.bind("<KP_Enter>", s.ret)
        t.bind("<Tab>", s.tab); t.bind("<Shift-Tab>", s.untab)
        try:
            t.bind("<ISO_Left_Tab>", s.untab)
        except tk.TclError:
            pass
        t.bind("<BackSpace>", s.bksp)
        t.bind("<Configure>", lambda e: s.lines())
        t.bind("<KeyRelease>", s.moved, add="+"); t.bind("<ButtonRelease-1>", s.moved, add="+")
        t.bind("<Button-2>" if MAC else "<Button-3>", s.popup)
        if path:
            s.load(path)
        t.edit_reset(); t.edit_modified(False)
        t.mark_set("insert", "1.0")
        app.theme_text(t); s.gut.config(bg=app.th["gut"])
        s.highlight(); s.moved()

    # ---- file ----
    def name(s):
        return os.path.basename(s.path) if s.path else "untitled-%d" % s.num

    def is_py(s):
        return not s.path or os.path.splitext(s.path)[1].lower() in (".py", ".pyw", ".pyi")

    def load(s, path):
        with open(path, "rb") as f:
            data = f.read()
        try:
            txt = data.decode("utf-8")
            if txt.startswith("﻿"):
                txt, s.enc = txt[1:], "utf-8-sig"
        except UnicodeDecodeError:
            txt, s.enc = data.decode("latin-1"), "latin-1"
        s.nl = "\r\n" if "\r\n" in txt else "\n"
        s.text.insert("1.0", txt.replace("\r\n", "\n").replace("\r", "\n"))

    def save(s, as_=False, copy=False):
        p = s.path
        if as_ or copy or not p:
            p = filedialog.asksaveasfilename(parent=s.app.root, defaultextension=".py", filetypes=FTYPES,
                                             initialfile=s.name() if s.path else "untitled.py",
                                             initialdir=os.path.dirname(s.path) if s.path else None)
            if not p:
                return False
        txt = s.text.get("1.0", "end-1c")
        if txt and not txt.endswith("\n"):
            txt += "\n"
        try:
            try:
                with open(p, "w", encoding=s.enc, newline=s.nl) as f:
                    f.write(txt)
            except UnicodeEncodeError:
                s.enc = "utf-8"
                with open(p, "w", encoding=s.enc, newline=s.nl) as f:
                    f.write(txt)
        except OSError as e:
            messagebox.showerror("Save failed", str(e), parent=s.app.root)
            return False
        if not copy:
            s.path, s.dirty = os.path.abspath(p), False
            s.app.retitle(s); s.highlight()
        s.app.add_recent(p); s.app.status("Saved " + p)
        return True

    # ---- change tracking / drawing ----
    def modified(s, e=None):
        if not s.text.edit_modified():
            return
        s.text.edit_modified(False)
        if not s.dirty:
            s.dirty = True; s.app.retitle(s)
        if s._hl:
            s.after_cancel(s._hl)
        s._hl = s.after(120, s.highlight)
        s.lines()

    def moved(s, e=None):
        t = s.text
        ln, col = t.index("insert").split(".")
        s.app.pos.config(text="Ln %s, Col %s" % (ln, col))
        t.tag_remove("curline", "1.0", "end"); t.tag_add("curline", "insert linestart", "insert lineend+1c")
        s.match(); s.lines()

    def lines(s):
        c = s.gut
        c.delete("all")
        if not s.app.cfg["lines"]:
            return
        t, th, f = s.text, s.app.th, s.app.font
        last = int(t.index("end-1c").split(".")[0])
        w = f.measure("9" * max(3, len(str(last)))) + 16
        if int(c["width"]) != w:
            c.config(width=w)
        cur = t.index("insert").split(".")[0]
        i = t.index("@0,0")
        while True:
            d = t.dlineinfo(i)
            if d is None:
                break
            n = i.split(".")[0]
            c.create_text(w - 8, d[1], anchor="ne", text=n, font=f, fill=th["gutcur"] if n == cur else th["gutfg"])
            if int(n) >= last:
                break
            i = t.index("%s+1line" % i)

    def highlight(s):
        s._hl = None
        t = s.text
        for tg in TAGS:
            t.tag_remove(tg, "1.0", "end")
        src = t.get("1.0", "end-1c")
        if not s.is_py() or len(src) > 600000:
            return
        starts = [0] + [m.end() for m in re.finditer("\n", src)]
        acc = {tg: [] for tg in TAGS}
        for m in PAT.finditer(src):
            a, b = m.span()
            acc[m.lastgroup] += (ix(starts, a), ix(starts, b))
        for m in DEFRE.finditer(src):
            a, b = m.span(1)
            acc["defname"] += (ix(starts, a), ix(starts, b))
        for tg, v in acc.items():
            if v:
                t.tag_add(tg, *v)

    def match(s):
        t = s.text
        t.tag_remove("match", "1.0", "end")
        cl = {")": "(", "]": "[", "}": "{"}
        op = {v: k for k, v in cl.items()}
        c = t.get("insert-1c")
        if c in cl and t.compare("insert", ">", "1.0"):
            src = t.get("insert-20001c", "insert-1c")
            d = 0
            for k in range(len(src) - 1, -1, -1):
                if src[k] == c: d += 1
                elif src[k] == cl[c]:
                    if d == 0:
                        a = "insert-%dc" % (len(src) - k + 1)
                        t.tag_add("match", a, a + "+1c", "insert-1c", "insert"); return
                    d -= 1
            return
        c = t.get("insert")
        if c in op:
            src = t.get("insert+1c", "insert+20000c")
            d = 0
            for k, ch in enumerate(src):
                if ch == c: d += 1
                elif ch == op[c]:
                    if d == 0:
                        t.tag_add("match", "insert", "insert+1c", "insert+%dc" % (k + 1)); return
                    d -= 1

    def words(s):
        return KW + BI + re.findall(r"[A-Za-z_]\w{2,}", s.text.get("1.0", "end"))

    # ---- editing keys ----
    def ret(s, e=None):
        t = s.text
        if t.tag_ranges("sel"):
            t.delete("sel.first", "sel.last")
        line = t.get("insert linestart", "insert")
        ind = re.match(r"[ \t]*", line).group()
        code = re.sub(r"#[^'\"]*$", "", line).rstrip()
        stack = []
        for i, ch in enumerate(code):
            if ch in "([{": stack.append(i)
            elif ch in ")]}" and stack: stack.pop()
        if code.endswith(":"):
            ind += "    "
        elif stack:
            ind = " " * (stack[-1] + 1) if stack[-1] + 1 < len(code) else ind + "    "
        elif re.match(r"\s*(return|pass|break|continue|raise)\b", code):
            ind = ind[:-4] if ind.endswith("    ") else ind[:-1]
        t.insert("insert", "\n" + ind)
        t.see("insert"); s.moved()
        return "break"

    def tab(s, e=None):
        t = s.text
        if t.tag_ranges("sel") and "\n" in t.get("sel.first", "sel.last"):
            s.app.indent(); return "break"
        before = t.get("insert linestart", "insert")
        if before and re.search(r"[\w.]$", before):
            s.comp.show(); return "break"
        t.insert("insert", " " * (4 - len(before.expandtabs(4)) % 4))
        return "break"

    def untab(s, e=None):
        s.app.dedent(); return "break"

    def bksp(s, e=None):
        t = s.text
        if t.tag_ranges("sel"):
            return None
        before = t.get("insert linestart", "insert")
        if before and not before.strip(" "):
            t.delete("insert-%dc" % ((len(before) - 1) % 4 + 1), "insert")
            return "break"

    def region(s, fn):
        t = s.text
        if t.tag_ranges("sel"):
            a = int(t.index("sel.first").split(".")[0])
            end = t.index("sel.last"); b = int(end.split(".")[0])
            if end.endswith(".0") and b > a:
                b -= 1
        else:
            a = b = int(t.index("insert").split(".")[0])
        lines = [t.get("%d.0" % i, "%d.end" % i) for i in range(a, b + 1)]
        new = fn(lines)
        t.edit_separator()
        for i, (o, n) in enumerate(zip(lines, new)):
            if o != n:
                t.delete("%d.0" % (a + i), "%d.end" % (a + i)); t.insert("%d.0" % (a + i), n)
        t.edit_separator()
        if a != b:
            t.tag_remove("sel", "1.0", "end"); t.tag_add("sel", "%d.0" % a, "%d.0" % (b + 1))
        s.moved()

    def popup(s, e):
        m = tk.Menu(s, tearoff=0)
        for lbl, f in (("Cut", lambda: s.text.event_generate("<<Cut>>")),
                       ("Copy", lambda: s.text.event_generate("<<Copy>>")),
                       ("Paste", lambda: s.text.event_generate("<<Paste>>")), None,
                       ("Toggle Comment", s.app.toggle_comment), ("Show Completions", s.app.complete), None,
                       ("Run Module", s.app.run)):
            if lbl is None:
                m.add_separator()
            else:
                m.add_command(label=lbl, command=f)
        m.tk_popup(e.x_root, e.y_root)


class Shell(ttk.Frame):
    def __init__(s, app, parent):
        super().__init__(parent)
        s.app, s.proc, s.q, s.hist, s.hi, s.mode, s.ind, s.pbuf = app, None, queue.Queue(), [], 0, "out", 0, ""
        bar = ttk.Frame(s)
        bar.pack(side="top", fill="x")
        ttk.Label(bar, text=" Python Shell").pack(side="left")
        for lbl, f in (("Clear", s.clear), ("Restart", s.restart), ("Stop", s.interrupt)):
            ttk.Button(bar, text=lbl, command=f, takefocus=0, style="Bar.TButton", width=8).pack(side="right", padx=1, pady=1)
        s.text = t = tk.Text(s, wrap="char", font=app.font, bd=0, highlightthickness=0, padx=6, pady=4,
                             undo=False, insertwidth=2, tabs=(app.font.measure("    "),))
        vs = ttk.Scrollbar(s, command=t.yview)
        t.config(yscrollcommand=vs.set)
        vs.pack(side="right", fill="y"); t.pack(side="left", fill="both", expand=True)
        t.mark_set("in", "end-1c"); t.mark_gravity("in", "left")
        app.common_keys(t)
        s.comp = Completer(app, t, lambda: KW + BI + re.findall(r"[A-Za-z_]\w{2,}", t.get("1.0", "end")))
        t.bind("<Return>", s.ret); t.bind("<KP_Enter>", s.ret)
        t.bind("<Key>", s.key); t.bind("<BackSpace>", s.bksp); t.bind("<Delete>", s.dele)
        t.bind("<Tab>", s.tab)
        t.bind("<<Cut>>", lambda e: "break" if s.protected() else None)
        t.bind("<<Paste>>", s.paste)
        t.bind("<Up>", lambda e: s.histmove(-1)); t.bind("<Down>", lambda e: s.histmove(1))
        t.bind("<Alt-p>", lambda e: s.histmove(-1)); t.bind("<Alt-n>", lambda e: s.histmove(1))
        t.bind("<Home>", s.home)
        t.bind("<Control-c>", lambda e: None if t.tag_ranges("sel") else (s.interrupt(), "break")[1])
        t.bind("<Double-Button-1>", s.dbl)
        t.bind("<Button-2>" if MAC else "<Button-3>", s.popup)
        s.poll()

    # ---- process ----
    def alive(s):
        return s.proc is not None and s.proc.poll() is None

    def start(s, path=None):
        s.kill()
        t = s.text
        t.delete("in", "end-1c")
        s.mode, s.ind = "out", 0
        if t.compare("in", ">", "1.0"):
            s.write(("" if t.get("in-1c") == "\n" else "\n") + "=" * 12 + " RESTART: %s " % (path or "Shell") + "=" * 12 + "\n", "info")
        else:
            s.write("PyNi %s  -  Python %s on %s\nType help(), copyright() or license() for more information.\n"
                    % (VER, sys.version.split()[0], sys.platform), "info")
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
        kw = dict(creationflags=0x08000000) if WIN else dict(start_new_session=True)
        try:
            s.proc = subprocess.Popen([pyexe(), "-u", "-c", BOOT] + ([path] if path else []),
                                      stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                      cwd=os.path.dirname(path) if path else os.path.expanduser("~"), env=env, **kw)
        except OSError as e:
            s.write("Could not start Python: %s\n" % e, "err"); return
        threading.Thread(target=s.reader, args=(s.proc,), daemon=True).start()

    def restart(s):
        s.start(); s.text.focus_set()

    def kill(s):
        if s.proc:
            try:
                s.proc.kill()
            except OSError:
                pass
            s.proc = None

    def interrupt(s):
        if not s.alive():
            return
        if WIN:
            s.send("\x03\n")
        else:
            try:
                os.kill(s.proc.pid, signal.SIGINT)
            except OSError:
                pass

    def send(s, x):
        try:
            s.proc.stdin.write(x.encode("utf-8")); s.proc.stdin.flush()
        except (OSError, AttributeError):
            pass

    def reader(s, p):
        dec = codecs.getincrementaldecoder("utf-8")("replace")
        while True:
            try:
                b = os.read(p.stdout.fileno(), 65536)
            except OSError:
                b = b""
            if not b:
                break
            s.q.put((p, dec.decode(b)))
        s.q.put((p, None))

    def poll(s):
        buf, ended = [], None
        try:
            for _ in range(400):
                p, d = s.q.get_nowait()
                if p is not s.proc:
                    continue
                if d is None:
                    ended = p
                else:
                    buf.append(d)
        except queue.Empty:
            pass
        if buf:
            s.feed("".join(buf))
        if ended:
            s.proc = None
            s.write("\n[Python exited with code %s. Press Enter to restart.]\n" % ended.wait(), "info")
            s.text.mark_set("insert", "end-1c")
        s.after(25, s.poll)

    # ---- output ----
    def feed(s, data):
        t = s.text
        for part in re.split(r"([\x02\x03\x05\x06])", data):
            if part == "\x02":
                s.mode = "err"
            elif part == "\x05":
                s.mode, s.pbuf = "prompt", ""
            elif part == "\x03":
                s.mode = "out"
            elif part == "\x06":
                s.mode = "out"
                t.mark_set("insert", "end-1c")
                if s.pbuf == "... " and s.ind:
                    t.insert("end-1c", " " * s.ind)
                elif s.pbuf == ">>> ":
                    s.ind = 0
            elif part:
                if s.mode == "prompt":
                    s.pbuf += part
                s.write(part, s.mode)
        if int(t.index("end").split(".")[0]) > 6000:
            t.delete("1.0", "1500.0")

    def write(s, txt, tag):
        t = s.text
        t.mark_gravity("in", "right")
        t.insert("in", txt, tag)
        t.mark_gravity("in", "left")
        t.see("end")

    def clear(s):
        t = s.text
        t.delete("1.0", "in")

    # ---- input ----
    def protected(s):
        t = s.text
        return bool(t.tag_ranges("sel")) and t.compare("sel.first", "<", "in")

    def ret(s, e=None):
        t = s.text
        if t.compare("insert", "<", "in"):
            line = t.get("insert linestart", "insert lineend")
            if s.jump(line):
                return "break"
            t.delete("in", "end-1c"); t.insert("end-1c", re.sub(r"^(>>> |\.\.\. )", "", line))
            t.mark_set("insert", "end-1c"); t.see("end")
            return "break"
        cmd = t.get("in", "end-1c")
        t.mark_set("insert", "end-1c"); t.insert("end-1c", "\n")
        t.tag_add("stdin", "in", "end-1c")
        t.mark_set("in", "end-1c"); t.see("end")
        if cmd.strip() and (not s.hist or s.hist[-1] != cmd):
            s.hist.append(cmd)
        s.hi = len(s.hist)
        last = cmd.split("\n")[-1]
        ind = len(last) - len(last.lstrip())
        s.ind = ind + 4 if last.rstrip().endswith(":") else (ind if last.strip() else 0)
        if not s.alive():
            s.start()
        else:
            s.send((cmd if cmd.strip() else "") + "\n")
        return "break"

    def key(s, e):
        t = s.text
        if e.char and (e.char >= " " or e.char == "\t") and not e.state & 0xC:
            if s.protected():
                t.tag_remove("sel", "1.0", "end")
            if t.compare("insert", "<", "in"):
                t.mark_set("insert", "end-1c")

    def bksp(s, e=None):
        t = s.text
        if t.tag_ranges("sel"):
            return "break" if s.protected() else None
        if t.compare("insert", "<=", "in"):
            return "break"
        before = t.get("in", "insert")
        if before.endswith("    ") and not before.strip(" "):
            t.delete("insert-4c", "insert"); return "break"

    def dele(s, e=None):
        t = s.text
        if s.protected() or (not t.tag_ranges("sel") and t.compare("insert", "<", "in")):
            return "break"

    def tab(s, e=None):
        t = s.text
        if t.compare("insert", "<", "in"):
            t.mark_set("insert", "end-1c")
        if re.search(r"[\w.]$", t.get("in", "insert")):
            s.comp.show()
        else:
            t.insert("insert", "    ")
        return "break"

    def paste(s, e=None):
        t = s.text
        if s.protected():
            t.tag_remove("sel", "1.0", "end")
        if t.compare("insert", "<", "in"):
            t.mark_set("insert", "end-1c")

    def home(s, e=None):
        t = s.text
        if t.compare("insert", ">=", "in") and t.compare("insert linestart", "<=", "in"):
            t.mark_set("insert", "in"); return "break"

    def histmove(s, d):
        t = s.text
        if t.compare("insert", "<", "in") or not s.hist:
            return None
        s.hi = max(0, min(len(s.hist), s.hi + d))
        t.delete("in", "end-1c")
        t.insert("end-1c", s.hist[s.hi] if s.hi < len(s.hist) else "")
        t.mark_set("insert", "end-1c"); t.see("end")
        return "break"

    def jump(s, line):
        m = TBRE.search(line)
        if m and os.path.isfile(m.group(1)):
            s.app.open(m.group(1)); s.app.goto(int(m.group(2)))
            return True
        return False

    def dbl(s, e):
        if s.jump(s.text.get("@%d,%d linestart" % (e.x, e.y), "@%d,%d lineend" % (e.x, e.y))):
            return "break"

    def popup(s, e):
        m = tk.Menu(s, tearoff=0)
        m.add_command(label="Copy", command=lambda: s.text.event_generate("<<Copy>>"))
        m.add_command(label="Paste", command=lambda: s.text.event_generate("<<Paste>>"))
        m.add_separator()
        m.add_command(label="Go to File/Line", command=lambda: s.jump(s.text.get("@%d,%d linestart" % (e.x, e.y), "@%d,%d lineend" % (e.x, e.y))))
        m.add_command(label="Clear Shell", command=s.clear)
        m.add_command(label="Restart Shell", command=s.restart)
        m.add_command(label="Interrupt", command=s.interrupt)
        m.tk_popup(e.x_root, e.y_root)


class FindDialog:
    def __init__(s, app):
        s.app, s.win = app, None
        s.fv, s.rv = tk.StringVar(), tk.StringVar()
        s.case, s.word, s.regex = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()

    def open(s, replace=False):
        t = s.app.ed().text
        if t.tag_ranges("sel"):
            sel = t.get("sel.first", "sel.last")
            if "\n" not in sel:
                s.fv.set(sel)
        if not s.win or not s.win.winfo_exists():
            s.win = w = tk.Toplevel(s.app.root)
            w.title("Find / Replace"); w.transient(s.app.root); w.resizable(False, False)
            f = ttk.Frame(w, padding=10); f.pack(fill="both", expand=True)
            ttk.Label(f, text="Find:").grid(row=0, column=0, sticky="w")
            s.fe = ttk.Entry(f, textvariable=s.fv, width=34); s.fe.grid(row=0, column=1, columnspan=3, sticky="ew", pady=2)
            ttk.Label(f, text="Replace:").grid(row=1, column=0, sticky="w")
            ttk.Entry(f, textvariable=s.rv, width=34).grid(row=1, column=1, columnspan=3, sticky="ew", pady=2)
            for i, (lbl, v) in enumerate((("Match case", s.case), ("Whole word", s.word), ("Regex", s.regex))):
                ttk.Checkbutton(f, text=lbl, variable=v).grid(row=2, column=1 + i, sticky="w", pady=4)
            b = ttk.Frame(f); b.grid(row=3, column=0, columnspan=4, sticky="e")
            for lbl, fn in (("Find Next", s.next), ("Find Prev", s.prev), ("Replace", s.replace), ("Replace All", s.replace_all)):
                ttk.Button(b, text=lbl, command=fn).pack(side="left", padx=2)
            s.msg = ttk.Label(f, text=""); s.msg.grid(row=4, column=0, columnspan=4, sticky="w")
            w.bind("<Return>", lambda e: s.next()); w.bind("<Escape>", lambda e: s.close())
            w.bind("<F3>", lambda e: s.next()); w.bind("<Shift-F3>", lambda e: s.prev())
            w.protocol("WM_DELETE_WINDOW", s.close)
            w.configure(bg=s.app.th["ui"])
        s.win.deiconify(); s.win.lift(); s.fe.focus_set(); s.fe.select_range(0, "end")

    def close(s):
        if s.win:
            s.app.ed().text.tag_remove("hit", "1.0", "end")
            s.win.destroy(); s.win = None

    def rx(s):
        p = s.fv.get()
        if not p:
            return None
        if not s.regex.get():
            p = re.escape(p)
        if s.word.get():
            p = r"\b(?:%s)\b" % p
        try:
            return re.compile(p, 0 if s.case.get() else re.I)
        except re.error as e:
            s.say("Bad regex: %s" % e); return None

    def say(s, m):
        if s.win:
            s.msg.config(text=m)
        else:
            s.app.status(m)

    def _find(s, back):
        rx = s.rx()
        if not rx:
            if not s.win:
                s.open()
            return None
        t = s.app.ed().text
        src = t.get("1.0", "end-1c")
        starts = [0] + [m.end() for m in re.finditer("\n", src)]
        t.tag_remove("hit", "1.0", "end")
        allm = [m for m in rx.finditer(src) if m.end() > m.start()]
        if allm and len(allm) < 5000:
            t.tag_add("hit", *[ix(starts, o) for m in allm for o in m.span()])
        if not allm:
            s.say("Not found"); t.bell(); return None
        if back:
            pos = len(t.get("1.0", "sel.first" if t.tag_ranges("sel") else "insert"))
            cand = [m for m in allm if m.end() <= pos]
            m = cand[-1] if cand else allm[-1]
        else:
            pos = len(t.get("1.0", "insert"))
            m = next((m for m in allm if m.start() >= pos), allm[0])
        a, b = ix(starts, m.start()), ix(starts, m.end())
        t.tag_remove("sel", "1.0", "end"); t.tag_add("sel", a, b)
        t.mark_set("insert", a if back else b); t.see(a)
        s.say("%d match%s" % (len(allm), "" if len(allm) == 1 else "es"))
        s.app.ed().moved()
        return m

    def next(s):
        s._find(False)

    def prev(s):
        s._find(True)

    def replace(s):
        rx, t = s.rx(), s.app.ed().text
        if rx and t.tag_ranges("sel"):
            m = rx.fullmatch(t.get("sel.first", "sel.last"))
            if m:
                new = m.expand(s.rv.get()) if s.regex.get() else s.rv.get()
                t.edit_separator()
                a = t.index("sel.first"); t.delete("sel.first", "sel.last"); t.insert(a, new)
                t.mark_set("insert", "%s+%dc" % (a, len(new)))
                t.edit_separator()
        s.next()

    def replace_all(s):
        rx = s.rx()
        if not rx:
            return
        t = s.app.ed().text
        src = t.get("1.0", "end-1c")
        starts = [0] + [m.end() for m in re.finditer("\n", src)]
        ms = list(rx.finditer(src))
        t.edit_separator()
        for m in reversed(ms):
            a, b = ix(starts, m.start()), ix(starts, m.end())
            t.delete(a, b); t.insert(a, m.expand(s.rv.get()) if s.regex.get() else s.rv.get())
        t.edit_separator()
        s.say("Replaced %d occurrence%s" % (len(ms), "" if len(ms) == 1 else "s"))


class App:
    def __init__(s, files):
        s.cfg = dict(theme="light", size=11, wrap=False, lines=True, recent=[], geom="1000x720")
        try:
            with open(CFG_PATH) as f:
                s.cfg.update(json.load(f))
        except (OSError, ValueError):
            pass
        s.root = r = tk.Tk(className="PyNi")
        r.title(APP); r.geometry(s.cfg["geom"]); r.minsize(420, 300)
        if ICON:
            try:
                s.icon = tk.PhotoImage(data=ICON); r.iconphoto(True, s.icon)
            except tk.TclError:
                pass
        fams = set(tkfont.families())
        fam = next((f for f in ("Consolas", "Menlo", "SF Mono", "DejaVu Sans Mono", "Liberation Mono", "Courier New") if f in fams),
                   tkfont.nametofont("TkFixedFont").actual()["family"])
        s.font = tkfont.Font(family=fam, size=s.cfg["size"])
        s.th = THEMES.get(s.cfg["theme"], THEMES["light"])
        s.style = ttk.Style()
        s.style.theme_use("clam")
        s.find = FindDialog(s)
        s.statusbar = ttk.Frame(r, style="Status.TFrame")
        s.statusbar.pack(side="bottom", fill="x")
        s.msg = ttk.Label(s.statusbar, text="", style="Status.TLabel"); s.msg.pack(side="left", padx=8)
        s.pos = ttk.Label(s.statusbar, text="Ln 1, Col 0", style="Status.TLabel"); s.pos.pack(side="right", padx=8)
        s.pw = tk.PanedWindow(r, orient="vertical", sashwidth=5, bd=0, sashrelief="flat", opaqueresize=True)
        s.pw.pack(fill="both", expand=True)
        s.nb = ttk.Notebook(s.pw)
        s.shell = Shell(s, s.pw)
        s.pw.add(s.nb, stretch="always", minsize=120)
        s.pw.add(s.shell, stretch="never", minsize=60, height=210)
        s.dark = tk.BooleanVar(value=s.cfg["theme"] == "dark")
        s.wrapv = tk.BooleanVar(value=s.cfg["wrap"])
        s.linesv = tk.BooleanVar(value=s.cfg["lines"])
        s.menus()
        s.common_keys(r)
        s.nb.bind("<<NotebookTabChanged>>", s.tab_changed)
        s.nb.bind("<Button-2>" if not MAC else "<Button-3>", s.tab_middle)
        r.protocol("WM_DELETE_WINDOW", s.quit)
        if MAC:
            r.createcommand("tk::mac::Quit", s.quit)
            r.createcommand("::tk::mac::OpenDocument", lambda *a: [s.open(p) for p in a])
        s.apply_theme()
        for f in files:
            if os.path.isfile(f):
                s.open(f)
        if not s.eds():
            s.new()
        s.shell.start()
        r.after(60, lambda: s.ed().text.focus_set())

    # ---- helpers ----
    def eds(s):
        return [s.nb.nametowidget(t) for t in s.nb.tabs()]

    def ed(s):
        sel = s.nb.select()
        return s.nb.nametowidget(sel) if sel else None

    def ftext(s):
        w = s.root.focus_get()
        return w if isinstance(w, tk.Text) else s.ed().text

    def status(s, m):
        s.msg.config(text=m)
        if getattr(s, "_st", None):
            s.root.after_cancel(s._st)
        s._st = s.root.after(6000, lambda: s.msg.config(text=""))

    def save_cfg(s):
        try:
            with open(CFG_PATH, "w") as f:
                json.dump(s.cfg, f, indent=1)
        except OSError:
            pass

    def common_keys(s, w):
        M = MOD
        keys = {
            "<%s-n>" % M: s.new, "<%s-o>" % M: s.open, "<%s-s>" % M: s.save, "<%s-S>" % M: s.save_as,
            "<%s-w>" % M: s.close, "<%s-q>" % M: s.quit, "<%s-z>" % M: s.undo, "<%s-Z>" % M: s.redo,
            "<%s-y>" % M: s.redo, "<%s-a>" % M: s.select_all, "<%s-f>" % M: s.find.open,
            "<%s-h>" % M: lambda: s.find.open(True), "<%s-g>" % M: s.goto, "<Alt-g>": s.goto,
            "<F3>": s.find.next, "<Shift-F3>": s.find.prev, "<%s-slash>" % M: s.toggle_comment,
            "<%s-bracketright>" % M: s.indent, "<%s-bracketleft>" % M: s.dedent,
            "<Alt-Key-3>": s.comment, "<Alt-Key-4>": s.uncomment,
            "<%s-equal>" % M: lambda: s.zoom(1), "<%s-plus>" % M: lambda: s.zoom(1),
            "<%s-minus>" % M: lambda: s.zoom(-1), "<%s-Key-0>" % M: lambda: s.zoom(0),
            "<F5>": s.run, "<Alt-x>": s.check, "<%s-F6>" % M: lambda: s.shell.restart(), "<Alt-c>": s.browser,
            "<Alt-m>": s.open_module, "<F1>": s.docs, "<Control-space>": s.complete,
            "<%s-t>" % M: s.toggle_theme, "<%s-Tab>" % ("Control"): lambda: s.cycle(1),
        }
        for k, f in keys.items():
            try:
                w.bind(k, lambda e, f=f: (f(), "break")[1])
            except tk.TclError:
                pass

    # ---- theme / view ----
    def apply_theme(s):
        th = s.th = THEMES[s.cfg["theme"]]
        st = s.style
        st.configure(".", background=th["ui"], foreground=th["fg"], fieldbackground=th["bg"], bordercolor=th["border"],
                     lightcolor=th["ui"], darkcolor=th["ui"], troughcolor=th["bg"], arrowcolor=th["fg"],
                     selectbackground=th["sel"], selectforeground=th["fg"], insertcolor=th["caret"], focuscolor=th["ui"])
        st.configure("TNotebook", background=th["ui"], borderwidth=0, tabmargins=(0, 2, 0, 0))
        st.configure("TNotebook.Tab", background=th["ui2"], foreground=th["fg"], padding=(12, 4), borderwidth=0)
        st.map("TNotebook.Tab", background=[("selected", th["bg"])], foreground=[("selected", th["fg"])])
        st.configure("TScrollbar", background=th["ui2"], troughcolor=th["bg"], borderwidth=0, arrowsize=13,
                     gripcount=0, relief="flat")
        st.map("TScrollbar", background=[("active", th["gutfg"])])
        st.configure("TButton", background=th["ui2"], padding=(8, 2), relief="flat")
        st.map("TButton", background=[("active", th["border"] if th is THEMES["light"] else th["gutfg"])])
        st.configure("Bar.TButton", padding=(6, 0))
        st.configure("TEntry", fieldbackground=th["bg"], foreground=th["fg"])
        st.map("TCheckbutton", background=[("active", th["ui"])], indicatorbackground=[("!selected", th["bg"]), ("selected", th["sel"])])
        st.configure("Status.TFrame", background=th["ui2"]); st.configure("Status.TLabel", background=th["ui2"])
        s.root.config(bg=th["ui"]); s.pw.config(bg=th["border"])
        for ed in s.eds():
            s.theme_text(ed.text); ed.gut.config(bg=th["gut"]); ed.lines()
        s.theme_text(s.shell.text)
        if s.find.win:
            s.find.win.configure(bg=th["ui"])

    def theme_text(s, t):
        th = s.th
        t.config(bg=th["bg"], fg=th["fg"], insertbackground=th["caret"], selectbackground=th["sel"],
                 selectforeground=th["fg"], inactiveselectbackground=th["sel"])
        for tg in TAGS + SHTAGS:
            t.tag_configure(tg, foreground=th[tg])
        t.tag_configure("curline", background=th["curline"])
        t.tag_configure("match", background=th["match"])
        t.tag_configure("hit", background=th["hit"])

    def toggle_theme(s, from_menu=False):
        if not from_menu:
            s.dark.set(not s.dark.get())
        s.cfg["theme"] = "dark" if s.dark.get() else "light"
        s.apply_theme(); s.save_cfg()

    def zoom(s, d):
        size = 11 if d == 0 else max(6, min(48, s.font.cget("size") + d))
        s.font.configure(size=size); s.cfg["size"] = size
        tabs = (s.font.measure("    "),)
        for ed in s.eds():
            ed.text.config(tabs=tabs); ed.lines()
        s.shell.text.config(tabs=tabs)
        s.save_cfg()

    def set_wrap(s):
        s.cfg["wrap"] = w = s.wrapv.get()
        for ed in s.eds():
            ed.text.config(wrap="word" if w else "none")
            ed.hs.grid_remove() if w else ed.hs.grid()
        s.save_cfg()

    def set_lines(s):
        s.cfg["lines"] = v = s.linesv.get()
        for ed in s.eds():
            ed.gut.grid() if v else ed.gut.grid_remove(); ed.lines()
        s.save_cfg()

    # ---- menus ----
    def menus(s):
        mb = tk.Menu(s.root)
        s.root.config(menu=mb)

        def menu(label, items):
            m = tk.Menu(mb, tearoff=0)
            mb.add_cascade(label=label, menu=m, underline=0)
            for it in items:
                if it is None:
                    m.add_separator()
                elif it[0] == "check":
                    m.add_checkbutton(label=it[1], variable=it[2], command=it[3], accelerator=it[4] if len(it) > 4 else "")
                elif it[0] == "cascade":
                    m.add_cascade(label=it[1], menu=it[2])
                else:
                    m.add_command(label=it[0], command=it[1], accelerator=it[2] if len(it) > 2 else "")
            return m
        c = MODL + "+"
        s.recent_menu = tk.Menu(mb, tearoff=0)
        menu("File", [("New File", s.new, c + "N"), ("Open...", s.open, c + "O"), ("Open Module...", s.open_module, "Alt+M"),
                      ("cascade", "Recent Files", s.recent_menu), None,
                      ("Save", s.save, c + "S"), ("Save As...", s.save_as, c + "Shift+S"),
                      ("Save Copy As...", lambda: s.ed().save(copy=True)), None,
                      ("Close Tab", s.close, c + "W"), ("Exit", s.quit, c + "Q")])
        menu("Edit", [("Undo", s.undo, c + "Z"), ("Redo", s.redo, c + "Y"), None,
                      ("Cut", lambda: s.ftext().event_generate("<<Cut>>"), c + "X"),
                      ("Copy", lambda: s.ftext().event_generate("<<Copy>>"), c + "C"),
                      ("Paste", lambda: s.ftext().event_generate("<<Paste>>"), c + "V"),
                      ("Select All", s.select_all, c + "A"), None,
                      ("Find...", s.find.open, c + "F"), ("Find Next", s.find.next, "F3"),
                      ("Find Previous", s.find.prev, "Shift+F3"), ("Replace...", lambda: s.find.open(True), c + "H"),
                      ("Go to Line...", s.goto, c + "G"), None, ("Show Completions", s.complete, "Ctrl+Space")])
        menu("Format", [("Indent Region", s.indent, c + "]"), ("Dedent Region", s.dedent, c + "["),
                        ("Comment Out Region", s.comment, "Alt+3"), ("Uncomment Region", s.uncomment, "Alt+4"),
                        ("Toggle Comment", s.toggle_comment, c + "/"), None,
                        ("Tabify Region", lambda: s.ed().region(lambda ls: [re.sub(r"^( {4})+", lambda m: "\t" * (len(m.group()) // 4), l) for l in ls])),
                        ("Untabify Region", lambda: s.ed().region(lambda ls: [l.expandtabs(4) for l in ls])),
                        ("Strip Trailing Whitespace", s.strip_ws)])
        menu("Run", [("Run Module", s.run, "F5"), ("Check Module", s.check, "Alt+X"), None,
                     ("Python Shell", lambda: s.shell.text.focus_set()), ("Restart Shell", s.shell.restart, c + "F6"),
                     ("Interrupt Execution", s.shell.interrupt, "Ctrl+C"), ("Clear Shell", s.shell.clear), None,
                     ("Module Browser", s.browser, "Alt+C")])
        menu("Options", [("check", "Dark Theme", s.dark, lambda: s.toggle_theme(True), c + "T"),
                         ("check", "Line Numbers", s.linesv, s.set_lines), ("check", "Word Wrap", s.wrapv, s.set_wrap), None,
                         ("Zoom In", lambda: s.zoom(1), c + "+"), ("Zoom Out", lambda: s.zoom(-1), c + "-"),
                         ("Reset Zoom", lambda: s.zoom(0), c + "0")])
        menu("Help", [("Keyboard Shortcuts", s.shortcuts), ("Python Docs", s.docs, "F1"), None, ("About PyNi", s.about)])
        s.fill_recent()

    def fill_recent(s):
        m = s.recent_menu
        m.delete(0, "end")
        for p in s.cfg["recent"]:
            m.add_command(label=p, command=lambda p=p: s.open(p))
        if not s.cfg["recent"]:
            m.add_command(label="(empty)", state="disabled")
        else:
            m.add_separator(); m.add_command(label="Clear List", command=lambda: (s.cfg.update(recent=[]), s.fill_recent(), s.save_cfg()))

    def add_recent(s, p):
        p = os.path.abspath(p)
        s.cfg["recent"] = [p] + [x for x in s.cfg["recent"] if x != p][:9]
        s.fill_recent(); s.save_cfg()

    # ---- tabs / files ----
    def retitle(s, ed):
        s.nb.tab(ed, text=("● " if ed.dirty else "") + ed.name())
        if ed is s.ed():
            s.root.title("%s%s - %s" % ("*" if ed.dirty else "", ed.path or ed.name(), APP))

    def tab_changed(s, e=None):
        ed = s.ed()
        if ed:
            s.retitle(ed); ed.moved(); ed.text.focus_set()

    def tab_middle(s, e):
        try:
            i = s.nb.index("@%d,%d" % (e.x, e.y))
        except tk.TclError:
            return
        s.close(s.eds()[i])

    def cycle(s, d):
        tabs = s.nb.tabs()
        if tabs:
            s.nb.select((tabs.index(s.nb.select()) + d) % len(tabs))

    def new(s, path=None):
        ed = Editor(s, path)
        s.nb.add(ed, text=ed.name())
        s.nb.select(ed); s.retitle(ed); ed.text.focus_set()
        return ed

    def open(s, path=None):
        paths = [path] if path else filedialog.askopenfilenames(parent=s.root, filetypes=FTYPES)
        for p in paths:
            p = os.path.abspath(p)
            for ed in s.eds():
                if ed.path and os.path.normcase(ed.path) == os.path.normcase(p):
                    s.nb.select(ed); break
            else:
                cur = s.ed()
                try:
                    ed = s.new(p)
                except OSError as e:
                    messagebox.showerror("Open failed", str(e), parent=s.root); continue
                if cur and not cur.path and not cur.dirty and not cur.text.get("1.0", "end-1c"):
                    s.nb.forget(cur); cur.destroy()
                s.add_recent(p)

    def save(s):
        s.ed().save()

    def save_as(s):
        s.ed().save(as_=True)

    def ask_save(s, ed):
        if not ed.dirty:
            return True
        s.nb.select(ed)
        r = messagebox.askyesnocancel("Save changes?", "Save changes to %s?" % ed.name(), parent=s.root)
        return r is False or (r is True and ed.save())

    def close(s, ed=None):
        ed = ed or s.ed()
        if not s.ask_save(ed):
            return
        s.nb.forget(ed); ed.destroy()
        if not s.eds():
            s.new()

    def quit(s):
        for ed in s.eds():
            if not s.ask_save(ed):
                return
        s.cfg["geom"] = s.root.geometry()
        s.save_cfg(); s.shell.kill(); s.root.destroy()

    def open_module(s):
        name = simpledialog.askstring("Open Module", "Module name (e.g. os.path):", parent=s.root)
        if not name:
            return
        try:
            import importlib.util
            spec = importlib.util.find_spec(name.strip())
            path = spec and spec.origin
        except (ImportError, ValueError):
            path = None
        if path and os.path.isfile(path) and path.endswith(".py"):
            s.open(path)
        else:
            messagebox.showerror("Open Module", "No Python source found for %r" % name, parent=s.root)

    def attrs(s, obj):
        if not obj or obj.split(".")[0] in ("antigravity", "this"):
            return []
        root = obj.split(".")[0]
        if root not in getattr(sys, "stdlib_module_names", ()) and root not in sys.modules:
            return []
        try:
            import importlib
            m = importlib.import_module(obj)
        except Exception:
            try:
                m = importlib.import_module(obj.rpartition(".")[0])
                m = getattr(m, obj.rpartition(".")[2])
            except Exception:
                return []
        return [n for n in dir(m) if not n.startswith("_")]

    # ---- edit commands ----
    def undo(s):
        try:
            s.ftext().edit_undo()
        except tk.TclError:
            pass

    def redo(s):
        try:
            s.ftext().edit_redo()
        except tk.TclError:
            pass

    def select_all(s):
        t = s.ftext()
        t.tag_add("sel", "1.0", "end-1c"); t.mark_set("insert", "end-1c")

    def complete(s):
        w = s.root.focus_get()
        (s.shell.comp if w is s.shell.text else s.ed().comp).show()

    def goto(s, n=None):
        ed = s.ed()
        if n is None:
            n = simpledialog.askinteger("Go to Line", "Line number:", parent=s.root, minvalue=1)
            if not n:
                return
        t = ed.text
        t.mark_set("insert", "%d.0" % n); t.tag_remove("sel", "1.0", "end")
        t.tag_add("sel", "insert linestart", "insert lineend"); t.see("insert"); t.focus_set(); ed.moved()

    def indent(s):
        s.ed().region(lambda ls: ["    " + l if l.strip() else l for l in ls])

    def dedent(s):
        s.ed().region(lambda ls: [l[1:] if l.startswith("\t") else l[min(4, len(l) - len(l.lstrip(" "))):] for l in ls])

    def comment(s):
        s.ed().region(lambda ls: ["##" + l for l in ls])

    def uncomment(s):
        s.ed().region(lambda ls: [re.sub(r"^(\s*)##?", r"\1", l) for l in ls])

    def toggle_comment(s):
        def fn(ls):
            code = [l for l in ls if l.strip()]
            if code and all(l.lstrip().startswith("#") for l in code):
                return [re.sub(r"^(\s*)# ?", r"\1", l) for l in ls]
            ind = min((len(l) - len(l.lstrip()) for l in code), default=0)
            return [l[:ind] + "# " + l[ind:] if l.strip() else l for l in ls]
        s.ed().region(fn)

    def strip_ws(s):
        t = s.ed().text
        t.edit_separator()
        for i in range(1, int(t.index("end-1c").split(".")[0]) + 1):
            l = t.get("%d.0" % i, "%d.end" % i)
            if l != l.rstrip():
                t.delete("%d.%d" % (i, len(l.rstrip())), "%d.end" % i)
        t.edit_separator()

    # ---- run ----
    def check(s, quiet=False):
        ed = s.ed()
        try:
            compile(ed.text.get("1.0", "end-1c"), ed.path or ed.name(), "exec")
        except (SyntaxError, ValueError) as e:
            ln = getattr(e, "lineno", None) or 1
            s.goto(ln)
            off = getattr(e, "offset", None)
            if off:
                ed.text.tag_remove("sel", "1.0", "end")
                ed.text.mark_set("insert", "%d.%d" % (ln, max(0, off - 1)))
                ed.text.tag_add("sel", "insert", "insert+1c")
            messagebox.showerror("Syntax error", "%s\n(line %s)" % (getattr(e, "msg", e), ln), parent=s.root)
            return False
        if not quiet:
            s.status("No syntax errors.")
        return True

    def run(s):
        ed = s.ed()
        if (ed.dirty or not ed.path) and not ed.save():
            return
        if not s.check(quiet=True):
            return
        s.shell.start(ed.path)
        s.shell.text.focus_set()

    def browser(s):
        ed = s.ed()
        items = [(i + 1, l.rstrip().rstrip(":")) for i, l in enumerate(ed.text.get("1.0", "end-1c").split("\n"))
                 if re.match(r"\s*(async\s+)?(def|class)\s+\w", l)]
        th = s.th
        w = tk.Toplevel(s.root); w.title("Module Browser - " + ed.name()); w.geometry("420x480"); w.transient(s.root)
        lb = tk.Listbox(w, font=s.font, bd=0, highlightthickness=0, bg=th["bg"], fg=th["fg"], activestyle="none",
                        selectbackground=th["sel"], selectforeground=th["fg"])
        sb = ttk.Scrollbar(w, command=lb.yview); lb.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y"); lb.pack(fill="both", expand=True)
        for n, l in items:
            lb.insert("end", l)
        if not items:
            lb.insert("end", "(no classes or functions)")

        def go(e=None):
            sel = lb.curselection()
            if sel and items:
                s.goto(items[sel[0]][0])
        lb.bind("<Double-Button-1>", go); lb.bind("<Return>", go); w.bind("<Escape>", lambda e: w.destroy())
        lb.focus_set(); lb.selection_set(0)

    # ---- help ----
    def docs(s):
        webbrowser.open("https://docs.python.org/%d.%d/" % sys.version_info[:2])

    def shortcuts(s):
        c = MODL + "+"
        txt = "\n".join("%-18s %s" % kv for kv in [
            (c + "N / O / S", "New / Open / Save"), (c + "Shift+S", "Save As"), (c + "W", "Close tab"),
            ("Ctrl+Tab", "Next tab"), (c + "Z / " + c + "Y", "Undo / Redo"), (c + "F / " + c + "H", "Find / Replace"),
            ("F3 / Shift+F3", "Find next / previous"), (c + "G", "Go to line"),
            ("Tab / Ctrl+Space", "Complete word (after a name)"), (c + "] / " + c + "[", "Indent / dedent"),
            (c + "/", "Toggle comment"), ("Alt+3 / Alt+4", "Comment / uncomment (IDLE)"),
            ("F5", "Run module in shell"), ("Alt+X", "Check syntax"), (c + "F6", "Restart shell"),
            ("Ctrl+C (shell)", "Interrupt running code"), ("Up / Down (shell)", "Command history"),
            ("Double-click (shell)", "Jump to traceback line"), ("Alt+C", "Module browser"),
            (c + "+ / - / 0", "Zoom"), (c + "T", "Toggle dark theme"), ("F1", "Python docs")])
        w = tk.Toplevel(s.root); w.title("Keyboard Shortcuts"); w.transient(s.root)
        t = tk.Text(w, font=s.font, width=52, height=txt.count("\n") + 2, bd=0, padx=12, pady=10)
        t.insert("1.0", txt); t.config(state="disabled"); t.pack(fill="both", expand=True)
        s.theme_text(t); w.bind("<Escape>", lambda e: w.destroy())

    def about(s):
        messagebox.showinfo("About PyNi", "PyNi %s - Python Mini\n\nA tiny, IDLE-style Python IDE.\nRunning on Python %s\nTk %s"
                            % (VER, sys.version.split()[0], tk.TkVersion), parent=s.root)


def main():
    if WIN:
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("PyNi.IDE")
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    app = App([a for a in sys.argv[1:] if not a.startswith("-psn")])
    app.root.mainloop()


if __name__ == "__main__":
    main()
