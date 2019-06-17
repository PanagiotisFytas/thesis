volatile int x = 0, y = 0, c = 0;
void *thr1(void *arg){
	y = 1;
	if(!x){
		c = 1;
	}
	return NULL;
}
int main(int argc, char *argv[]){
	pthread_t t;
	pthread_create(&t,NULL,thr1,NULL);
	x = 1;
	if(!y){
		c = 0;
	}
	pthread_join(t,NULL);
	return 0;
}
