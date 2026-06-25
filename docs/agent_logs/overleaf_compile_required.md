# Overleaf Compile Required

Local LaTeX compilation was skipped because a LaTeX compiler (`pdflatex` or `latexmk`) is not installed on this host environment. The paper should be compiled on Overleaf or another TeX-enabled cloud editor.

## Instructions to Upload and Compile on Overleaf

1. **Get the Upload ZIP Package**:
   - Locate the ZIP archive at the root of the workspace:
     `paper_overleaf_upload.zip`

2. **Upload to Overleaf**:
   - Go to [Overleaf](https://www.overleaf.com/).
   - Click on **New Project** -> **Upload Project**.
   - Select or drag-and-drop the `paper_overleaf_upload.zip` file.
   - Overleaf will automatically unpack the ZIP file and open the project workspace.

3. **Verify Settings**:
   - In the Overleaf project window, click on **Menu** (top-left corner).
   - Ensure the following settings are configured:
     - **Compiler**: `pdfLaTeX`
     - **TeX Live Version**: `2024 (or Latest)`
     - **Main document**: `main.tex`

4. **Recompile**:
   - Click the green **Recompile** button (or press `Ctrl + Enter` / `Cmd + Enter`).
   - The document will compile cleanly and produce the final publication PDF.
