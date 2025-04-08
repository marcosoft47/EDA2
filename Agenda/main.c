#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct data{
    int dia;
    int mes;
    int ano;
};
typedef struct{
    int cod;
    char descricao[50];
    struct data data;
} entrada;


entrada *criarEntrada(int cod, char descricao[50], int dia, int mes, int ano){
    entrada *novo = NULL;
    novo = (entrada *) malloc(sizeof(entrada));

    struct data *aeiou = NULL;
    aeiou = (struct data *) malloc(sizeof(struct data));
    aeiou->ano=ano;
    aeiou->mes=mes;
    aeiou->dia=dia;

    novo->cod=cod;
    strcpy(novo->descricao,descricao);
    novo->data=*aeiou;
    return novo;
}

char *getfield(const char* line, int num) {
    const char *p = line;
    size_t len;
    char *res;
    for (;;) {
        len = strcspn(p, ",\n");
        if (--num <= 0)
            break;
        p += len;
        if (*p == ',')
            p++;
    }
    res = malloc(len + 1);
    if (res) {
        memcpy(res, p, len);
        res[len] = '\0';
    }
    return res;
}

int armazenarSimples(entrada **v, FILE* f){
    int n = sizeof(**v) / sizeof(entrada);
    printf("%i", n);
    for (int i = 0; i <= n; i++){
        printf("%s,%i,%i,%i\n",v[i]->descricao,v[i]->data.dia,v[i]->data.mes,v[i]->data.ano);
        fprintf(f, "%s,%i,%i,%i\n",v[i]->descricao,v[i]->data.dia,v[i]->data.mes,v[i]->data.ano);
    }
    return 1;
}

int main(){
    entrada *teste = NULL;
    entrada *teste2 = NULL;
    teste = criarEntrada(0,"afaefa",2,5,2005);
    teste2 = criarEntrada(0,"aeaeca",3,6,2007);
    entrada *v[] = {teste, teste2};
    FILE *f = fopen("teste.csv","wr");
    armazenarSimples(v,f);
    fclose(f);
}