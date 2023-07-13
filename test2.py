import pickle

with open("res_lr0.pickle", "rb") as archivo_t_lr0:
    r_lr0 = pickle.load(archivo_t_lr0)
    r_lr0.tokens_vt['10'] = 'mas'
    r_lr0.tokens_vt['20'] = 'menos'
    # print(r_lr0.tokens_vt)
with open("res_lr0.pickle", "wb") as f_res:
    pickle.dump(r_lr0, f_res)
