import requests
from rich.console import Console
from datetime import datetime
from colorist import Color, Effect
import zipfile
import os
import pathlib
import shutil
import json
import time
import stat
import uuid

from tui import choose, choose_select, custom_input

from utils import ansi_supported

if not ansi_supported:
    print('This terminal doesn\'t support ANSI codes, please, try to change to another terminal.')
    input('Type "CONTINUE" to continue, press enter to kill the process > ')
    exit(0)


def request_release(t="Please, select a release"):
    releases = requests.get('https://api.github.com/repos/sdfxf31/Descendant-Plus/releases').json()
    r = [
        [
            release['name'],
            (
                "Draft" if release["draft"]
                else "Pre-release" if release["prerelease"]
                else "Release"
            ),
            " ".join(release['body'].split()),
            datetime.strptime(release['updated_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%B %d, %Y at %I:%M %p")
        ]
        for release in releases
    ]
    headers = ["Name", "Kind", "Description", "Last Updated"]
    m = [
        max(len(headers[i]), *(len(row[i]) for row in r))
        for i in range(len(headers))
    ]
    l = {}
    for i,release in enumerate(releases):
        l['   '.join([
            r[i][_].ljust(m[_],' ') for _ in range(len(r[i]))
        ])] = release['name']
    release = choose(
        l,
        title=t,
        header=' | '.join([t.ljust(m[i],' ') for i,t in enumerate(headers)]),
        return_index=True
    )

    return releases[release]

def release_zip(release, return_index=False):
    assets = release["assets"]

    zip_assets = [
        (i, asset)
        for i, asset in enumerate(assets)
        if asset["name"].lower().endswith(".zip")
    ]

    if not zip_assets:
        zip_assets = list(enumerate(assets))

    if len(zip_assets) > 1:
        choice = choose(
            [asset["name"] for _, asset in zip_assets],
            title="Select the file",
            return_index=True,
        )
        index, asset = zip_assets[choice]
    else:
        index, asset = zip_assets[0]

    return index if return_index else asset

def download(release,root_path=lambda name:f'downloads/Descendant-{name}',alert=True,ask_overwrite=True):
    root_path = root_path(release["name"])
    if os.path.exists(root_path):
        if ask_overwrite:
            if choose(['Yes','No'],title=f'The release {release["name"]} is already downloaded, do you want to overwrite it?') == 'No':
                print('Aborting...')
                exit(0)
        os.chmod(root_path, stat.S_IWRITE)
        shutil.rmtree(root_path, ignore_errors=True)

    selected_file = release_zip(release,return_index=True)

    print('Downloading...',end='',flush=True)

    with open(f'{root_path}.zip','wb') as file:
        file.write(
            requests.get(f'https://github.com/sdfxf31/Descendant-Plus/releases/download/{release["tag_name"]}/{release_zip(release)["name"]}').content
        )

    print(' [DONE]')
    print('Extracting...',end='')
    with zipfile.ZipFile(f'{root_path}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{root_path}')
    print(' [DONE]')

    os.remove(f"{root_path}.zip")

    def unwrap(root: pathlib.Path):
        zip_folders = set()
        while True:
            lock = next(root.rglob("session.lock"), None)
            if lock is None:
                files = list(root.rglob("*"))
                _ = []
                for f in files:
                    if f.suffix == ".zip":
                        _.append(f)
                        zip_folders.add(f.parent)
                    else:
                        if f.is_dir():
                            continue
                        if os.path.exists(f):
                            os.remove(f)
                for f in _:
                    time.sleep(0.1)
                    with zipfile.ZipFile(f) as z:
                        z.extractall(f.parent)
                # delete_files()
            else:
                world = lock.parent

                if world == root:
                    return

                moved = set()

                for item in list(world.iterdir()):
                    target = root / item.name
                    shutil.move(item, target)
                    moved.add(target.name)

                for item in list(root.iterdir()):
                    if item.name in moved:
                        continue
                    if item.suffix == ".zip":
                        continue

                    if item.is_dir():pass
                        # shutil.rmtree(item)
                    else:
                        item.unlink()

                for f in zip_folders:
                    if f != root:
                        shutil.rmtree(f)

    print('Unwrapping...',end='')
    P = pathlib.Path(f'{root_path}')
    unwrap(P)
    print(' [DONE]')

    if alert:print(f'The release was downloaded successfully. Check {Color.GREEN}"{P}"{Effect.OFF}')











if __name__ == '__main__':
    console = Console()
    console.print(f'Welcome to [green]Descendant Atlas[/green]!\n[dim](This project is not affiliated with Gerg or the Descendant+ team)[/dim]\nMade by: [blue][link=https://github.com/Mikequez12]Mikequez12[/link][/blue]')

    match choose(['Download','Mods','Quit'],title='Please, select an option'):
        case 'Download':
            print('Fetching GitHub...')
            release = request_release()

            download(release)
        case 'Mods':
            match choose([
                'Import mod',
                'Export mod',
            ], title='Please, select an option'):
                case 'Export mod':
                    dir_name = choose([
                        _ for _ in os.listdir('downloads') if os.path.isdir(f'downloads/{_}') and _ != '.temp'
                    ], title='Please, select a release')

                    if dir_name is None:
                        print('No releases are installed. Please install at least one to continue.')
                        exit(0)
                    
                    MOD_NAME = custom_input(title='Select a name for the mod',accept=lambda _:_.strip() != '',error_msg='Invalid path')
                    if os.path.exists(f'mods/{MOD_NAME}') or os.path.exists(f'mods/{MOD_NAME}.dscmod') or os.path.exists(f'mods/{MOD_NAME}.zip'):
                        if choose([
                            'Abort',
                            'Overwrite'
                        ],title='The mod already exists. Do you want to overwrite it?') == 'Abort':
                            print('Aborting...')
                            exit(0)
                        if os.path.exists(f'mods/{MOD_NAME}'):shutil.rmtree(f'mods/{MOD_NAME}')
                        if os.path.exists(f'mods/{MOD_NAME}.dscmod'):os.remove(f'mods/{MOD_NAME}.dscmod')
                        if os.path.exists(f'mods/{MOD_NAME}.zip'):os.remove(f'mods/{MOD_NAME}.zip')
                    os.mkdir(f'mods/{MOD_NAME}')
                    os.mkdir(f'mods/{MOD_NAME}/structures')
                    with open(f'mods/{MOD_NAME}/placing.json','w',encoding='utf-8') as file:file.write('[]')
                    for k,v in choose_select({
                        _:['No','Yes'] for _ in os.listdir(f'downloads/{dir_name}/datapacks')
                    }, title='Which datapacks do you want to export?', return_index=True).items():
                        if v:
                            shutil.copytree(f'downloads/{dir_name}/datapacks/{k}',f'mods/{MOD_NAME}/datapacks/{k}')
                    for k,v in choose_select({
                        _:['No','Yes'] for _ in os.listdir(f'mods/.resourcepacks')
                    }, title='Which resource packs do you want to export?', return_index=True).items():
                        if v:
                            src = f'mods/.resourcepacks/{k}'
                            dst = f'mods/{MOD_NAME}/resourcepacks/{k}'
                            if os.path.isdir(src):
                                shutil.copytree(src, dst)

                            elif k.lower().endswith(".zip"):
                                with zipfile.ZipFile(src, "r") as z:
                                    z.extractall(dst)
                    try:structures = choose_select({
                        _:['No','Yes'] for _ in os.listdir(f'downloads/{dir_name}/generated/minecraft/structure')
                    }, title='Select the structures you want to export', return_index=True).items()
                    except:structures = {}
                    for k,v in structures:
                        if v:
                            shutil.copy(f'downloads/{dir_name}/generated/minecraft/structure/{k}',f'mods/{MOD_NAME}/structures/{k}')
                    structure = None
                    while structure != '\x1b[?9999hQuit...':
                        structure = choose([
                            k for k,v in structures if v
                        ] + ['\x1b[?9999hQuit...'], title='Select a structure to enter place mode')
                        if structure != '\x1b[?9999hQuit...':
                            try:
                                parts = custom_input(
                                    f'Placing "{structure}"... Enter origin coords {Effect.DIM}<x> <y> <z>{Effect.OFF}'
                                ).split()

                                if len(parts) != 3:
                                    print("Please enter exactly 3 coordinates.")
                                    time.sleep(2)
                                    continue

                                x, y, z = map(int, parts)
                                
                                with open(f'mods/{MOD_NAME}/placing.json','r',encoding='utf-8') as file:placing = json.load(file)
                                placing.append({
                                    'structure':structure,
                                    'pos':[x,y,z]
                                })
                                with open(f'mods/{MOD_NAME}/placing.json','w',encoding='utf-8') as file:json.dump(placing, file)

                            except ValueError:
                                print("Coordinates must be integers.")
                                time.sleep(2)
                    
                    def zipdir(path, ziph):
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                ziph.write(os.path.join(root, file), 
                                        os.path.relpath(os.path.join(root, file), 
                                                        os.path.join(path, '..')))

                    with zipfile.ZipFile(f'mods/{MOD_NAME}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                        zipdir(f'mods/{MOD_NAME}', zipf)
                    
                    shutil.rmtree(f'mods/{MOD_NAME}')
                    os.rename(f'mods/{MOD_NAME}.zip',f'mods/{MOD_NAME}.dscmod')

                    print(f'The mod was created successfully. Check {Color.GREEN}"mods/{MOD_NAME}.dscmod"{Effect.OFF}')
                case 'Import mod':
                    DIR_NAME = choose([
                        _ for _ in os.listdir('downloads') if os.path.isdir(f'downloads/{_}') and _ != '.temp'
                    ], title='Please, select a release')
                    if DIR_NAME is None:
                        print('No releases are installed. Please install at least one to continue.')
                        exit(0)
                    MOD_PATH = choose([
                        mod for mod in os.listdir('mods') if pathlib.Path(f'mods/{mod}').suffix == '.dscmod'
                    ],title='Please, select a mod')
                    MOD_PATHF = '.'.join(MOD_PATH.split('.')[:-1])
                    if choose([
                        'Abort',
                        'Continue'
                    ],title='Are you sure you want to continue? These changes cannot be undone') == 'Abort':
                        print('Aborting...')
                        exit(0)
                    def try_create_folder(dir):
                        if not os.path.exists(dir):os.mkdir(dir)
                    
                    print('Creating mod directory... ',end='')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/minecraft')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/minecraft/tags')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/minecraft/tags/function')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/function')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/structure')
                    try_create_folder(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/tags')
                    print(' [DONE]')
                    with open(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/pack.mcmeta','w',encoding='utf-8') as file:json.dump({
                        "pack": {
                            "pack_format": 61,
                            "description": "§bDescendant-Atlas§f is an advanced modloader for §cDescendant+§f made by §aMikequez12"
                        }
                    },file)
                    with open(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/minecraft/tags/function/load.json','w',encoding='utf-8') as file:
                        json.dump({"values":["descendant-atlas:update","descendant-atlas:load"]},file)
                    
                    print('Importing mods:')
                    with zipfile.ZipFile(f'mods/{MOD_PATH}', 'r') as zip_ref:
                        zip_ref.extractall(f'mods/.temp')
                    try:structs = os.listdir(f'mods/.temp/{MOD_PATHF}/structures')
                    except:structs = []
                    for structure in structs:
                        if os.path.isdir(f'mods/.temp/{MOD_PATHF}/structures/{structure}'):continue
                        print(f'    Importing structure "{structure}"... ',end='')
                        path = f'mods/.temp/{MOD_PATHF}/structures/{structure}'
                        try:
                            os.rename(path,f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/structure/{structure}')
                        except FileExistsError:
                            print('[ERROR] File already exists')
                        else:
                            print('[DONE]')
                    try:dataps = os.listdir(f'mods/.temp/{MOD_PATHF}/datapacks')
                    except:dataps = []
                    for datapack in dataps:
                        if os.path.isfile(f'mods/.temp/{MOD_PATHF}/datapacks/{datapack}'):continue
                        print(f'    Importing datapack "{datapack}"... ',end='')
                        try:
                            shutil.move(f'mods/.temp/{MOD_PATHF}/datapacks/{datapack}',f'downloads/{DIR_NAME}/datapacks/{datapack}')
                        except FileExistsError:
                            print('[ERROR] File already exists')
                        else:
                            print('[DONE]')
                    

                    try:
                        resources_zip = zipfile.ZipFile(f"downloads/{DIR_NAME}/resources.zip", "a", compression=zipfile.ZIP_DEFLATED)
                        ress = os.listdir(f"mods/.temp/{MOD_PATHF}/resourcepacks")
                    except:
                        ress = []
                        resources_zip = None

                    for resourcepack in ress:
                        pack_path = pathlib.Path(f"mods/.temp/{MOD_PATHF}/resourcepacks/{resourcepack}")

                        if not pack_path.is_dir():
                            continue

                        print(f'    Importing resourcepack "{resourcepack}"... ', end="")

                        try:
                            for file in pack_path.rglob("*"):
                                if file.is_file():
                                    arcname = file.relative_to(pack_path)  # elimina la carpeta raíz
                                    resources_zip.write(file, arcname)

                        except Exception as e:
                            print(f"[ERROR] {e}")
                        else:
                            print("[DONE]")

                    if resources_zip is not None:
                        resources_zip.close()


                    with open(f'mods/.temp/{MOD_PATHF}/placing.json','r',encoding='utf-8') as file:
                        placing = json.load(file)
                    CODE = str(uuid.uuid4().hex)
                    with open(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/function/update.mcfunction','w',encoding='utf-8') as file:
                        file.write('''
execute unless entity @e[type=minecraft:armor_stand,tag=descendant-atlas] run summon minecraft:armor_stand 0 0 0 {Invisible:1b,Marker:1b,Small:1b,Tags:[descendant-atlas]}
execute unless entity @e[type=minecraft:armor_stand,tag=descendant-atlas,tag='''+CODE+'''] run tellraw @a [{text:"[Descendant-Atlas]",color:aqua}," ",{color:white,text:"New patch applied.\\n"},{color:gray,text:"-------------------------------\\n"},{color:white,text:"Version ID: "},{text:"'''+CODE+'''",color:green}]
'''+'\n'.join([
    f'execute unless entity @e[type=minecraft:armor_stand,tag=descendant-atlas,tag={CODE}] run place template descendant-atlas:{".".join(_.get("structure").split(".")[:-1])} {" ".join(map(str,_.get("pos")))}' for _ in placing
])+'''
execute unless entity @e[type=minecraft:armor_stand,tag=descendant-atlas,tag='''+CODE+'''] as @e[type=minecraft:armor_stand,tag=descendant-atlas] run data merge entity @s {Tags:["descendant-atlas","'''+CODE+'''"]}
''')
                    with open(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/function/load.mcfunction','w',encoding='utf-8') as file:file.write('# Couldn\'t generate load.mcfunction')
                        
                    print('Applying patches...',end='')
                    try:
                        with open(f'downloads/{DIR_NAME}/datapacks/sddf_Datapack/data/minecraft/tags/function/load.json','r',encoding='utf-8') as file:
                            LOAD = json.load(file)
                        os.remove(f'downloads/{DIR_NAME}/datapacks/sddf_Datapack/data/minecraft/tags/function/load.json')
                        with open(f'downloads/{DIR_NAME}/datapacks/descendant-atlas/data/descendant-atlas/function/load.mcfunction','w',encoding='utf-8') as file:
                            file.write('\n'.join([
                                f'function {func}' for func in LOAD.get('values')
                            ]))
                    except Exception as err:print(f' [DONE*]')
                    else:print(' [DONE]')

                    shutil.rmtree(f'mods/.temp/'+MOD_PATHF)

                    os.rename(f'downloads/{DIR_NAME}',f'downloads/{DIR_NAME} (modded)')
                    
                    print(f'The mod was applied successfully.')