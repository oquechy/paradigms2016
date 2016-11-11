#include <stdio.h>
#include <stdlib.h>
#include "../include/thread_pool.h"

typedef struct Arg{
    struct ThreadPool *pool;
    int *l, *r, rec;
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

/*void finish(void *t) {
    struct Task *task = t;
    thpool_wait(task);
    --*task->cont;
    if (!*task->cont)
        wsqueue_notify_all(task->q);
    task_finit(task);
}*/

void arg_init(args *arg1, struct ThreadPool *pool, int *l, int *r, int rec) {
    arg1->pool= pool;
    arg1->l = l;
    arg1->r = r;
    arg1->rec = rec;
}

void pqsort(void *ptr) {
    args *arg;
    int *last, *first;
    int **i = &first, **j = &last;
    struct Task *left, *right;
    /*struct Task *w_left, *w_right;*/
    args *arg1, *arg2;
    arg = ptr;
    last = arg->r - 1;
    first = arg->l;

    if (!arg->rec){
        qsort(arg->l, arg->r - arg->l, sizeof(int), cmp_i);
        --arg->pool->cont;
        return;
    }

    if (arg->r - arg->l <= 1){
        --arg->pool->cont;
        return;
    }

    left = malloc(sizeof(struct Task));
    right = malloc(sizeof(struct Task));
    /*w_left = malloc(sizeof(struct Task));
    //w_right = malloc(sizeof(struct Task));*/
    arg1 = malloc(sizeof(args));
    arg2 = malloc(sizeof(args));


    partition(i, j, arg->l[rand() % (arg->r - arg->l)]);

    arg_init(arg1, arg->pool, arg->l, *j + 1, arg->rec - 1);
    arg_init(arg2, arg->pool, *i, arg->r, arg->rec - 1);

    task_init(left, pqsort, arg1, arg->pool, 0);
    task_init(right, pqsort, arg2, arg->pool, 0);
    /*task_init(w_left, finish, left, arg->pool, 1);
    //task_init(w_right, finish, right, arg->pool, 1);*/
    thpool_submit(arg->pool, left);
    thpool_submit(arg->pool, right);

    ++arg->pool->cont;

    /*thpool_submit(arg->pool, w_left);
    //thpool_submit(arg->pool, w_right);*/
}

int main(int argc, char **argv) {

    int nm, n, rec, i;
    int *arr, *arr0;
    struct ThreadPool pool;
    int sorted = 1;
    args *arg = malloc(sizeof(args));
    struct Task *t = malloc(sizeof(struct Task))/*, *wt = malloc(sizeof(struct Task))*/;
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

    arg_init(arg, &pool, arr, arr + n, rec);

    task_init(t, pqsort, arg, &pool, 0);
    /*task_init(wt, finish, t, &pool, 1);*/
    thpool_submit(&pool, t);
    /*thpool_submit(&pool, wt);*/

    qsort(arr0, (size_t)n, sizeof(int), cmp_i);

    thpool_finit(&pool);

    for(i = 0; i < n; ++i)
        sorted &= (arr[i] == arr0[i]);
    for(i = 0; i < n; ++i)
        printf("%d ",arr[i]);
    printf("\n");
    for(i = 0; i < n; ++i)
        printf("%d ", arr0[i]);
    printf("\n");

    printf("%d", sorted);

    free(arr);
    free(arr0);

    return 0;
}
