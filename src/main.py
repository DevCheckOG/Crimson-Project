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

from email import message
import os
import json
import getpass
import platform
import shutil
import sys
from typing import Callable, List, Literal, Dict
import webbrowser
import minecraft_launcher_lib
import psutil
import jdk
import customtkinter
import tkinter
import signal
import winotify
import coloredlogs
import logging
import time
from PIL import Image
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
from utils import check_internet
from constants import constants

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal.SIG_IGN)
    LOGGER = logging.getLogger(__name__)
    
    class Logging:

        def __init__(self) -> None:

            coloredlogs.install(level='DEBUG', logger= LOGGER, milliseconds= True)

        def debug(self, msg : str) -> None:

            LOGGER.debug(msg)    

        def info(self, msg : str) -> None:

            LOGGER.info(msg)   

        def warning(self, msg : str) -> None:

            LOGGER.warning(msg)

        def error(self, msg : str) -> None:

            LOGGER.error(msg)

        def critical(self, msg : str) -> None:

            LOGGER.critical(msg)   

    if not platform.platform().startswith('Windows'):
        Logging().critical(f'System not compatible.')
        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'Sistema operativo incompatible.', type= 'ok')
        sys.exit(0)                   

    class Download:

        def __init__(self, os : Literal['Windows', 'Linux'], path : str, software : Literal['Vanilla', 'Fabric', 'Quilt'], version : str, parent : customtkinter.CTkToplevel, frame_center : customtkinter.CTkFrame) -> None:

            self.os : Literal['Windows', 'Linux'] = os
            self.path : str = path

            self.os = 'Windows' if self.path.find('C:') != -1 else 'Linux'

            self.software : Literal['Vanilla', 'Fabric', 'Quilt'] = software
            self.version : str = version
            self.parent = parent
            self.frame_center = frame_center

            self.callback_dict : minecraft_launcher_lib.types.CallbackDict = {

                "setStatus": self.logging_status

            }
            
            if self.os == 'Windows' and self.software == 'Vanilla': self.download_vanilla()

            elif self.os == 'Windows' and self.software == 'Fabric': self.download_fabric()

            elif self.os == 'Windows' and self.software == 'Quilt': self.download_quilt()

        def download_vanilla(self) -> None:

            try:

                for name in self.frame_center.children.items():

                    if isinstance(name[1], customtkinter.CTkSwitch):

                        name[1].configure(state= 'disabled')
                        continue
                
                messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'Descargando la versión vanilla {self.version}...', type= 'ok', parent= self.parent)
                Logging().info(f'Downloading Vanilla version {self.version}...')

                time.sleep(3)

                minecraft_launcher_lib.install.install_minecraft_version(self.version, self.path, self.callback_dict)

            except Exception as e:

                for name in self.frame_center.children.items():

                    if isinstance(name[1], customtkinter.CTkSwitch):

                        name[1].configure(state= 'normal')
                        continue
                
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'Error al descargar la versión vanilla {self.version}.', type= 'ok', parent= self.parent)
                Logging().error(f'Error while downloading Vanilla version: {e}')

        def download_fabric(self) -> None:

            ...

        def download_quilt(self) -> None:

            ...     

        def logging_status(self, status: str) -> None:

            Logging().info(status)

    def download(os : Literal['Windows', 'Linux'], path : str, software : Literal['Vanilla', 'Fabric', 'Quilt'], version : str, parent : customtkinter.CTkToplevel, frame_center : customtkinter.CTkFrame) -> None:   

        Download(os, path, software, version, parent, frame_center)     

    class NotifierWindows:

        def __init__(self, ASSETS_PATH : str, TITLE : str, MSG : str) -> None:

            self.assets_path : str = ASSETS_PATH
            self.title : str = TITLE
            self.msg : str = MSG

            self.notify()

        def notify(self) -> None:

            notification = winotify.Notification(

                app_id= f'Crimson Launcher - {constants.VERSION.value}',
                title= self.title,
                msg= self.msg,
                icon= f'{self.assets_path}/logo.png'

            )

            Logging().debug(f'Sending notification...')

            notification.set_audio(winotify.audio.Default, loop= False)
            notification.show()

            Logging().debug(f'Notification send.')

            return

    class CrimsonLauncher:

        def __init__(self, user : str) -> None:

            Logging().debug(f'User: {user}')
            Logging().debug(f'Starting the Crimson Launcher...')

            self.BASE_PATH : str = f'C:/Users/{user}/AppData/Roaming/'
            self.PATH : str = f'C:/Users/{user}/AppData/Roaming/.crimson/'
            self.CRIMSON_BACKGROUND_THREAD_POOL : ThreadPoolExecutor = ThreadPoolExecutor(max_workers= 10, thread_name_prefix= 'Crimson Background Process')
            self.USER : str = user
            self.RAM_TOTAL : int  = round(0.65 * psutil.virtual_memory().total / (1024 ** 2))
            self.RAM_ASSIGNED : int = 500
            self.ASSETS_PATH : str = os.getcwd().replace('\\', '/') + '/assets'
            self.FONTS_PATH : str = os.getcwd().replace('\\', '/') + '/fonts'
            self.COLOR : str = '#333333'
            self.MINECRAFT_VANILLA_RELEASES : List[str] = []
            self.MINECRAFT_VANILLA_SNAPSHOTS : List[str] = []
            self.FABRIC_RELEASES : List[str] = []
            self.FABRIC_SNAPSHOTS : List[str] = []
            self.QUILT_RELEASES : List[str] = []
            self.QUILT_SNAPSHOTS : List[str] = []
            self.VERSIONS_LIST : List[str] = []
            self.JAVA_CURRENT : str = ''
            self.OPEN_OR_CLOSE : bool = False
            self.JAVA_LIST : List[str] = []
            self.ACCOUNTS_LIST : List[str] = []
            self.ACCOUNT_CURRENT : Dict[str, str] = {}

            Logging().debug(f'All variables initialized.')

            Logging().debug(f'Loading fonts...')

            try:

                customtkinter.FontManager.load_font(f'{self.FONTS_PATH}/JetBrains.ttf') 

            except Exception as e:
                
                Logging().error(f'Fatal error while loading fonts: {e}')
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'No se logro cargar las fuentes, se recomienda revisar la consola.', type= 'ok')
                self.terminate()    

            Logging().debug(f'Fonts loaded.')

            Logging().debug(f'Starting the checker...')

            self.checker()

        def java(self, version : Literal['17', '8']) -> None:

            try:
                jdk.install(version= version, operating_system= jdk.OperatingSystem.WINDOWS, path= self.PATH + 'Java/', arch= jdk.Architecture.X64)
                messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'Java {version} instalado correctamente.', type = 'ok')
                Logging().info(f'Java {version} installed, removing of the queue.')

            except:    
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No se logró instalar Java {version} correctamente.')
                Logging().error(f'Fatal error while installing Java {version}.')
                self.terminate()  

        def checker(self) -> None:

            internet : bool = check_internet()

            if internet == False:
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'No hay conexión a internet.', type= 'ok')
                self.CRIMSON_BACKGROUND_THREAD_POOL.shutdown()
                Logging().error(f'Not connected to the internet.')
                Logging().debug('Checker terminated.')
                self.terminate()

            elif not os.path.exists(self.BASE_PATH):
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No existe la ruta principal de programas {self.BASE_PATH}.', type= 'ok')
                self.CRIMSON_BACKGROUND_THREAD_POOL.shutdown(cancel_futures= True)
                Logging().error(f'The path {self.BASE_PATH} does not exist.')
                Logging().debug('Checker terminated.')
                self.terminate()
            
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

            if not os.path.exists(self.PATH + 'Java/'):
                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'No existe la carpeta principal de Java {self.PATH}.', type= 'ok')
                self.CRIMSON_BACKGROUND_THREAD_POOL.shutdown()
                Logging().error(f'The path {self.PATH} does not exist.')
                Logging().debug('Checker terminated.')
                self.terminate()
            
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

                if config['java']['path'] != None:

                    self.JAVA_CURRENT = config['java']['path']    

                for account in config['accounts'].items():

                    if account[1]['type'] == 'no_premium':

                        for name in config['accounts'].keys():

                            if name.lower() == account[0].lower():

                                self.ACCOUNTS_LIST.append(name + ' | No Premium')             

            jdks : List[str] = [java for java in os.listdir(self.PATH + 'Java/') if java.startswith('jdk-17') or java.startswith('jdk-8')]

            if len(jdks) == 0:
                self.CRIMSON_BACKGROUND_THREAD_POOL.submit(self.java, '17')
                Logging().info('Java 17 not found. Installing... (JDK in Queue)')

            else:

                for java in jdks:

                    if not os.path.exists(self.PATH + f'Java/{java}/bin/java.exe'):
                        
                        if java.startswith('jdk-17'):  
                            shutil.rmtree(path= self.PATH + f'Java/{java}',ignore_errors= True)
                            self.CRIMSON_BACKGROUND_THREAD_POOL.submit(self.java, '17')
                            Logging().info('Java 17 not found. Installing... (JDK in Queue)')
                            break

                        elif java.startswith('jdk-8'):    
                            shutil.rmtree(path= self.PATH + f'Java/{java}',ignore_errors= True)
                            self.CRIMSON_BACKGROUND_THREAD_POOL.submit(self.java, '8')
                            Logging().info('Java 8 not found. Installing... (JDK in Queue)')
                            break

            for vanilla_version in minecraft_launcher_lib.utils.get_version_list():

                if vanilla_version['type'] == 'release':
                    self.MINECRAFT_VANILLA_RELEASES.append(vanilla_version['id'])
                elif vanilla_version['type'] == 'snapshot':
                    self.MINECRAFT_VANILLA_SNAPSHOTS.append(vanilla_version['id'])
            
            for fabric_version in minecraft_launcher_lib.fabric.get_all_minecraft_versions():

                if fabric_version['stable']:
                    self.FABRIC_RELEASES.append(fabric_version['version'])
                else:
                    self.FABRIC_SNAPSHOTS.append(fabric_version['version'])
            
            for quilt_version in minecraft_launcher_lib.quilt.get_all_minecraft_versions():

                if quilt_version['stable']:
                    self.QUILT_RELEASES.append(quilt_version['version'])
                else:
                    self.QUILT_SNAPSHOTS.append(quilt_version['version'])   

            Logging().debug('Vanilla releases: ' + ', '.join(self.MINECRAFT_VANILLA_RELEASES))
            Logging().debug('Vanilla snapshots: ' + ', '.join(self.MINECRAFT_VANILLA_SNAPSHOTS))
            Logging().debug('Fabric releases: ' + ', '.join(self.FABRIC_RELEASES))
            Logging().debug('Fabric snapshots: ' + ', '.join(self.FABRIC_SNAPSHOTS))
            Logging().debug('Quilt releases: ' + ', '.join(self.QUILT_RELEASES))
            Logging().debug('Quilt snapshots: ' + ', '.join(self.QUILT_SNAPSHOTS))

            Logging().debug('Checker terminated.')

            self.start()

        def start(self) -> None:

            def terminate_start_window() -> None:

                Logging().debug('Terminating start window...')

                StartWindowLoadBar.stop()
                StartWindow.quit()
                StartWindow.withdraw()

                Logging().debug('Start window terminated.')

                return self.main()
            
            Logging().debug('Starting the start window...')

            StartWindow : customtkinter.CTk = customtkinter.CTk()   
            StartWindow.title(f'Crimson Launcher - {constants.VERSION.value}')
            StartWindow.config(bg= self.COLOR)
            StartWindow.resizable(False, False)
            StartWindow.geometry('580x620')
            StartWindow.wm_iconbitmap(f'{self.ASSETS_PATH}/logo.ico')
            StartWindow.overrideredirect(True)

            StartWindowImage : customtkinter.CTkLabel = customtkinter.CTkLabel(
                StartWindow,
                text= None,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/logo.png'), size= (256, 256)),
                bg_color= 'transparent',
                fg_color= self.COLOR 
            )
            StartWindowImage.pack_configure(anchor= 'n', pady= 100)

            StartWindowTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                StartWindow,
                text= 'Crimson Launcher',
                text_color= '#0077ff',
                font= ('JetBrains', 30),
                bg_color= 'transparent',
                fg_color= self.COLOR
            )
            StartWindowTitle.place_configure(relx= 0.5, rely= 0.6_5, anchor= 'center')
            
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

            Logging().debug('Start window terminated.')

        def main(self) -> None:

            Logging().debug('Starting the main window...')

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
            
            def select_java_version(version : str) -> None:

                if version == self.JAVA_CURRENT: return

                with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                    config = json.load(read)
                    config['java']['path'] = version

                with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                    json.dump(config, write, indent= 5)

                self.JAVA_CURRENT = version    

                messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'{version} ahora es el Java seleccionado.', type= 'ok', parent= HomeWindow)
                return        
            
            def assign_ram(value : int) -> None:

                if value <= 999: value = 1000

                with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                    config = json.load(read)
                    config['launcher settings']['ram_asigned'] = round(value)
                    
                with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                    json.dump(config, write, indent= 5)

                self.RAM_ASSIGNED = round(value)        

                AssignedMemoryTitle.configure(text= f'Memoria asignada: {round(self.RAM_ASSIGNED)} MB')    
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
            
            def accounts() -> None:

                VersionsAndMods.configure(state= 'normal')
                Launch.configure(state= 'normal')
                Accounts.configure(state= 'disabled')

                def premium() -> None:
                    
                    messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'Proximamente estará disponible.', type= 'ok', parent= HomeWindow)
                    return
                
                def select_account(account : str) -> None:

                    if account.find(' | No Premium') != -1:

                        ACCOUNT = account.replace(' | No Premium', '')

                        with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                            config = json.load(read)
                        
                            for key in config['accounts'].keys():

                                if config['accounts'][key]['select']:

                                    config['accounts'][key]['select'] = False

                            for key in config['accounts'].keys():

                                if config['accounts'][key]['nickname'].lower() == ACCOUNT.lower():

                                    config['accounts'][key]['select'] = True 
                                    self.ACCOUNT_CURRENT = config['accounts'][key]['nickname']
                                    break        

                        with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                            json.dump(config, write, indent= 5)

                        messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'Cuenta seleccionada: {self.ACCOUNT_CURRENT}', type= 'ok', parent= HomeWindow)    
                        return

                    #Lógica para las cuentas premium...  

                def delete_account(account : str) -> None:

                    if account.find(' | No Premium') != -1:

                        ACCOUNT = account.replace(' | No Premium', '')

                        with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                            config = json.load(read)

                            for key in config['accounts'].keys():

                                if config['accounts'][key]['nickname'].lower() == ACCOUNT.lower():

                                    if config['accounts'][key]['select']:

                                        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'No puedes borrar la cuenta seleccionada.', type= 'ok', parent= HomeWindow)
                                        return

                                    del config['accounts'][key]
                                    break

                        with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                            json.dump(config, write, indent= 5)

                        for value in self.ACCOUNTS_LIST:

                            if value.find(' | No Premium') != -1 and value.replace(' | No Premium', '') == ACCOUNT:
                                
                                self.ACCOUNTS_LIST.remove(value)
                                break
                        
                        SelectAccount.configure(values= self.ACCOUNTS_LIST)
                        DeleteAccount.configure(values= self.ACCOUNTS_LIST)

                        DeleteAccount.set(self.ACCOUNTS_LIST[0])

                        messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= f'Cuenta eliminada: {ACCOUNT}', type= 'ok', parent= HomeWindow)
                        return    

                def no_premium() -> None:

                    tempList : list[str] = EntryNoPremiumAccount.get().split(' ')

                    if len(EntryNoPremiumAccount.get()) >= 14:

                        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'El tamaño del nick no puede ser mayor a 14 carácteres.', type= 'ok', parent= HomeWindow)
                        return
                    
                    elif EntryNoPremiumAccount.get() == '':
                        
                        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'El nick no puede estar vacío.', type= 'ok', parent= HomeWindow)
                        return
                    
                    elif EntryNoPremiumAccount.get().lower() == 'Nombre de la nueva cuenta.'.lower():

                        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'El nick no puede ser el placeholder por defecto.', type= 'ok', parent= HomeWindow)
                        return 
                    
                    elif len(tempList) >= 2:

                        messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'El nick no puede contener espacios.', type= 'ok', parent= HomeWindow)
                        return
                        
                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                        config = json.load(read)

                        for name in config['accounts'].keys():

                            if name.lower() == EntryNoPremiumAccount.get().lower():
                                
                                messagebox.showerror(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'Cuenta ya existente.', type= 'ok', parent= HomeWindow)
                                return
                    
                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                        config = json.load(read)
                        config['accounts'][EntryNoPremiumAccount.get()] = {

                            'nickname' : EntryNoPremiumAccount.get(),
                            'type' : 'no_premium',
                            'select' : False

                        }

                    with open(self.PATH + 'Crimson Settings/config.json', 'w') as write:

                        json.dump(config, write, indent= 5)

                    self.ACCOUNTS_LIST.clear()   

                    with open(self.PATH + 'Crimson Settings/config.json', 'r') as read:

                        config = json.load(read) 

                        for account in config['accounts'].items():

                            if account[1]['type'] == 'no_premium':

                                for name in config['accounts'].keys():

                                    if name.lower() == account[0].lower():

                                        self.ACCOUNTS_LIST.append(name + ' | No Premium')      

                        SelectAccount.configure(values = self.ACCOUNTS_LIST)   
                        DeleteAccount.configure(values = self.ACCOUNTS_LIST)

                    messagebox.showinfo(title= f'Crimson Launcher - {constants.VERSION.value}', message= 'Cuenta guardada, ahora puede seleccionarla.', type= 'ok', parent= HomeWindow)
                    return

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

                    if isinstance(name[1], customtkinter.CTkSlider):

                        name[1].place_forget()
                        continue    

                    if isinstance(name[1], customtkinter.CTkEntry):

                        name[1].place_forget()
                        continue

                NoPremiumAccount : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' No Premium',
                    compound= 'left',
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/no_premium.png'), size= (96, 96))

                )
                NoPremiumAccount.place_configure(relx= 0.0_3, rely= 0.2_7, anchor= 'sw')    

                EntryNoPremiumAccount : customtkinter.CTkEntry = customtkinter.CTkEntry(
                    FrameDecorationCenter,
                    placeholder_text= 'Nombre de la nueva cuenta.',
                    placeholder_text_color= 'white',
                    text_color= 'white',
                    font=('JetBrains', 15),
                    width= 210,
                    height= 35,
                    corner_radius= 20,
                    bg_color= '#232323',
                    fg_color= '#232323'
                )
                EntryNoPremiumAccount.place_configure(relx= 0.0_8, rely= 0.4_1, anchor= 'sw')

                CreateNoPremiumAccount : customtkinter.CTkButton = customtkinter.CTkButton(
                    FrameDecorationCenter,
                    height= 37,
                    bg_color= '#232323',
                    fg_color= '#0077ff',
                    corner_radius= 20,
                    text= 'Crear cuenta',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/create.png'), size= (22, 22)),
                    compound= 'left',
                    font= ('JetBrains', 15),
                    border_width= 2,
                    border_color= '#70ceff',
                    command= no_premium
                )
                CreateNoPremiumAccount.place_configure(relx= 0.1_1, rely= 0.5_5, anchor= 'sw')

                SelectAccountLabel : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Selecionar',
                    compound= 'left',
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/select.png'), size= (96, 96))

                )
                SelectAccountLabel.place_configure(relx= 0.5, rely= 0.1_6, anchor= 'center') 

                if len(self.ACCOUNTS_LIST) <= 0:

                    self.ACCOUNTS_LIST.append('No hay cuentas disponibles.')

                SelectAccount : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.ACCOUNTS_LIST,
                    command= select_account
                )
                SelectAccount.place_configure(relx= 0.5_2, rely= 0.3_7, anchor= 'center')

                if len(self.ACCOUNTS_LIST) <= 1 and self.ACCOUNTS_LIST[0] == 'No hay cuentas disponibles.':

                    SelectAccount.configure(state= 'disabled')

                DeleteAccountLabel : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Eliminar Cuenta',
                    compound= 'left',
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/garbage.png'), size= (96, 96))

                )  
                DeleteAccountLabel.place_configure(relx= 0.5, rely= 0.5_7, anchor= 'center')

                DeleteAccount : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.ACCOUNTS_LIST,
                    command= delete_account
                )
                DeleteAccount.place_configure(relx= 0.5_2, rely= 0.7_7, anchor= 'center')

                if len(self.ACCOUNTS_LIST) <= 1 and self.ACCOUNTS_LIST[0] == 'No hay cuentas disponibles.':

                    DeleteAccount.configure(state= 'disabled')

                PremiumAccount : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Premium',
                    compound= 'left',
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/premium.png'), size= (96, 96))

                )
                PremiumAccount.place_configure(relx= 0.9_5, rely= 0.0_7, anchor= 'ne')

                EntryGmailPremiumAccount : customtkinter.CTkEntry = customtkinter.CTkEntry(
                    FrameDecorationCenter,
                    placeholder_text= 'Correo de la cuenta.',
                    placeholder_text_color= 'white',
                    text_color= 'white',
                    font=('JetBrains', 15),
                    width= 210,
                    height= 35,
                    corner_radius= 20,
                    bg_color= '#232323',
                    fg_color= '#232323'
                )
                EntryGmailPremiumAccount.place_configure(relx= 0.9_6, rely= 0.3_4, anchor= 'ne')

                EntryPasswordPremiumAccount : customtkinter.CTkEntry = customtkinter.CTkEntry(
                    FrameDecorationCenter,
                    placeholder_text= 'Contraseña de la cuenta.',
                    placeholder_text_color= 'white',
                    text_color= 'white',
                    font=('JetBrains', 15),
                    width= 210,
                    height= 35,
                    corner_radius= 20,
                    bg_color= '#232323',
                    fg_color= '#232323'
                )
                EntryPasswordPremiumAccount.place_configure(relx= 0.9_6, rely= 0.4_7, anchor= 'ne')

                LoginPremiumAccount : customtkinter.CTkButton = customtkinter.CTkButton(
                    FrameDecorationCenter,
                    height= 37,
                    bg_color= '#232323',
                    fg_color= '#0077ff',
                    corner_radius= 20,
                    text= 'Iniciar Sesión',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/create.png'), size= (22, 22)),
                    compound= 'left',
                    font= ('JetBrains', 15),
                    border_width= 2,
                    border_color= '#70ceff',
                    command= premium
                )
                LoginPremiumAccount.place_configure(relx= 0.9_3_7, rely= 0.6, anchor= 'ne')
            
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

                    if isinstance(name[1], customtkinter.CTkSlider):

                        name[1].place_forget()
                        continue    

                    if isinstance(name[1], customtkinter.CTkEntry):

                        name[1].place_forget()
                        continue

                LaunchTitle.place_configure(relx= 0.0_4, rely= 0.2_7, anchor= 'sw')  
                LaunchVersion.place_configure(relx= 0.0_5, rely= 0.5_0, anchor= 'sw')
                OptimizationTitle.place_configure(relx= 0.9_5, rely= 0.2_7, anchor= 'se')
                OptimizeJavaArgs.place_configure(relx= 0.9, rely= 0.4_4, anchor= 'se')
                OpenOrClose.place_configure(relx= 0.9_2, rely= 0.6_0, anchor= 'se')
                JavaTitle.place_configure(relx= 0.4_8, rely= 0.1_7, anchor= 'center')
                SelectJavaVersion.place_configure(relx= 0.4_8, rely= 0.4_5_9, anchor= 'center')
                AssignMemory.place_configure(relx= 0.4_8, rely= 0.5_9, anchor= 'center')
                AssignedMemoryTitle.place_configure(relx= 0.4_8, rely= 0.7_0, anchor= 'center')
                TotalMemoryTitle.place_configure(relx= 0.4_8, rely= 0.7_5, anchor= 'center')

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

                else:    

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

                if self.JAVA_CURRENT != '':
                    SelectJavaVersion.set(self.JAVA_CURRENT)        

                if len(self.JAVA_LIST) <= 1 and self.JAVA_LIST[0] == 'No hay versiones instaladas en las librerías locales.':
                    SelectJavaVersion.configure(state= 'disabled')       
                
            def versions_and_mods() -> None:

                def fabricmc() -> None:

                    webbrowser.open_new_tab(constants.FABRICMC.value)
                    return
                
                def quilt() -> None:

                    webbrowser.open_new_tab(constants.QUILT.value)
                    return
                
                def download_specific_version(version : str) -> None:

                    self.CRIMSON_BACKGROUND_THREAD_POOL.submit(download, 'Windows', self.PATH, 'Vanilla', version, HomeWindow, FrameDecorationCenter)

                VersionsAndMods.configure(state= 'disabled')
                Launch.configure(state= 'normal')
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

                    if isinstance(name[1], customtkinter.CTkSlider):

                        name[1].place_forget()
                        continue    

                    if isinstance(name[1], customtkinter.CTkEntry):

                        name[1].place_forget()
                        continue

                InstallVanillaVersion : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Vanilla',
                    compound= 'left',
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/vanilla.png'), size= (96, 96))

                )
                InstallVanillaVersion.place_configure(relx= 0.0_6, rely= 0.2_7, anchor= 'sw')  

                SelectVanillaReleaseVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
                    dynamic_resizing= False,
                    text_color= 'white',
                    dropdown_fg_color= '#232323',
                    dropdown_text_color= 'white',
                    width= 210,
                    fg_color= '#0077ff', 
                    button_color= '#0077ff',
                    values= self.MINECRAFT_VANILLA_RELEASES,
                    command= download_specific_version
                )
                SelectVanillaReleaseVersion.place_configure(relx= 0.0_7, rely= 0.5_1, anchor= 'sw')
                
                SelectVanillaSnapshotVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
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
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/fabric.png'), size= (96, 96))

                )
                InstallFabricVersion.place_configure(relx= 0.3_9, rely= 0.2_7, anchor= 'sw')

                SelectFabricReleaseVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
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
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
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
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/fabric.png'), size= (26, 26)),
                    height= 40,
                    font= ('JetBrains', 15),
                    text_color= 'white',
                    text= 'FabricMC',
                    command= fabricmc,
                    compound= 'left',
                    hover= False
                )
                FabricMC.place_configure(relx= 0.4_2_5, rely= 0.8_8, anchor= 'sw')

                InstallQuiltVersion : customtkinter.CTkLabel = customtkinter.CTkLabel(
                    FrameDecorationCenter,
                    text= ' Quilt',
                    compound= 'left',
                    font= ('JetBrains', 30),
                    text_color= '#70ceff',
                    bg_color= '#232323',
                    fg_color= '#232323',
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/quilt.png'), size= (96, 96))

                )
                InstallQuiltVersion.place_configure(relx= 0.7_3, rely= 0.2_7, anchor= 'sw')

                SelectQuiltReleaseVersion : customtkinter.CTkOptionMenu = customtkinter.CTkOptionMenu(
                    FrameDecorationCenter,
                    height= 40,
                    corner_radius= 20,
                    bg_color= '#232323',
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
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
                    font= ('JetBrains', 15),
                    dropdown_font= ('JetBrains', 15),
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
                    image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/quilt.png'), size= (26, 26)),
                    height= 40,
                    font= ('JetBrains', 15),
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
            HomeWindow.after(300, HomeWindow.iconbitmap, f'{self.ASSETS_PATH}/logo.ico')
            HomeWindow.geometry('1290x720')
            HomeWindow.minsize(1290, 720)
            HomeWindow.maxsize(1920, 1080)
            HomeWindow.protocol('WM_DELETE_WINDOW', terminate_home_window)

            CanvasLogo : customtkinter.CTkLabel = customtkinter.CTkLabel(
                HomeWindow,
                text= None,
                fg_color= self.COLOR,
                image=  customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/logo.png'), size= (160, 160)),
                bg_color= self.COLOR
            )
            CanvasLogo.place_configure(relx= 0.0_2, rely= 0.0_4, anchor= 'nw')

            Discord : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/discord.png'), size= (96, 96)),
                height= 35,
                text= None,
                hover= False,
                command= discord
            )
            Discord.place_configure(relx= 0.99, rely= 0.0_8, anchor= 'ne')

            Github : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/github.png'), size= (96, 96)),
                height= 35,
                text= None,
                hover= False,
                command= github
            )
            Github.place_configure(relx= 0.99, rely= 0.4_8, anchor= 'e')

            Donate : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                corner_radius= 20,
                bg_color= self.COLOR,
                fg_color= self.COLOR,
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/donate.png'), size= (96, 96)),
                height= 35,
                text= None,
                hover= False,
                command= paypal
            )
            Donate.place_configure(relx= 0.99, rely= 0.8_8, anchor= 'se')

            VersionsAndMods : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 40,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Versiones y Mods',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/download.png'), size= (22, 22)),
                compound= 'left',
                font= ('JetBrains', 15),
                border_width= 2,
                border_color= '#0077ff',
                command= versions_and_mods
            )
            VersionsAndMods.place_configure(relx= 0.2_5, rely= 0.1, anchor= 'n')

            Launch : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 40,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Lanzar',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/home.png'), size= (22, 22)),
                compound= 'left',
                font= ('JetBrains', 15),
                command= launch
            )
            Launch.place_configure(relx= 0.5, rely= 0.1, anchor= 'n')

            Launch.configure(state= 'disabled')

            Accounts : customtkinter.CTkButton = customtkinter.CTkButton(
                HomeWindow,
                height= 40,
                bg_color= self.COLOR,
                fg_color= '#0077ff',
                corner_radius= 20,
                text= 'Cuentas',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/account.png'), size= (22, 22)),
                compound= 'left',
                font= ('JetBrains', 15),
                command= accounts
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
                font= ('JetBrains', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/launch.png'), size= (96, 96))
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
                font= ('JetBrains', 15),
                dropdown_font= ('JetBrains', 15),
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
                font= ('JetBrains', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/java.png'), size= (96, 96))
            )
            JavaTitle.place_configure(relx= 0.4_8, rely= 0.1_7, anchor= 'center')

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
                font= ('JetBrains', 15),
                dropdown_font= ('JetBrains', 15),
                dynamic_resizing= False,
                text_color= 'white',
                dropdown_fg_color= '#232323',
                dropdown_text_color= 'white',
                width= 210,
                fg_color= '#0077ff', 
                button_color= '#0077ff',
                values= self.JAVA_LIST,
                command= select_java_version
            )
            SelectJavaVersion.place_configure(relx= 0.4_8, rely= 0.4_5_9, anchor= 'center')

            if self.JAVA_CURRENT != '':
                SelectJavaVersion.set(self.JAVA_CURRENT)

            if len(self.JAVA_LIST) <= 1 and self.JAVA_LIST[0] == 'No hay versiones instaladas en las librerías locales.':
                SelectJavaVersion.configure(state= 'disabled')

            AssignMemory : customtkinter.CTkSlider = customtkinter.CTkSlider(
                FrameDecorationCenter,
                to= self.RAM_TOTAL,
                from_= 1000,
                width= 200,
                height= 25,
                bg_color= '#232323',
                corner_radius= 20,
                button_corner_radius= 20,
                hover= False,
                button_color= '#232323',
                progress_color= '#0077ff',
                command= assign_ram
            )    
            AssignMemory.place_configure(relx= 0.4_8, rely= 0.5_9, anchor= 'center')
            AssignMemory.set(self.RAM_ASSIGNED)

            AssignedMemoryTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                FrameDecorationCenter,
                text= f'Memoria asignada: {self.RAM_ASSIGNED} MB',
                font= ('JetBrains', 15),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323'
            )
            AssignedMemoryTitle.place_configure(relx= 0.4_8, rely= 0.7_0, anchor= 'center')

            TotalMemoryTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                FrameDecorationCenter,
                text= f'Memoria disponible: {round(1 * psutil.virtual_memory().total / (1024 ** 2))} MB',
                font= ('JetBrains', 15),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323'
            )
            TotalMemoryTitle.place_configure(relx= 0.4_8, rely= 0.7_5, anchor= 'center')

            OptimizationTitle : customtkinter.CTkLabel = customtkinter.CTkLabel(
                FrameDecorationCenter,
                text= ' Optimización',
                compound= 'left',
                font= ('JetBrains', 30),
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#232323',
                image= customtkinter.CTkImage(light_image= Image.open(f'{self.ASSETS_PATH}/optimize.png'), size= (96, 96))

            )
            OptimizationTitle.place_configure(relx= 0.9_5, rely= 0.2_7, anchor= 'se')

            OptimizeJavaArgs : customtkinter.CTkSwitch = customtkinter.CTkSwitch(
                FrameDecorationCenter,
                text= ' Optimizar Java',
                text_color= '#70ceff',
                bg_color= '#232323',
                fg_color= '#0077ff',
                font= ('JetBrains', 18),
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
                font= ('JetBrains', 18),
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

            Logging().debug('Main Window terminated.')
            
        def terminate(self) -> None:

            Logging().debug('Terminating...')
            Logging().warning('If there is a JDK in the installation queue, it cannot be closed quickly.')
            self.CRIMSON_BACKGROUND_THREAD_POOL.shutdown(cancel_futures= True)
            Logging().debug('Terminated all processes.')
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
    
    Logging().debug('Starting the Crimson Launcher...')

    CrimsonLauncher(get_user())
    
    sys.exit(0)
