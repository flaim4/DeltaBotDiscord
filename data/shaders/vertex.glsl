#version 330
in vec2 in_vert;
out vec2 uv;
void main() {
    uv = in_vert * 0.5 + 0.5;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}