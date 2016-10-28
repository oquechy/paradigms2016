#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "../include/thread_pool.h"

int *minmin, *maxmax;

typedef struct Arg{
    struct ThreadPool *pool;
    int *l, *r, rec;
}args;

void swap(int *i, int *j) {
    int temp;
    temp = *i;
    *i = *j;
    *j = temp;
}


void partition(int **i, int **j, int x, FILE *f) {
    fprintf(f, "%i\n", x);
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

void pqsort(void *ptr) {
    args *arg;
    int *last, *first, h;
    int **i = &first, **j = &last, *k;
    struct Task left, right;args *arg1 = malloc(sizeof(args)), *arg2 = malloc(sizeof(args));
    char fn[100];
    FILE *f;
    assert(ptr);
    arg = ptr;
    assert(arg->l);
    assert(arg->l >= minmin);
    assert(arg->pool);
    assert(arg->r);
    assert(arg->r <= maxmax);
    last = arg->r - 1;
    first = arg->l;

    for (h = 0; h < 3; ++h)
        fn[h] = (char)(rand() % ('z' - 'a' + 1) + 'a');
    fn[3] = '.';
    fn[4] = 't';
    fn[5] = 'x';
    fn[6] = 't';
    fn[7] = 0;
    f = fopen(fn, "w");
    assert(f);
    fprintf(f, "%li %li \n", arg->l - minmin, arg->r - minmin);
    if (!arg->rec){
        qsort(arg->l, arg->r - arg->l, sizeof(int), cmp_i);
        fprintf(f,"rec!\n");
        return;
    }
    if (arg->r - arg->l <= 1){
        fprintf(f,"small\n");
        return;
    }
    partition(i, j, arg->l[rand() % (arg->r - arg->l)], f)  ;

    /*fprintf(f, "%i ", *arg->l);*/
    for(k = arg->l; k < arg->r; ++k)
        fprintf(f, "%i ", *k);
    fprintf(f, "\n%d %lu %lu %lu\n", 0, *j - arg->l + 1, *i - arg->l, arg->r - arg->l);

    fclose(f);

    arg1->pool= arg->pool;
    arg1->l = arg->l;
    arg1->r = *j + 1;
    arg1->rec = arg->rec - 1;
    arg2->pool= arg->pool;
    arg2->l = *i;
    arg2->r = arg->r;
    arg2->rec = arg->rec - 1;

    task_init(&left, pqsort, arg1);
    task_init(&right, pqsort, arg2);
    thpool_submit(arg->pool, &left);
    thpool_submit(arg->pool, &right);
}

int main(int argc, char **argv) {

    int nm, n, rec, i;
    int *arr, *arr0;
    struct ThreadPool pool;
    int sorted = 1;
    args arg;

    (void) argc;

    sscanf(argv[1], "%d", &nm);
    sscanf(argv[2], "%d", &n);
    sscanf(argv[3], "%d", &rec);

    arr = malloc(sizeof(int) * n);
    arr0 = malloc(sizeof(int) * n);

    minmin = arr;
    maxmax = arr + n;

    srand(42);
    for (i = 0; i < n; ++i)
        arr0[i] = arr[i] = rand();

    thpool_init(&pool, (unsigned int)nm);

    arg.pool= &pool;
    arg.l = arr;
    arg.r = arr + n;
    arg.rec = rec;
    pqsort(&arg);
    qsort(arr0, (size_t)n, sizeof(int), cmp_i);

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
