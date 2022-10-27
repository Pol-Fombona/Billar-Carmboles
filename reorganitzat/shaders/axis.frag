#version 330

layout (location = 0) out vec4 fragColor;

in vec3 color_0;

void main() { 
    fragColor = vec4(color_0,1.0);
}