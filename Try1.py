"""
    NORMAL
"""

import prettytable as prettytable
import random as rnd
import copy
import xlsxwriter

POPULATION_SIZE = 10
ELITISM_SIZE = 4
MINIMUM_RANDOM_MUTASI = 1
MAXIMUM_RANDOM_MUTASI = 12
MAXIMUM_ITERATION = 10000

HARI = [
    # Senin
    ["Senin", "07.40-08.20"], ["Senin", "08.20-09.00"], ["Senin", "09.00-09.40"], ["Senin", "10.00-10.40"], ["Senin", "10.40-11.20"], ["Senin", "11.20-12.00"], ["Senin", "12.40-13.20"], ["Senin", "13.20-14.00"], ["Senin", "14.00-14.40"], ["Senin", "14.40-15.20"],
    # Selasa
    ["Selasa", "07.00-07.40"], ["Selasa", "07.40-08.20"], ["Selasa", "08.20-09.00"], ["Selasa", "09.00-09.40"], ["Selasa", "10.00-10.40"], ["Selasa", "10.40-11.20"], ["Selasa", "11.20-12.00"], ["Selasa", "12.40-13.20"], ["Selasa", "13.20-14.00"], ["Selasa", "14.00-14.40"],
    # Rabu
    ["Rabu", "07.00-07.40"], ["Rabu","07.40-08.20"], ["Rabu","08.20-09.00"], ["Rabu","09.00-09.40"], ["Rabu","10.00-10.40"], ["Rabu","10.40-11.20"], ["Rabu","11.20-12.00"], ["Rabu","12.40-13.20"],
    # Kamis
    ["Kamis", "07.00-07.40"], ["Kamis", "07.40-08.20"], ["Kamis", "08.20-09.00"], ["Kamis", "09.00-09.40"], ["Kamis", "10.00-10.40"], ["Kamis", "10.40-11.20"], ["Kamis", "11.20-12.00"], ["Kamis", "12.40-13.20"],
    # Jumat
    ["Jumat", "07.00-07.40"], ["Jumat","07.40-08.20"], ["Jumat","08.20-09.00"], ["Jumat","09.00-09.40"]
]
GURU = [
    ["Bahasa Indonesia", "A"],
    ["Bahasa Indonesia", "B"],
    ["Bahasa Indonesia", "C"],
    ["Bahasa Indonesia", "D"],
    ["Matematika", "E"],
    ["Matematika", "F"],
    ["Matematika", "G"],
    ["Matematika", "H"],
    ["IPA", "I"],
    ["IPA", "J"],
    ["IPA", "K"],
    ["IPA", "L"],
    ["Bahasa Inggris", "M"],
    ["Bahasa Inggris", "N"],
    ["Bahasa Inggris", "O"],
    ["Bahasa Inggris", "P"],
    ["PPKn", "Q"],
    ["PPKn", "R"],
    ["PPKn", "S"],
    ["PPKn", "T"],
    ["IPS", "U"],
    ["IPS", "V"],
    ["IPS", "W"],
    ["IPS", "X"],
    ["Seni Budaya", "Y"],
    ["Seni Budaya", "Z"],
    ["Penjaskes", "AA"],
    ["Penjaskes", "BB"],
    ["Prakarya", "CC"],
    ["Prakarya", "DD"],
    ["Muatan Lokal", "EE"],
    ["Muatan Lokal", "FF"],
    ["TIK", "GG"],
    ["TIK", "HH"],
    ["PAI", "II"],
    ["PAI", "JJ"],
    ["PAI", "KK"],
    ["PAI", "LL"],
    ["BTQ", "MM"],
    ["BTQ", "NN"]
]
MAPEL = [
    ["Bahasa Indonesia", 4],
    ["Matematika", 4],
    ["IPA", 4],
    ["Bahasa Inggris", 4],
    ["PPKn", 4],
    ["IPS", 4],
    ["PAI", 4],
    ["Seni Budaya", 2],
    ["Penjaskes", 2],
    ["Prakarya", 2],
    ["Muatan Lokal", 2],
    ["TIK", 2],
    ["BTQ", 2]
]
KELAS = ["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "7I", "7J", "8A", "8B", "8C", "8D", "8E", "8F", "8G", "8H", "8I", "8J", "9A", "9B", "9C", "9D", "9E", "9F", "9G", "9H", "9I", "9J",]
ERROR = []
SHIFT = 0

# Gen => Jam - Mapel - Guru
def generateGen():
    gen = []
    for i in range(0, int(len(HARI)/2)):
        random = rnd.randint(0,39)
        mapel = GURU[random][0]
        guru = GURU[random][1]
        gen.append([HARI[i*2][1], mapel, guru])
        gen.append([HARI[i*2+1][1], mapel, guru])
    return gen

# Kromosom = Individu => kelas - hari - gen
def generateKromosom():
    gen = []
    for i in range(0, 40):
        gen.append(generateGen())

    # gen = generateGen()
    kromosom = []
    namaH = "Senin"
    for i in range(0, len(KELAS)):
        for j in range(0, 5):
            if(j == 0):
                l = 0
                k = 10
                namaH = "Senin"
            elif(j == 1):
                l = 10
                k = 20
                namaH = "Selasa"
            elif(j == 2):
                l = 20
                k = 28
                namaH = "Rabu"
            elif(j == 3):
                l = 28
                k = 36
                namaH = "Kamis"
            elif(j == 4):
                l = 36
                k = 40
                namaH = "Jumat"
            for m in range(l, k):
                kromosom.append([KELAS[i], namaH, gen[i][m]])
    return kromosom

def fitnessFunction(kromosom):
    """ 
        1. Bentrok => Guru ada di satu hari yang sama dan jam yang sama (beda kelas).
        2. JP/Minggu untuk 1 kelas
        3. 1 Kelas tidak boleh diajar lebih dari 1 guru untuk mapel yang sama.
        4. Untuk mapel yang 4 jam, gak boleh bersambung.
    """
    Fitness = 0

    # """ Constraint #1 """
    # # 7A - 9I
    # for l in range(0, len(KELAS)-1):
    #     # 40 Jadwal Pelajaran
    #     for i in range(l*40, (len(HARI) + l * 40), 2):
    #         # 7B - 9J
    #         k = i + 40
    #         for j in range(l+1, len(KELAS)):
    #             if(kromosom[i][2][2] == kromosom[k][2][2]):
    #                 Fitness = Fitness + 1
    #             k = k + 40

    """ Constraint #1 """
    # 7A - 9I
    for l in range(0, len(KELAS)-1):
        # 40 Jadwal Pelajaran
        for i in range(l*40, (len(HARI) + l * 40), 2):
            # 7B - 9J
            k = i + 40
            for j in range(l+1, len(KELAS)):
                if(kromosom[i][2][2] == kromosom[k][2][2]):
                    Fitness = Fitness + 1
                    ERROR.append(k)
                k = k + 40
    
    # """ Constraint #2 """
    # x = 0
    # for i in range(0, len(KELAS)):
    #     jp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #     for j in range(x, len(HARI)+x):
    #         for k in range(0, len(MAPEL)):
    #             if (kromosom[j][2][1] == MAPEL[k][0]):
    #                 jp[k] += 1
    #                 break
    #     x += 40
    #     for j in range(0, len(MAPEL)):
    #         if(MAPEL[j][1] != jp[j]):
    #             Fitness = Fitness + 1

    # """ Constraint #2 """
    # x = 0
    # for i in range(0, len(KELAS)):
    #     jp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #     for j in range(x, len(HARI)+x):
    #         for k in range(0, len(MAPEL)):
    #             if (kromosom[j][2][1] == MAPEL[k][0]):
    #                 jp[k] += 1
    #                 if(jp[k] > MAPEL[k][1]):
    #                     Fitness = Fitness + 1
    #                     ERROR.append(j)
    #                 break
    #     x += 40
    
    # """ Constraint #3 """
    # x = 0
    # for i in range(0, len(KELAS)):
    #     teacher = ["@", "@", "@", "@", "@", "@", "@"]
    #     tanda = [0, 0, 0, 0, 0, 0, 0]
    #     for j in range(x, len(HARI)+x):
    #         for k in range(0, 7):
    #             if (kromosom[j][2][1] == MAPEL[k][0]):
    #                 tanda[k] += 1
    #                 if(teacher[k] == "@" and tanda[k] == 1):
    #                     teacher[k] = kromosom[j][2][2]
    #                 elif(teacher[k] != "@" and tanda[k] == 3):
    #                     if(teacher[k] != kromosom[j][2][2]):
    #                         Fitness = Fitness + 1
    #     x += 40

    """ Constraint #3 """
    x = 0
    for i in range(0, len(KELAS)):
        teacher = ["@", "@", "@", "@", "@", "@", "@"]
        tanda = [0, 0, 0, 0, 0, 0, 0]
        for j in range(x, len(HARI)+x):
            for k in range(0, 7):
                if (kromosom[j][2][1] == MAPEL[k][0]):
                    tanda[k] += 1
                    if(teacher[k] == "@" and tanda[k] == 1):
                        teacher[k] = kromosom[j][2][2]
                    elif(teacher[k] != "@" and tanda[k] == 3):
                        if(teacher[k] != kromosom[j][2][2]):
                            ERROR.append(j)
                            Fitness = Fitness + 1
        x += 40

    # """ Constraint #4 """
    # x = 0
    # for i in range(0, len(KELAS)):
    #     # 0 - 10
    #     # [['7A', 'Senin', ['07.40-08.20', 'BTQ', 'MM']], ['7A', 'Senin', ['08.20-09.00', 'BTQ', 'MM']]]
    #     for j in range(x, int(len(HARI)/2+x-1)):
    #         if (kromosom[j*2][2][1] == kromosom[j*2+2][2][1]):
    #             Fitness = Fitness + 1
    #     x += 20
    
    # """ Constraint #4 """
    # x = 0
    # for i in range(0, len(KELAS)):
    #     for j in range(x, int(len(HARI)/2+x-1)):
    #         if (kromosom[j*2][2][1] == kromosom[j*2+2][2][1]):
    #             ERROR.append(j*2+2)
    #             Fitness = Fitness + 1
    #     x += 20

    # # return Fitness
    return 1 / ((1.0*Fitness + 1))

def generateXlsx(kromosom):
    # Membuat individu
    individu = kromosom

    workbook = xlsxwriter.Workbook("jadwal.xlsx")

    bold_format = workbook.add_format({'bold': True})
    bold_format.set_align('center')
    bold_format.set_border(True)

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('middle')
    cell_format.set_align('center')
    cell_format.set_border(True)
    
    worksheet = workbook.add_worksheet('Jadwal')

    kolom = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH"]
    
    # label kelas
    for i in range(0, len(KELAS)):
        worksheet.write(kolom[i+3] + '4', individu[i*len(HARI)][0], bold_format)

    # label waktu dan hari
    for i in range(0, len(HARI)):
        worksheet.write(kolom[2] + str(i+5), HARI[i][1], cell_format)
        if (HARI[i][0] != HARI[i-1][0]):
            worksheet.write(kolom[1] + str(i+5), HARI[i][0], cell_format)
    
    # mapel dan guru
    for i in range(0, len(KELAS)):
        x = i * len(HARI)
        for j in range(x, x + len(HARI)):
            worksheet.write(kolom[i+3] + str((j - i*len(HARI))+5), individu[j][2][1] + ", " + individu[j][2][2], cell_format)

    # workbook.insert_rows(5, amount=1)
        
    worksheet.set_column(2, 2 + len(KELAS), width=17.5)
    
    workbook.close()
    print("==================================")
    print("||  'jadwal.xlsx' telah dibuat  ||")
    print("==================================")

# Membuat Populasi
populasi = []
for i in range(0, POPULATION_SIZE):
    populasi.append(generateKromosom())

a = 0
flag = 0
while((flag == 0) & (a < MAXIMUM_ITERATION)):
    # Menghitung nilai fitness tiap individu
    # nilai_fitness = []
    # old_fitness = []
    # for i in range(0, POPULATION_SIZE):
    #     nilai_fitness.append(fitnessFunction(populasi[i]))
    #     old_fitness.append(fitnessFunction(populasi[i]))
    #     if(nilai_fitness[i] == 0):
    #         flag = 1
    
    # Tournament
    # new_populasi = []
    # for j in range(0,2):
    #     pendekar = rnd.sample(range(0, POPULATION_SIZE), int(POPULATION_SIZE))
    #     for i in range(0, int((POPULATION_SIZE-ELITISM_SIZE)/2)):
    #         if(nilai_fitness[pendekar[i*2]] > nilai_fitness[pendekar[i*2+1]]):
    #             new_populasi.append(populasi[pendekar[i*2]])
    #         else:
    #             new_populasi.append(populasi[pendekar[i*2+1]])

    # Roulette
    # new_populasi = []
    # calon = rnd.sample(range(0, POPULATION_SIZE), int(POPULATION_SIZE - ELITISM_SIZE))
    # for i in range(0, len(calon)):
    #     new_populasi.append(populasi[calon[i]])
    
    # Elitism => mengambil n individu terbaik dari populasi
    # sort populasi berdasarkan fitness, ambil yg terbaik
    # nilai_fitness.sort()
    # tanda = 0
    # for i in range(0, int(ELITISM_SIZE)):
    #     for j in range (0, POPULATION_SIZE):
    #         if((old_fitness[j] == nilai_fitness[POPULATION_SIZE-(i+1)]) & (tanda < int(ELITISM_SIZE))):
    #             new_populasi.append(populasi[j])
    #             tanda += 1

    # Crossover hasil selection tournament
    # temp = "ayam"
    # for i in range(0, int(POPULATION_SIZE/2)):
    #     for j in range(0, 360):
    #         temp = new_populasi[i*2][j]
    #         new_populasi[i*2][j] = new_populasi[i*2+1][j]
    #         new_populasi[i*2+1][j] = temp
    #     for j in range(839, 1200):
    #         temp = new_populasi[i*2][j]
    #         new_populasi[i*2][j] = new_populasi[i*2+1][j]
    #         new_populasi[i*2+1][j] = temp

    # print("# " + str(new_populasi[2][0]) + " - " + str(new_populasi[3][0]))
    # random = rnd.sample(range(0, POPULATION_SIZE), POPULATION_SIZE)
    # [[['9J', 'Jumat', ['09.00-09.40', 'BTQ', 'NN']], ['9J', 'Jumat', ['09.00-09.40', 'BTQ', 'NN']]]]
    # temp = []
    # for i in range(0, int(POPULATION_SIZE/2)):
    #     for j in range(0, 360):
    #         temp = new_populasi[random[i*2]][j]
    #         new_populasi[random[i*2]][j] = new_populasi[random[i*2+1]][j]
    #         new_populasi[random[i*2+1]][j] = temp
    #     for j in range(839, 1200):
    #         temp = new_populasi[random[i*2]][j]
    #         new_populasi[random[i*2]][j] = new_populasi[random[i*2+1]][j]
    #         new_populasi[random[i*2+1]][j] = temp

    # Mutasi hasil selection tournament dan elitist
    # for i in range(0, POPULATION_SIZE):
    #     for j in range(1, rnd.randint(MINIMUM_RANDOM_MUTASI,MAXIMUM_RANDOM_MUTASI)):
    #         indeks = rnd.randint(0,1199)
    #         if(indeks%2 != 0):
    #             indeks -= 1
    #         random = rnd.randint(0,39)
    #         mapel = GURU[random][0]
    #         guru = GURU[random][1]

    #         new_populasi[i][indeks][2][1] = mapel
    #         new_populasi[i][indeks][2][2] = guru
    #         new_populasi[i][indeks+1][2][1] = mapel
    #         new_populasi[i][indeks+1][2][2] = guru
    
    # generate mutasi baru
    new_populasi = []
    new_populasi = copy.deepcopy(populasi)
    
    # Sorting
    temp = []
    for i in range(0, len(populasi)-1):
        for j in range(i+1, len(populasi)):
            if(fitnessFunction(new_populasi[i]) > fitnessFunction(new_populasi[j])):
                temp = new_populasi[i]
                new_populasi[i] = new_populasi[j]
                new_populasi[j] = temp
                
    # CrossOver
    temp = []
    for i in range(0, int(POPULATION_SIZE/2)):
        for j in range(0, 360):
            temp = new_populasi[i*2][j]
            new_populasi[i*2][j] = new_populasi[i*2+1][j]
            new_populasi[i*2+1][j] = temp
        for j in range(840, 1200):
            temp = new_populasi[i*2][j]
            new_populasi[i*2][j] = new_populasi[i*2+1][j]
            new_populasi[i*2+1][j] = temp
        populasi.append(new_populasi[i*2])
        populasi.append(new_populasi[i*2+1])

    # Mutation
    for i in range(POPULATION_SIZE, POPULATION_SIZE*2):
        ERROR = []
        fitnessFunction(populasi[i])
        j = 0
        # mutation_rate = rnd.randint(MINIMUM_RANDOM_MUTASI, MAXIMUM_RANDOM_MUTASI)
        while((j < len(ERROR))):
            if(ERROR[j]%2 != 0):
                ERROR[j] -= 1
            random = rnd.randint(0,39)
            mapel = GURU[random][0]
            guru = GURU[random][1]

            populasi[i][ERROR[j]][2][1] = mapel
            populasi[i][ERROR[j]][2][2] = guru
            populasi[i][ERROR[j]+1][2][1] = mapel
            populasi[i][ERROR[j]+1][2][2] = guru
            j += 1

        # for j in range(1, rnd.randint(MINIMUM_RANDOM_MUTASI, MAXIMUM_RANDOM_MUTASI)):
        #     indeks = rnd.randint(0,1199)
        #     if(indeks%2 != 0):
        #         indeks -= 1
        #     random = rnd.randint(0,39)
        #     mapel = GURU[random][0]
        #     guru = GURU[random][1]

        #     populasi[i][indeks][2][1] = mapel
        #     populasi[i][indeks][2][2] = guru
        #     populasi[i][indeks+1][2][1] = mapel
        #     populasi[i][indeks+1][2][2] = guru

    # Menghitung nilai fitness tiap individu
    nilai_fitness = []
    old_fitness = []
    for i in range(0, len(populasi)):
        nilai_fitness.append(fitnessFunction(populasi[i]))
        old_fitness.append(fitnessFunction(populasi[i]))
        if(nilai_fitness[i] == 1):
            flag = 1
            generateXlsx(populasi[i])
            break

    if(flag == 1):
        break

    # Elitism => mengambil n individu terbaik dari populasi
    # Sorting
    for i in range(0, len(populasi)-1):
        for j in range(i+1, len(populasi)):
            if(fitnessFunction(populasi[i]) > fitnessFunction(populasi[j])):
                temp = populasi[i]
                populasi[i] = populasi[j]
                populasi[j] = temp

    new_populasi = copy.copy(populasi[POPULATION_SIZE:])

    # nilai_fitness.sort()
    # for i in range(0, POPULATION_SIZE):
    #     tanda = 0
    #     for j in range (0, len(populasi)):
    #         if((old_fitness[j] == nilai_fitness[len(populasi)-(i+1)]) and (tanda != 1)):
    #             new_populasi[i] = populasi[j]
    #             tanda = 1
    # print(nilai_fitness)

    print(nilai_fitness)
    populasi = []
    populasi = new_populasi.copy()

    a += 1