import subprocess

res = subprocess.run(["git", "diff", "index.html"], capture_output=True, text=True, encoding="utf-8", errors="ignore")
diff_text = res.stdout

deleted_lines = [l for l in diff_text.split("\n") if l.startswith("-") and not l.startswith("---")]
print(f"Total deleted lines: {len(deleted_lines)}")
for l in deleted_lines[:50]:
    print(l[:100])

