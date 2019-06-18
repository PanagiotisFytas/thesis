// test.c
#include <pthread.h>
#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

volatile int mine = 0, c = 0;
void *writer(){
	c = 2;
	return NULL;
}

void *reader(void * arg){
	int local;
	local = c;
	return NULL;
}

int main(int argc, char *argv[]){
    pthread_t w,r[N];
    int rw;
    pthread_create(&w,NULL,writer,NULL);
    for(rw = 0 ;rw<N;rw++){
            pthread_create(&r[rw],NULL,reader,NULL);
    }
	return 0;
}

