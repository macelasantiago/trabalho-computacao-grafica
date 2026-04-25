import glfw
from OpenGL.GL import *
import glm
from shader_utils import Shader
from camera import Camera
from models import Cube
from texture_loader import load_texture

# 1. DEFINA A FUNÇÃO MOUSE_CALLBACK FORA DA CLASSE
def mouse_callback(window, xpos, ypos):
    game = glfw.get_window_user_pointer(window)
    if game:
        if game.camera.first_mouse:
            game.camera.last_x = xpos
            game.camera.last_y = ypos
            game.camera.first_mouse = False

        xoffset = xpos - game.camera.last_x
        yoffset = game.camera.last_y - ypos # Invertido: y vai de baixo para cima
        game.camera.last_x = xpos
        game.camera.last_y = ypos

        game.camera.process_mouse_movement(xoffset, yoffset)

class Game:
    def __init__(self):
        if not glfw.init():
            return
        
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

        self.window = glfw.create_window(1280, 720, "Academic Wheels: The Dev Wars", None, None)
        if not self.window:
            glfw.terminate()
            return
            
        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)

        # Inicialização
        self.shader = Shader("vertex_shader.glsl", "fragment_shader.glsl")
        self.camera = Camera(1280, 720)
        self.table = Cube() 
        self.mesa_texture = load_texture("assets/madeira.jpg")

        # 2. CONFIGURAÇÃO DOS CALLBACKS (Aqui é onde o erro sumirá)
        glfw.set_window_user_pointer(self.window, self)
        glfw.set_cursor_pos_callback(self.window, mouse_callback)
        # Opcional: Trava o mouse dentro da janela para melhor controle
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    def run(self):
        while not glfw.window_should_close(self.window):
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glClearColor(0.05, 0.05, 0.1, 1.0) 

            self.shader.use()
            
            # Configuração de Luz
            light_pos = glm.vec3(1.2, 5.0, 2.0)
            glUniform3f(glGetUniformLocation(self.shader.program, "lightPos"), *light_pos)
            glUniform3f(glGetUniformLocation(self.shader.program, "viewPos"), *self.camera.camera_pos)
            glUniform3f(glGetUniformLocation(self.shader.program, "lightColor"), 1.0, 1.0, 1.0)
            
            # Matrizes de Câmera (Atualizadas a cada frame pelo mouse)
            view, proj = self.camera.get_matrices()
            glUniformMatrix4fv(glGetUniformLocation(self.shader.program, "view"), 1, GL_FALSE, glm.value_ptr(view))
            glUniformMatrix4fv(glGetUniformLocation(self.shader.program, "projection"), 1, GL_FALSE, glm.value_ptr(proj))

            # DESENHAR A MESA
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.mesa_texture)
            glUniform1i(glGetUniformLocation(self.shader.program, "ourTexture"), 0)

            model = glm.mat4(1.0)
            model = glm.translate(model, glm.vec3(0.0, -1.0, 0.0))
            model = glm.scale(model, glm.vec3(10.0, 0.2, 6.0)) 
            glUniformMatrix4fv(glGetUniformLocation(self.shader.program, "model"), 1, GL_FALSE, glm.value_ptr(model))
            
            self.table.draw()

            glfw.swap_buffers(self.window)
            glfw.poll_events()
            
        glfw.terminate()

if __name__ == "__main__":
    app = Game()
    app.run()