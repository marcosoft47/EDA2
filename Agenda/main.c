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


entrada *criarEntrada(int cod, char* descricao, int dia, int mes, int ano){
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

entrada *solicitarEntrada(){
    printf("Informe a descrição do evento: ");
    char *descricao = scanf("%s");
    printf("Informe o dia do evento: ");
    int dia = scanf("%i");
    printf("Informe o mês do evento: ");
    char mes = scanf("%i");
    printf("Informe o ano do evento: ");
    char ano = scanf("%i");

    return criarEntrada(0,descricao,dia,mes,ano);
}

entrada *solicitarEntradaOrdenada(){
    printf("Informe o código do evento: ");
    int cod = scanf("%i");
    entrada* novo = solicitarEntrada();
    novo->cod=cod;
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

int armazenarSimples(entrada *v, FILE* f){
    fprintf(f, "%s,%i,%i,%i\n",v->descricao,v->data.dia,v->data.mes,v->data.ano);

    return 1;
}
int armazenarOrdenado(entrada *v, int chave, FILE* f){
    fprintf(f, "%i,%s,%i,%i,%i\n",chave, v->descricao,v->data.dia,v->data.mes,v->data.ano);
}

char* buscaOrdenado(FILE *f, int chave){
    char line[1024];
    fseek(f,0,SEEK_SET);
    while (fgets(line, 1024, f)){

        printf("ajkvbdsjkfbjkkfds");
        if (atoi(getfield(line, 1))==chave){
            printf("ajkvbdsjkfbjkkfds");
            char buffer[1024];
            sprintf(buffer, "%i,%s,%i,%i,%i", chave, getfield(line,1), atoi(getfield(line,2)), atoi(getfield(line,3)), atoi(getfield(line,4)), atoi(getfield(line,5)));
            return buffer;
        }
    }
}

int main(){
    int escolha;
    entrada *teste = NULL;
    printf("Escolha qual exercício testar:\n1- Armazenar dados numa agenda em arquivo sequencial simples\n2- Ler os registros escritos em 1 e criar arquivo sequencial\n3- Criar arquivo invertido de 1\n");
    escolha = scanf("%i");
    switch(escolha){
        case(1):
            entrada *teste = NULL;
            teste = criarEntrada(0,"afaefa",2,5,2005);
            FILE *f = fopen("teste.csv","rw");
            armazenarSimples(teste,f);

            teste = criarEntrada(0,"aeaeca",3,6,2007);
            armazenarSimples(teste,f);
            fclose(f);
            free(teste);
        case(2):
            // Parte 2
            FILE *f2 = fopen("teste.csv","r");
            entrada *teste3 = NULL;
            FILE *f3 = fopen("teste2.csv","wr");
            char line[1024];
            int chave = 0;
            while (fgets(line, 1024, f2)){
                chave++;
                fprintf(f3, "%i,%s,%i,%i,%i\n", chave, getfield(line,1), atoi(getfield(line,2)), atoi(getfield(line,3)), atoi(getfield(line,4)), atoi(getfield(line,5)));
            }

            teste = criarEntrada(0,"afaefa",2,5,2005);
            armazenarOrdenado(teste, 2, f3);
            printf(buscaOrdenado(f3,1));
            fclose(f3);
            fclose(f2);
    }

}