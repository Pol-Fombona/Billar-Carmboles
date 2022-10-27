from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, app):
        self.ctx = app.ctx
        self.vbo = VBO(app)
        self.program = ShaderProgram(app.ctx)
        self.vaos = {}

        self.vaos["legs"] = self.get_vao(
            program=self.program.programs["legs"], vbo=self.vbo.vbos["legs"]
        )
        self.vaos["table"] = self.get_vao(
            program=self.program.programs["table"], vbo=self.vbo.vbos["table"]
        )
        self.vaos["table_floor"] = self.get_vao(
            program=self.program.programs["table_floor"],
            vbo=self.vbo.vbos["table_floor"],
        )
        self.vaos["balls"] = self.get_vao(
            program=self.program.programs["balls"], vbo=self.vbo.vbos["balls"]
        )
        self.vaos["subdivision_balls"] = self.get_vao(
            program=self.program.programs["subdivision_balls"], 
            vbo=self.vbo.vbos["subdivision_balls"]
        )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)])

        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
