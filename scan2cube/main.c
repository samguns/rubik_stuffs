#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mcmoves.h"

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
static int solve_n = 0;

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
    int c0, ret;

    ret = pesudo_find_corner(cube, U, 4, B, 6, R, 6, 0,  1,  2, f0, f1, f2);
    FIND_CORNER(U, 4, B, 6, R, 6, 0,  1,  2);

    ret = pesudo_find_corner(cube, U, 2, L, 4, B, 0, 3,  4,  5, f0, f1, f2);
    FIND_CORNER(U, 2, L, 4, B, 0, 3,  4,  5);

    ret = pesudo_find_corner(cube, U, 0, F, 2, L, 6, 6,  7,  8, f0, f1, f2);
    FIND_CORNER(U, 0, F, 2, L, 6, 6,  7,  8);

    ret = pesudo_find_corner(cube, U, 6, R, 4, F, 4, 9,  10, 11, f0, f1, f2);
    FIND_CORNER(U, 6, R, 4, F, 4, 9,  10, 11);

    ret = pesudo_find_corner(cube, D, 2, L, 0, F, 0, 12, 13, 14, f0, f1, f2);
    FIND_CORNER(D, 2, L, 0, F, 0, 12, 13, 14);

    ret = pesudo_find_corner(cube, D, 0, B, 2, L, 2, 15, 16, 17, f0, f1, f2);
    FIND_CORNER(D, 0, B, 2, L, 2, 15, 16, 17);

    ret = pesudo_find_corner(cube, D, 6, R, 0, B, 4, 18, 19, 20, f0, f1, f2);
    FIND_CORNER(D, 6, R, 0, B, 4, 18, 19, 20);

    ret = pesudo_find_corner(cube, D, 4, F, 6, R, 2, 21, 22, 23, f0, f1, f2);
    FIND_CORNER(D, 4, F, 6, R, 2, 21, 22, 23);

    return -1;
}

static int find_edge(int *cube, int f0, int f1)
{
    int e0, ret;

    ret = pesudo_find_edge(cube, U, 3, B, 7, 0,  1, f0, f1);
    FIND_EDGE(U, 3, B, 7, 0,  1);

    ret = pesudo_find_edge(cube, U, 1, L, 5, 2,  3, f0, f1);
    FIND_EDGE(U, 1, L, 5, 2,  3);

    ret = pesudo_find_edge(cube, U, 7, F, 3, 4,  5, f0, f1);
    FIND_EDGE(U, 7, F, 3, 4,  5);

    ret = pesudo_find_edge(cube, U, 5, R, 5, 6,  7, f0, f1);
    FIND_EDGE(U, 5, R, 5, 6,  7);

    ret = pesudo_find_edge(cube, L, 7, F, 1, 8,  9, f0, f1);
    FIND_EDGE(L, 7, F, 1, 8,  9);

    ret = pesudo_find_edge(cube, B, 1, L, 3, 10, 11, f0, f1);
    FIND_EDGE(B, 1, L, 3, 10, 11);

    ret = pesudo_find_edge(cube, D, 1, L, 1, 12, 13, f0, f1);
    FIND_EDGE(D, 1, L, 1, 12, 13);

    ret = pesudo_find_edge(cube, R, 7, B, 5, 14, 15, f0, f1);
    FIND_EDGE(R, 7, B, 5, 14, 15);

    ret = pesudo_find_edge(cube, D, 7, B, 3, 16, 17, f0, f1);
    FIND_EDGE(D, 7, B, 3, 16, 17);

    ret = pesudo_find_edge(cube, F, 5, R, 3, 18, 19, f0, f1);
    FIND_EDGE(F, 5, R, 3, 18, 19);

    ret = pesudo_find_edge(cube, D, 5, R, 1, 20, 21, f0, f1);
    FIND_EDGE(D, 5, R, 1, 20, 21);

    ret = pesudo_find_edge(cube, D, 3, F, 7, 22, 23, f0, f1);
    FIND_EDGE(D, 3, F, 7, 22, 23);

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

static int solve_fce[100];
static int solve_rot[100];
static int solve_cube[48];
static int mv_n;
static int mv_f[100];
static int mv_r[100];

static int opposite[] = {D, B, U, F, L, R};

static void copy_cube(int *cube0, int *cube1)
{
    int f, i, o;

    o = 0;
    for (f = 0; f < 6; f++)
    {
        for (i = 0; i < 8; i++)
        {
            cube0[o] = cube1[o];
            o++;
        }
    }
}

static int solved(int *cube)
{
    int i, o, f;

    o = 0;

    for (f = 0; f < 6; f++)
    {
        for (i = 0; i < 8; i++)
        {
            if (cube[o++] != f)
                return -1;
        }
    }

    return 0;
}

static int idx_ic;
static int idx_ie;
static int idx_idx[3];
static int idx_nc;
static int idx_ne;
static int idx;

static void index_init(void)
{
    idx_nc = 0;
    idx_ne = 0;
    idx = 0;
}

static void index_last(void)
{
    idx = ((idx >> 2) << 1) | (idx & 1);
}

static void index_edge(int *cube, int f0, int f1)
{
    int ie, i;

    ie = find_edge(cube, f0, f1);
    for (i = 0; i < idx_ne; i++)
    {
        if (ie > idx_idx[i])
            ie -= 2;
    }

    idx = (idx * idx_ie) + ie;
    idx_idx[idx_ne++] = ie;
    idx_ie -= 2;
}

static void index_corner(int *cube, int f0, int f1, int f2)
{
    int ic, i;

    ic = find_corner(cube, f0, f1, f2);
    for (i = 0; i < idx_nc; i++)
    {
        if (ic > idx_idx[i])
            ic -= 3;
    }

    idx = (idx * idx_ic) + ic;
    idx_idx[idx_nc++] = ic;
    idx_ic -= 3;
}

#define RFIX(RR) ((((RR)+1)&3)-1)

static void add_mv(int f, int r)
{
    int i, mrg, fi;

    mrg = 0;
    i = mv_n;

    while (i > 0)
    {
        i--;
        fi = mv_f[i];
        if (f == fi)
        {
            r += mv_r[i];
            r = RFIX(r);
            if (r != 0)
            {
                mv_r[i] = r;
            }
            else
            {
                mv_n--;
                while (i < mv_n)
                {
                    mv_f[i] = mv_f[i+1];
                    mv_r[i] = mv_f[i+1];
                    i++;
                }
            }
            mrg = 1;
            break;
        }

        if (opposite[f] != fi)
            break;
    }

    if (mrg == 0)
    {
        mv_f[mv_n] = f;
        mv_r[mv_n] = RFIX(r);
        mv_n++;
    }
}

static void rot_edges(int *cube, int r,
               int f0, int o0, int f1, int o1,
               int f2, int o2, int f3, int o3) {
  f0 *= 8;
  f1 *= 8;
  f2 *= 8;
  f3 *= 8;
  o0 += f0;
  o1 += f1;
  o2 += f2;
  o3 += f3;
  int p;
  switch (r) {
  case 1:
    p = cube[o3];
    cube[o3] = cube[o2];
    cube[o2] = cube[o1];
    cube[o1] = cube[o0];
    cube[o0] = p;
    o0 ++; o1 ++; o2 ++; o3 ++;
    p = cube[o3];
    cube[o3] = cube[o2];
    cube[o2] = cube[o1];
    cube[o1] = cube[o0];
    cube[o0] = p;
    o0 = f0+((o0+1)&7); o1 = f1+((o1+1)&7);
    o2 = f2+((o2+1)&7); o3 = f3+((o3+1)&7);
    p = cube[o3];
    cube[o3] = cube[o2];
    cube[o2] = cube[o1];
    cube[o1] = cube[o0];
    cube[o0] = p;
    break;

  case 2:
    p = cube[o0];
    cube[o0] = cube[o2];
    cube[o2] = p;
    p = cube[o1];
    cube[o1] = cube[o3];
    cube[o3] = p;
    o0 ++; o1 ++; o2 ++; o3 ++;
    p = cube[o0];
    cube[o0] = cube[o2];
    cube[o2] = p;
    p = cube[o1];
    cube[o1] = cube[o3];
    cube[o3] = p;
    o0 = f0+((o0+1)&7); o1 = f1+((o1+1)&7);
    o2 = f2+((o2+1)&7); o3 = f3+((o3+1)&7);
    p = cube[o0];
    cube[o0] = cube[o2];
    cube[o2] = p;
    p = cube[o1];
    cube[o1] = cube[o3];
    cube[o3] = p;
    break;

  case 3:
    p = cube[o0];
    cube[o0] = cube[o1];
    cube[o1] = cube[o2];
    cube[o2] = cube[o3];
    cube[o3] = p;
    o0 ++; o1 ++; o2 ++; o3 ++;
    p = cube[o0];
    cube[o0] = cube[o1];
    cube[o1] = cube[o2];
    cube[o2] = cube[o3];
    cube[o3] = p;
    o0 = f0+((o0+1)&7); o1 = f1+((o1+1)&7);
    o2 = f2+((o2+1)&7); o3 = f3+((o3+1)&7);
    p = cube[o0];
    cube[o0] = cube[o1];
    cube[o1] = cube[o2];
    cube[o2] = cube[o3];
    cube[o3] = p;
    break;

  default:
    printf("Error rot_edges:%d\n", r);
  }
}

static void rotate(int *cube, int f, int r) {
  r &= 3;
  switch (f) {
/*
  case U:  rot_edges(cube, r, B, 4, R, 0, F, 0, L, 0); break;
  case F:  rot_edges(cube, r, U, 4, R, 6, D, 0, L, 2); break;
  case D:  rot_edges(cube, r, F, 4, R, 4, B, 0, L, 4); break;
  case B:  rot_edges(cube, r, D, 4, R, 2, U, 0, L, 6); break;
  case R:  rot_edges(cube, r, U, 2, B, 2, D, 2, F, 2); break;
  case L:  rot_edges(cube, r, U, 6, F, 6, D, 6, B, 6); break;
*/
  case 0:  rot_edges(cube, r, B, 6, R, 4, F, 2, L, 4); break;
  case 1:  rot_edges(cube, r, U, 6, R, 2, D, 2, L, 6); break;
  case 2:  rot_edges(cube, r, F, 6, R, 0, B, 2, L, 0); break;
  case 3:  rot_edges(cube, r, D, 4, R, 2, U, 0, L, 6); break;
  case 4:  rot_edges(cube, r, U, 2, B, 2, D, 2, F, 2); break;
  case 5:  rot_edges(cube, r, U, 6, F, 6, D, 6, B, 6); break;
  default: printf("Error rot face:%d\n", f);
  }
  f *= 8;
  int p;
  switch (r) {
  case 1:
    p         = cube[f+7];
    cube[f+7] = cube[f+5];
    cube[f+5] = cube[f+3];
    cube[f+3] = cube[f+1];
    cube[f+1] = p;
    p         = cube[f+6];
    cube[f+6] = cube[f+4];
    cube[f+4] = cube[f+2];
    cube[f+2] = cube[f];
    cube[f]   = p;
    break;

  case 2:
    p         = cube[f+1];
    cube[f+1] = cube[f+5];
    cube[f+5] = p;
    p         = cube[f+3];
    cube[f+3] = cube[f+7];
    cube[f+7] = p;
    p         = cube[f];
    cube[f]   = cube[f+4];
    cube[f+4] = p;
    p         = cube[f+2];
    cube[f+2] = cube[f+6];
    cube[f+6] = p;
    break;

  case 3:
    p         = cube[f+1];
    cube[f+1] = cube[f+3];
    cube[f+3] = cube[f+5];
    cube[f+5] = cube[f+7];
    cube[f+7] = p;
    p         = cube[f];
    cube[f]   = cube[f+2];
    cube[f+2] = cube[f+4];
    cube[f+4] = cube[f+6];
    cube[f+6] = p;
    break;

  default:
    printf("Error rot:%d\n", r);
  }
}

static void solve_phase(int *cube, int mtb, const unsigned char *mtd, int mtd_size, int dorot)
{
    int sz, i, b;

    sz = mtd_size / mtb;
    idx = sz - idx;

    if (idx > 0)
    {
        i = (idx - 1) * mtb;
        b = mtd[i++];

        if (b != 0xFF)
        {
            int mvm, mv, f0, r0, b0, f1;

            mvm = mtb * 2 - 1;
            mv = 0;
            f0 = b/3;
            r0 = RFIX(b-(f0 *3) + 1);

            add_mv(f0, r0);
            if (dorot)
                rotate(cube, f0, r0);

            mv++;

            while(mv < mvm)
            {
                b >>= 4;
                if ((mv & 1) != 0)
                    b = mtd[i++];

                b0 = b & 0x0F;
                if (b0 == 0x0F)
                    break;

                f1 = b0 / 3;
                r0 = RFIX(b0-(f1*3)+1);
                if (f1 >= f0)
                    f1++;

                f0 = f1;
                add_mv(f0, r0);
                if (dorot)
                    rotate(cube, f0, r0);

                mv++;
            }
        }
    }
}

static void solve_one(int *cube, int dorot)
{
    mv_n = 0;

    idx_ic = 24;
    idx_ie = 24;

    index_init();
    index_edge(cube, D, F);
    index_edge(cube, D, R);
    solve_phase(cube, mtb0, mtd0, sizeof(mtd0), dorot);

    index_init();
    index_corner(cube, D, F, R);
    index_edge(cube, F, R);
    solve_phase(cube, mtb1, mtd1, sizeof(mtd1), dorot);

    index_init();
    index_edge(cube, D, B);
    solve_phase(cube, mtb2, mtd2, sizeof(mtd2), dorot);

    index_init();
    index_corner(cube, D, R, B);
    index_edge(cube, R, B);
    solve_phase(cube, mtb3, mtd3, sizeof(mtd3), dorot);

    index_init();
    index_edge(cube, D, L);
    solve_phase(cube, mtb4, mtd4, sizeof(mtd4), dorot);

    index_init();
    index_corner(cube, D, B, L);
    index_edge(cube, B, L);
    solve_phase(cube, mtb5, mtd5, sizeof(mtd5), dorot);

    index_init();
    index_corner(cube, D, L, F);
    index_edge(cube, L, F);
    solve_phase(cube, mtb6, mtd6, sizeof(mtd6), dorot);

    index_init();
    index_corner(cube, U, R, F);
    index_corner(cube, U, F, L);
    index_corner(cube, U, L, B);
    solve_phase(cube, mtb7, mtd7, sizeof(mtd7), dorot);

    index_init();
    index_edge(cube, U, R);
    index_edge(cube, U, F);
    index_edge(cube, U, L);
    index_last();
    solve_phase(cube, mtb8, mtd8, sizeof(mtd8), dorot);
}

static int solve_nomap(int *cube)
{
    int i, ret;

    solve_n = 0;
    copy_cube(solve_cube, cube);
    solve_one(solve_cube, 1);

    ret = solved(solve_cube);
    if (ret != 0)
        return -1;

    solve_n = mv_n;
    for (i = 0; i < mv_n; i++)
    {
        solve_fce[i] = mv_f[i];
        solve_rot[i] = mv_r[i];
    }

    return 0;
}

#define TARGET  42

static int solve(int *cube)
{
    int ret;

    ret = solve_nomap(cube);
    if (ret != 0)
        return -1;

    if (solve_n <= TARGET)
        return 0;

    return -1;
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
            int ret;
            pieces_valid++;
            valid_i = i;

            ret = solve(cube);
            printf("i:%d solve:%d\n", i, ret);
            if (ret == 0)
            {
                printf("Cube solved\n");
            }
        }
    }
    printf("pieces_valid:%d\n", pieces_valid);
    return 0;
}
