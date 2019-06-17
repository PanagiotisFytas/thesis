#include <assert.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>
#include  <stdatomic.h>

#define SIZE 128
#define MAX  1

atomic_int table[SIZE];

void *thread_n()
{
    int h = 0, zero = 0;
    while (!atomic_compare_exchange_strong_explicit(&table[h], &zero, 1,
                                                    memory_order_relaxed,
                                                    memory_order_relaxed))
    {
        h = (h + 1) % SIZE;
        zero = 0;
    }
    return NULL;
}

int idx[N];

int main()
{
	pthread_t t[N];

	for (int i = 0; i < N; i++) {
		pthread_create(&t[i], NULL, thread_n, NULL);
	}

	return 0;
}
