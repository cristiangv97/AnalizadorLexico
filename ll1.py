import copy

from clases import DescensoRecGramGram, AnalizadorLexico


class AnalizadorLL1(object):
    def __init__(self, cad_gramatica):
        self.res_sigma_ll1 = list()
        self.gram = cad_gramatica
        self.desc_rec_gg = DescensoRecGramGram(cad_gramatica)
        # self.a_lex = AnalizadorLexico(cad_gramatica, archivo_a_lex)

        self.num_renglones_ira = 0
        self.sigma = ""
        self.tabla_ll1 = list()
        self.v_t = list()
        self.tokens_vt = dict()
        self.v_n = list()
        self.v = list()

    def calcular_tabla_ll1(self):
        if not self.desc_rec_gg.analizar_gramatica():
            return False

        temp_terminales = copy.deepcopy(self.desc_rec_gg.v_t)
        temp_terminales.append('$')

        temp_no_terminales = copy.deepcopy(self.desc_rec_gg.v_n)
        temp_no_terminales.append('$')

        for fila in range(0, len(temp_no_terminales)):
            self.tabla_ll1.append(['-1'] * len(temp_terminales))

        for index, elemento_arr in enumerate(self.desc_rec_gg.arr_reglas):
            f = self.desc_rec_gg.first(elemento_arr.lista_lado_derecho)

            no_fila = temp_no_terminales.index(elemento_arr.info_simbolo.simbolo)

            if 'epsilon' in f:

                f.update(self.desc_rec_gg.follow(elemento_arr.info_simbolo.simbolo))
                f.remove('epsilon')

            for item in f:
                self.tabla_ll1[no_fila][temp_terminales.index(item)] = f'{index + 1}'
        # self.tabla_ll1[-1][0] = '$'
        self.tabla_ll1[-1][-1] = 'ACEPTAR'
        for index, simb in enumerate(temp_no_terminales):
            self.tabla_ll1[index].insert(0, simb)
        return True

    def asignar_token(self, simb_terminal, token_terminal):
        self.tokens_vt[token_terminal] = simb_terminal

    def analizar_sigma(self, sigma, archivo_a_lex):
        a_lex = AnalizadorLexico(sigma, archivo_a_lex)

        self.desc_rec_gg.v_t.append('$')
        self.tokens_vt['0'] = '$'

        q_reglas = list()
        q_reglas.append('$')
        q_reglas.append(self.desc_rec_gg.v_n[0])

        posicion_sigma = 0
        posicion_pila = 1

        lista_lexemas = self.analisis_lexico(copy.deepcopy(a_lex))

        print(f"Analizando {lista_lexemas}")

        if lista_lexemas is None:
            return False

        while len(q_reglas) != 0:

            # Recupero el ultimo valor de mi pila
            simb_regla = q_reglas[-1]

            token_sigma = a_lex.yylex()
            simb_sigma = a_lex.yytext

            # Verifico si mi simbolo de regla es igual a mi simb terminal, para realizar el pop
            if simb_regla == simb_sigma:
                # Imprimo en consola mi operacion
                print(self.res_sigma_ll1[-1], '-> POP')

                # Lineas para guardar mi pila
                tupla = list()
                tupla.append(copy.deepcopy(q_reglas))
                tupla.append(lista_lexemas[posicion_sigma:])
                self.res_sigma_ll1.append(tupla)

                # Saco mi simbolo terminal de pila
                q_reglas.pop()

                # Avanzo en mi cadena un valor
                posicion_sigma += 1

                # Retrocedo un valor en cual se insertara en mi pila
                posicion_pila -= 1

                continue

            elif simb_regla == 'epsilon':
                # Imprimo en consola mi operacion
                print(self.res_sigma_ll1[-1], '-> MOVE')

                a_lex.undo_token()

                # Saco a epsilon
                q_reglas.pop()

                # Retrocedo un valor en cual se insertara en mi pila
                posicion_pila -= 1
                continue

            # Lineas para guardar mi pila
            tupla = list()
            tupla.append(copy.deepcopy(q_reglas))
            tupla.append(lista_lexemas[posicion_sigma:])
            self.res_sigma_ll1.append(tupla)

            # Guardo el index de mi simbolo terminal y le sumo uno debido a que en la primera columna se
            # encuentran mis no terminales
            index = int(self.desc_rec_gg.v_t.index(self.tokens_vt.get(token_sigma))) + 1

            # Busco la posicion de mi regla de q en mi tabla
            try:
                posicion_regla = self.v_n.index(simb_regla)
            except ValueError:
                return False

            # Obtengo la regla a la cual llege con mi tabla con mi simbolo de sigma
            regla = self.tabla_ll1[posicion_regla][index]

            print(self.res_sigma_ll1[-1], '->', regla)

            # Si la regla es -1 significa que la cadena sigma es sinctacticamente incorrecta
            if regla == '-1':
                return False

            # Como se llegue a una regla entonces la guardo y le resto -1 por el arreglo
            regla = int(regla) - 1

            # Inicializo una variable para saber cuantas reglas se han agregado
            reglas_agregadas = 0

            # Saco la regla de mi pila y la reemplazo con su respectiva regla
            q_reglas.pop()

            # Saco mi lado derecho de la regla a la que se llego y agrego el simbolo en mi pila para ser
            # analizado en la posicion posicion_pila
            for nodo in self.desc_rec_gg.arr_reglas[regla].lista_lado_derecho:
                q_reglas.insert(posicion_pila, nodo.simbolo)
                reglas_agregadas += 1
            #
            # if q_reglas[-1] == 'epsilon':
            #     q_reglas.pop(-1)
            #     posicion_pila -= 1
            #     continue

            # Modifico la posicion en la cual estare agregando a mi pila
            posicion_pila += reglas_agregadas - 1

        self.v_t.remove('$')
        # print('*' * 12)
        # for linea in self.res_sigma_ll1:
        #     print(linea)
        return True

    # noinspection PyMethodMayBeStatic
    def analisis_lexico(self, a_lexico):
        lista = list()
        while True:
            token = a_lexico.yylex()
            if token == 'ERROR':
                return False
            elif token == '0':
                lista.append('$')
                return lista
            lista.append(a_lexico.yytext)



