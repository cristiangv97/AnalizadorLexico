import pickle

with open("res_lr0.pickle", "rb") as archivo_t_lr0:
    r_lr0 = pickle.load(archivo_t_lr0)
    r_lr0.evaluar_con_lr0("1+1*1", "./afd_fijos/afd_post_espacios")
    for linea in r_lr0.tabla_txt_eval_lr0:
        print(linea)

    # print(r_lr0.tabla_lr0[9][5])

    # for _ in range(0, 2):
    #     print("Hola")

    # texto = "d12"
    # print(texto[1:])

    # print(r_lr0.v)
