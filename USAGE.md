# Descendant Atlas Usage Guide

A usage guide for Descendant Atlas.

## Atlas

> This section refers to the `main.py` (or `.exe`) file.

### Execution

As explained in the `README.md` file, you first need to install `Python`.
Then run:

**Windows**

```bat
python -m pip install -r requirements.txt
python main.py
```

**Linux / MacOS**

```sh
python3 -m pip install -r requirements.txt
python3 main.py
```

>[!NOTE]
> In Windows you can execute the `.exe` as well in case you don't want to install `Python`.

### Controls

* To move up and down, use the **Up** and **Down** arrow keys.
* To enter a menu, press **Space** or **Enter**.
* To switch between options in the same category, use the **Left** and **Right** arrow keys.
* To edit a setting in the configuration menu, press **Right**.
* To save the configuration, press **Enter**.
* To quit the app, press **Escape**. If you're entering text, it may not work; in that case, use **Ctrl+C** instead.

### Tutorial

#### Download Descendant+ releases

1. First execute Atlas.
2. Then select the **Download** option and press **Enter**.
3. Select the release you want and press **Enter** again.
4. Wait until the download is complete.


#### Apply mods
1. Execute Atlas.
2. Select **Mods**.
3. Select **Import mods**.
4. Select the Descendant+ release.
5. Select the `.dscmod` files you want to install.
6. Confirm the installation.
7. Wait until Atlas finishes.

Atlas automatically imports the mod's:

* Datapacks
* Structures
* Resource packs
* Dependencies

If a selected mod has a dependency that is not installed, Atlas will ask whether you want to:

* **Abort** the installation.
* **Continue** without installing the dependency.
* **Install** the missing dependency.

If the dependency provides a download URL, Atlas can download it automatically.

>[!IMPORTANT]
>Launch the Minecraft world after applying mods before importing additional mods. Atlas needs the world to be opened once to finish applying the installation.

#### Export mods
1. Execute Atlas.
2. Select **Mods**.
3. Select **Export mod**.
4. Select the world containing your modifications.
5. Enter a name for the mod.
6. Select the datapacks to include.
7. Select the resource packs to include.
8. Select the structures to include.
9. Optionally configure automatic structure placement.
10. Select the **dependencies** of your mod.
11. Optionally provide a download URL for each dependency.
12. Finish the export.

The resulting `.dscmod` file will be placed in the mods directory.

##### Dependencies

When exporting a mod, Atlas can create a dependency list for other `.dscmod` files.

Each dependency is identified by its SHA-256 hash, rather than only its filename. This allows Atlas to recognize a dependency even if it has been renamed.

A dependency can also have an optional download URL. This allows Atlas to retrieve the dependency automatically when another user imports the mod.

##### Automatic structure placement

If a structure should be placed automatically:

1. Select the structure under Place mode.
2. Enter its X, Y and Z coordinates.
3. Optionally enter a dimension.
4. Leave the dimension empty to use `minecraft:overworld`.
5. Continue when all structures have been configured.

>[!NOTE]
>The coordinates refer to the position where the structure itself will be generated, not the position of the Structure Block used to create it.

#### Launch Minecraft locally (BETA)

>[!WARNING]
>This is an experimental feature that is being tested and may not work. Please use it with caution.

1. Execute Atlas.
2. Then select the **Launch Minecraft locally (BETA)** option.
3. Wait for Minecraft to launch.

Atlas creates a temporary Minecraft instance using the `.mc` directory.
The `downloads` directory is linked as the Minecraft `saves` directory, allowing downloaded releases to be tested without manually copying them.

#### Config

1. Execute Atlas.
2. Select **Config**.
3. Select one of the available options.

##### Reset config

**Reset config** restores the default configuration for your platform.

##### Edit config

**Edit config** allows individual configuration values to be changed.

* Select a property.
* Press **Right** to edit it.
* Press **Enter** to finish editing.
* Press **Enter** again to save the configuration.
* Press `.` to show or hide hidden settings.

>[!WARNING]
>If you're a **MacOS** user, please check the configuration is appropriate for your system.

## Atlas-Extra
> This section refers to the tools inside the `atlas-extra/` directory.

>[!WARNING]
>Atlas-Extra is an experimental feature that is being tested.

### Saving

>[!IMPORTANT]
>To save and load an old world, first **make sure you have Atlas-Extra** installed in your old world.

Then launch the world and run:

```mcfunction
/function atlas-extra:save
```

>If you also want to save your storage (items, loot crates, etc.):
>1. Go to the storage in the class selector.
>2. Locate the structure block.
>3. Open its interface.
>4. Press **Save** manually.

This will save your data in a `.nbt` file.

Then open the world folder and copy the path.

Execute the `save.py` file:

---

As explained in the `README.md` file, you first need to install `Python`.
Then run:

**Windows**

```bat
python -m pip install -r requirements.txt
python atlas-extra/save.py
```

**Linux / MacOS**

```sh
python3 -m pip install -r requirements.txt
python3 atlas-extra/save.py
```

---

Paste the world's folder path and press **Enter**.

>[!NOTE]
>Depending on your terminal, pasting may require **Right Click** instead of **Ctrl+V**.

>If you saved your storage, the program may ask if you want to import it, select `Yes` to replace your actual storage with the saved storage or select `No` to discard it.

>[!IMPORTANT]
>Make sure you have the Atlas-Extra installed in the brand-new world before continuing.

Copy the new-world's folder's path and paste it in the app, then press **Enter**.

Wait until the process is completed.

The save data has now been copied to the new world. To continue, run the following command in the new world:

```mcfunction
/function atlas-extra:load
```

>[!NOTE]
>You'll need to execute this command twice in less than 5 seconds to ensure you want to import the saved changes.

Finally Atlas-Extra will load the changes.

### Developing

Atlas-Extra is a **framework** made for Minecraft datapack developers.

I highly recommend reading Atlas-Extra's source code to better understand what it does, but if you want to check what data Atlas-Extra provides to your script, try this command:

```mcfunction
/data get storage atlas-extra:<data>
```

> You'll need to replace `<data>` with a real data storage such as `unlocks`.