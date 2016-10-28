#include "barrier.h"

#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <time.h>

int nanosleep(const struct timespec *req, struct timespec *rem);

#define LIMIT 1000
#define NTHREADS 4
#define STEP   100

const struct timespec c_to_sleep = {0, 100000000L}; /* 0 sec + 10^8 ns = 100 ms */

void* walk(void* args) {
	barrier_t* b = (barrier_t*) args;

	for (;;) { /* silly */
		barrier_add(b, rand() % STEP);

		printf("%d\n", barrier_get(b));

		nanosleep(&c_to_sleep, NULL);
	}
}

int main(void)
{
	int i, rc;
	pthread_t walkers[NTHREADS];
	barrier_t* b = barrier_make(LIMIT);

	srand(time(NULL));


	for (i = 0; i < NTHREADS; ++i) {
		rc = pthread_create(walkers + i, NULL, walk, b);
		assert(!rc);
	}

	printf("Value after wait: %d\n", barrier_wait(b));

	for (i = 0; i < NTHREADS; ++i) {
		rc = pthread_cancel(walkers[i]);
		assert(!rc);
		pthread_join(walkers[i], NULL);
	}

	barrier_free(b);

  return 0;
}
