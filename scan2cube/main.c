#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CLR_R     0
#define CLR_B     1
#define CLR_O     2
#define CLR_G     3
#define CLR_W     4
#define CLR_Y     5

/*
#define U        0
#define F        1
#define D        2
#define B        3
#define R        4
#define L        5
*/
#define U        3
#define F        2
#define D        1
#define B        0
#define R        5
#define L        4

static char scan_table_chars[54];
static int scan_table_ints[54];
static int cube[48];
static int pieces_valid = 0;
static int valid_i = 0;

static void init_Ug(void)
{
    scan_table_chars[27] = 'g';
    scan_table_chars[28] = 'g';
    scan_table_chars[29] = 'g';
    scan_table_chars[30] = 'g';
    scan_table_chars[31] = 'g';
    scan_table_chars[32] = 'g';
    scan_table_chars[33] = 'g';
    scan_table_chars[34] = 'g';
    scan_table_chars[35] = 'g';
}

static void init_Fo(void)
{
    scan_table_chars[18] = 'o';
    scan_table_chars[19] = 'o';
    scan_table_chars[20] = 'w';
    scan_table_chars[21] = 'w';
    scan_table_chars[22] = 'w';
    scan_table_chars[23] = 'o';
    scan_table_chars[24] = 'o';
    scan_table_chars[25] = 'o';
    scan_table_chars[26] = 'o';
}

static void init_Db(void)
{
    scan_table_chars[9] = 'b';
    scan_table_chars[10] = 'b';
    scan_table_chars[11] = 'b';
    scan_table_chars[12] = 'b';
    scan_table_chars[13] = 'b';
    scan_table_chars[14] = 'b';
    scan_table_chars[15] = 'b';
    scan_table_chars[16] = 'b';
    scan_table_chars[17] = 'b';
}

static void init_Br(void)
{
    scan_table_chars[0] = 'y';
    scan_table_chars[1] = 'r';
    scan_table_chars[2] = 'r';
    scan_table_chars[3] = 'r';
    scan_table_chars[4] = 'r';
    scan_table_chars[5] = 'r';
    scan_table_chars[6] = 'y';
    scan_table_chars[7] = 'y';
    scan_table_chars[8] = 'r';
}

static void init_Lw(void)
{
    scan_table_chars[36] = 'w';
    scan_table_chars[37] = 'w';
    scan_table_chars[38] = 'w';
    scan_table_chars[39] = 'w';
    scan_table_chars[40] = 'r';
    scan_table_chars[41] = 'r';
    scan_table_chars[42] = 'r';
    scan_table_chars[43] = 'w';
    scan_table_chars[44] = 'w';
}

static void init_Ry(void)
{
    scan_table_chars[45] = 'y';
    scan_table_chars[46] = 'y';
    scan_table_chars[47] = 'y';
    scan_table_chars[48] = 'y';
    scan_table_chars[49] = 'o';
    scan_table_chars[50] = 'o';
    scan_table_chars[51] = 'o';
    scan_table_chars[52] = 'y';
    scan_table_chars[53] = 'y';
}

static void char2int(void)
{
    int i;

    for (i = 0; i < 54; i++)
    {
        switch (scan_table_chars[i])
        {
        case 'r':
            scan_table_ints[i] = 0;
            break;

        case 'b':
            scan_table_ints[i] = 1;
            break;

        case 'o':
            scan_table_ints[i] = 2;
            break;

        case 'g':
            scan_table_ints[i] = 3;
            break;

        case 'w':
            scan_table_ints[i] = 4;
            break;

        case 'y':
            scan_table_ints[i] = 5;
            break;

        default:
            break;
        }
    }

    return;
}

#define POS(FF, OO) (((FF)*8)+(OO))

#define FIND_EDGE(F0, O0, F1, O1, I0, I1) \
  e0 = cube[POS(F0, O0)]; \
  if (e0 == f0) { \
    if (cube[POS(F1, O1)] == f1) return I1; \
  } else if (e0 == f1) { \
    if (cube[POS(F1, O1)] == f0) return I0; \
  }

#define FIND_CORNER(F0, O0, F1, O1, F2, O2, I0, I1, I2) \
  c0 = cube[POS(F0, O0)]; \
  if (c0 == f0) { \
    if (cube[POS(F1, O1)] == f1 && \
        cube[POS(F2, O2)] == f2) return I2; \
  } else if (c0 == f2) { \
    if (cube[POS(F1, O1)] == f0 && \
        cube[POS(F2, O2)] == f1) return I1; \
  } else if (c0 == f1) { \
    if (cube[POS(F1, O1)] == f2 && \
        cube[POS(F2, O2)] == f0) return I0; \
  }

static int pesudo_find_corner(int *cube, int F0, int O0,
                              int F1, int O1,
                              int F2, int O2,
                              int I0, int I1, int I2,
                              int f0, int f1, int f2)
{
    int c0, pos, pos1, pos2;

    pos = POS(F0, O0);
    pos1 = POS(F1, O1);
    pos2 = POS(F2, O2);
    c0 = cube[pos];

    if (c0 == f0)
    {
        if ((cube[pos1] == f1) &&
            (cube[pos2] == f2))
        {
            return I2;
        }
    }
    else if (c0 == f2)
    {
        if ((cube[pos1] == f0) &&
            (cube[pos2] == f1))
        {
            return I1;
        }
    }
    else if (c0 == f1)
    {
        if ((cube[pos1] == f2) &&
            (cube[pos2] == f0))
        {
            return I0;
        }
    }
}

static int pesudo_find_edge(int *cube, int F0, int O0, int F1, int O1, int I0, int I1, int f0, int f1)
{
    int pos, pos1, e0;

    pos = POS(F0, O0);
    pos1 = POS(F1, O1);
    e0 = cube[pos];

    if (e0 == f0)
    {
        if (cube[pos1] == f1)
            return I1;
    }
    else if (e0 == f1)
    {
        if (cube[pos1] == f0)
            return I0;
    }
}

static int find_corner(int *cube, int f0, int f1, int f2)
{
    int c0;

    pesudo_find_corner(cube, U, 2, B, 4, R, 2, 0,  1,  2, f0, f1, f2);
    FIND_CORNER(U, 2, B, 4, R, 2, 0,  1,  2);

    pesudo_find_corner(cube, U, 0, L, 0, B, 6, 3,  4,  5, f0, f1, f2);
    FIND_CORNER(U, 0, L, 0, B, 6, 3,  4,  5);

    pesudo_find_corner(cube, U, 6, F, 0, L, 2, 6,  7,  8, f0, f1, f2);
    FIND_CORNER(U, 6, F, 0, L, 2, 6,  7,  8);

    pesudo_find_corner(cube, U, 4, R, 0, F, 2, 9,  10, 11, f0, f1, f2);
    FIND_CORNER(U, 4, R, 0, F, 2, 9,  10, 11);

    pesudo_find_corner(cube, D, 0, L, 4, F, 6, 12, 13, 14, f0, f1, f2);
    FIND_CORNER(D, 0, L, 4, F, 6, 12, 13, 14);

    pesudo_find_corner(cube, D, 6, B, 0, L, 6, 15, 16, 17, f0, f1, f2);
    FIND_CORNER(D, 6, B, 0, L, 6, 15, 16, 17);

    pesudo_find_corner(cube, D, 4, R, 4, B, 2, 18, 19, 20, f0, f1, f2);
    FIND_CORNER(D, 4, R, 4, B, 2, 18, 19, 20);

    pesudo_find_corner(cube, D, 2, F, 4, R, 6, 21, 22, 23, f0, f1, f2);
    FIND_CORNER(D, 2, F, 4, R, 6, 21, 22, 23);

    return -1;
}

static int find_edge(int *cube, int f0, int f1)
{
    int e0;

    pesudo_find_edge(cube, U, 3, B, 7, 0,  1, f0, f1);
    FIND_EDGE(U, 3, B, 7, 0,  1);

    pesudo_find_edge(cube, U, 1, L, 5, 2,  3, f0, f1);
    FIND_EDGE(U, 7, L, 1, 2,  3);

    pesudo_find_edge(cube, U, 7, F, 3, 4,  5, f0, f1);
    FIND_EDGE(U, 5, F, 1, 4,  5);

    pesudo_find_edge(cube, U, 5, R, 5, 6,  7, f0, f1);
    FIND_EDGE(U, 3, R, 1, 6,  7);

    pesudo_find_edge(cube, L, 3, F, 7, 8,  9, f0, f1);
    FIND_EDGE(L, 3, F, 7, 8,  9);

    pesudo_find_edge(cube, B, 7, L, 7, 10, 11, f0, f1);
    FIND_EDGE(B, 7, L, 7, 10, 11);

    pesudo_find_edge(cube, D, 7, L, 5, 12, 13, f0, f1);
    FIND_EDGE(D, 7, L, 5, 12, 13);

    pesudo_find_edge(cube, R, 3, B, 3, 14, 15, f0, f1);
    FIND_EDGE(R, 3, B, 3, 14, 15);

    pesudo_find_edge(cube, D, 5, B, 1, 16, 17, f0, f1);
    FIND_EDGE(D, 5, B, 1, 16, 17);

    pesudo_find_edge(cube, F, 3, R, 7, 18, 19, f0, f1);
    FIND_EDGE(F, 3, R, 7, 18, 19);

    pesudo_find_edge(cube, D, 3, R, 5, 20, 21, f0, f1);
    FIND_EDGE(D, 3, R, 5, 20, 21);

    pesudo_find_edge(cube, D, 1, F, 5, 22, 23, f0, f1);
    FIND_EDGE(D, 1, F, 5, 22, 23);

    return -1;
}

static int valid_pieces(int *cube)
{
    return
        (find_edge(cube, U, F) >= 0) &&
        (find_edge(cube, U, L) >= 0) &&
        (find_edge(cube, U, B) >= 0) &&
        (find_edge(cube, U, R) >= 0) &&
        (find_edge(cube, F, L) >= 0) &&
        (find_edge(cube, L, B) >= 0) &&
        (find_edge(cube, B, R) >= 0) &&
        (find_edge(cube, R, F) >= 0) &&
        (find_edge(cube, D, F) >= 0) &&
        (find_edge(cube, D, L) >= 0) &&
        (find_edge(cube, D, B) >= 0) &&
        (find_edge(cube, D, R) >= 0) &&
        (find_corner(cube, U, F, L) >= 0) &&
        (find_corner(cube, U, L, B) >= 0) &&
        (find_corner(cube, U, B, R) >= 0) &&
        (find_corner(cube, U, R, F) >= 0) &&
        (find_corner(cube, D, F, R) >= 0) &&
        (find_corner(cube, D, R, B) >= 0) &&
        (find_corner(cube, D, B, L) >= 0) &&
        (find_corner(cube, D, L, F) >= 0);
}

int main()
{
    int f, o, i;

    init_Ug();
    init_Fo();
    init_Db();
    init_Br();
    init_Lw();
    init_Ry();
    char2int();

    for (f = 0; f < 6; f++)
    {
        for (o = 0; o < 8; o++)
        {
            cube[f*8+o] = scan_table_ints[f*9+o];
            printf("cube[%d] = %d;\n", (f*8+o), cube[f*8+o]);
        }
    }

    for (i = 0; i < 6; i++)
    {
        if (0 != valid_pieces(cube))
        {
            pieces_valid++;
            valid_i = i;
        }
    }
    printf("pieces_valid:%d\n", pieces_valid);
    return 0;
}
