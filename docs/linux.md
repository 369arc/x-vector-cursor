# X-Vector on Linux

X-Vector is a native XCursor theme. It works on X11 and on Wayland
compositors that use XCursor, including Hyprland, Sway/wlroots, GNOME and
KDE Plasma.

## Install

```bash
git clone https://github.com/369arc/x-vector-cursor.git
cd x-vector-cursor
./install.sh
```

This installs both variants to
`${XDG_DATA_HOME:-$HOME/.local/share}/icons` and applies `X-Vector` in the
current Hyprland session when `hyprctl` is available.

To apply the inverse variant:

```bash
./install.sh X-Vector-Inverse
```

Some older applications only look in the legacy `~/.icons` directory. If a
program does not see the theme, add symlinks:

```bash
ICONS="${XDG_DATA_HOME:-$HOME/.local/share}/icons"
mkdir -p ~/.icons
ln -sfn "$ICONS/X-Vector" ~/.icons/X-Vector
ln -sfn "$ICONS/X-Vector-Inverse" ~/.icons/X-Vector-Inverse
```

## Hyprland

Add this to `~/.config/hypr/hyprland.conf`:

```ini
env = XCURSOR_THEME,X-Vector
env = XCURSOR_SIZE,28
env = HYPRCURSOR_THEME,X-Vector
env = HYPRCURSOR_SIZE,28
```

For the inverse, replace `X-Vector` with `X-Vector-Inverse`.

If you use Hyprland's Lua configuration, the equivalent is:

```lua
hl.env("XCURSOR_THEME", "X-Vector")
hl.env("XCURSOR_SIZE", "28")
hl.env("HYPRCURSOR_THEME", "X-Vector")
hl.env("HYPRCURSOR_SIZE", "28")
```

Apply immediately:

```bash
hyprctl setcursor X-Vector 28
```

## GNOME

```bash
gsettings set org.gnome.desktop.interface cursor-theme 'X-Vector'
gsettings set org.gnome.desktop.interface cursor-size 28
```

You can also use **Settings → Accessibility → Seeing → Cursor Size** and
GNOME Tweaks for the theme. Log out and back in if an application keeps the
old cursor.

## Cinnamon

```bash
gsettings set org.cinnamon.desktop.interface cursor-theme 'X-Vector'
gsettings set org.cinnamon.desktop.interface cursor-size 28
```

The same options are in **Settings → Themes → Mouse Pointer**.

## MATE

```bash
gsettings set org.mate.peripherals-mouse cursor-theme 'X-Vector'
gsettings set org.mate.peripherals-mouse cursor-size 28
```

The same options are in **Control Center → Appearance → Theme → Customize →
Pointer**.

## XFCE

```bash
xfconf-query -c xsettings -p /Gtk/CursorThemeName -s X-Vector
xfconf-query -c xsettings -p /Gtk/CursorThemeSize -s 28
```

The same options are in **Settings → Mouse and Touchpad → Theme**.

## KDE Plasma

Open **System Settings → Appearance → Cursors**, select `X-Vector` and apply.

On Plasma 6, the command-line equivalent is:

```bash
plasma-apply-cursortheme X-Vector
```

If that tool is unavailable, write the setting directly:

```bash
kwriteconfig6 --file kcminputrc --group Mouse --key cursorTheme X-Vector
```

On Plasma 5 use `kwriteconfig5` instead. Log out and back in, or restart
Plasma, to apply it everywhere.

## Generic X11

Add this to `~/.Xresources`:

```xresources
Xcursor.theme: X-Vector
Xcursor.size: 28
```

Then apply it:

```bash
xrdb -merge ~/.Xresources
```

Also export the environment variables from `~/.xprofile` or `~/.xsessionrc`:

```sh
export XCURSOR_THEME=X-Vector
export XCURSOR_SIZE=28
```

Log out and back in for all applications to pick them up.

## GTK applications outside GNOME

Add this to both `~/.config/gtk-3.0/settings.ini` and
`~/.config/gtk-4.0/settings.ini`:

```ini
[Settings]
gtk-cursor-theme-name=X-Vector
gtk-cursor-theme-size=28
```

## Flatpak

Flatpak applications may not see host cursor themes. Grant read access to the
icon directory:

```bash
flatpak override --user --filesystem="$HOME/.local/share/icons:ro"
```

Then restart the application. Some Flatpak runtimes ship their own cursor
themes and may still ignore the host setting.

## Size

The theme contains 24, 28, 32, 48 and 64 px images. **28 px** is the
recommended size. Change `XCURSOR_SIZE`, `cursor-size` or the desktop
environment's cursor-size setting if you prefer another size.

## Build

```bash
./build.sh
```

This regenerates both XCursor themes plus the Windows and macOS assets.

## Uninstall

```bash
./uninstall.sh
```

Then select another cursor theme in your desktop environment.
