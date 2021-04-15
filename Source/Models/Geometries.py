from OpenGL.GL import *
import numpy as np

class Cube:
    def __init__(self):

        #Vertícies e Cores
        cube = np.array([-0.5, -0.5,  0.5, 1.0, 0.0, 0.0,
                        0.5, -0.5,  0.5, 0.0, 1.0, 0.0,
                        0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                        -0.5,  0.5,  0.5, 1.0, 1.0, 1.0,

                        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                        0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                        0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
                        -0.5,  0.5, -0.5, 1.0, 1.0, 1.0,

                        0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                        0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
                        0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                        0.5, -0.5,  0.5, 1.0, 1.0, 1.0,

                        -0.5,  0.5, -0.5, 1.0, 0.0, 0.0,
                        -0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                        -0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
                        -0.5,  0.5,  0.5, 1.0, 1.0, 1.0,

                        -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
                        0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
                        0.5, -0.5,  0.5, 0.0, 0.0, 1.0,
                        -0.5, -0.5,  0.5, 1.0, 1.0, 1.0,

                        0.5,  0.5, -0.5, 1.0, 0.0, 0.0,
                        -0.5,  0.5, -0.5, 0.0, 1.0, 0.0,
                        -0.5,  0.5,  0.5, 0.0, 0.0, 1.0,
                        0.5,  0.5,  0.5, 1.0, 1.0, 1.0],  dtype=np.float32)

        #Indices
        indices = np.array([0,  1,  2,  2,  3,  0,
                            4,  5,  6,  6,  7,  4,
                            8,  9, 10, 10, 11,  8,
                            12, 13, 14, 14, 15, 12,
                            16, 17, 18, 18, 19, 16,
                            20, 21, 22, 22, 23, 20], dtype=np.uint32)

        #Define a quantidade de Indices
        self.indicesCount = len(indices)

        #Define a quantidade de Verticies
        self.vertexCount = int(len(cube) / 6)

        #Coloca no Buffer
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo_cube = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_cube)
        glBufferData(GL_ARRAY_BUFFER, len(cube) * 4, cube, GL_STATIC_DRAW)

        cube_ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, cube_ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

        # Ponteiros dos Vertices
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

       # Ponteiros das Cores
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        #Limpa
        glBindVertexArray(0)

    def Bind(self):
        glBindVertexArray(self.vao)

    def Draw(self):
        glDrawElements(GL_TRIANGLES, self.indicesCount, GL_UNSIGNED_INT, None)

    def BindAndDraw(self):
        self.Bind()
        self.Draw()

class Triangle():
    def __init__(self):

        #Vertícies e Cores
        triangle = np.array([-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                              0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                              0.0, 0.5, 0.0, 0.0, 0.0, 1.0], dtype=np.float32)

        #Define a quantidade de Verticies
        self.vertexCount = int(len(triangle) / 6) 

        #Coloca no Buffer
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo_triangle = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_triangle)
        glBufferData(GL_ARRAY_BUFFER, len(triangle) * 4, triangle, GL_STATIC_DRAW)

        # Ponteiros dos Vertices
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Ponteiros das Cores
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        #Limpa
        glBindVertexArray(0)

    def Bind(self):
        glBindVertexArray(self.vao)
    
    def Draw(self):
        glDrawArrays(GL_TRIANGLES, 0, self.vertexCount)

    def BindAndDraw(self):
        self.Bind()
        self.Draw()

class Quad():
    def __init__(self):

        #Vertícies e Cores
        quad = np.array([-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                        0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                        -0.5,  0.5, 0.0, 0.0, 0.0, 1.0,
                        0.5,  0.5, 0.0, 1.0, 1.0, 1.0], dtype=np.float32)

        #Define a quantidade de Verticies
        self.vertexCount = int(len(quad) / 6) 

        #Coloca no Buffer
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        vbo_quad = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo_quad)
        glBufferData(GL_ARRAY_BUFFER, len(quad) * 4, quad, GL_STATIC_DRAW)

        # Ponteiros dos Vertices
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # Ponteiros das Cores
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        
        #Limpa
        glBindVertexArray(0)

    def Bind(self):
        glBindVertexArray(self.vao)

    def Draw(self):
        glDrawArrays(GL_TRIANGLE_STRIP, 0, self.vertexCount)

    def BindAndDraw(self):
        self.Bind()
        self.Draw()