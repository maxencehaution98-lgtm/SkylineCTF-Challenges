#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_flag() {
  char flag[128];
  FILE *f = fopen("/flag.txt", "r");
  if (f) {
    fgets(flag, sizeof(flag), f);
    fclose(f);
    printf("Accès autorisé !\n%s\n", flag);
  } else {
    printf("Erreur: flag introuvable.\n");
  }
}

int main() {
  struct {
    char buffer[32];
    int authorized;
  } data;

  data.authorized = 0;

  printf("=== SKL Corp - Terminal d'accès ===\n");
  printf("Identifiant :  ");
  fflush(stdout);

  gets(data.buffer);

  if (data.authorized != 0) {
    print_flag();
  } else {
    printf("Accès refusé.\n");
  }

  return 0;
}
