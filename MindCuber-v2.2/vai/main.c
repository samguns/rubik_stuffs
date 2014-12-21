#include <stdio.h>

#define NFACE           6
#define POS(FF, OO) (((FF)*8)+(OO))

const long cmax = 1024;

int clr_map[] = {0, 1, 2, 3, 4, 5};
int clr_ord[NFACE * 4];

int  sc_r[NFACE*9];
int  sc_g[NFACE*9];
int  sc_b[NFACE*9];
int  sc_h[NFACE*9];
int  sc_s[NFACE*9];
int  sc_l[NFACE*9];
int  sc_sl[NFACE*9];
int sc_clr[NFACE * 9];

#define CMP_H    0
#define CMP_S    1
#define CMP_SL   2
#define CMP_SLR  3
#define CMP_L    4
#define CMP_LR   5
#define CMP_R_G  6
#define CMP_R_B  7
#define CMP_B_G  8

#define CLR_R     0
#define CLR_B     1
#define CLR_O     2
#define CLR_G     3
#define CLR_W     4
#define CLR_Y     5

#define CHR_R    'r'
#define CHR_B    'b'
#define CHR_O    'o'
#define CHR_G    'g'
#define CHR_W    'w'
#define CHR_Y    'y'

char clr_chr[] = {CHR_R, CHR_B, CHR_O, CHR_G, CHR_W, CHR_Y};

void scan_result(void)
{
    sc_r[29] = 378;
    sc_g[29] = 392;
    sc_b[29] = 371;
    sc_h[29] = 484;
    sc_s[
}

int clr_ratio(long c0, long c1)
{
    int ratio;

    if (c0 < c1)
        ratio = -(2000 * (c1-c0) / (c1+c0));
    else if (c0 > c1)
        ratio = (2000 * (c0-c1) / (c1+c0));
    else
        ratio = 0;

    return ratio;
}

int compare_clrs(const int cmp_fn, const int c0, const int c1)
{
    int cmp = 0;

    switch (cmp_fn)
    {
        case CMP_H:
            cmp = ((sc_h[c1] > sc_h[c0]) ? 1 : 0);
            break;
        case CMP_S:
            cmp = ((sc_s[c1] > sc_s[c0]) ? 1 : 0);
            break;
        case CMP_SL:
            cmp = ((sc_sl[c1] > sc_sl[c0]) ? 1 : 0);
            break;
        case CMP_SLR:
            cmp = ((sc_sl[c1] < sc_sl[c0]) ? 1 : 0);
            break;
        case CMP_L:
            cmp = ((sc_l[c1] > sc_l[c0]) ? 1 : 0);
            break;
        case CMP_LR:
            cmp = ((sc_l[c1] < sc_l[c0]) ? 1 : 0);
            break;
        case CMP_R_G:
            cmp = (clr_ratio(sc_r[c1], sc_g[c1]) <
                    clr_ratio(sc_r[c0], sc_g[c0]) ? 1 : 0);
            break;
        case CMP_R_B:
            cmp = (clr_ratio(sc_r[c1], sc_b[c1]) <
                    clr_ratio(sc_r[c0], sc_b[c0]) ? 1 : 0);
            break;
        case CMP_B_G:
            cmp = (clr_ratio(sc_b[c1], sc_g[c1]) <
                    clr_ratio(sc_b[c0], sc_g[c0]) ? 1 : 0);
            break;
        default:
            break;
    }

    return cmp;
}

void sort_clrs(int *co, const int s, const int n, const int cmp_fn)
{
    const int e = s + n - 2;
    int is = s;
    int ie = e;

    do
    {
        int il = e + 2;
        int ih = s - 2;
        int i;

        for (i = is; i <= ie; i++)
        {
            if (compare_clrs(cmp_fn, co[i+1], co[i]))
            {
                int o = co[i];

                co[i] = co[i+1];
                co[i+1] = o;

                if (i < il)
                    il = i;

                if (i > ih)
                    ih = i;
            }
        }

        is = il - 1;
        if (is < s)
            is = s;

        ie = ih + 1;
        if (ie > e)
            ie = e;
    }while (is <= ie);

    return;
}

void sort_colors(int *co, int t, int s)
{
    int i;
    sort_clrs(co, 0 * s, 6 * s, CMP_LR);
    sort_clrs(co, 0 * s, 3 * s, CMP_SL);

    sort_clrs(co, 1*s, 5*s, CMP_H);

    switch (t)
    {
        case 0:
            break;
        case 1:
            sort_clrs(co, 1 * s, 2 * s, CMP_R_G);
            break;
        case 2:
            sort_clrs(co, 1 * s, 2 * s, CMP_B_G);
            break;
        case 3:
            sort_clrs(co, 1 * s, 2 * s, CMP_R_B);
            break;
        case 4:
            sort_clrs(co, 1 * s, 2 * s, CMP_SLR);
            break;
        case 5:
            sort_clrs(co, 1 * s, 2 * s, CMP_L);
            break;
        default:
            break;
    }

    for (i = 0; i < s; i++)
    {
        sc_clr[co[i]] = CLR_W;
    }

    for (; i < 2 * s; i++)
    {
        sc_clr[co[i]] = CLR_R;
    }

    for (; i < 3 * s; i++)
    {
        sc_clr[co[i]] = CLR_O;
    }

    for (; i < 4 * s; i++)
    {
        sc_clr[co[i]] = CLR_Y;
    }

    for (; i < 5 * s; i++)
    {
        sc_clr[co[i]] = CLR_G;
    }

    for (; i < 6 * s; i++)
    {
        sc_clr[co[i]] = CLR_B;
    }

    return;
}

void determine_colors(int *cu, int t)
{
    int i, f, o;

    for (i = 0; i < NFACE; i++)
        clr_ord[i] = 9 * i + 8;

    sort_colors(clr_ord, t, 1);

    for (i = 0; i < NFACE; i++)
    {
        clr_ord[4*i+0] = 9*i+0;
        clr_ord[4*i+1] = 9*i+2;
        clr_ord[4*i+2] = 9*i+4;
        clr_ord[4*i+3] = 9*i+6;
    }

    sort_colors(clr_ord, t, 4);

    for (i = 0; i < NFACE; i++)
    {
        clr_ord[4*i+0] = 9*i+1;
        clr_ord[4*i+1] = 9*i+3;
        clr_ord[4*i+2] = 9*i+5;
        clr_ord[4*i+3] = 9*i+7;
    }

    sort_colors(clr_ord, t, 4);

    for (f = 0; f < NFACE; f++)
        clr_map[sc_clr[f*9+8]] = f;

    clr_chr[clr_map[CLR_R]] = CHR_R;
    clr_chr[clr_map[CLR_B]] = CHR_B;
    clr_chr[clr_map[CLR_O]] = CHR_O;
    clr_chr[clr_map[CLR_G]] = CHR_G;
    clr_chr[clr_map[CLR_W]] = CHR_W;
    clr_chr[clr_map[CLR_Y]] = CHR_Y;

    for (f = 0; f < NFACE; f++)
    {
        for (o = 0; o < 8; o++)
        {
            cu[POS(f, o)] = clr_map[sc_clr[f*9+o]];
        }
    }

    return;
}

void init_cube(int *cube)
{
    int o = 0;
    int i, f;
    for (f = 0; f < NFACE; f++)
    {
        for (i = 0; i < 8; i++)
            cube[o++] = f;
    }
}

int main(int argc, char *argv[])
{
    int cube[48];
    int i;

    init_cube(cube);

    scan_result();

	for (i = 0; i < 6; i++)
	{
	    determine_colors(cube, i);
	}

	return 0;
}
