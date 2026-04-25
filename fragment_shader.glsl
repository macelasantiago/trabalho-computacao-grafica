#version 330 core
out vec4 FragColor;

in vec3 Normal;
in vec3 FragPos;
in vec2 TexCoord; // Recebe as coordenadas UV do Vertex Shader

uniform vec3 lightPos; 
uniform vec3 viewPos; 
uniform vec3 lightColor;
uniform sampler2D ourTexture; // A variável que segura a imagem

void main() {
    // 1. Ambiente
    float ambientStrength = 0.3;
    vec3 ambient = ambientStrength * lightColor;
  	
    // 2. Difusa 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    // 3. Especular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;  
        
    // APLICAÇÃO DA TEXTURA: Multiplica o resultado do Phong pela cor da imagem
    vec3 texColor = texture(ourTexture, TexCoord).rgb;
    vec3 result = (ambient + diffuse + specular) * texColor;
    
    FragColor = vec4(result, 1.0);
}