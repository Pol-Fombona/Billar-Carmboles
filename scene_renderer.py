class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        self.table_objects = self.scene.table_objects
        self.ball_objects = self.scene.ball_objects
        self.all_objects = self.scene.all_objects
        # depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)


    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.table_objects:
            obj.render_shadow()

        for sphere in self.ball_objects:
            sphere.render_shadow()

    def render_shadow_cue(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.all_objects:
            print(obj)
            obj.render_shadow()

    def render(self):
        self.ctx.screen.use()
        # Render table + spheres

        #self.render_shadow()

        for obj in self.table_objects:
            obj.render()

        for sphere in self.ball_objects:
            sphere.render()


    def render_with_cue(self):
        self.ctx.screen.use()
        # Render table + spheres + cue

        self.render_shadow_cue()

        for obj in self.all_objects:
            obj.render()


    def replay_render(self):
        self.ctx.screen.use()

        #self.render_shadow()
        # Render table + special render spheres

        for obj in self.table_objects:
            obj.render()

        for sphere in self.ball_objects:
            sphere.replay_render()
        
    def destroy(self):
        self.depth_fbo.release()
