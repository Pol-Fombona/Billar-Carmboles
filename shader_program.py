class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs["default"] = self.get_program("default")
        self.programs["legs"] = self.get_program("default")
        self.programs["table"] = self.get_program("default")
        self.programs["table_floor"] = self.get_program("default")
        self.programs["axis"] = self.get_program("default")
        self.programs["balls"] = self.get_program("default")
        self.programs["subdivision_balls"] = self.get_program("default")
        self.programs["cue"] = self.get_program("default")
        self.programs["terra"] = self.get_program("default")
        self.programs["sostre"] = self.get_program("default")
        self.programs["line"] = self.get_program("default")
        self.programs["parets"] = self.get_program("default")
        self.programs["shadow_map"] = self.get_program("shadow_map")


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
