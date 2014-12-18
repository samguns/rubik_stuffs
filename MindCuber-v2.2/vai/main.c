#include <SDL.h>
#include <SDL_thread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef bool
typedef unsigned char       bool;
#endif // bool

#ifndef true
#define true        1
#endif // true
#ifndef false
#define false       0
#endif // false

#define NFACE       6

#define NMOTORS     3
#define  OUT_A   0x00
#define  OUT_B   0x01
#define  OUT_C   0x02
#define  OUT_AB   0x03
#define  OUT_AC   0x04
#define  OUT_BC   0x05
#define  OUT_ABC   0x06

#define M_DELAY     10
#define M_SCALE     12
#define AMAX        24
#define VMAX        100

#define P_LOW       35
#define P_HIGH      87

#define  RESET_NONE   0x00
#define  RESET_COUNT   0x08
#define  RESET_BLOCK_COUNT   0x20
#define  RESET_ROTATION_COUNT   0x40
#define  RESET_BLOCKANDTACHO   0x28
#define  RESET_ALL   0x68


static int tacho_A = 0;
static int tacho_B = 0;
static int tacho_C = 0;

SDL_mutex *motor_mtx = NULL;
bool quit = false;

const unsigned char mmot[] = {OUT_A, OUT_B, OUT_C};
bool mon[] = {false, false, false};
bool mgo[] = {false, false, false};
bool mup[] = {false, false, false};

long mtx[] = {0, 0, 0};
long mx[] = {0, 0, 0};
long mv[] = {0, 0, 0};
long ma[] = {0, 0, 0};
long mp[] = {0, 0, 0};
long me[] = {0, 0, 0};

static int MotorTachoCount(int motor)
{
    int retval = 0;

    switch (motor)
    {
    case OUT_A:
        retval = tacho_A;
        break;
    case OUT_B:
        retval = tacho_B;
        break;
    case OUT_C:
        retval = tacho_C;
        break;
    default:
        break;
    }

    return retval;
}

static void OnFwdEx(int motor, int power, int reset)
{
    switch (motor)
    {
    case OUT_A:
        if (reset == RESET_NONE)
            tacho_A += 1;
        else
            tacho_A = 0;
        break;

    case OUT_B:
        if (reset == RESET_NONE)
            tacho_B += 1;
        else
            tacho_B = 0;
        break;

    case OUT_C:
        if (reset == RESET_NONE)
            tacho_C += 1;
        else
            tacho_C = 0;
        break;

    default:
        break;
    }

    return;
}

static void OnRevEx(int motor, int power, int reset)
{
    switch (motor)
    {
    case OUT_A:
        if (reset == RESET_NONE)
            tacho_A -= 1;
        else
            tacho_A = 0;
        break;

    case OUT_B:
        if (reset == RESET_NONE)
            tacho_B -= 1;
        else
            tacho_B = 0;
        break;

    case OUT_C:
        if (reset == RESET_NONE)
            tacho_C -= 1;
        else
            tacho_C = 0;
        break;

    default:
        break;
    }

    return;
}

static void OffEx(int motor, int reset)
{
    return;
}

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

static int motor_task(void *ptr)
{
    Uint32 ms = SDL_GetTicks();

    while (quit == false)
    {
        int m;
        SDL_LockMutex(motor_mtx);
        for (m = 0; m < NMOTORS; m++)
        {
            if (mon[m])
            {
                bool rev = false;
                unsigned char mot = mmot[m];
                long x = mx[m];
                long v = mv[m];
                long a = ma[m];
                long p = mp[m];
                long e = 0;
                long ax = M_SCALE * MotorTachoCount(mot);
                long ex = ax - x;

                if (-M_SCALE < ex && ex < M_SCALE)
                    ax = x;
                else if (mgo[m])
                    e = me[m] - ex;

                long d = mtx[m] - ax;

                if (mup[m] ? (d < M_SCALE) : (d > -M_SCALE))
                {
                    mgo[m] = false;
                    e = 0;
                }
                if (d < 0)
                {
                    d = -d;
                    v = -v;
                    a = -a;
                    p = -p;
                    e = -e;
                    rev = true;
                }

                if (d >= M_SCALE)
                {
                    if (v >= 0)
                    {
                        long dd = (v + AMAX / 2) + (v * v) / (2 * AMAX);
                        if (d >= dd)
                        {
                            p = P_HIGH;
                            a = (AMAX * (VMAX - v)) / VMAX;
                            e = 0;
                        }
                        else
                        {
                            a = -(v * v) / (2 *d);
                            if (a < -v)
                                a = -v;
                            if (a < -AMAX)
                                a = -AMAX;
                            p = (P_HIGH * a * (VMAX - v)) / (AMAX * VMAX);
                        }
                    }
                    else
                    {
                        a = -v;
                        if (a > AMAX)
                            a = AMAX;
                        p = (P_HIGH * a * (VMAX - v)) / (AMAX * VMAX);
                    }
                }
                else
                {
                    a = -v;
                    if (a < -AMAX)
                        a = -AMAX;
                    else if (a > AMAX)
                        a = AMAX;
                    p = (P_HIGH * a) / AMAX;
                }
                d = v + a / 2;
                v += a;
                p += e;
                if (p > P_HIGH)
                {
                    p = P_HIGH;
                    e = 0;
                }
                else if (p < -P_HIGH)
                {
                    p = -P_HIGH;
                    e = 0;
                }
                if (rev)
                {
                    d = -d;
                    v = -v;
                    a = -a;
                    p = -p;
                    e = -e;
                }
                if (p != mp[m])
                {
                    if (p > 0)
                        OnFwdEx(mot, p, RESET_NONE);
                    else if (p < 0)
                        OnRevEx(mot, p, RESET_NONE);
                    else
                        OffEx(mot, RESET_NONE);

                    mp[m] = p;
                }

                mx[m] = ax + d;
                mv[m] = v;
                ma[m] = a;
                me[m] = e;
            }
        }
        SDL_UnlockMutex(motor_mtx);

        ms += M_DELAY;
        Uint32 del = ms - SDL_GetTicks();
        if (del < 1)
            del = 1;
        else if (del > M_DELAY)
            del = M_DELAY;

        SDL_Delay(del);
    }

    return 0;
}

int main(int argc, char *argv[])
{
    SDL_Window *window = NULL;
    unsigned char cube[NFACE * 8];
    SDL_Event e;

    /* Initialize SDL (Note: video is required to start event loop) */
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Couldn't initialize SDL: %s\n", SDL_GetError());
        exit(1);
    }

    /* Create a window to display joystick axis position */
    window = SDL_CreateWindow("Mindcuber Test", SDL_WINDOWPOS_CENTERED,
                              SDL_WINDOWPOS_CENTERED, 640,
                              480, 0);
    if (window == NULL) {
        SDL_LogError(SDL_LOG_CATEGORY_APPLICATION, "Couldn't create window: %s\n", SDL_GetError());
        return SDL_FALSE;
    }

    motor_mtx = SDL_CreateMutex();

    SDL_Thread* threadID = SDL_CreateThread(motor_task, "motor_task", NULL);

    init_cube(cube);

    while(quit == false)
    {
        while( SDL_PollEvent( &e ) != 0 )
        {
            if( e.type == SDL_QUIT )
                quit = true;
        }
    }

    SDL_DetachThread(threadID);
    SDL_DestroyMutex(motor_mtx);
    motor_mtx = NULL;

    SDL_DestroyWindow(window);
    SDL_QuitSubSystem(SDL_INIT_VIDEO);

    return 0;
}
