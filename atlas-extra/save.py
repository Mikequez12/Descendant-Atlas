from colorist import Color, Effect
import os
import sys
import zipfile
import nbtlib
import gzip
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tui import choose, custom_input
from utils import ansi_supported

if not ansi_supported:
    print('ERROR: This terminal doesn\'t support ANSI codes. Atlas has a simple system that tries to get rid of ANSI by default.')
    if input('Do you wanna enable it [Y/N]? ').upper() in ['YES','Y','1','ACCEPT','OK']:
        from utils import Color, Effect, Console
    else:
        print('Aborting...')
        exit(0)

if __name__ == '__main__':
    print(f'{Color.YELLOW}WARNING: {Color.OFF}Make sure {Color.BLUE}Atlas-Extra{Color.OFF} was correctly installed in the two worlds and you have used the save command in the old world.\n')

    def get_dir(t):
        path = custom_input(t,accept=lambda value:os.path.exists(value),error_msg='The directory doesn\'t exist')
        
        if os.path.isfile(path):
            if zipfile.is_zipfile(path):
                with zipfile.ZipFile(path) as z:
                    save = None
                    if 'generated/atlas-extra/structure/save.nbt' in z.namelist():
                        with z.open('generated/atlas-extra/structure/save.nbt','r') as file:
                            save = file.read()
                    return (path,z.open("data/atlas-extra/command_storage.dat","rb"),save)
            else:
                print(f'{Color:RED}ERROR: {Color.OFF}The file isn\'t compatible with this app. Needs to be a folder or a .zip.')
                exit(0)
        else:
            os.makedirs(f'{path}/data/atlas-extra',exist_ok=True)
            if not os.path.exists(f'{path}/data/atlas-extra/command_storage.dat'):
                nbt = nbtlib.File({
                    "data": nbtlib.Compound({
                        "contents": nbtlib.Compound({})
                    })
                })
                nbt.save(f"{path}/data/atlas-extra/command_storage.dat", gzipped=True)
            save = None
            if os.path.exists(f'{path}/generated/atlas-extra/structure/save.nbt'):
                with open(f'{path}/generated/atlas-extra/structure/save.nbt','rb') as file:
                    save = file.read()
            return (path,open(f"{path}/data/atlas-extra/command_storage.dat","rb"),save)
    
    p_old,f_old,s = get_dir(f'Path to your saved world\'s folder {Effect.DIM}(Example: %APPDATA%/.minecraft/saves/my-old-descendant-world){Effect.OFF}')
    with f_old as f:
        with gzip.open(f, "rb") as g:
            old_nbt = nbtlib.File.parse(g)
    data = old_nbt['data']['contents']
    S = False
    if s:
        S = choose(
            [
                'Yes',
                'No'
            ],
            title='This world includes a saved storage. Do you want to import it?' # Thanks to sdfxf31 for the help with the `storage` word
        ) == 'Yes'
    if 'save-file' not in list(data):
        print(f'{Color:RED}ERROR: {Color.OFF}This world hasn\'t exported the data to a save file, please, run {Effect.YELLOW}/function atlas-extra:save{Effect.OFF}')
        exit(0)
    p_new,f_new,s_ = get_dir(f'Path to your brand new world\'s folder {Effect.DIM}(Example: %APPDATA%/.minecraft/saves/my-new-descendant-world){Effect.OFF}')
    with f_new as f:
        with gzip.open(f, "rb") as g:
            new_nbt = nbtlib.File.parse(g)
        new_nbt['data']['contents']['load-save-file'] = data['save-file']
        new_nbt.save(f"{p_new}/data/atlas-extra/command_storage.dat", gzipped=True)

    if S:
        os.makedirs(f'{p_new}/generated/atlas-extra/structure',exist_ok=True)
        os.makedirs(f'{p_new}/datapacks/atlas-extra/data/atlas-extra/functions',exist_ok=True)
        with open(f'{p_new}/generated/atlas-extra/structure/storage-saved.nbt','wb') as file:
            file.write(s)
        with open(f'{p_new}/datapacks/atlas-extra/data/atlas-extra/functions/load.mcfunction','a',encoding='utf-8') as file:
            file.write('place template atlas-extra:storage-saved 203 80 137')
    
    print(f'{Color.GREEN}Success! {Color.OFF}The save data has been moved to the world.')