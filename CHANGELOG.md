# v1.0

Initial release.

### Features
- Download official Descendant+ releases directly from GitHub.
- Export mods into portable `.dscmod` packages.
- Import `.dscmod` packages into existing Descendant+ worlds.
- Merge resource packs into `resources.zip`.
- Import structures and configure automatic placement.
- Automatic datapack patching for compatibility.

# v1.1

Fixed ANSI handling.

### Features
- Improved compatibility with legacy Windows consoles by detecting ANSI support automatically.
- Improved compatibility with non-Unicode terminals.

# v1.2

Improved usability and project documentation.

### Features
- Added an integrated Help section.
- Added the MIT License.
- Improved the installation guide and project documentation.
- Added an About page inside Atlas.
- Improved first-time user experience.

# v1.3

Improved `descendant-atlas` datapack.

### Features
- Fixed an issue that could cause patches to be applied multiple times.
- Mods are now initialized only once after installation.
- Replaced entity-based persistent state tracking with storage-based tracking for improved reliability.

# v1.4

Improved mod importing workflow.

### Features
- Added support for importing multiple `.dscmod` packages in a single operation.
- All imported mods are now applied together the next time the world is loaded.
- Added two example mods: `bosstitle.dscmod` and `Dark-Market.dscmod`.
- Added a `Press ENTER to continue...` prompt for executable users.

# v1.5

Improved diagnostics and developer tools.

### Features
- Added improved environment detection.
- Added detailed debug output for Atlas operations.
- Improved error reporting to make issues easier to identify.

# v1.6

### Features
- Improved the reliability of automatic structure placement.
- Atlas now temporarily force-loads destination chunks while placing structures.
- Improved the internal mod installation process.
- Various terminal interface improvements.
- Internal code cleanup and maintenance.
- Removed example mods.

# v1.7
### New features
- Added a built-in Minecraft launcher (Beta).
- Added an interactive configuration editor.
- Added configurable Minecraft installation directory.
- Added configurable Minecraft version.
- Atlas now automatically creates a temporary game directory when launching Minecraft.
- Downloaded worlds are automatically linked into the temporary launcher instance.
- Added automatic configuration reset for first-time users.

### Improvements
- Greatly improved release extraction.
- Improved terminal interface rendering.
- Improved configuration management.
- Improved structure placement pipeline.
- Improved resource pack importing.
- Improved compatibility with different operating systems.
- Improved progress and status messages throughout the application.
- Better automatic detection of ANSI-capable terminals.
- Added automatic Unicode fallback for legacy terminals.

### Internal changes
- Refactored configuration handling.
- Refactored terminal UI rendering.
- Added portable ANSI fallback implementation.
- Added portable Unicode fallback implementation.
- Reworked menu system.
- Simplified release download workflow.
- Improved launcher integration architecture.

### Bug fixes
- Fixed several extraction edge cases.
- Fixed issues when importing releases containing nested ZIP files.
- Fixed various terminal compatibility issues.
- Fixed several file handling edge cases during import/export.

# v1.8

### New Features

- Added Atlas-Extra (Early Access).
- Atlas-Extra introduces cross-world progression transfer.

### Improvements

- Atlas-Extra utilities are now located in their own `atlas-extra/` directory.

### Changes

- Standalone `.exe` files are no longer published as release assets.
- The executable is now distributed inside the project `.zip`, as Atlas expects to run from within its project directory.

### Fixes

- Various bug fixes and internal improvements.