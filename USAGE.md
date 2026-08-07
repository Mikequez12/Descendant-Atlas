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

* First execute Atlas.
* Then select the **Download** option and press **Enter**.
* Select the release you want and press **Enter** again.
* Wait until the download is complete.

#### Apply mods

* First execute Atlas.
* Then select the **Mods** option and press **Enter**.
* Next select **Import mods** and press **Enter**.
* Select your release and the mods you want to use.
* Wait until the import is complete.
>[!IMPORTANT]
>Launch the Minecraft world after applying mods before importing additional ones.

#### Export mods

* First execute Atlas.
* Then select the **Mods** option and press **Enter**.
* Next select **Export mod** and press **Enter**.
* Select the world containing your modifications.
* Select the datapacks, resource packs, and structures that will be included in the mod.
* If a structure should be placed automatically:
    * Select it under `Place mode`.
    * Enter the coordinates where the structure should be placed.
    * Optionally enter a custom dimension. Leave it blank to use the Overworld.
    >[!NOTE]
    >These are the coordinates where the structure will be generated, **not** the position of the Structure Block used to create it.
* Select **Quit...** and press **Enter**.
* Wait until Atlas finishes exporting the mod.
* Your mod will be in the `mods` folder.

#### Launch Minecraft locally (BETA)

>[!WARNING]
>This is an experimental feature that is being tested and may not work. Please use it with caution.

* First execute Atlas.
* Then select the **Launch Minecraft locally (BETA)** option.
* Wait for Minecraft to launch.
* A temporary Minecraft instance will be launched on the `.mc` folder.
* The `downloads` folder will be used as the Minecraft saves directory to make testing faster.

#### Config

* First execute Atlas.
* Then select the **Config** option.
* Select **Reset config** if you want to restore the default configuration for your platform.
* Select **Edit config** if you want to modify the config of Atlas.
    * Select a property and then press **Right** to edit it.
    * To finish editing it, press **Enter**.
    * To save your changes and leave, press **Enter** again.
    * To show or hide hidden settings, press `.`.
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
>* Go to the storage in the class selector.
>* Locate the structure block.
>* Open its interface.
>* Press **Save** manually.

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