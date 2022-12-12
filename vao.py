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
        self.vaos["shadow_legs"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["legs"]
        )
        self.vaos["table"] = self.get_vao(
            program=self.program.programs["table"], vbo=self.vbo.vbos["table"]
        )
        self.vaos["shadow_table"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["table"]
        )
        self.vaos["table_floor"] = self.get_vao(
            program=self.program.programs["table_floor"],
            vbo=self.vbo.vbos["table_floor"],
        )
        self.vaos["shadow_table_floor"] = self.get_vao(
            program=self.program.programs["shadow_map"],
            vbo=self.vbo.vbos["table_floor"],
        )
        self.vaos["balls"] = self.get_vao(
            program=self.program.programs["balls"], vbo=self.vbo.vbos["balls"]
        )
        self.vaos["shadow_balls"] = self.get_vao(
            program=self.program.programs["shadow_map"], vbo=self.vbo.vbos["balls"]
        )
        self.vaos["subdivision_balls"] = self.get_vao(
            program=self.program.programs["subdivision_balls"], 
            vbo=self.vbo.vbos["subdivision_balls"]
        )
        self.vaos["cue"] = self.get_vao(program=self.program.programs["cue"],
            vbo=self.vbo.vbos["cue"]
        )
        self.vaos["shadow_cue"] = self.get_vao(program=self.program.programs["shadow_map"],
            vbo=self.vbo.vbos["cue"]
        )
        self.vaos["terra"] = self.get_vao(program=self.program.programs["terra"],
            vbo=self.vbo.vbos["terra"]
        )
        self.vaos["shadow_terra"] = self.get_vao(program=self.program.programs["shadow_map"],
            vbo=self.vbo.vbos["terra"]
        )
        self.vaos["sostre"] = self.get_vao(program=self.program.programs["sostre"],
            vbo=self.vbo.vbos["sostre"]
        )
        self.vaos["shadow_sostre"] = self.get_vao(program=self.program.programs["shadow_map"],
            vbo=self.vbo.vbos["sostre"]
        )
        self.vaos["line"] = self.get_vao(program=self.program.programs["line"],
            vbo=self.vbo.vbos["line"]
        )
        self.vaos["shadow_line"] = self.get_vao(program=self.program.programs["shadow_map"],
            vbo=self.vbo.vbos["line"]
        )
        self.vaos["parets"] = self.get_vao(program=self.program.programs["parets"],
            vbo=self.vbo.vbos["parets"]
        )
        self.vaos["shadow_parets"] = self.get_vao(program=self.program.programs["shadow_map"],
            vbo=self.vbo.vbos["parets"]
        )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)], skip_errors=True)

        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
