#include "../include/thread_pool.h"
#include <stdlib.h>
#include <stdio.h>

void task_init(struct Task* task, void (*f)(void *), void* arg){
    pthread_cond_init(&task->cond, NULL);
    pthread_mutex_init(&task->mutex, NULL);
    task->done = 0;
    task->f = f;
    task->arg = arg;
    task->link.prev = task->link.next = 0;
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
        pthread_mutex_lock(&pool->tasks.squeue.mutex);
        while (pool->cont && !queue_size(&pool->tasks.squeue.queue))
               pthread_cond_wait(&pool->tasks.cond, &pool->tasks.squeue.mutex);
        pthread_mutex_unlock(&pool->tasks.squeue.mutex);
        if (!pool->cont)
            break;
        node = wsqueue_pop(&pool->tasks);
        if (node) {
            struct Task *task = (struct Task *)node;
            task->f(task->arg);
            task->done = 1;
            pthread_mutex_lock(&task->mutex);
            pthread_cond_broadcast(&task->cond);
            pthread_mutex_unlock(&task->mutex);
            task_finit(task);
            if (!pool->cont)
                pthread_cond_broadcast(&pool->cond);
        }
    }

    return NULL;
}

void thpool_init(struct ThreadPool* pool, unsigned threads_nm) {
    int rc, i;
    wsqueue_init(&pool->tasks);
    rc = 0;
    pthread_cond_init(&pool->cond, NULL);
    pthread_mutex_init(&pool->mutex, NULL);
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

void thpool_tasks_wait(struct ThreadPool *pool) {
    pthread_mutex_lock(&pool->mutex);
    while (pool->cont)
        pthread_cond_wait(&pool->cond, &pool->mutex);
    pthread_mutex_unlock(&pool->mutex);
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

void thpool_notify_all(struct ThreadPool* pool) {
    wsqueue_notify_all(&pool->tasks);
}
