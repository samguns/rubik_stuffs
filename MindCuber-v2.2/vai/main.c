#include <stdio.h>
#include <stdlib.h>

#define NFACE       6

void init_cube(unsigned char *cube)
{
    int o = 0;
    unsigned char f;
    int i;
    for (f = 0; f < NFACE; f++)
    {
        for (i = 0; i < 8; i++)
            cube[o++] = f;
    }
}

int main()
{
    unsigned char cube[NFACE * 8];
    int i;

    init_cube(cube);

    for (i = 0; i < NFACE * 8; i++)
    {
        printf("%d  ", cube[i]);
    }
    printf("\n");
    return 0;
}
