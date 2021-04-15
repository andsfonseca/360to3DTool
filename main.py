import wx
from wx import glcanvas

from OpenGL.GL import *
from OpenGL.GL.shaders import *
from pyrr import Matrix44, matrix44, Vector3

import numpy as np

import time
import sys

from Components.ImportImage import ImportImageFrame
from Source.Models.Geometries import Cube

TRIANGLE_VERTEX_SHADER_PATH = "./shaders/triangles.vert"
TRIANGLE_FRAGMENT_SHADER_PATH = "./shaders/triangles.frag"

class OpenGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)

        self.init = False
        self.aspect_ratio = 1
        self._parent = parent
        self.vertex_shader = self.LoadShaderFromPath(TRIANGLE_VERTEX_SHADER_PATH)
        self.fragment_shader = self.LoadShaderFromPath(TRIANGLE_FRAGMENT_SHADER_PATH)
        self.rotate = True
        self.rotate_y = Matrix44.identity()

        #Contexto do Canvas
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)

        glClearColor(0.0, 0.0, 0.0, 0.0)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def SetSize(self, size):
        self.aspect_ratio = size.width / size.height

    def InitGL(self):
        # triangle = np.array([-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
        #                       0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
        #                       0.0, 0.5, 0.0, 0.0, 0.0, 1.0], dtype=np.float32)

        self.mesh = Cube()

        shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(self.vertex_shader, GL_VERTEX_SHADER), 
                                                  OpenGL.GL.shaders.compileShader(self.fragment_shader, GL_FRAGMENT_SHADER))

        glClearColor(0.0, 0.0, 0.0, 0.0)

        view = matrix44.create_from_translation(Vector3([0.0, 0.0, -2.0]))
        projection = matrix44.create_perspective_projection_matrix(45.0, self.aspect_ratio, 0.1, 100.0)

        vp = matrix44.multiply(view, projection)

        glUseProgram(shader)
        glEnable(GL_DEPTH_TEST)

        vp_loc = glGetUniformLocation(shader, "vp")
        glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)

        self.model_location = glGetUniformLocation(shader, "model")
        self.Refresh()

    def OnResize(self, event):
        #Se não estiver inicializado, pega o valor da tela do cliente
        if not self.init:
            size = self.GetClientSize()
        #Pega o tamanho definido do canvas
        else:
            size = self._parent._grid_layout.GetCellSize(0, 1)

        self.SetSize(size)

        #Atualiza o ViewPort
        glViewport(0,0, size.width, size.height)

    def OnPaint(self, event):
        wx.PaintDC(self)
        #Se for a primeira chamada do evento
        if not self.init:
            size = self._parent._grid_layout.GetCellSize(0, 1)
            self.SetSize(size)

            glViewport(0,0, size.width, size.height)
            self.InitGL()
            self.init = True
        
        self.OnDraw()                  

    def OnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.rotate:
            ct = time.perf_counter() * 0.1
            self.rotate_y = Matrix44.from_y_rotation(ct)
            glUniformMatrix4fv(self.model_location, 1,GL_FALSE, self.rotate_y)
            self.Refresh()
        else:
            glUniformMatrix4fv(self.model_location, 1,GL_FALSE, self.rotate_y)

        self.mesh.BindAndDraw()

        self.SwapBuffers()

    def LoadShaderFromPath(self, path):
        with open(path, 'r') as file:
            return file.read()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._grid_layout = wx.GridBagSizer(2, 1)

        self._left_panel = LeftPanel(self)
        self._canvas = OpenGLCanvas(self)

        self._grid_layout.Add(self._left_panel, pos=(0,0), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)
        self._grid_layout.Add(self._canvas, pos=(0,1), span=(0,4), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=0)

        self._grid_layout.AddGrowableCol(1)
        self._grid_layout.AddGrowableRow(0)

        self.SetSizer(self._grid_layout)

class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._grid_layout = wx.GridBagSizer()

        self._separator1= wx.StaticLine(self, size=(200, 1), style=wx.LI_HORIZONTAL)
        self._hierarchyBox = wx.StaticBox(parent, label="Hierarquia")

        self._grid_layout.Add(self._separator1, pos=(0,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=0)
        self._grid_layout.Add(self._hierarchyBox, pos=(1,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=2)

        self.SetSizer(self._grid_layout)

class MainMenu(wx.MenuBar):
    def __init__(self):
        wx.MenuBar.__init__(self)

        fileMenu = imageImportMenu = wx.Menu()

        imageImportMenu = wx.Menu()
        _360ImageImportMenu = imageImportMenu.Append(wx.ID_ANY, 'Imagem 360')
        imageImportMenu.Append(wx.ID_ANY, 'Imagem Panorâmica')
        
        fileMenu.Append(wx.ID_ANY, 'Imagem', imageImportMenu)
        fileMenu.Append(wx.ID_ANY, 'Modelo 3D')

        self.Append(fileMenu, 'Importar')

        #Eventos
        self.Bind(wx.EVT_MENU, self.OnClickImport360Image, _360ImageImportMenu)
    
    def OnClickImport360Image(self, event):

        openFileDialog = wx.FileDialog(self, "Abrir Imagem 360", "", "", 
            "Imagens  (*.jpeg,*.png)|*.jpeg;*.png;*.JPG", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()

        if(path == ""):
            return
        
        openFileDialog.Destroy()

        frame = ImportImageFrame(parent=wx.GetTopLevelParent(self), imagePath=path)

class MainFrame(wx.Frame):
    def __init__(self):
        self.size = (1280, 720)
        wx.Frame.__init__(self, None, title="360 to 3D Tool", size=self.size)

        # Configurações do Frame
        # self.SetMinSize(self.size)
        # self.SetMaxSize(self.size)

        # Componentes
        self._menuBar = MainMenu()
        self.SetMenuBar(self._menuBar)
        self._mainPanel = MainPanel(self)

        # Eventos
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Destroy()
        sys.exit(0)
    
        
class MainApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show()
        return True

if __name__ == "__main__":
    app = MainApp()
    app.MainLoop()