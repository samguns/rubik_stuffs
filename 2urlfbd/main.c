#include <stdio.h>
#include <stdlib.h>

/*++++++++++++++++The layout of the facelets on the cube+++++++++++++++++++++++

             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
|************|************|************|************|
|*L1**L2**L3*|*F1**F2**F3*|*R1**R2**F3*|*B1**B2**B3*|
|************|************|************|************|
|*L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*|
|************|************|************|************|
|*L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*|
|************|************|************|************|
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|
*/
//++++++++++++Mapping this definition string to facelets+++++++++++++++++++++++
//The definiton string of the Identity cube in Singmaster notation is
//++++ UF UR UB UL DF DR DB DL FR FL BR BL UFR URB UBL ULF DRF DFL DLB DBR ++++
/*
const Facelet SingmasterToFacelet[48] =
{   U8,F2,U6,R2,U2,B2,U4,L2,D2,F8,D6,R8,D8,B8,D4,L8,F6,R4,F4,L6,B4,R6,B6,L4,
    U9,F3,R1,U3,R3,B1,U1,B3,L1,U7,L3,F1,D3,R7,F9,D1,F7,L9,D7,L7,B9,D9,B7,R9};
*/
#define U       0
#define F       1
#define D       2
#define B       3
#define R       4
#define L       5

#define X1      0
#define X2      1
#define X3      2
#define X4      3
#define X5      4
#define X6      5
#define X7      6
#define X8      7
#define X9      8

static char rgb_chars[6][9] =
{
    { // U  -- 0
        'g', 'w', 'g', 'r', 'g', 'o', 'b', 'o', 'o'
    },
    { // F  -- 1
        'y', 'w', 'w', 'y', 'w', 'b', 'y', 'w', 'w'
    },
    { // D  -- 2
        'g', 'r', 'r', 'o', 'b', 'r', 'o', 'o', 'o'
    },
    { // B  -- 3
        'w', 'b', 'w', 'g', 'y', 'g', 'y', 'y', 'y'
    },
    { // R  -- 4
        'b', 'b', 'r', 'y', 'o', 'w', 'b', 'b', 'g'
    },
    { // L  -- 5
        'o', 'g', 'r', 'y', 'r', 'r', 'b', 'g', 'r'
    }
};

static int rgb_ints[6][9] = {};

static void rgb_chars_2_ints(void)
{
    int i, j;

    for (i = 0; i < 6; i++)
    {
        for (j = 0; j < 9; j++)
        {
            if (rgb_chars[i][j] == rgb_chars[0][4])
                rgb_ints[i][j] = 0;
            else if (rgb_chars[i][j] == rgb_chars[1][4])
                rgb_ints[i][j] = 1;
            else if (rgb_chars[i][j] == rgb_chars[2][4])
                rgb_ints[i][j] = 2;
            else if (rgb_chars[i][j] == rgb_chars[3][4])
                rgb_ints[i][j] = 3;
            else if (rgb_chars[i][j] == rgb_chars[4][4])
                rgb_ints[i][j] = 4;
            else if (rgb_chars[i][j] == rgb_chars[5][4])
                rgb_ints[i][j] = 5;
            else
                rgb_ints[i][j] = 100;
        }
    }

    return;
}

static char int_2_facelet(int idx)
{
    char retval = 0;

    switch (idx)
    {
        case 0:
            retval = 'U';
            break;
        case 1:
            retval = 'F';
            break;
        case 2:
            retval = 'D';
            break;
        case 3:
            retval = 'B';
            break;
        case 4:
            retval = 'R';
            break;
        case 5:
            retval = 'L';
            break;
        default:
            break;
    }

    return retval;
}

/* UF UR UB UL  DF DR DB DL  FR FL BR BL  UFR URB UBL ULF  DRF DFL DLB DBR
 * UF == U8,F2
 * UR == U6,R2
 * UB == U2,B2
 * UL == U4,L2
 *
 * DF == D2,F8
 * DR == D6,R8
 * DB == D8,B8
 * DL == D4,L8
 *
 * FR == F6,R4
 * FL == F4,L6
 * BR == B4,R6
 * BL == B6,L4
 *
 * UFR == U9,F3,R1
 * URB == U3,R3,B1
 * UBL == U1,B3,L1
 * ULF == U7,L3,F1
 *
 * DRF == D3,R7,F9
 * DFL == D1,F7,L9
 * DLB == D7,L7,B9
 * DBR == D9,B7,R9
 */

int main()
{
    int i, j;
    printf("Hello world!\n");

    rgb_chars_2_ints();
    for (i = 0; i < 6; i++)
    {
        for (j = 0; j < 9; j++)
        {
            printf("%d, ", rgb_ints[i][j]);
        }
        printf("\n");
    }

    // UF == U8,F2
    printf("%c%c ", int_2_facelet(rgb_ints[U][X8]),
                    int_2_facelet(rgb_ints[F][X2]));
    // UR == U6,R2
    printf("%c%c ", int_2_facelet(rgb_ints[U][X6]),
                    int_2_facelet(rgb_ints[R][X2]));
    // UB == U2,B2
    printf("%c%c ", int_2_facelet(rgb_ints[U][X2]),
                    int_2_facelet(rgb_ints[B][X2]));
    // UL == U4,L2
    printf("%c%c ", int_2_facelet(rgb_ints[U][X4]),
                    int_2_facelet(rgb_ints[L][X2]));

    // DF == D2,F8
    printf("%c%c ", int_2_facelet(rgb_ints[D][X2]),
                    int_2_facelet(rgb_ints[F][X8]));
    // DR == D6,R8
    printf("%c%c ", int_2_facelet(rgb_ints[D][X6]),
                    int_2_facelet(rgb_ints[R][X8]));
    // DB == D8,B8
    printf("%c%c ", int_2_facelet(rgb_ints[D][X8]),
                    int_2_facelet(rgb_ints[B][X8]));
    // DL == D4,L8
    printf("%c%c ", int_2_facelet(rgb_ints[D][X4]),
                    int_2_facelet(rgb_ints[L][X8]));

    // FR == F6,R4
    printf("%c%c ", int_2_facelet(rgb_ints[F][X6]),
                    int_2_facelet(rgb_ints[R][X4]));
    // FL == F4,L6
    printf("%c%c ", int_2_facelet(rgb_ints[F][X4]),
                    int_2_facelet(rgb_ints[L][X6]));
    // BR == B4,R6
    printf("%c%c ", int_2_facelet(rgb_ints[B][X4]),
                    int_2_facelet(rgb_ints[R][X6]));
    // BL == B6,L4
    printf("%c%c ", int_2_facelet(rgb_ints[B][X6]),
                    int_2_facelet(rgb_ints[L][X4]));

    // UFR == U9,F3,R1
    printf("%c%c%c ",   int_2_facelet(rgb_ints[U][X9]),
                        int_2_facelet(rgb_ints[F][X3]),
                        int_2_facelet(rgb_ints[R][X1]));
    // URB == U3,R3,B1
    printf("%c%c%c ",   int_2_facelet(rgb_ints[U][X3]),
                        int_2_facelet(rgb_ints[R][X3]),
                        int_2_facelet(rgb_ints[B][X1]));
    // UBL == U1,B3,L1
    printf("%c%c%c ",   int_2_facelet(rgb_ints[U][X1]),
                        int_2_facelet(rgb_ints[B][X3]),
                        int_2_facelet(rgb_ints[L][X1]));
    // ULF == U7,L3,F1
    printf("%c%c%c ",   int_2_facelet(rgb_ints[U][X7]),
                        int_2_facelet(rgb_ints[L][X3]),
                        int_2_facelet(rgb_ints[F][X1]));

    // DRF == D3,R7,F9
    printf("%c%c%c ",   int_2_facelet(rgb_ints[D][X3]),
                        int_2_facelet(rgb_ints[R][X7]),
                        int_2_facelet(rgb_ints[F][X9]));
    // DFL == D1,F7,L9
    printf("%c%c%c ",   int_2_facelet(rgb_ints[D][X1]),
                        int_2_facelet(rgb_ints[F][X7]),
                        int_2_facelet(rgb_ints[L][X9]));
    // DLB == D7,L7,B9
    printf("%c%c%c ",   int_2_facelet(rgb_ints[D][X7]),
                        int_2_facelet(rgb_ints[L][X7]),
                        int_2_facelet(rgb_ints[B][X9]));
    // DBR == D9,B7,R9
    printf("%c%c%c ",   int_2_facelet(rgb_ints[D][X9]),
                        int_2_facelet(rgb_ints[B][X7]),
                        int_2_facelet(rgb_ints[R][X9]));

    return 0;
}
