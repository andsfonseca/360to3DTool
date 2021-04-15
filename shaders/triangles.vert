# version 330

in layout(location = 0) vec3 positions;
in layout(location = 1) vec3 colors;

out vec3 newColor;
uniform mat4 model;
uniform mat4 vp;

void main(){
    gl_Position = vp * model * vec4(positions, 1.0);
    newColor = colors;
}