volatile int x = 1;

void *divider() {
  return 42 / x;
}

void *zero() {
  x = 0;
}
