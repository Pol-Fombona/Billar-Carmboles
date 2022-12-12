#version 330

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
//uniform Light light2;
//uniform Light light3;
uniform sampler2D u_texture_0;
uniform vec3 camPos;
uniform sampler2DShadow shadowMap;
uniform vec2 u_resolution;

float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / u_resolution;
    return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                     oy * pixelOffset.y * shadowCoord.w, 0.0, 0.0));
}


float getSoftShadowX4() {
    float shadow;
    float swidth = 1.5;  // shadow spread
    vec2 offset = mod(floor(gl_FragCoord.xy), 2.0) * swidth;
    shadow += lookup(-1.5 * swidth + offset.x, 1.5 * swidth - offset.y);
    shadow += lookup(-1.5 * swidth + offset.x, -0.5 * swidth - offset.y);
    shadow += lookup( 0.5 * swidth + offset.x, 1.5 * swidth - offset.y);
    shadow += lookup( 0.5 * swidth + offset.x, -0.5 * swidth - offset.y);
    return shadow / 4.0;
}



float getSoftShadowX16() {
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}


float getSoftShadowX64() {
    float shadow;
    float swidth = 0.6;
    float endp = swidth * 3.0 + swidth / 2.0;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 64;
}


float getShadow() {
    float shadow = textureProj(shadowMap, shadowCoord);
    return shadow;
}

vec3 getLight(vec3 color){
    vec3 Normal = normalize(normal);
    // ambient
    vec3 ambient = light.Ia * 1.2;
    //vec3 ambient2 = light2.Ia;
    //vec3 ambient3 = light3.Ia;
    //diffuse
    vec3 lightDir = normalize(light.position - fragPos);
    //vec3 lightDir2 = normalize(light2.position - fragPos);
    //vec3 lightDir3 = normalize(light3.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    //float diff2 = max(0, dot(lightDir2, Normal));
    //float diff3 = max(0, dot(lightDir3, Normal));
    vec3 diffuse = diff * light.Id;
    //vec3 diffuse2 = diff2 * light2.Id;
    //vec3 diffuse3 = diff3 * light3.Id;

    // specular
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    //vec3 reflectDir2 = reflect(-lightDir2, Normal);
    //vec3 reflectDir3 = reflect(-lightDir3, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 12);
    //float spec2 = pow(max(dot(viewDir, reflectDir2), 0), 12);
    //float spec3 = pow(max(dot(viewDir, reflectDir3), 0), 12);
    vec3 specular = spec * light.Is * 2;
    //vec3 specular2 = spec2 * light2.Is * 2;
    //vec3 specular3 = spec3 * light3.Is * 2;

    // Shadow
    float shadow = getSoftShadowX16();

    //return color * (ambient + ambient2 + ambient3 + (diffuse + specular + diffuse2 + specular2  + diffuse3 + specular3)*shadow);
    return color * (ambient + (diffuse + specular) * shadow);

}


void main() { 
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));

    color = getLight(color);

    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}