#ifndef PARADIGMS_THREAD_POOL_H
#define PARADIGMS_THREAD_POOL_H

#define MAXT 6

#include <pthread.h>
#include "wsqueue.h"

struct Task {
    struct list_node link;
    void (*f)(void *);
    void* arg;
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    int volatile done;
};

struct ThreadPool {
    pthread_t ths[MAXT];
    struct wsqueue tasks;
    int volatile cont;
    int ths_nm;
};

void thpool_init(struct ThreadPool* pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);\
void task_init(struct Task* task, void (*f)(void *), void* arg);
#endif