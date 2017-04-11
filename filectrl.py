# -*- coding: utf-8 -*-


# man_alpha=[]
# man_r=[]



def text_save(content,filename,mode='a'):
    # Try to save a list variable in txt file.
    file = open(filename,mode)
    for i in range(len(content)):
        file.write(str(content[i])+'\n')
    file.close()



def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        file = open(filename,'r')
    except IOError:
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]

    file.close()
    return content



# if __name__ == '__main__':
#     #test_list.append("yuanbao")
#     #text_save(test_list,'test.txt')
#     #test_content=text_read('test.txt')
#     #print test_content
#     alpha_db=text_read('man_alpha_db.txt')
#     r_db=text_read('man_r_db.txt')
#
#     alpha_db[5]=876
#     r_db[4]=900
#
#     text_save(alpha_db,'man_alpha_db.txt','w')
#     text_save(r_db,'man_r_db.txt','w')
#
#     man_alpha_read=text_read('man_alpha_db.txt')
#     man_r_read=text_read('man_r_db.txt')
#     print man_alpha_read[5]
#     print man_r_read[4]


