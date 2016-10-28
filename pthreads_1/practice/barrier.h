#ifndef __BARRIER_H_
#define __BARRIER_H_

#include "atomic.h"

struct barrier;
typedef struct barrier barrier_t;

barrier_t* barrier_make(int limit);
int        barrier_get(barrier_t* b);
void       barrier_add(barrier_t* b, int value);
int        barrier_wait(barrier_t* b);
void       barrier_free(barrier_t* b);

#endif
