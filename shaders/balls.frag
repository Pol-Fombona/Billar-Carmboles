#version 330

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;

vec3 getLight(vec3 color){
    vec3 Normal = normalize(normal);
    // ambient
    vec3 ambient = light.Ia;
    //diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    return color * (ambient + diffuse);
}


void main() { 
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = getLight(color);
    fragColor = vec4(color,1.0);
}