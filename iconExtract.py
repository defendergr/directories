import glob
import win32ui
import win32gui
import win32con
import win32api
import os
from PIL import Image

class IconExtract():

    def __init__(self):
        self.patternEXE = r'./**/*.exe'
        self.fileListEXE = glob.glob(self.patternEXE, recursive=True)

        self.patternMSI = r'./**/*.msi'
        self.fileListMSI = glob.glob(self.patternMSI, recursive=True)

        self.fileList = self.fileListEXE + self.fileListMSI

        self.pathToSaveIcons = r'./icons'
        if not os.path.exists(self.pathToSaveIcons):
            os.mkdir(self.pathToSaveIcons)

        self.numberOfSetupFiles = 0


    def extract_icon_from_exe(self, icon_in_path, icon_name, icon_out_path, size=120):

        try:
            ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
            ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

            large, small = win32gui.ExtractIconEx(icon_in_path, 0)
            win32gui.DestroyIcon(small[0])

            hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
            hbmp = win32ui.CreateBitmap()
            hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
            hdc = hdc.CreateCompatibleDC()

            hdc.SelectObject(hbmp)
            hdc.DrawIcon((0, 0), large[0])

            bmpstr = hbmp.GetBitmapBits(True)
            icon = Image.frombuffer('RGBA', (32, 32), bmpstr, 'raw', 'BGRA', 0, 1)

            full_outpath = os.path.join(icon_out_path, "{}.png".format(icon_name))
            # print(icon_name)
            icon.resize((size, size))
            icon.save(full_outpath)
        except:
            full_outpath = './images/msi.ico'

        #return the final path to the image
        return full_outpath


    def extract(self):
        self.filesDict = []
        for f in self.fileList:
            fileInstall = {}
            name = f.split("\\")
            # print(f)
            self.numberOfSetupFiles +=1
            # print(name[-1])
            self.extract_icon_from_exe(f, name[-1], self.pathToSaveIcons)
            # print(self.pathToSaveIcons)
            fileInstall['num'] = self.numberOfSetupFiles
            fileInstall['img'] = name[-1]
            fileInstall['path'] = f
            self.filesDict.append(fileInstall)

        return self.filesDict



