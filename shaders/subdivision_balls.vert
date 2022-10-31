#version 330 core
                layout (location = 0) in vec3 in_color;
                layout (location = 1) in vec3 in_normal;
                layout (location = 2) in vec3 in_position;
                out vec3 color;
                
                struct Light {
                    vec3 position;
                    vec3 Ia;
                    vec3 Id;
                    vec3 Is;
                };
                
                uniform Light light;
                uniform mat4 m_proj;
                uniform mat4 m_view;
                uniform mat4 m_model;
                uniform vec3 camPos;
                
                void main() {
                    vec3 normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
                    vec3 ambient = light.Ia;
                    vec3 lightDir = normalize(light.position-in_position);
                    vec3 diffuse = light.Id * max(0,dot(lightDir,normalize(normal)));
                    
                    //Specular light
                    vec3 viewDir = normalize(camPos-in_position);
                    vec3 reflectDir = reflect(-lightDir, normalize(normal));
                    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
                    vec3 specular = spec * light.Is;

                    //color = ambient + in_color * diffuse;
                    color = in_color * (ambient + diffuse + specular);
                    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
                }