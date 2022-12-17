class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs["default"] = self.get_program("default")
        self.programs["legs"] = self.get_program("legs")
        self.programs["table"] = self.get_program("table")
        self.programs["table_floor"] = self.get_program("table_floor")
        self.programs["axis"] = self.get_program("axis")
        self.programs["balls"] = self.get_program("balls")
        self.programs["subdivision_balls"] = self.get_program("subdivision_balls")
        self.programs["cue"] = self.get_program("cue")
        self.programs["terra"] = self.get_program("terra")
        self.programs["sostre"] = self.get_program("sostre")
        self.programs["line"] = self.get_program("line")
        self.programs["parets"] = self.get_program("parets")
        self.programs["shadow_map"] = self.get_program("shadow_map")
        self.programs['ombres_esferes'] = self.get_program('ombres_esferes')
        self.programs['jukebox'] = self.get_program('jukebox')


    def get_program(self, shader_program_name):
        with open(f"shaders/{shader_program_name}.vert") as file:
            vertex_shader = file.read()

        with open(f"shaders/{shader_program_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
