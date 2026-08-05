# Descendant Atlas
<sub>v1.6</sub>

![IMAGE](docs/screenshot.png)

**Descendant Atlas** is a command-line utility for creating, managing and applying mods for **Descendant+**.

Instead of manually copying datapacks, structures and resource packs between worlds, Descendant Atlas packages them into a portable `.dscmod` file that can later be applied to another installation.

## Why Atlas?

Descendant Atlas was created to make installing and modifying Descendant+ simpler.

While experienced users may already be familiar with GitHub releases, archive extraction and Minecraft's world structure, many players are not. Atlas automates those repetitive tasks so users can focus on playing and creating content instead of managing files.

Its goal is to provide a straightforward way to download official Descendant+ releases, create portable mods and apply them safely without manually navigating world folders.

## What's New in v1.6

### Improved installation reliability
Atlas now performs additional setup steps when applying mods to ensure structures can be placed more reliably across dimensions during the first world load.

### Better terminal interface
The terminal interface has received several quality-of-life improvements, making Atlas easier to use.

> [!WARNING]
> Installing another mod before opening the world can corrupt your installation.
> After every mod installation, launch the world once to let Atlas finish applying the changes before importing another mod.

## About

Descendant Atlas is an independent utility built around Descendant+.

Atlas is **not** a fork of Descendant+, does not replace it and is not affiliated with its development team. Instead, it complements existing Descendant+ releases by providing tools for downloading, packaging and applying community-made modifications.

Atlas is built around three design principles:

- Preserve official Descendant+ releases whenever possible.
- Keep mods portable through the `.dscmod` format.
- Automate repetitive installation tasks without changing gameplay by itself.

Rather than altering existing game content, Atlas only adds or patches the minimum components required to manage and load Atlas mods.

## Features

- Download official Descendant+ releases directly from GitHub.
- Create portable `.dscmod` mod packages.
- Import many mods at the same time.
- Apply mods into existing Descendant+ worlds.
- Merge resource packs into the world's `resources.zip`.
- Import structures automatically.
- Apply structure placement automatically on first world load.
- Preserve compatibility with existing datapacks.

## Requirements

- Python 3.10 or later (when running from source)
- Git (when cloning the repository) or download `.zip` (not recommended)

## Installation

### Windows

#### Option 1 — Executable (Recommended)

Download the latest `.exe` from the [Releases](https://github.com/Mikequez12/Descendant-Atlas/releases) page and run it.

> [!NOTE]
> Windows SmartScreen may display a warning because Atlas is not code-signed. If you trust the release, click **More info** → **Run anyway**.

#### Option 2 — From source

Install Python from [python.org](https://www.python.org/downloads/) if it isn't already installed.

```bat
git clone https://github.com/Mikequez12/descendant-atlas
cd descendant-atlas
python -m pip install -r requirements.txt
python main.py
```
### Linux

Ensure Python 3 is installed, then run:

```sh
git clone https://github.com/Mikequez12/descendant-atlas
cd descendant-atlas
python3 -m pip install -r requirements.txt
python3 main.py
```

### macOS

Ensure Python 3 is installed (Homebrew is recommended), then run:

```sh
git clone https://github.com/Mikequez12/descendant-atlas
cd descendant-atlas
python3 -m pip install -r requirements.txt
python3 main.py
```

## Creating a mod

1. Download a Descendant+ release.
2. Create and save your changes using a `structure block`.
3. Select **Mods → Export mod**.
4. Choose:
   - Datapacks
   - Resource packs
   - Structures
5. Configure structure placement (optional).
6. A `.dscmod` package will be created.

## Applying a mod

1. Select **Mods → Import mod**.
2. Choose a downloaded Descendant+ release.
3. Select a `.dscmod`.
4. Descendant Atlas will:
   - copy datapacks,
   - merge resource packs,
   - import structures,
   - patch the required load functions.

## FAQ

**Q: Does Atlas cause issues with Descendant+?**  
**A:** No known issues caused by Atlas itself have been reported so far. However, third-party mods or newly released versions of Descendant+ may introduce incompatibilities. If you find a bug that appears to be caused by Atlas, please report it by opening an issue on GitHub.

---

**Q: Does Atlas use real Minecraft mods?**  
**A:** No. Atlas uses `.dscmod` files, which package datapacks, resource packs, structures and other world modifications.

---

**Q: Does Atlas work on Linux?**  
**A:** Yes. Atlas is designed to be cross-platform and should work on Linux.

---

**Q: How does Atlas work?**  
**A:** Atlas downloads releases from the Descendant+ GitHub repository and applies modifications locally. If you're curious about the implementation, feel free to read the source code in `main.py`.

---

**Q: Is Atlas a virus?**  
**A:** No. Atlas is open source and only downloads and modifies files from GitHub repositories.

---

**Q: Where can I find Atlas mods?**  
**A:** There is currently no official repository for Atlas mods. You'll need to obtain `.dscmod` files directly from their creators.

---

**Q: Why doesn't Atlas include modified Descendant+ releases?**  
**A:** Atlas intentionally distributes the official Descendant+ releases without altering their contents. Any changes introduced by Atlas are limited to the infrastructure required to load Atlas mods, helping keep releases as close as possible to the originals.

---

**Q: Why do I need to open the descendant world after modding it?**
**A:** Atlas doesn't directly modify your in-game world when using the app, it just drops the resources and how to apply them. This is made for various reasons, but most importantly: it's easy to debug and way more safe. If you don't open the world and just add another installation, chances are the entire world gets erased, this is caused because when executing Atlas, it thinks it was installed, and gets glitched. This has not been 100% tested and your world can continue as normal after this happening. This practice is not recommended: please, launch the world after modding it.

## Project structure

```
downloads/
mods/
    .resourcepacks/
    *.dscmod
```

## Before you start
> [!CAUTION]
> This project is still experimental. Please make a backup before importing any files. Better safe than sorry.

> [!CAUTION]
> Installing multiple modpacks without loading the world in between will cause issues: After every installation you need to run the world to finish the installing process.
