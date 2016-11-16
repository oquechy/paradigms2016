#include <stdio.h>
#include <stdlib.h>
#include "../include/thread_pool.h"

typedef struct Arg{
    struct ThreadPool *pool;
    int *l, *r, rec;
    struct RecursiveTask *rt;
}args;

void swap(int *i, int *j) {
    int temp;
    if (i == j)
        return;
    temp = *i;
    *i = *j;
    *j = temp;
}

void partition(int **i, int **j, int x) {
    while (*i <= *j) {
        while (**i < x) (*i)++;
        while (**j > x) (*j)--;
        if (*i  <= *j) swap((*i)++, (*j)--);
    }
}

int cmp_i(const void *i1, const void *i2) {
    int a = *((int *) i1), b = *((int *) i2);
    return a - b;
}

void arg_init(args *arg1, struct ThreadPool *pool, int *l, int *r, int rec, struct RecursiveTask *rt) {
    arg1->pool= pool;
    arg1->l = l;
    arg1->r = r;
    arg1->rec = rec;
    arg1->rt = rt;
}

void pqsort(void *ptr) {
    args *arg;
    int *last, *first;
    int **i = &first, **j = &last;
    struct Task *left, *right;
    args *arg1, *arg2;
    struct RecursiveTask *l, *r;
    arg = ptr;
    last = arg->r - 1;
    first = arg->l;

    if (!arg->rec){
        qsort(arg->l, arg->r - arg->l, sizeof(int), cmp_i);
        if (!atomicint_get(&arg->pool->cont))
            thpool_notify_all(arg->pool);
        return;
    }

    if (arg->r - arg->l <= 1){
        if (!atomicint_get(&arg->pool->cont))
            thpool_notify_all(arg->pool);
        return;
    }

    left = malloc(sizeof(struct Task));
    right = malloc(sizeof(struct Task));
    arg1 = malloc(sizeof(args));
    arg2 = malloc(sizeof(args));
    l = malloc(sizeof(struct RecursiveTask));
    r = malloc(sizeof(struct RecursiveTask));


    partition(i, j, arg->l[0]);

    rtask_init(l, left);
    rtask_init(r, right);
    arg->rt->l = l;
    arg->rt->r = r;
    arg_init(arg1, arg->pool, arg->l, *j + 1, arg->rec - 1, l);
    arg_init(arg2, arg->pool, *i, arg->r, arg->rec - 1, r);

    task_init(left, pqsort, arg1);
    task_init(right, pqsort, arg2);
    thpool_submit(arg->pool, left);
    thpool_submit(arg->pool, right);
}

int main(int argc, char **argv) {

    int nm, n, rec, i;
    int *arr, *arr0;
    struct ThreadPool pool;
    int sorted = 1;
    args *arg = malloc(sizeof(args));
    struct Task *t = malloc(sizeof(struct Task));
    struct RecursiveTask *rt = malloc(sizeof(struct RecursiveTask));
    (void) argc;

    sscanf(argv[1], "%d", &nm);
    sscanf(argv[2], "%d", &n);
    sscanf(argv[3], "%d", &rec);

    arr = malloc(sizeof(int) * n);
    arr0 = malloc(sizeof(int) * n);

    srand(42);
    for (i = 0; i < n; ++i)
        arr0[i] = arr[i] = rand();

    thpool_init(&pool, (unsigned int)nm);

    arg_init(arg, &pool, arr, arr + n, rec, rt);
    task_init(t, pqsort, arg);
    rtask_init(rt, t);
    thpool_submit(&pool, t);

    qsort(arr0, (size_t)n, sizeof(int), cmp_i);

    rtask_wait(rt);
    rtask_free(rt);
    /*thpool_tasks_wait(&pool);*/
    thpool_finit(&pool);

    for(i = 0; i < n; ++i)
        sorted &= (arr[i] == arr0[i]);

    if (sorted)
        printf("I made it :)\n");
    else
        printf("Fail\n");

    free(arr);
    free(arr0);

    return 0;
}
