#version 330

in vec2 uv;
out vec4 fragColor;

uniform vec2 u_center = vec2(426, 178);
uniform sampler2D u_texture;
uniform vec2 u_level;
uniform vec2 u_size;

bool colision(float x, float y, vec4 box4) {
    return (x >= box4.x && x <= box4.z && y >= box4.y && y <= box4.w);
}

vec4 databox;
vec4 namebox;

void main() {
    databox = vec4(10, 60, u_size.x/1.5, 248.0);
    namebox = vec4((u_size.x/1.5)+10, 60, u_size.x - 10, 104.0);


    vec2 fragCoord = gl_FragCoord.xy;
    float dist = distance(fragCoord, u_center);
    
    vec4 color = vec4(0.2275, 0.2157, 0.2157, 0.0);

    if (dist <= 68.0) {
        vec2 uv = (fragCoord - u_center) / 68.0 * 0.5 + 0.5;
        color = texture(u_texture, 1.0 - uv);
    } else if (dist <= 72.0) {
        color = vec4(0.1804, 0.1765, 0.1765, 1.0);
    } else {
        if (fragCoord.y < 52.0 && fragCoord.y > 8.0&& (fragCoord.x < u_size.x - 8.0 && fragCoord.x > 8.0)) {
            color = vec4(0.1529, 0.149, 0.149, 1.0);
        }
        if (fragCoord.y < 50.0 && fragCoord.y > 10.0 && (fragCoord.x < u_size.x - 10.0 && fragCoord.x > 10.0)) {
            color = vec4(0.3255, 0.3255, 0.3255, 0.0);
        }

        float bar_x = (u_level.x / u_level.y) * u_size.x;

        if (fragCoord.x < bar_x + 10 && fragCoord.y < 50.0 && fragCoord.y > 10.0 && (fragCoord.x < u_size.x - 10.0 && fragCoord.x > 10.0)) {
            color = vec4(0.0, 1.0, 0.0, 1.0);
        }

        if (colision(fragCoord.x, fragCoord.y, databox)) {
            color = vec4(0.2863, 0.2863, 0.3059, 1.0);
        }

        if (colision(fragCoord.x, fragCoord.y, namebox)) {
            color = vec4(0.2863, 0.2863, 0.3059, 1.0);
        }
    }

    fragColor = color;
}
