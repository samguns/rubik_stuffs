#include <stdio.h>
#include <stdlib.h>

struct rgb_color
{
    unsigned char r;
    unsigned char g;
    unsigned char b;
};

struct hsv_color
{
    unsigned char hue;
    unsigned char sat;
    unsigned char val;
    unsigned char lum;
};

#define MIN3(x,y,z)  ((y) <= (z) ? \
                         ((x) <= (y) ? (x) : (y)) \
                     : \
                         ((x) <= (z) ? (x) : (z)))

#define MAX3(x,y,z)  ((y) >= (z) ? \
                         ((x) >= (y) ? (x) : (y)) \
                     : \
                         ((x) >= (z) ? (x) : (z)))

struct hsv_color rgb_to_hsv(struct rgb_color rgb)
{
    struct hsv_color hsv;
    unsigned char rgb_min, rgb_max;

    rgb_min = MIN3(rgb.r, rgb.g, rgb.b);
    rgb_max = MAX3(rgb.r, rgb.g, rgb.b);

    hsv.val = rgb_max;
    if (hsv.val == 0)
    {
        hsv.hue = hsv.sat = 0;
        return hsv;
    }

    hsv.sat = 255 * (long)(rgb_max - rgb_min) / hsv.val;
    if (hsv.sat == 0)
    {
        hsv.hue = 0;
        return hsv;
    }

    if (rgb_max == rgb.r)
    {
        hsv.hue = 0 + 43 * (rgb.g - rgb.b)/(rgb_max - rgb_min);
    }
    else if (rgb_max == rgb.g)
    {
        hsv.hue = 85 + 43 * (rgb.g - rgb.r)/(rgb_max - rgb_min);
    }
    else
    {
        hsv.hue = 171 + 43 * (rgb.r - rgb.g)/(rgb_max - rgb_min);
    }

    hsv.lum = (rgb_max + rgb_min) / 2;

    return hsv;
};

int main(int argc, char *argv[])
{
    struct rgb_color rgb;
    struct hsv_color hsv;

    rgb.r = (unsigned char)atoi(argv[1]);
    rgb.g = (unsigned char)atoi(argv[2]);
    rgb.b = (unsigned char)atoi(argv[3]);

    hsv = rgb_to_hsv(rgb);
    printf("Hue:%d Sat:%d Val:%d Lum:%d\n", hsv.hue, hsv.sat, hsv.val, hsv.lum);
    return 0;
}
