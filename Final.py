"""
    TO DO:
    (1) Ngubah Mutasi =>  hanya mutasi yang jeleknya saja
"""

"""
    Library:
    (1) random = buat melakukan random
    (2) copy = Untuk meng-copy list agar tidak pass by reference
    (3) xlsxwriter = untuk menghasilkan file excel
"""
import random as rnd
import copy
import xlsxwriter


"""
    (1) Inisialisasi
"""
# Banyak individu dalam suatu populasi
POPULATION_SIZE = 10
# Maksimum iterasi looping pencarian individu terbaik
MAXIMUM_ITERATION = 100
# Berisi hari dan jam pelajaran
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
# Berisi mata pelajaran dan guru yang mengajarnya
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
# Berisi mata pelajaran dan guru yang mengajarnya
GURU2 = [
    ["Bahasa Indonesia", ["A", "B", "C", "D"]],
    ["Matematika", ["E", "F", "G", "H"]],
    ["IPA", ["I", "J", "K", "L"]],
    ["Bahasa Inggris", ["M", "N", "O", "P"]],
    ["PPKn", ["Q", "R", "S", "T"]],
    ["IPS", ["U", "V", "W", "X"]],
    ["Seni Budaya", ["Y", "Z"]],
    ["Penjaskes", ["AA", "BB"]],
    ["Prakarya", ["CC", "DD"]],
    ["Muatan Lokal", ["EE", "FF"]],
    ["TIK", ["GG", "HH"]],
    ["PAI", ["II", "JJ", "KK", "LL"]],
    ["BTQ", ["MM", "NN"]]
]
# Berisi mata pelajaran dan jumlah jam pelajaran dalam satu minggu di suatu kelas
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
# Berisi kelas
KELAS = ["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "7I", "7J", "8A", "8B", "8C", "8D", "8E", "8F", "8G", "8H", "8I", "8J", "9A", "9B", "9C", "9D", "9E", "9F", "9G", "9H", "9I", "9J",]
# Variabel yang akan diisi dengan index dalam individu yang menyebabkan error (nantinya akan dilakukan mutasi)
ERROR = []
"""
    Fase pengecekan kesesuai individu dengan sebuah constraint
    (1) SHIFT 0 = pengecekan constraint 2
    (2) SHIFT 1 = pengecekan constraint 1
    (3) SHIFT 2 = sudah sesuai/selesai
""" 
SHIFT = 0

"""
   (2) Generate random gen
"""
# Gen => Hari - Jam - Mapel - Guru
def generateGen():
    gen = []
    for i in range(0, int(len(HARI)/2)):
        random = rnd.randint(0,39)
        mapel = GURU[random][0]
        guru = GURU[random][1]
        gen.append([HARI[i*2][1], mapel, guru])
        gen.append([HARI[i*2+1][1], mapel, guru])
    return gen

"""
   (3) Generate random kromosom
"""
# Kromosom = Individu => kelas - hari - gen (full jadwal semua kelas)
def generateKromosom():
    # Generate Gen
    gen = []
    for i in range(0, 40):
        gen.append(generateGen())

    # Generate Kromosom
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

"""
   (4) Buat menghitung nilai fitness setiap individu
"""
def fitnessFunction(kromosom):
    """ 
        Constraint:
        1. Bentrok => Guru ada di satu hari yang sama dan jam yang sama (beda kelas).
        2. JP/Minggu untuk 1 kelas
    """
    Fitness = 0

    """ Constraint #1 """
    if(SHIFT == 1):
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
                        break
                    k = k + 40

    """ Constraint #2 """
    if(SHIFT == 0):
        x = 0
        for i in range(0, len(KELAS)):
            jp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for j in range(x, len(HARI)+x):
                for k in range(0, len(MAPEL)):
                    if (kromosom[j][2][1] == MAPEL[k][0]):
                        jp[k] += 1
                        if(jp[k] > MAPEL[k][1]):
                            Fitness = Fitness + 1
                            ERROR.append(j)
                        break
            x += 40

    """ Nilai Fitness akan memiliki range 0 - 1 """
    return 1 / ((1.0*Fitness + 1))

"""
    (5) Meng-generate file excel
"""
def generateXlsx(individu):
    # Inisialisasi
    workbook = xlsxwriter.Workbook("jadwal.xlsx")

    # Formatting Excel
    bold_format = workbook.add_format({'bold': True})
    bold_format.set_align('center')
    bold_format.set_border(True)

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    cell_format.set_align('middle')
    cell_format.set_align('center')
    cell_format.set_border(True)

    istirahat_format = workbook.add_format()
    istirahat_format.set_text_wrap()
    istirahat_format.set_align('middle')
    istirahat_format.set_align('center')
    istirahat_format.set_bg_color('yellow')
    istirahat_format.set_border(True)

    worksheet = workbook.add_worksheet('Jadwal')

    kolom = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH"]
    
    # label kelas
    for i in range(0, len(KELAS)):
        worksheet.write(kolom[i+3] + '4', individu[i*len(HARI)][0], bold_format)

    # label waktu dan hari
    shift = 0
    for i in range(0, len(HARI)):
        if (i == 0):
            worksheet.write(kolom[2] + str(i+5+shift), "07.00-07.40", istirahat_format)
            worksheet.write(kolom[1] + str(i+5+shift), "Senin", cell_format)
            shift += 1
        elif (i+shift == 4 or i+shift == 8 or i+shift == 17 or i+shift == 21 or i+shift == 29 or i+shift == 33 or i+shift == 39 or i+shift == 43):
            worksheet.write(kolom[2] + str(i+5+shift), "ISTIRAHAT", istirahat_format)
            worksheet.write(kolom[1] + str(i+5+shift), "", cell_format)
            shift += 1
            
        worksheet.write(kolom[2] + str(i+5+shift), HARI[i][1], cell_format)
        if ( (HARI[i][0] != HARI[i-1][0]) and (i != 0) ):
            worksheet.write(kolom[1] + str(i+5+shift), HARI[i][0], cell_format)
        elif (i != 0):
            worksheet.write(kolom[1] + str(i+5+shift), "", cell_format)
        
    # mapel dan guru
    for i in range(0, len(KELAS)):
        shift = 0
        x = i * len(HARI)
        for j in range(x, x + len(HARI)):
            if (j == x):
                worksheet.write(kolom[i+3] + str((j - i*len(HARI))+5+shift), "UPACARA", istirahat_format)
                shift += 1
            elif ((j-x)+shift == 4 or (j-x)+shift == 8 or (j-x)+shift == 17 or (j-x)+shift == 21 or (j-x)+shift == 29 or (j-x)+shift == 33 or (j-x)+shift == 39 or (j-x)+shift == 43):
                worksheet.write(kolom[i+3] + str((j - i*len(HARI))+5+shift), "", istirahat_format)
                shift += 1
            
            worksheet.write(kolom[i+3] + str((j - i*len(HARI))+5+shift), individu[j][2][1] + ", " + individu[j][2][2], cell_format)

    worksheet.write(kolom[1] + str(4), "HARI", bold_format)
    worksheet.write(kolom[2] + str(4), "JAM", bold_format)
    worksheet.write(kolom[1] + str(6), "", cell_format)
    
    worksheet.set_column(2, 2 + len(KELAS), width=17.5)
    
    workbook.close()
    print("==================================")
    print("||  'jadwal.xlsx' telah dibuat  ||")
    print("==================================")

""" (6) Meng-generate mata pelajaran yang error (tidak sesusai dengan constraint 2) """
def createSwapMapelError(kromosom):
    SwapMapelAll = []
    SwapMapelError = []

    # Membuat list => [[2, [154, 634, 714, 994, 1074]], [7, [756, 836, 916]]]
    for i in range(0, 20):
        SwapMapelAll.append([])
        SwapMapelError.append([])
        for j in range(0, len(MAPEL)):
            SwapMapelAll[i].append([j, []])
        # Add semua
        for j in range(0, len(KELAS)):
            index = j * 40 + i * 2
            for k in range(0, len(MAPEL)):
                if(kromosom[index][2][1] == MAPEL[k][0]):
                    SwapMapelAll[i][k][1].append(index)
                    break
        # Add yang error aja
        for j in range(0, len(MAPEL)):
            if(len(SwapMapelAll[i][j][1]) > MAPEL[j][1]):
                SwapMapelError[i].append(SwapMapelAll[i][j])
    
    return SwapMapelError

""" (7) Swap mata pelajaran dalam satu kelas yang sama untuk membatasi mata pelajaran agar tidak melebihi jumlah guru dalam suatu jam pelajaran yang sama """
def swap(kromosom):
    SwapMapelError = createSwapMapelError(kromosom)

    temp = []
    for i in range(0, len(SwapMapelError) - 1):
        for j in range(0, len(SwapMapelError[i])):
            for k in range(0, len(SwapMapelError[i][j][1])):
                for a in range(i + 1, len(SwapMapelError)):
                    for b in range(0, len(SwapMapelError[a])):
                        for c in range(0, len(SwapMapelError[a][b][1])):
                            idxI = SwapMapelError[i][j][1][k]
                            idxA = SwapMapelError[a][b][1][c]
                            # Kondisi kalau kelasnya sama dan mapel beda
                            if ( ((idxI - (idxI % 40)) == (idxA - (idxA % 40))) and (SwapMapelError[i][j][0] != SwapMapelError[a][b][0]) ):
                                # Proses pertukaran
                                temp = kromosom[idxI]
                                kromosom[idxI] = kromosom[idxA]
                                kromosom[idxA] = temp

                                temp = kromosom[idxI+1]
                                kromosom[idxI+1] = kromosom[idxA+1]
                                kromosom[idxA+1] = temp
    
    SwapMapelError = createSwapMapelError(kromosom)
    
    # Pengecekan apakah masih ada error
    i = 0
    while (i < len(SwapMapelError)):
        if (len(SwapMapelError[i]) != 0):
            i = len(SwapMapelError)
        i += 1
    
    # Kondisi jadwal masih ada error (mata pelajaran melebihi jumlah guru dalam suatu jam pelajaran yang sama)
    if (i != len(SwapMapelError)):
        # Melakukan random swap
        randomSwap(kromosom, SwapMapelError)

""" (8) Nge-swap mata pelajaran secara random dalam satu kelas yang sama """
def randomSwap(kromosom, SwapMapelError):
    temp = []
    for i in range(0, 20):
        if (len(SwapMapelError[i]) != 0):
            for k in range(0, len(SwapMapelError[i])):
                for j in range(0, len(SwapMapelError[i][k][1]) - MAPEL[SwapMapelError[i][k][0]][1]):
                    # Ngambil mata pelajaran di suatu jam pelajaran secara random dalam satu kelas yang sama
                    random = rnd.randint(0,39)
                    if (random % 2 != 0):
                        random = random - 1

                    indeks = SwapMapelError[i][k][1][j]
                    
                    # Proses pertukaran
                    temp = kromosom[indeks]
                    kromosom[indeks] = kromosom[(indeks - (indeks%40) + random)]
                    kromosom[(indeks - (indeks%40) + random)] = temp

                    temp = kromosom[indeks+1]
                    kromosom[indeks+1] = kromosom[(indeks - (indeks%40) + random)+1]
                    kromosom[(indeks - (indeks%40) + random)+1] = temp
    swap(kromosom)

""" (9) Meng-generate populasi (10 individu) """
populasi = []
for i in range(0, POPULATION_SIZE):
    populasi.append(generateKromosom())

""" (10) Main Loop """
a = 0
flag = 0
while((flag == 0) & (a < MAXIMUM_ITERATION)):
    # generate mutasi baru
    new_populasi = []
    new_populasi = copy.deepcopy(populasi)
    
    """ (11) Proses Crossover 2 individu, total 10 individu | 5 crossover """
    """ Sorting individu secara ascending berdasarkan nilai fitness """
    temp = []
    for i in range(0, len(populasi)-1):
        for j in range(i+1, len(populasi)):
            # Kondisi dimana invidu sebelah kiri nilai fitnessnya > dari individu yang kanan
            if(fitnessFunction(new_populasi[i]) > fitnessFunction(new_populasi[j])):
                # Proses pertukaran
                temp = new_populasi[i]
                new_populasi[i] = new_populasi[j]
                new_populasi[j] = temp
    """ Proses Crossover ketika SHIFT = 0 """
    """
        Note:
        (1) Banyak populasi nantinya akan berjumlah 2x Population Size => 20 (ditambah individu hasil crossover)
        (2) Individu hasil crossover nantinya akan di mutasi
        (3) Setelah dilakukan reproduksi, nantinya akan dipilih 10 individu terbaik dari 20 individu tersebut (Selection => Elitism)
    """
    if(SHIFT == 0):
        temp = []
        for i in range(0, int(POPULATION_SIZE/2)):
            # Proses crossover x<=30% data suatu individu
            for j in range(0, 360):
                temp = new_populasi[i*2][j]
                new_populasi[i*2][j] = new_populasi[i*2+1][j]
                new_populasi[i*2+1][j] = temp
            # Proses crossover x>=70% data suatu individu
            for j in range(840, 1200):
                temp = new_populasi[i*2][j]
                new_populasi[i*2][j] = new_populasi[i*2+1][j]
                new_populasi[i*2+1][j] = temp
            # Penambahan hasil crossover ke variabel populasi
            populasi.append(new_populasi[i*2])
            populasi.append(new_populasi[i*2+1])
    else:
        for i in range(0, POPULATION_SIZE):
            populasi.append(populasi[i])


    """ (12) Proses mutasi individu """
    for i in range(POPULATION_SIZE, POPULATION_SIZE*2):
        ERROR = []
        # Memanggil fungsi untuk melakukan pengecekan error pada suatu individu dan memasukkan index yang membuat error pada variabel ERROR
        fitnessFunction(populasi[i])      
        j = 0
        # Looping untuk melakukan mutasi sebanyak jumlah index data yang menyebabkan error pada suatu individu
        while(j < len(ERROR)):
            if(ERROR[j]%2 != 0):
                ERROR[j] -= 1
            if(SHIFT == 0):
                # Me-random guru dan mapel
                random = rnd.randint(0,39)
                mapel = GURU[random][0]
                guru = GURU[random][1]

                # Meng-assign guru dan mapel hasil random ke individu
                populasi[i][ERROR[j]][2][1] = mapel
                populasi[i][ERROR[j]][2][2] = guru
                populasi[i][ERROR[j]+1][2][1] = mapel
                populasi[i][ERROR[j]+1][2][2] = guru
            if(SHIFT == 1):
                for z in range(0, 13):
                    if(populasi[i][ERROR[j]][2][1] == GURU2[z][0]):
                        break
                
                # Me-random guru
                random = rnd.randint(0,len(GURU2[z][1])-1)
                guru = GURU2[z][1][random]

                # Meng-assign guru hasil random ke individu
                populasi[i][ERROR[j]][2][2] = guru
                populasi[i][ERROR[j]+1][2][2] = guru
            j += 1

    """ (13) Perhitungan nilai fitness tiap individu """
    nilai_fitness = []
    tanda = 0
    for i in range(0, len(populasi)):
        # Menghitung nilai fitness suatu individu
        nilai_fitness.append(fitnessFunction(populasi[i]))
        if(nilai_fitness[i] == 1):
            if(SHIFT == 0 and tanda == 0):
                tanda = 1
                # Melakukan swap mata pelajaran jika sudah memenuhi constraint 2
                swap(populasi[i])
                swapped_kromosom = populasi[i]
                populasi.clear()
                for j in range(0, POPULATION_SIZE*2):
                    populasi.append(swapped_kromosom)
            if(SHIFT == 0):
                SHIFT = 10
            elif(SHIFT == 1):
                SHIFT += 1
            if(SHIFT == 2 and tanda == 0):
                tanda = 1
                flag = 1
                # Pemberian output pada prompt
                print("[ Generasi ke-{} ]".format(a+1))
                print("- Cek constraint 1")
                print("- Top fitness: " + str(fitnessFunction(populasi[i])))
                print(" ")
                # Meng-generate excel berupa jadwal dari individu dengan nilai fitness 1 (sudah sesuai constraint)
                generateXlsx(populasi[i])


    """ (14) Proses sorting individu secara ascending berdasarkan nilai fitness-nya """
    for i in range(0, len(populasi)-1):
        for j in range(i+1, len(populasi)):
            if(fitnessFunction(populasi[i]) > fitnessFunction(populasi[j])):
                # Proses pertukaran
                temp = populasi[i]
                populasi[i] = populasi[j]
                populasi[j] = temp
    
    # Keluar dari looping while (sudah menemukan individu yang sesuai dengan constraint)
    if(flag == 1):
        break

    # Mengambil 10 individu terbaik
    new_populasi = copy.copy(populasi[POPULATION_SIZE:])
    # Sorting nilai fitness secara ascending
    nilai_fitness.sort()
    
    """ (15) Proses pengeluaran output dalam Prompt """
    print("[ Generasi ke-{} ]".format(a+1))
    if (SHIFT == 0):
        print("- Cek constraint 2")
    elif (SHIFT == 1):
        print("- Cek constraint 1")
    elif (SHIFT == 10):
        print("- Cek constraint 2")
        SHIFT = 1
    print("- Top fitness: " + str(nilai_fitness[19]))
    print(" ")

    populasi = []
    populasi = new_populasi.copy()

    # Iterasi
    a += 1