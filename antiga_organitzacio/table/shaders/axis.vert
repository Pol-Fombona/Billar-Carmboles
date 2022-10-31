#version 330
layout (location = 0) in vec3 in_color;
layout (location = 1) in vec3 in_position;

out vec3 color_0;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    color_0 = in_color;
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}