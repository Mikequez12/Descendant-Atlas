# Descendant Atlas
<sub>v1.0</sub>

**Descendant Atlas** is a command-line utility for creating, managing and applying mods for **Descendant+**.

Instead of manually copying datapacks, structures and resource packs between worlds, Descendant Atlas packages them into a portable `.dscmod` file that can later be applied to another installation.

## Features

- Download official Descendant+ releases directly from GitHub.
- Create portable `.dscmod` mod packages.
- Import mods into existing Descendant+ worlds.
- Merge resource packs into the world's `resources.zip`.
- Import structures automatically.
- Apply structure placement automatically on first world load.
- Preserve compatibility with existing datapacks.

## Installation

Clone the repository:

```bash
git clone https://github.com/Mikequez12/descendant-atlas
cd descendant-atlas
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python atlas.py
```

## Creating a mod

1. Download a Descendant+ release.
2. Select **Mods → Export mod**.
3. Choose:
   - Datapacks
   - Resource packs
   - Structures
4. Configure structure placement (optional).
5. A `.dscmod` package will be created.

## Applying a mod

1. Select **Mods → Import mod**.
2. Choose a downloaded Descendant+ release.
3. Select a `.dscmod`.
4. Descendant Atlas will:
   - copy datapacks,
   - merge resource packs,
   - import structures,
   - patch the required load functions.

## Project structure

```
downloads/
mods/
    .resourcepacks/
    *.dscmod
```

## License

This project is not affiliated with Gerg or the Descendant+ team.