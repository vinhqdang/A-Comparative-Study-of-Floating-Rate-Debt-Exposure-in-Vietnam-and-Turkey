"""
Flatten manuscript.tex into a pandoc-friendly .tex source for conversion to
Word: resolves all \\ref/\\eqref against the compiled .aux file's \\newlabel
entries, converts custom theorem-like environments (proposition, corollary,
remark, proof) into plain bolded paragraph headers with the resolved number
baked in, and strips frontmatter/journal-class-only commands pandoc's
generic LaTeX reader does not know. Not meant to be reusable beyond this
one conversion -- it is a scratch tool for producing a submission Word
file, not part of the analysis pipeline.
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "manuscript.tex"
AUX = ROOT / "manuscript.aux"
OUT = ROOT / "manuscript_for_word.tex"


def parse_aux(aux_path):
    text = aux_path.read_text()
    label_map = {}
    for m in re.finditer(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", text):
        label, number = m.group(1), m.group(2)
        # Strip any nested \ref{...} pandoc-unfriendly leftovers (rare, in
        # aux titles only, not in the number field itself).
        label_map[label] = number
    return label_map


def main():
    label_map = parse_aux(AUX)
    src = SRC.read_text()

    # --- Frontmatter: keep title/abstract/keywords, drop the wrapper ---
    src = src.replace("\\begin{frontmatter}\n\n", "")
    src = src.replace("\n\\end{frontmatter}", "")
    src = re.sub(r"%% Double-blind review:.*\n", "", src)
    src = src.replace("\\begin{keyword}", "\n\\textbf{Keywords:} ")
    src = src.replace("\\end{keyword}", "\n")
    src = src.replace("\\sep", ";")

    # --- Theorem-like environments -> bold paragraph headers ---
    def env_replacer(kind_word):
        def _sub(m):
            label = m.group("label")
            title = m.group("title")
            number = label_map.get(label, "?") if label else "?"
            head = f"{kind_word} {number}"
            if title:
                head += f" ({title})"
            return f"\n\n\\textbf{{{head}.}} "
        return _sub

    # proposition / corollary: \begin{env}[Title]\label{x} or \begin{env}\label{x}
    for env, word in (("proposition", "Proposition"), ("corollary", "Corollary")):
        pattern = re.compile(
            r"\\begin\{" + env + r"\}(?:\[(?P<title>[^\]]*)\])?\s*"
            r"(?:\\label\{(?P<label>[^}]+)\})?"
        )
        src = pattern.sub(env_replacer(word), src)
        src = src.replace(f"\\end{{{env}}}", "\n\n")

    # remark: same shape, but the plain \begin{remark} (no label/title) needs
    # its own running count since it is not in label_map.
    remark_counter = {"n": 0}

    def remark_sub(m):
        label = m.group("label")
        title = m.group("title")
        if label and label in label_map:
            number = label_map[label]
            remark_counter["n"] = int(number)
        else:
            remark_counter["n"] += 1
            number = str(remark_counter["n"])
        head = f"Remark {number}"
        if title:
            head += f" ({title})"
        return f"\n\n\\textbf{{{head}.}} "

    src = re.sub(
        r"\\begin\{remark\}(?:\[(?P<title>[^\]]*)\])?\s*"
        r"(?:\\label\{(?P<label>[^}]+)\})?",
        remark_sub, src,
    )
    src = src.replace("\\end{remark}", "\n\n")

    # assumption: not used in this manuscript, but handle defensively.
    assumption_counter = {"n": 0}

    def assumption_sub(m):
        assumption_counter["n"] += 1
        title = m.group("title")
        head = f"Assumption {assumption_counter['n']}"
        if title:
            head += f" ({title})"
        return f"\n\n\\textbf{{{head}.}} "

    src = re.sub(r"\\begin\{assumption\}(?:\[(?P<title>[^\]]*)\])?", assumption_sub, src)
    src = src.replace("\\end{assumption}", "\n\n")

    # proof
    src = src.replace("\\begin{proof}", "\n\n\\emph{Proof.} ")
    src = src.replace("\\end{proof}", " $\\blacksquare$\n\n")

    # --- Resolve remaining \ref / \eqref against the aux map ---
    def ref_sub(m):
        label = m.group(1)
        return label_map.get(label, "??")

    def eqref_sub(m):
        label = m.group(1)
        return f"({label_map.get(label, '??')})"

    src = re.sub(r"\\eqref\{([^}]+)\}", eqref_sub, src)
    src = re.sub(r"\\ref\{([^}]+)\}", ref_sub, src)

    # --- Prefix table/figure captions with their resolved number ---
    # Word has no auto-numbering field here (this is a flattened LaTeX
    # source, not a live document), so a caption reading only "Firms per
    # year" gives a reader nothing to match against a body-text mention of
    # "Table 1" -- belt-and-suspenders alongside the lead-in sentences.
    def caption_sub(m):
        word = "Table" if m.group("label").startswith("tab:") else "Figure"
        number = label_map.get(m.group("label"), "?")
        return f"\\caption{{{word} {number}: {m.group('text')}}}\n\\label{{{m.group('label')}}}"

    src = re.sub(
        r"\\caption\{(?P<text>.*?)\}\s*\n\\label\{(?P<label>tab:[^}]+|fig:[^}]+)\}",
        caption_sub, src, flags=re.S,
    )

    # --- Drop now-unused \label{...} ---
    src = re.sub(r"\\label\{[^}]+\}", "", src)

    # --- Figures: point at the rasterised PNGs instead of PDFs ---
    src = src.replace("figs/dose_response.pdf", "figs/dose_response.png")
    src = src.replace("figs/event_studies.pdf", "figs/event_studies.png")
    src = src.replace("figs/validation.pdf", "figs/validation.png")

    # --- Drop elsarticle/journal-class-only commands pandoc won't know ---
    src = re.sub(r"\\journal\{[^}]*\}\n*", "", src)
    src = re.sub(r"\\modulolinenumbers\[[^\]]*\]\n*", "", src)
    src = src.replace("\\usepackage{lineno}\n", "")
    src = re.sub(
        r"\\documentclass\[review,12pt,authoryear\]\{elsarticle\}",
        r"\\documentclass[12pt]{article}",
        src,
    )

    OUT.write_text(src)
    print(f"wrote {OUT} ({len(src.splitlines())} lines)")


if __name__ == "__main__":
    main()
