#version 330
//layout (location = 0) in vec2 in_texcoord_1;
layout (location = 0) in vec3 in_position;

//out vec2 uv_1;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    //uv_1 = in_texcoord_1;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}