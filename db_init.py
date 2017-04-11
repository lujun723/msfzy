# -*- coding: utf-8 -*-
from filectrl import text_save, text_read

test_list=['sam','linda']

man_alpha=[]
man_r=[]

def db_init(db_obj,man_num):
    for i in range(man_num):
        db_obj.append(0)

if __name__ == '__main__':
    db_init(man_alpha,1000)
    db_init(man_r,1000)

    text_save(man_alpha,'man_alpha_db.txt')
    text_save(man_r,'man_r_db.txt')