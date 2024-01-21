"""

    Main archive of Crimson Launcher v1.0 by @devcheckog

"""

"""

MIT License

Copyright (c) 2024 DevCheck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import os
import json
import getpass
import platform
import shutil
import sys
from typing import List, Literal
import webbrowser
import minecraft_launcher_lib
import psutil
import jdk
import customtkinter
import tkinter
import signal
from PIL import Image
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
from utils import check_internet
from constants import constants

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal.SIG_IGN)

    if not platform.platform().startswith('Windows'):
        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'Sistema operativo incompatible.', type= 'ok')
        raise RuntimeError('Sistema operativo incompatible.')

    class CrimsonLauncher:

        def __init__(self, user : str) -> None:

            self.BASE_PATH : str = f'C:/Users/{user}/AppData/Roaming/'
            self.PATH : str = f'C:/Users/{user}/AppData/Roaming/.crimson/'
            self.CRIMSON_BACKGROUND : ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 10, thread_name_prefix= 'Crimson Background Process')
            self.USER : str = user
            self.RAM_TOTAL : int  = round(0.65 * psutil.virtual_memory().total / (1024 ** 2))
            self.RAM_ASSIGNED : int = 500
            self.PATH_ASSETS : str = os.getcwd().replace('\\', '/') + '/assets'
            self.COLOR : str = '#333333'
            self.MINECRAFT_VANILLA_RELEASES : List[str] = [version['id'] for version in minecraft_launcher_lib.utils.get_version_list() if version['type'] == 'release']
            self.MINECRAFT_VANILLA_SNAPSHOTS : List[str] = [version['id'] for version in minecraft_launcher_lib.utils.get_version_list() if version['type'] == 'snapshot']
            self.FABRIC_RELEASES : List[str] = [version['version'] for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version['stable'] == True]
            self.FABRIC_SNAPSHOTS : List[str] = [version['version'] for version in minecraft_launcher_lib.fabric.get_all_minecraft_versions() if version['stable'] == False]
            self.QUILT_RELEASES : List[str] = [version['version'] for version in minecraft_launcher_lib.quilt.get_all_minecraft_versions() if version['stable'] == True]
            self.QUILT_SNAPSHOTS : List[str] = [version['version'] for version in minecraft_launcher_lib.quilt.get_all_minecraft_versions() if version['stable'] == False]
            self.VERSIONS_LIST : List[str] = []
            self.JAVA_CURRENT : str = ''
            self.OPEN_OR_CLOSE : bool = False
            self.JAVA_LIST : List[str] = []

            self.checker()

        def java(self, version : Literal['17', '8']) -> None:

            try:
                jdk.install(version= version, operating_system= jdk.OperatingSystem.WINDOWS, path= self.PATH + 'Java/', arch= jdk.Architecture.X64)
                messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'Java {version} instalado correctamente.', type = 'ok')

            except:    
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No se logró instalar Java {version} correctamente.')
                raise RuntimeError(f'No se instaló correctamente Java {version}')    

        def checker(self) -> None:

            internet : bool = check_internet()

            if internet == False:
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'No hay conexión a internet.', type= 'ok')
                self.CRIMSON_BACKGROUND.shutdown()
                raise RuntimeError('No hay conexión a internet.')

            elif not os.path.exists(self.BASE_PATH):
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No existe la ruta principal de programas {self.BASE_PATH}.', type= 'ok')
                self.CRIMSON_BACKGROUND.shutdown(cancel_futures= True)
                raise RuntimeError(f'No existe la ruta principal {self.BASE_PATH}')
            
            elif not os.path.exists(self.PATH):
                os.mkdir(self.BASE_PATH + '.crimson')
                os.mkdir(self.BASE_PATH + '.crimson/Crimson Settings')
                os.mkdir(self.BASE_PATH + '.crimson/Java')
                
                if not os.path.exists(self.PATH + 'Crimson Settings/config.json'):
                    with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:
                        json.dump({
                            'accounts' : {},
                            'java' : {
                                'path' : None,
                            },
                            'launcher settings' : {
                                'close_on_start' : False,
                                'ram_asigned' : 1000
                            }
                        }, write, indent= 5)

                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        config = json.load(read)
                        self.RAM_ASSIGNED = config['launcher settings']['ram_asigned']      

                if not os.path.exists(self.PATH + 'launcher_profiles.json'):
                    with open(self.PATH + 'launcher_profiles.json', 'w') as write:
                        json.dump({
                            'profiles' : {},                  
                            'settings': {
                                'enableAdvanced': False,
                                'profileSorting': 'byName'
                            },
                            'version': 3
                        }, write, indent= 5)

                self.CRIMSON_BACKGROUND.submit(self.java, '17')
                self.start()

            else:

                if not os.path.exists(self.PATH + 'Java/'):
                    messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No existe la carpeta principal de Java {self.PATH}.', type= 'ok')
                    self.CRIMSON_BACKGROUND.shutdown()
                    raise RuntimeError(f'No existe la carpeta principal de Java {self.PATH}.')
                
                if not os.path.exists(self.PATH + 'Crimson Settings/config.json'):
                    with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:
                        json.dump({
                            'accounts' : {},
                            'java' : {
                                'path' : None,
                            },
                            'launcher settings' : {
                                'close_on_start' : False,
                                'ram_asigned' : 1000
                            }
                        }, write, indent= 5)

                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        config = json.load(read)
                        self.RAM_ASSIGNED = config['launcher settings']['ram_asigned']      

                if not os.path.exists(self.PATH + 'launcher_profiles.json'):
                    with open(self.PATH + 'launcher_profiles.json', 'w') as write:
                        json.dump({
                            'profiles' : {},                  
                            'settings': {
                                'enableAdvanced': False,
                                'profileSorting': 'byName'
                            },
                            'version': 3
                        }, write, indent= 5)

                with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                    config = json.load(read)
                    self.RAM_ASSIGNED = config['launcher settings']['ram_asigned']            

                jdks : List[str] = [java for java in os.listdir(self.PATH + 'Java/') if java.startswith('jdk-17') or java.startswith('jdk-8')]

                if len(jdks) == 0:
                    self.CRIMSON_BACKGROUND.submit(self.java, '17')

                else:

                    for java in jdks:

                        if not os.path.exists(self.PATH + f'Java/{java}/bin/java.exe'):
                            
                            if java.startswith('jdk-17'):  
                                shutil.rmtree(path= self.PATH + f'Java/{java}',ignore_errors= True)
                                self.CRIMSON_BACKGROUND.submit(self.java, '17')
                                break

                            elif java.startswith('jdk-8'):    
                                shutil.rmtree(path= self.PATH + f'Java/{java}',ignore_errors= True)
                                self.CRIMSON_BACKGROUND.submit(self.java, '8')
                                break

                self.start()

        def start(self) -> None:

            def terminate_start_window() -> None:

                StartWindowLoadBar.stop()
                StartWindow.quit()
                StartWindow.withdraw()

                return self.main()

            StartWindow : customtkinter.CTk = customtkinter.CTk()   
            StartWindow.title(f'Crimson Launcher - {constants.VERSION.value}')
            StartWindow.config(bg= self.COLOR)
            StartWindow.resizable(False, False)
            StartWindow.geometry('580x620')
            StartWindow.wm_iconbitmap(f'{self.PATH_ASSETS}/logo.ico')
            StartWindow.wm_protocol('WM_DELETE_WINDOW', terminate_start_window)

            StartWindowImage : customtkinter.CTkLabel = customtkinter.CTkLabel(
                StartWindow,
                text= None,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/logo.png'), size= (256, 256)),
                bg_color= 'transparent',
                fg_color= self.COLOR 
            )
            StartWindowImage.pack_configure(anchor= 'center', pady= 100)
            
            StartWindowLoadBar : customtkinter.CTkProgressBar = customtkinter.CTkProgressBar(
                StartWindow,
                corner_radius= 20,
                progress_color= '#0077ff',
                orientation= 'horizontal',
                mode= 'indeterminate',
                height= 30,
                width= 300,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                indeterminate_speed= 1.2
            )
            StartWindowLoadBar.place_configure(relx= 0.2_5, rely= 0.8)
            StartWindowLoadBar.start()

            StartWindow.after(300, terminate_start_window)
            StartWindow.mainloop()

        def main(self) -> None:

            def terminate_home_window() -> None:
                
                HomeWindow.quit()
                HomeWindow.withdraw()

                return self.terminate()
            
            def discord() -> None:

                webbrowser.open_new_tab(constants.DISCORD.value)
                return

            def github() -> None:

                webbrowser.open_new_tab(constants.GITHUB.value)   
                return

            def paypal() -> None:

                webbrowser.open_new_tab(constants.PAYPAL.value)  
                return
            
            def open_or_close() -> None:

                self.OPEN_OR_CLOSE = OpenOrClose.get()

                if self.OPEN_OR_CLOSE:

                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        
                        config = json.load(read)
                        config['launcher settings']['close_on_start'] = True

                    with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                        json.dump(config, write, indent= 5)    

                    messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'El launcher se va cerrar cuando el juego se inicie.', type= 'ok', parent= HomeWindow)
                    return
                
                with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        
                    config = json.load(read)
                    config['launcher settings']['close_on_start'] = False

                with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                    json.dump(config, write, indent= 5)    
                
                messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'El launcher se mantendra abierto cuando el juego se inicie.', type= 'ok', parent= HomeWindow)
                return
            
            def launch() -> None:

                VersionsAndMods.configure(state= 'normal')
                Launch.configure(state= 'disabled')
                Accounts.configure(state= 'normal')

                for name in FrameDecorationCenter.children.items():

                    if isinstance(name[1], customtkinter.CTkButton):

                        name[1].place_forget()
                        continue

                    if isinstance(name[1], customtkinter.CTkLabel):

                        name[1].place_forget()
                        continue

                    if isinstance(name[1], customtkinter.CTkSwitch):

                        name[1].place_forget()
                        continue

                    if isinstance(name[1], customtkinter.CTkOptionMenu):

                        name[1].place_forget()
                        continue   

                LaunchTitle.place_configure(relx= 0.0_4, rely= 0.2_7, anchor= 'sw')  
                LaunchVersion.place_configure(relx= 0.0_5, rely= 0.5_0, anchor= 'sw')
                OptimizationTitle.place_configure(relx= 0.9_5, rely= 0.2_7, anchor= 'se')
                OptimizeJavaArgs.place_configure(relx= 0.9, rely= 0.4_4, anchor= 'se')
                OpenOrClose.place_configure(relx= 0.9_2, rely= 0.6_0, anchor= 'se')
                JavaTitle.place_configure(relx= 0.3_5, rely= 0.2_7, anchor= 'sw')
                SelectJavaVersion.place_configure(relx= 0.3_6, rely= 0.5_0, anchor= 'sw')

                # Versions

                self.VERSIONS_LIST.clear()

                if not os.path.exists(self.PATH + 'versions/') or not len(os.listdir(self.PATH + 'versions/')) == 0 and len(self.VERSIONS_LIST) == 1:
                    
                    self.VERSIONS_LIST.insert(0, 'No hay versiones instaladas.')

                else:

                    for name in os.listdir(self.PATH + 'versions/'):

                        self.VERSIONS_LIST.append(name)  

                LaunchVersion.configure(values= self.VERSIONS_LIST)        

                if self.VERSIONS_LIST[0] == 'No hay versiones instaladas.':

                    LaunchVersion.configure(state= 'disabled')   

                # Java     
                    
                self.JAVA_LIST.clear()

                if not os.path.exists(self.PATH + 'Java/') or len(os.listdir(self.PATH + 'Java/')) == 0:

                    self.JAVA_LIST.insert(0, 'No hay versiones instaladas en las librerías locales.')

                for java_local in os.listdir(self.PATH + 'Java/'):    

                    if os.path.exists(self.PATH + 'Java/' + java_local + '/bin/java.exe'):

                        self.JAVA_LIST.append(self.PATH + 'Java/' + java_local + '/bin/java.exe')

                for java_system in ['C:/Program Files/' + folder for folder in os.listdir('C:/Program Files/') if folder.find('.') == -1]:

                    try:

                        for java in [f'/{jdk}' for jdk in os.listdir(java_system) if jdk.find('jdk') != -1 or jdk.find('java') != -1]:

                            if os.path.exists(java_system + java + '/bin/java.exe'):

                                self.JAVA_LIST.append(java_system + java + '/bin/java.exe')

                    except:

                        pass              

                if len(self.JAVA_LIST) <= 1 and self.JAVA_LIST[0] == 'No hay versiones instaladas en las librerías locales.':

                    SelectJavaVersion.configure(state= 'disabled')       
                
            def versions_and_mods() -> None:

                def fabricmc() -> None:

                    webbrowser.open_new_tab(constants.FABRICMC.value)
                    return
                
                def quilt() -> None:

                    webbrowser.open_new_tab(constants.QUILT.value)
                    return

                VersionsAndMods.configure(state= 'disabled')
                Launch.configure(state= 'normal')

                for name in FrameDecorationCenter.children.items():

                    if isinstance(name[1], customtkinter.CTkButton):

                        name[1].place_forget()
                        continue

                    if isinstance(name[1], customtkinter.CTkLabel):

                        name[1].place_forget()
                        continue

                    if isinstance(name[1], customtkinter.CTkSwitch):

                        name[1].place_forget()
                        continue

                    if isinstance(name[1], customtkinter.CTkOptionMenu):

                        name[1].place_forget()
                        continue   

                InstallVanillaVersion : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Vanilla',
                    compound= 'left',
                    font= ('Roboto', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/vanilla.png'), size= (96, 96))

                )
                InstallVanillaVersion.place_configure(relx= 0.0_6, rely= 0.2_7, anchor= 'sw')  

                SelectVanillaReleaseVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('Roboto', 15),
                    dropdown_font= ('Roboto', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.MINECRAFT_VANILLA_RELEASES
                )
                SelectVanillaReleaseVersion.place_configure(relx= 0.0_7, rely= 0.5_1, anchor= 'sw')
                
                SelectVanillaSnapshotVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('Roboto', 15),
                    dropdown_font= ('Roboto', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.MINECRAFT_VANILLA_SNAPSHOTS
                )
                SelectVanillaSnapshotVersion.place_configure(relx= 0.0_7, rely= 0.7_5, anchor= 'sw')

                InstallFabricVersion : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Fabric',
                    compound= 'left',
                    font= ('Roboto', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/fabric.png'), size= (96, 96))

                )
                InstallFabricVersion.place_configure(relx= 0.3_9, rely= 0.2_7, anchor= 'sw')

                SelectFabricReleaseVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('Roboto', 15),
                    dropdown_font= ('Roboto', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.FABRIC_RELEASES
                )
                SelectFabricReleaseVersion.place_configure(relx= 0.4, rely= 0.5_1, anchor= 'sw')

                SelectFabricSnapshotVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('Roboto', 15),
                    dropdown_font= ('Roboto', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.FABRIC_SNAPSHOTS
                )
                SelectFabricSnapshotVersion.place_configure(relx= 0.4, rely= 0.7_5, anchor= 'sw')

                FabricMC : customtkinter.CTkButton = customtkinter.CTkButton(
                    FrameDecorationCenter,
                    corner_radius= 20,
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/fabric.png'), size= (26, 26)),
                    height= 40,
                    font= ('Roboto', 15),
                    text_color= 'white',
                    text= 'FabricMC',
                    command= fabricmc,
                    compound= 'left',
                    hover= False
                )
                FabricMC.place_configure(relx= 0.4_3, rely= 0.8_8, anchor= 'sw')

                InstallQuiltVersion : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Quilt',
                    compound= 'left',
                    font= ('Roboto', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/quilt.png'), size= (96, 96))

                )
                InstallQuiltVersion.place_configure(relx= 0.7_3, rely= 0.2_7, anchor= 'sw')

                SelectQuiltReleaseVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('Roboto', 15),
                    dropdown_font= ('Roboto', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.QUILT_RELEASES
                )
                SelectQuiltReleaseVersion.place_configure(relx= 0.7_4, rely= 0.5_1, anchor= 'sw')

                SelectQuiltSnapshotVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('Roboto', 15),
                    dropdown_font= ('Roboto', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.QUILT_SNAPSHOTS
                )
                SelectQuiltSnapshotVersion.place_configure(relx= 0.7_4, rely= 0.7_5, anchor= 'sw')

                Quilt : customtkinter.CTkButton = customtkinter.CTkButton(
                    FrameDecorationCenter,
                    corner_radius= 20,
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/quilt.png'), size= (26, 26)),
                    height= 40,
                    font= ('Roboto', 15),
                    text_color= 'white',
                    text= 'Quilt',
                    command= quilt,
                    compound= 'left',
                    hover= False
                )
                Quilt.place_configure(relx= 0.7_7, rely= 0.8_8, anchor= 'sw')

            HomeWindow : customtkinter.CTkToplevel = customtkinter.CTkToplevel()
            HomeWindow.title(f'Crimson Launcher - {constants.VERSION.value}')
            HomeWindow.config(bg= self.COLOR)
            HomeWindow.after(300, HomeWindow.iconbitmap, f'{self.PATH_ASSETS}/logo.ico')
            HomeWindow.geometry('1290x720')
            HomeWindow.minsize(1290, 720)
            HomeWindow.maxsize(1920, 1080)
            HomeWindow.protocol('WM_DELETE_WINDOW', terminate_home_window)

            CanvasLogo : customtkinter.CTkLabel = customtkinter.CTkLabel(
                HomeWindow,
                text= None,
                fg_color= self.COLOR,
                image=  customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/logo.png'), size= (160, 160)),
                bg_color= self.COLOR
            )
            CanvasLogo.place_configure(relx= 0.0_2, rely= 0.0_4, anchor= 'nw')

            Discord : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/discord.png'), size= (96, 96)),
                height= 35,
                text= None,
                command= discord
            )
            Discord.place_configure(relx= 0.99, rely= 0.0_8, anchor= 'ne')

            Github : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/github.png'), size= (96, 96)),
                height= 35,
                text= None,
                command= github
            )
            Github.place_configure(relx= 0.99, rely= 0.4_8, anchor= 'e')

            Donate : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/donate.png'), size= (96, 96)),
                height= 35,
                text= None,
                command= paypal
            )
            Donate.place_configure(relx= 0.99, rely= 0.8_8, anchor= 'se')

            VersionsAndMods : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 37,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Versiones y Mods',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/download.png'), size= (22, 22)),
                compound= 'left',
                font= ('Roboto', 15),
                border_width= 2,
                border_color= '#70ceff',
                command= versions_and_mods
            )
            VersionsAndMods.place_configure(relx= 0.2_5, rely= 0.1, anchor= 'n')

            Launch : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 37,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Lanzar',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/config.png'), size= (22, 22)),
                compound= 'left',
                font= ('Roboto', 15),
                border_width= 2,
                border_color= '#70ceff',
                command= launch
            )
            Launch.place_configure(relx= 0.5, rely= 0.1, anchor= 'n')

            Launch.configure(state= 'disabled')

            Accounts : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 37,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Cuentas',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/account.png'), size= (22, 22)),
                compound= 'left',
                font= ('Roboto', 15),
                border_width= 2,
                border_color= '#70ceff'
            )
            Accounts.place_configure(relx= 0.7_5, rely= 0.1, anchor= 'n')

            FrameDecorationCenter : customtkinter.CTkFrame = customtkinter.CTkFrame(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= '#232323',
                border_color= '#0077ff',
                border_width= 2
            )
            FrameDecorationCenter.place_configure(relx= 0.09, rely= 0.9_1, anchor= 'sw', relheight= 0.6_3, relwidth= 0.7_2)

            LaunchTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                FrameDecorationCenter,
                text= ' Lanzar',
                compound= 'left',
                font= ('Roboto', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/launch.png'), size= (96, 96))
            )
            LaunchTitle.place_configure(relx= 0.0_4, rely= 0.2_7, anchor= 'sw')

            if not os.path.exists(self.PATH + 'versions/') or len(os.listdir(self.PATH + 'versions/')) == 0:
                self.VERSIONS_LIST.insert(0, 'No hay versiones instaladas.')

            else:

                for name in os.listdir(self.PATH + 'versions/'):

                    self.VERSIONS_LIST.append(name)    

            LaunchVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                FrameDecorationCenter,
                height= 40,
                corner_radius= 20,
                bg_color= '#232323',
                font= ('Roboto', 15),
                dropdown_font= ('Roboto', 15),
                dynamic_resizing= False,
                text_color= 'white',
                dropdown_fg_color= '#232323',
                dropdown_text_color= 'white',
                width= 210,
                fg_color= '#0077ff', 
                button_color= '#0077ff',
                values= self.VERSIONS_LIST
            )
            LaunchVersion.place_configure(relx= 0.0_5, rely= 0.5_0, anchor= 'sw')

            if self.VERSIONS_LIST[0] == 'No hay versiones instaladas.':

                LaunchVersion.configure(state= 'disabled')

            JavaTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                FrameDecorationCenter,
                text= ' Java',
                compound= 'left',
                font= ('Roboto', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/java.png'), size= (96, 96))
            )
            JavaTitle.place_configure(relx= 0.3_5, rely= 0.2_7, anchor= 'sw')

            if not os.path.exists(self.PATH + 'Java/') or len(os.listdir(self.PATH + 'Java/')) == 0:
                self.JAVA_LIST.insert(0, 'No hay versiones instaladas en las librerías locales.')

            for java_local in os.listdir(self.PATH + 'Java/'):    

                if os.path.exists(self.PATH + 'Java/' + java_local + '/bin/java.exe'):
                    self.JAVA_LIST.append(self.PATH + 'Java/' + java_local + '/bin/java.exe')

            for java_system in ['C:/Program Files/' + folder for folder in os.listdir('C:/Program Files/') if folder.find('.') == -1]:

                try:

                    for java in [f'/{jdk}' for jdk in os.listdir(java_system) if jdk.find('jdk') != -1 or jdk.find('java') != -1]:

                        if os.path.exists(java_system + java + '/bin/java.exe'):

                            self.JAVA_LIST.append(java_system + java + '/bin/java.exe')

                except:

                    pass            

            SelectJavaVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                FrameDecorationCenter,
                height= 40,
                corner_radius= 20,
                bg_color= '#232323',
                font= ('Roboto', 15),
                dropdown_font= ('Roboto', 15),
                dynamic_resizing= False,
                text_color= 'white',
                dropdown_fg_color= '#232323',
                dropdown_text_color= 'white',
                width= 210,
                fg_color= '#0077ff', 
                button_color= '#0077ff',
                values= self.JAVA_LIST
            )
            SelectJavaVersion.place_configure(relx= 0.3_6, rely= 0.5_0, anchor= 'sw')

            if len(self.JAVA_LIST) <= 1 and self.JAVA_LIST[0] == 'No hay versiones instaladas en las librerías locales.':

                SelectJavaVersion.configure(state= 'disabled')

            OptimizationTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                FrameDecorationCenter,
                text= ' Optimización',
                compound= 'left',
                font= ('Roboto', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.PATH_ASSETS}/optimize.png'), size= (96, 96))

            )
            OptimizationTitle.place_configure(relx= 0.9_5, rely= 0.2_7, anchor= 'se')

            OptimizeJavaArgs : customtkinter.CTkSwitch = customtkinter.CTkSwitch(
                FrameDecorationCenter,
                text= ' Optimizar Java',
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#0077ff',
                font= ('Roboto', 18),
                onvalue= True,
                offvalue= False,
                button_color= 'white',
                button_hover_color= 'white',
                progress_color= '#70ceff',
                height= 60,
				width= 100
            ) 
            OptimizeJavaArgs.place_configure(relx= 0.9, rely= 0.4_4, anchor= 'se')

            OpenOrClose : customtkinter.CTkSwitch = customtkinter.CTkSwitch(
                FrameDecorationCenter,
                text= 'Abrir o cerrar al iniciar',
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#0077ff',
                font= ('Roboto', 18),
                onvalue= True,
                offvalue= False,
                button_color= 'white',
                button_hover_color= 'white',
                progress_color= '#70ceff',
                height= 60,
				width= 100,
                command= open_or_close
            ) 
            OpenOrClose.place_configure(relx= 0.9_2, rely= 0.6_0, anchor= 'se')

            with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:
                        
                config = json.load(read)

                if config['launcher settings']['close_on_start'] == True:
                    self.OPEN_OR_CLOSE = True
                    OpenOrClose.select()

                else:    
                    OpenOrClose.deselect()  
        
            HomeWindow.mainloop()
            
        def terminate(self) -> None:

            self.CRIMSON_BACKGROUND.shutdown()
            sys.exit(0)

    def get_user() -> str:

        USER : str = ''
        USERS_PATH : str = 'C:/Users'

        if not os.path.exists(USERS_PATH):
            messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No existe la carpeta {USERS_PATH} del sistema.', type= 'ok')
            raise RuntimeError(f'No existe la carpeta {USERS_PATH} del sistema.')
        
        for user in [username for username in os.listdir('C:/Users') if username.find('.') == -1 and username == 'ingke' or username == getpass.getuser() or username == getpass.getuser().lower()]:

            if os.path.exists(f'C:/Users/{user}/AppData/Roaming/'):
                USER = user
                break

        return USER
    
    CrimsonLauncher(get_user())
    
    sys.exit(0)
