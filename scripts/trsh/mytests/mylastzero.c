#define N 3
atomic_int array[N+1] = {0};
int idx[N+1];

void *thread_reader(void *unused)
{
	for (int i = N; atomic_load_explicit(&array[i], memory_order_acquire) != 0; i--)
		;
	return NULL;
}

void *thread_writer1()
{
	atomic_store_explicit(&array[1],
			      atomic_load_explicit(&array[0], memory_order_acquire) + 1,
			      memory_order_release);
	return NULL;
}

void *thread_writer2()
{
	atomic_store_explicit(&array[2],
			      atomic_load_explicit(&array[1], memory_order_acquire) + 1,
			      memory_order_release);
	return NULL;
}

void *thread_writer3()
{
	atomic_store_explicit(&array[3],
			      atomic_load_explicit(&array[2], memory_order_acquire) + 1,
			      memory_order_release);
	return NULL;
}
