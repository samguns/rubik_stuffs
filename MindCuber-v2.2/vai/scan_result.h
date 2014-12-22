#ifndef SCAN_RESULT_H
#define SCAN_RESULT_H

#define NFACE           6

int  sc_r[NFACE*9];
int  sc_g[NFACE*9];
int  sc_b[NFACE*9];
int  sc_h[NFACE*9];
int  sc_s[NFACE*9];
int  sc_l[NFACE*9];
int  sc_sl[NFACE*9];
int sc_clr[NFACE * 9];

void scan_result(void);

#endif /* SCAN_RESULT_H */

