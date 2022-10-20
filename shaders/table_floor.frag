#version 330

layout (location = 0) out vec4 fragColor;

//in vec2 uv_1;
//uniform sampler2D u_texture_1;


void main() { 
    //vec3 color = texture(u_texture_1, uv_1).rgb;
    vec3 color = vec3(0, 1, 0);
    fragColor = vec4(color,1.0);
}