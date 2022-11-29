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
uniform Light light2;
uniform Light light3;
uniform sampler2D u_texture_0;
uniform vec3 camPos;

vec3 getLight(vec3 color){
    vec3 Normal = normalize(normal);
    // ambient
    vec3 ambient = light.Ia * 1.2;
    vec3 ambient2 = light2.Ia;
    vec3 ambient3 = light3.Ia;
    //diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    vec3 lightDir2 = normalize(light2.position - fragPos);
    vec3 lightDir3 = normalize(light3.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    float diff2 = max(0, dot(lightDir2, Normal));
    float diff3 = max(0, dot(lightDir3, Normal));
    vec3 diffuse = diff * light.Id;
    vec3 diffuse2 = diff2 * light2.Id;
    vec3 diffuse3 = diff3 * light3.Id;

    // specular
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    vec3 reflectDir2 = reflect(-lightDir2, Normal);
    vec3 reflectDir3 = reflect(-lightDir3, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 12);
    float spec2 = pow(max(dot(viewDir, reflectDir2), 0), 12);
    float spec3 = pow(max(dot(viewDir, reflectDir3), 0), 12);
    vec3 specular = spec * light.Is * 0.5;
    vec3 specular2 = spec2 * light2.Is * 0.5;
    vec3 specular3 = spec3 * light3.Is * 0.5;

    return color * (ambient + diffuse + specular + ambient2 + diffuse2 + specular2 + ambient3 + diffuse3 + specular3);
}


void main() { 
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = getLight(color);
    fragColor = vec4(color,1.0);
}