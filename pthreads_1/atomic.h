#ifndef __ATOMIC_H_
#define __ATOMIC_H_

#include <pthread.h>


typedef struct atomicint {
	int value;
	pthread_mutex_t value_mutex;
} atomicint_t;


void atomicint_init(atomicint_t* atomic_int,int init_value);
int  atomicint_get(atomicint_t* atomic_int);
void atomicint_add(atomicint_t* atomic_int, int value);
void atomicint_destroy(atomicint_t* atomic_int);

#endif
