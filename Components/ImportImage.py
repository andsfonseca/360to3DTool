from wx import Frame, Panel, GridBagSizer, FlexGridSizer, StaticBitmap, Image, StaticText, StaticLine, StaticBox, TextCtrl, BoxSizer, EmptyImage
from wx import ALL, ALIGN_LEFT, EXPAND, TOP, LEFT, RIGHT, BOTTOM, ST_ELLIPSIZE_MIDDLE, BITMAP_TYPE_ANY, LI_HORIZONTAL, DEFAULT_FRAME_STYLE, RESIZE_BORDER, MAXIMIZE_BOX, HORIZONTAL

import numpy as np
import io
import cv2
import matplotlib.pyplot as plt

class ImportImageFrame(Frame):
    """
    Frame para Importação de Imagem
    """
    def __init__(self, parent, imagePath):
        self._size = (1280, 720)
        Frame.__init__(self, parent=parent, title="Importação de Imagem", size=self._size, style=DEFAULT_FRAME_STYLE ^ RESIZE_BORDER ^ MAXIMIZE_BOX)
        self._panel = ImportImagePanel(self, imagePath)
        self.SetFocus()
        self.ShowWithoutActivating()

class ImportImagePanel(Panel):
    """
    Panel Principal para Importação de Imagem
    """
    def __init__(self, parent, imagePath):
        Panel.__init__(self, parent)

        self._hbox = BoxSizer(HORIZONTAL)
        self._grid_layout = FlexGridSizer(1, 2, 1, 1)

        # self._grid_layout = GridBagSizer(2, 1)

        self._configurationAndImportPanel = ConfigurationAndImportPanel(self)
        self._bitmapPanel = BitmapPanel(self, imagePath)

        self._grid_layout.AddMany([
            (self._configurationAndImportPanel, 1, LEFT),
            (self._bitmapPanel, 1, EXPAND)
        ])
        
        self._grid_layout.AddGrowableCol(1, 1)
        self._grid_layout.AddGrowableRow(0, 1)

        self._hbox.Add(self._grid_layout, proportion=1, flag=ALL|EXPAND, border=0)
        self.SetSizer(self._hbox)

class ConfigurationAndImportPanel(Panel):
    def __init__(self, parent):
        Panel.__init__(self, parent)
        self._grid_layout = GridBagSizer()
        self._separator1= StaticLine(self, size=(250, 1), style=LI_HORIZONTAL)
        self._hierarchyBox = StaticBox(parent, label="Configurar Importação")

        self._grid_layout.Add(self._separator1, pos=(0,0), flag=TOP|LEFT|BOTTOM, border=0)
        self._grid_layout.Add(self._hierarchyBox, pos=(1,0), flag=TOP|LEFT|BOTTOM, border=2)

        self.SetSizer(self._grid_layout)

class BitmapPanel(Panel):
    def __init__(self, parent, imagePath):
        Panel.__init__(self, parent)

        #Cor do Fundo
        self.BackgroundColour=((100,100,100))
        
        #Tamanhos do BitMap
        self._bitmap_width = 510
        self._bitmap_height = 720

        #Grid do BitMap
        self._hbox = BoxSizer(HORIZONTAL)
        self._grid_layout = FlexGridSizer(1, 2, 0, 10)

        #Lê a Imagem
        self._image = cv2.imread(imagePath)

        defaultImage = self.GetImageDataInPanelSize(self._bitmap_width, self._bitmap_height, self._image)

        defaultImage_wx = EmptyImage(self._bitmap_width,self._bitmap_height) 
        defaultImage_wx.SetData(defaultImage.tostring()) # convert from cv.iplimage to wxImage

        defaultImage_png = defaultImage_wx.ConvertToBitmap()
        # png = Image(image.GetWidth(), image.GetHeight(), imageData)
        # png = Image(imagePath, BITMAP_TYPE_ANY).ConvertToBitmap()

        # test1 = StaticBitmap(self, -1, png, size=(self._bitmap_width,self._bitmap_height))
        # test2 = StaticBitmap(self, -1, png, size=(self._bitmap_width,self._bitmap_height))
        test1 = StaticBitmap(self, -1, defaultImage_png, (0,0), (defaultImage_wx.GetWidth(), defaultImage_wx.GetHeight()))
        test2 = StaticBitmap(self, -1, defaultImage_png, (0,0), (defaultImage_wx.GetWidth(), defaultImage_wx.GetHeight()))

        self._grid_layout.AddMany([
            (test1, 1, EXPAND),
            (test2, 1, EXPAND)
        ])

        self._grid_layout.AddGrowableRow(0, 1)

        self._hbox.Add(self._grid_layout, proportion=1, flag=ALL|EXPAND, border=0)
        self.SetSizer(self._hbox)

    def GetImageDataInPanelSize(self, f_width, f_height, image):
        
        copy = image.copy()
        h, w, _ = copy.shape

        #Partindo da premissa que imagens 360 possui largura esparsas
        aspect = f_width/w

        print(h * aspect)
        resize = cv2.resize(copy, (int(w * aspect),int(h * aspect)))

        h, w, _ = resize.shape

        h_up = h//2
        h_down = h-h_up

        result = np.full((f_height, f_width, 3), 0, dtype=np.uint8)

        result[(f_height//2)-h_up:(f_height//2)+h_down, 0:f_width] = resize

        return cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        





        
