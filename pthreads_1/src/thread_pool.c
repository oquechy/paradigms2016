#include "../include/thread_pool.h"
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

void task_init(struct Task* task, void (*f)(void *), void* arg, struct ThreadPool *pool, int type){
    pthread_cond_init(&task->cond, NULL);
    pthread_mutex_init(&task->mutex, NULL);
    task->done = 0;
    task->f = f;
    task->arg = arg;
    task->link.prev = task->link.next = 0;
    task->cont = &pool->cont;
    task->type = type;
    task->q = &pool->tasks;
}

void task_finit(struct Task* task) {
    pthread_mutex_destroy(&task->mutex);
    pthread_cond_destroy(&task->cond);
    free(task->arg);
    free(task);
}

void *process(void *data)
{
    struct ThreadPool *pool = data;

    while (pool->cont || queue_size(&pool->tasks.squeue.queue)) {
        struct list_node *node;
        if (pool->cont)
            wsqueue_wait(&pool->tasks);
        if (!pool->cont)
            break;
        node = wsqueue_pop(&pool->tasks);
        if (node) {
            struct Task *task = (struct Task *)node;
            task->f(task->arg);
            pthread_mutex_lock(&task->mutex);
            pthread_cond_broadcast(&task->cond);
            pthread_mutex_unlock(&task->mutex);
            task->done = 1;
            task_finit(task);
        }
    }

    return NULL;
}

void thpool_init(struct ThreadPool* pool, unsigned threads_nm) {
    int rc, i;
    wsqueue_init(&pool->tasks);
    rc = 0;
    pool->cont = 1;
    pool->ths_nm = threads_nm;
    for(i = 0; i < (int)threads_nm; ++i)
        rc |= pthread_create(&pool->ths[i], NULL, process, pool);
    if (rc){
        wsqueue_finit(&pool->tasks);
        perror("thpool_init");
        exit(1);
    }
}

void thpool_submit(struct ThreadPool* pool, struct Task* task) {
    wsqueue_push(&pool->tasks, (struct list_node *)task);
}

void thpool_wait(struct Task* task) {
    if (!task->done) {
        pthread_mutex_lock(&task->mutex);
        while (!task->done)
            pthread_cond_wait(&task->cond, &task->mutex);
        pthread_mutex_unlock(&task->mutex);
    }
}

void thpool_finit(struct ThreadPool* pool) {
    int i;
    for (i = 0; i < pool->ths_nm; ++i)
        pthread_join(pool->ths[i], NULL);
    wsqueue_finit(&pool->tasks);
}
