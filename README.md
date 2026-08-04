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
python main.py
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
**A:** No issues caused by Atlas itself are currently known. However, third-party mods or newly released versions of Descendant+ may introduce incompatibilities. If you find a bug that appears to be caused by Atlas, please report it.

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

## Project structure

```
downloads/
mods/
    .resourcepacks/
    *.dscmod
```

## License

This project is not affiliated with Gerg or the Descendant+ team.
