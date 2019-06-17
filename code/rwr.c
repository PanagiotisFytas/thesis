
volatile int c = 0;
void *writer(void* arg){
	c = 2;
	return NULL;
}

void *reader(void* arg){
	int local = c;
	return NULL;
}

