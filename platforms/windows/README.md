# X-Vector for Windows

Windows does not read Linux XCursor themes. This folder contains the same
eight-point star converted to Windows `.cur` files.

All four variants are included:

- `X-Vector` — white core, black outline;
- `X-Vector-Inverse` — black core, white outline;
- `X-Vector-Meta` — rhombic axes, white core, black outline;
- `X-Vector-Meta-Inverse` — rhombic axes, black core, white outline.

## Quick install

1. Open PowerShell in this folder (`platforms/windows`).
2. Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

For another variant:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Variant X-Vector-Inverse
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Variant X-Vector-Meta
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Variant X-Vector-Meta-Inverse
```

The script copies the cursors to `%LOCALAPPDATA%\X-Vector\Cursors` and sets
the current user's cursor roles. No administrator rights are needed.

If Windows keeps showing the old cursor, open **Mouse Properties** once or
sign out and back in.

## What gets replaced

- normal select;
- help select;
- working in background;
- busy;
- precision select;
- text select;
- unavailable;
- hand, link, location and person select;
- move.

Resize cursors stay native: a star gives no directional cue, so the standard
Windows resize arrows remain in place.

## Manual install

Open **Settings → Bluetooth & devices → Mouse → Additional mouse settings →
Pointers**. Select a role, click **Browse**, and choose the `.cur` file from
the folder of the variant you want in `platforms\windows`.

Use `text.cur` for text select and `not-allowed.cur` for unavailable. All other
star roles use `default.cur`.

## Uninstall

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Uninstall
```

This removes the copied files and the cursor values written by the script.
Then choose another scheme in Mouse Properties if needed.

## Notes

- Windows may label the current scheme **Custom**. That is expected: the
  installer sets the active cursor values instead of registering a named
  system scheme.
- The cursors are static; there is no click animation.
- Each `.cur` contains 32, 48 and 64 px images.
- The files are generated from the same source as the Linux theme. The
  containers and hotspots are format-validated, but the package has not been
  tested on every Windows build.
