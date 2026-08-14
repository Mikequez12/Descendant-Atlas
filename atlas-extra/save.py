from colorist import Color, Effect
import os
import sys
import zipfile
import nbtlib
import json
import gzip
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tui import choose, custom_input
from utils import ansi_supported

with open('config.json','r',encoding='utf-8') as file:
    CONFIG = json.load(file)


if (not ansi_supported) or CONFIG.get('.ansi-ldm',False):
    print('ERROR: This terminal doesn\'t support ANSI codes. Atlas has a simple system that tries to get rid of ANSI by default.')
    if input('Do you want to enable it [Y/N]? ').upper() in ['YES','Y','1','ACCEPT','OK']:
        from utils import Color, Effect, Console
    else:
        print('Aborting...')
        exit(0)

if __name__ == '__main__':
    print(f'{Color.YELLOW}WARNING: {Color.OFF}Make sure {Color.BLUE}Atlas-Extra{Color.OFF} was correctly installed in both worlds and you have used the save command in the old world.\n')

    class AtlasWorld:
        def __init__(self,input_text:str=None,path:str=None,relative_paths=None,requires_save_file=False,relative_path_index=0): # thanks to z.c58 for reporting the bug on macOS
            if path is not None:
                self.world_path = path
            else:
                self.world_path = custom_input(input_text,accept=lambda value:os.path.exists(value),error_msg='The directory doesn\'t exist')

            self.save_file_required = requires_save_file

            if relative_paths is None:
                relative_paths = {'standard':'data/atlas-extra/command_storage.dat','side':'data/command_storage_atlas-extra.dat'}

            self.relative_paths = relative_paths
            self.relative_path_index = relative_path_index

            while True:
                if self.extract_data():
                    break

        @property
        def relative_path(self) -> str:
            return list(self.relative_paths.values())[self.relative_path_index]
        
        def extract_data(self) -> bool:
            if self.relative_path_index >= len(self.relative_paths):
                print(
                    f"{Color.YELLOW}WARNING:{Color.OFF} "
                    "No exported save data was found in this world."
                )
                exit(0)
            relative_path_name, relative_path = list(self.relative_paths.items())[self.relative_path_index]
            if os.path.isfile(self.world_path):
                if zipfile.is_zipfile(self.world_path):
                    with zipfile.ZipFile(self.world_path) as z:
                        self.storage_structure = None
                        if relative_path in z.namelist():
                            if 'generated/atlas-extra/structure/save.nbt' in z.namelist():
                                with z.open('generated/atlas-extra/structure/save.nbt','r') as file:
                                    self.storage_structure = file.read()
                            self.save_file = z.open(relative_path,"rb")
                        elif self.save_file_required:
                            print(f'(*) Not found using "{relative_path_name}" path, checking other paths...')
                            self.relative_path_index += 1
                            return False # Error -> Retry
                        else:
                            nbt = nbtlib.File({
                                "data": nbtlib.Compound({
                                    "contents": nbtlib.Compound({})
                                })
                            })

                            buffer = io.BytesIO()

                            with gzip.GzipFile(fileobj=buffer, mode="wb") as gz:
                                nbt.write(gz)

                            with zipfile.ZipFile(self.world_path, "a") as z:
                                z.writestr(relative_path, buffer.getvalue())
                            
                            self.save_file = z.open(relative_path,"rb")
                else:
                    print(f'{Color.RED}ERROR: {Color.OFF}The file isn\'t compatible with this app. Needs to be a folder or a .zip.')
                    exit(0)
            else:
                os.makedirs(f'{self.world_path}/data/atlas-extra',exist_ok=True)
                if os.path.exists(f'{self.world_path}/{relative_path}'):
                    self.storage_structure = None
                    if os.path.exists(f'{self.world_path}/generated/atlas-extra/structure/save.nbt'):
                        with open(f'{self.world_path}/generated/atlas-extra/structure/save.nbt','rb') as file:
                            self.storage_structure = file.read()
                    self.save_file = open(f"{self.world_path}/{relative_path}","rb")
                elif self.save_file_required:
                    print(f'(*) Not found using "{relative_path_name}" path, checking other paths...')
                    self.relative_path_index += 1
                    return False # Error -> Retry
                else:
                    nbt = nbtlib.File({
                        "data": nbtlib.Compound({
                            "contents": nbtlib.Compound({})
                        })
                    })
                    nbt.save(f"{self.world_path}/{relative_path}", gzipped=True)

                    self.save_file = open(f'{self.world_path}/{relative_path}',"rb")
            return True # Success -> Stop loop
    
    old_world = AtlasWorld(input_text=f'Path to your saved world\'s folder {Effect.DIM}(Example: %APPDATA%/.minecraft/saves/my-old-descendant-world){Effect.OFF}',requires_save_file=True)
    with old_world.save_file as f:
        with gzip.open(f, "rb") as g:
            old_nbt = nbtlib.File.parse(g)
    data = old_nbt['data']['contents']
    save_storage = False
    if old_world.storage_structure is not None:
        save_storage = choose(
            [
                'Yes',
                'No'
            ],
            title='This world includes a saved storage. Do you want to import it?' # Thanks to sdfxf31 for the help with the `storage` word
        ) == 'Yes'
    if 'save-file' not in list(data):
        print(f'{Color.RED}ERROR: {Color.OFF}This world doesn\'t have any exported save data. Please run {Color.YELLOW}/function atlas-extra:save{Effect.OFF}')
        exit(0)
    new_world = AtlasWorld(f'Path to your brand new world\'s folder {Effect.DIM}(Example: %APPDATA%/.minecraft/saves/my-new-descendant-world){Effect.OFF}',relative_path_index=old_world.relative_path_index)
    with new_world.save_file as f:
        with gzip.open(f, "rb") as g:
            new_nbt = nbtlib.File.parse(g)
        new_nbt['data']['contents']['load-save-file'] = data['save-file']
        new_nbt.save(f"{new_world.world_path}/{new_world.relative_path}", gzipped=True)

    if save_storage:
        os.makedirs(f'{new_world.world_path}/generated/atlas-extra/structure',exist_ok=True)
        os.makedirs(f'{new_world.world_path}/datapacks/atlas-extra/data/atlas-extra/functions',exist_ok=True)
        with open(f'{new_world.world_path}/generated/atlas-extra/structure/storage-saved.nbt','wb') as file:
            file.write(old_world.storage_structure)
        with open(f'{new_world.world_path}/datapacks/atlas-extra/data/atlas-extra/functions/load.mcfunction','a',encoding='utf-8') as file:
            file.write('place template atlas-extra:storage-saved 203 80 137')
    
    print(f'{Color.GREEN}Success! {Color.OFF}The save data has been moved to the new world.')