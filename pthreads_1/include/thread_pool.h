#ifndef PARADIGMS_THREAD_POOL_H
#define PARADIGMS_THREAD_POOL_H

#define MAXT 6

#include <pthread.h>
#include "wsqueue.h"

struct RecursiveTask {
    struct RecursiveTask *l, *r;
    struct Task *task;
};

struct Task {
    struct list_node link;
    void (*f)(void *);
    void* arg;
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    int done;
};

struct ThreadPool {
    pthread_t ths[MAXT];
    struct wsqueue tasks;
    int cont;
    pthread_cond_t cond;
    pthread_mutex_t mutex;
    int ths_nm;
};

void thpool_init(struct ThreadPool* pool, unsigned threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_finit(struct ThreadPool* pool);
void task_init(struct Task* task, void (*f)(void *), void* arg);
void task_finit(struct Task* task);
void thpool_notify_all(struct ThreadPool* pool);
void thpool_tasks_wait(struct ThreadPool *pool);
void rtask_wait(struct RecursiveTask *rt);
void rtask_init(struct RecursiveTask *rt, struct Task *t);
void rtask_free(struct RecursiveTask *rt);

#endif
