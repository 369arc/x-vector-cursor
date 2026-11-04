# X-Vector for macOS

macOS does not read Linux XCursor themes. The `.cape` files in this folder
are [Mousecape](https://github.com/alexzielenski/Mousecape) packages generated
from the same X-Vector star.

- `X-Vector.cape` — white core, black outline;
- `X-Vector-Inverse.cape` — black core, white outline;
- `X-Vector-Meta.cape` — rhombic axes, white core, black outline;
- `X-Vector-Meta-Inverse.cape` — rhombic axes, black core, white outline;
- `X-Vector-Link.cape` — linked rhombic axes, white core, black outline;
- `X-Vector-Link-Inverse.cape` — linked rhombic axes, black core, white outline.

## Install

1. Download Mousecape from its
   [releases page](https://github.com/alexzielenski/Mousecape/releases).
2. Open Mousecape and choose **Mousecape → Install Helper Tool**.
   Approve the macOS prompt if one appears.
3. Double-click the `.cape` file you want.
4. Select the cape in Mousecape and click **Apply**.
5. If macOS blocks Mousecape, allow it in
   **System Settings → Privacy & Security**.

If double-clicking does not import the cape, run:

```bash
open -a Mousecape X-Vector.cape
```

## What is included

- arrow, context arrow, alias, copy and move;
- wait;
- link, crosshair, pointing hand, context menu and help;
- zoom in and zoom out;
- text cursor;
- unavailable cursor.

The cape contains 1×, 2×, 5× and 10× representations, so it stays crisp on
Retina and scaled displays. Resize and other system cursors stay native.

## Notes

- Mousecape is a third-party tool and is not affiliated with X-Vector.
- Cursors are static; animated busy cursors are not included.
- macOS updates can reset the cursor. Reapply the cape in Mousecape.
- The cape format follows Mousecape's example files. It has not been tested on
  every macOS release.

## Uninstall

In Mousecape, select the default system cape and click **Apply**, then remove
the X-Vector cape from the library. Do this before removing Mousecape itself;
otherwise its helper may keep the last applied cursor until the helper is
removed.
