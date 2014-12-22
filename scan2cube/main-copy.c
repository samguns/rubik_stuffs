#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CLR_R     0
#define CLR_B     1
#define CLR_O     2
#define CLR_G     3
#define CLR_W     4
#define CLR_Y     5

static char scan_table_chars[54];
static int scan_table_ints[54];
static int cube[48];

static void init_Ug(void)
{
    scan_table_chars[27] = 'b';
    scan_table_chars[28] = 'w';
    scan_table_chars[29] = 'w';
    scan_table_chars[30] = 'r';
    scan_table_chars[31] = 'g';
    scan_table_chars[32] = 'r';
    scan_table_chars[33] = 'b';
    scan_table_chars[34] = 'y';
    scan_table_chars[35] = 'g';
}

static void init_Fo(void)
{
    scan_table_chars[18] = 'g';
    scan_table_chars[19] = 'o';
    scan_table_chars[20] = 'o';
    scan_table_chars[21] = 'g';
    scan_table_chars[22] = 'r';
    scan_table_chars[23] = 'b';
    scan_table_chars[24] = 'y';
    scan_table_chars[25] = 'o';
    scan_table_chars[26] = 'o';
}

static void init_Db(void)
{
    scan_table_chars[9] = 'r';
    scan_table_chars[10] = 'y';
    scan_table_chars[11] = 'r';
    scan_table_chars[12] = 'g';
    scan_table_chars[13] = 'g';
    scan_table_chars[14] = 'b';
    scan_table_chars[15] = 'w';
    scan_table_chars[16] = 'w';
    scan_table_chars[17] = 'b';
}

static void init_Br(void)
{
    scan_table_chars[0] = 'b';
    scan_table_chars[1] = 'r';
    scan_table_chars[2] = 'g';
    scan_table_chars[3] = 'b';
    scan_table_chars[4] = 'r';
    scan_table_chars[5] = 'g';
    scan_table_chars[6] = 'o';
    scan_table_chars[7] = 'y';
    scan_table_chars[8] = 'r';
}

static void init_Lw(void)
{
    scan_table_chars[36] = 'y';
    scan_table_chars[37] = 'o';
    scan_table_chars[38] = 'w';
    scan_table_chars[39] = 'b';
    scan_table_chars[40] = 'o';
    scan_table_chars[41] = 'r';
    scan_table_chars[42] = 'y';
    scan_table_chars[43] = 'w';
    scan_table_chars[44] = 'w';
}

static void init_Ry(void)
{
    scan_table_chars[45] = 'b';
    scan_table_chars[46] = 'y';
    scan_table_chars[47] = 'o';
    scan_table_chars[48] = 'o';
    scan_table_chars[49] = 'y';
    scan_table_chars[50] = 'g';
    scan_table_chars[51] = 'w';
    scan_table_chars[52] = 'w';
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

int main()
{
    int f, o;

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
    printf("\n");
    return 0;
}
