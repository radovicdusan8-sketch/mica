#include <stdio.h>

int main(void) {
    double a, b;
    char op;
    char nastavi = 'd';

    printf("=== Jednostavan kalkulator ===\n");

    while (nastavi == 'd' || nastavi == 'D') {
        printf("\nUnesite izraz (npr. 5 + 3): ");
        if (scanf("%lf %c %lf", &a, &op, &b) != 3) {
            printf("Neispravan unos.\n");
            /* ocisti ulazni bafer */
            int c;
            while ((c = getchar()) != '\n' && c != EOF) {}
            if (c == EOF) break;
            continue;
        }

        switch (op) {
            case '+':
                printf("Rezultat: %g\n", a + b);
                break;
            case '-':
                printf("Rezultat: %g\n", a - b);
                break;
            case '*':
            case 'x':
                printf("Rezultat: %g\n", a * b);
                break;
            case '/':
                if (b == 0)
                    printf("Greska: deljenje nulom!\n");
                else
                    printf("Rezultat: %g\n", a / b);
                break;
            default:
                printf("Nepoznata operacija '%c'. Koristite + - * /\n", op);
        }

        printf("Nastaviti? (d/n): ");
        if (scanf(" %c", &nastavi) != 1) break;
    }

    printf("Dovidjenja!\n");
    return 0;
}
