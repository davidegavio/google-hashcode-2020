#####################INPUT PARSER##############################
books = 0  # number of books
libraries = 0  # number of libraries
days = 0  #number of days
books_score = {}
libraries_info = {}
book_per_lib = {}
id_lib = 0
set_books = {0}
with open("datasets/c_incunabula.txt", "r") as f:  # a_example.txt #b_read_on #c_incunabula #f_libraries_of_the_world #e_so_many_books #d_tough_choices
    line_counter = 0
    for line in f:
        split_ = line.split(" ")
        if line_counter == 0:
            books = int(split_[0])
            libraries = int(split_[1])
            days = int(split_[2])
            line_counter += 1
            continue
        if line_counter == 1:
            for i in range(len(split_)):
                books_score[i] = int(split_[i])
                set_books.add(i)
            line_counter += 1
            continue
        if line_counter >= 2 and line_counter <= libraries + 3:
            if line_counter % 2 == 0:  # libreria
                id_lib += 1
                libraries_info.update({id_lib - 1: (int(split_[0]), int(split_[1]), int(split_[2]))})
            else:  #libri che contiene
                for num in split_:
                    if book_per_lib.get(id_lib - 1, -1) == -1:  #non c'è
                        book_per_lib.update({id_lib - 1: [(int(num), books_score.get(int(num)))]})
                    else:
                        book_per_lib.get(id_lib - 1).append((int(num), books_score.get(int((num)))))
                book_per_lib.get(id_lib - 1).sort(key=lambda tup: tup[1])
            line_counter += 1
            continue


###################################################
############ CREZIONE LISTA ORDINATA DELLE LIBRERIE ##################################
def library_books_weight(tot_number_of_books, library_books_score_sum):
    return library_books_score_sum / tot_number_of_books


def calc_urgenza_pesata(par_scan, days, lib_books_weight):
    return (par_scan / days) * lib_books_weight


def score_tot_per_lib(id):
    sum_ = 0
    for book in book_per_lib[id]:
        sum_ += book[1]
    return sum_


# libreria : urgenza
lib_urgenza = {}
for lib in libraries_info.keys():
    lib_urgenza.update({lib: calc_urgenza_pesata(libraries_info[lib][2], libraries_info[lib][1], library_books_weight(books, score_tot_per_lib(lib)))})
lib_urgenza = {k: v for k, v in sorted(lib_urgenza.items(), key=lambda item: item[1], reverse=True)}


##########################################################################################
############################### SCANNING E CREAZIONE RISULTATO ################################
# funzione aggiornamento dinamico
def dynamic_update(id_lib, n_book):
    global books
    global lib_urgenza
    to_remove = []
    for key in book_per_lib:
        for value in book_per_lib.get(key):
            to_remove.append(value[0])
    to_remove = book_per_lib.get(id_lib)
    del book_per_lib[id_lib]
    for key in book_per_lib:
        book_per_lib[key] = list(set(book_per_lib.get(key)) - set(to_remove[:n_book]))
    books -= len(to_remove)
    # libreria : urgenza
    lib_urgenza.clear()
    for lib in book_per_lib.keys():
        lib_urgenza.update({lib: calc_urgenza_pesata(libraries_info[lib][2], libraries_info[lib][1], library_books_weight(books, score_tot_per_lib(lib)))})
    lib_urgenza = {k: v for k, v in sorted(lib_urgenza.items(), key=lambda item: item[1], reverse=True)}


signup_days = 0
cont_lib = 0
book_scanned = {}
lib_scanned = []
# self.distances = [[0 for i in range(self.numdocs())] for j in range(self.numdocs())]
while signup_days < days and len(lib_urgenza) != 0:
    library = list(lib_urgenza.keys())[0]
    signup_days += libraries_info[library][1]  #aggiungo il signup
    lib_scanned.append(library)
    day_av = days - signup_days - (len(book_per_lib[library]) // libraries_info[library][2])
    book_scanned[cont_lib] = book_per_lib[library]
    dynamic_update(library, len(book_per_lib[library]) // libraries_info[library][2])
    cont_lib += 1
# FILE DI OUTPUT
with open("results/c_result.txt", "w") as f:
    print(str(cont_lib), file=f)
    for i in range(len(lib_scanned)):
        if len(book_scanned[i]) != 0:
            print(str(lib_scanned[i]) + " " + str(len(book_scanned[i])), file=f)
            str_ = [str(el[0]) for el in book_scanned[i]]
            print(' '.join(str_), file=f)
################################################################################################
pass