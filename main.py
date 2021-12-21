import os
import shutil
import time  # для ожидания перед завершением работы программы


class fileio:  # объявляем класс fileio для того, чтобы работать с файлами

    RAM = 1024 * 1024  # размер буфера в байтах

    # шифрование и дешифрование имеют одинаковую скорость операций и они не изменяют размер папки, а также не создают файлы в процессе работы, благодаря чему можно экономить вычислительные ресурсы!
    # шифрование присходит следующим образом: в настоящем файле к каждому байту прибавляется значение байта из следующего файла с позиции размера предыдущего файла, поделённого по модулю.
    # на размер следующего файла. В случае достижения указателя следующего файла конца этого файла - указатель переходит в начало этого файла.
    def encrypt(path):
        counter = 0
        filecounter = fileio.countfiles(path)
        while counter < filecounter:
            print("Осталось зашифровать еще: " + str(filecounter - counter) + " файлов!")
            lastfilesize = fileio.size(fileio.getFileByID(path, counter - 1))
            filesize = fileio.size(fileio.getFileByID(path, counter))
            nextfilesize = fileio.size(fileio.getFileByID(path, counter + 1))
            currentfile = open(fileio.getFileByID(path, counter), "r+b")
            seekpos = 0
            tellpos = 0
            nextfile = open(fileio.getFileByID(path, counter + 1), "rb")
            if lastfilesize > 0 and nextfilesize > 0:
                nextfile.seek(lastfilesize % nextfilesize)
            tempsize = filesize
            while tempsize > 0:
                if tempsize >= fileio.RAM:
                    data1 = currentfile.read(fileio.RAM)
                    tempsize -= fileio.RAM
                else:
                    data1 = currentfile.read(tempsize)
                    tempsize -= tempsize
                arr = bytearray(data1)
                i = 0
                if nextfilesize > 0:
                    while i < len(arr):
                        if (nextfile.tell() == nextfilesize):
                            nextfile.seek(0)
                        t = nextfile.read(1)
                        arr[i] = (arr[i] + t[0]) % 256
                        i += 1
                tellpos = currentfile.tell()
                currentfile.seek(seekpos)
                currentfile.write(arr)
                currentfile.seek(tellpos)
                seekpos = tellpos
            currentfile.flush()
            currentfile.close()
            counter += 1

    # дешифрование происходит таким же образом, как и шифрование, но значения байтов следующего файла не прибавляются, а отнимаются, а также все операции выполняются
    # не от первого файла к последнему, а наоборот, то есть от последнего файла к первому.
    def decrypt(path):
        counter = fileio.countfiles(path) - 1
        while counter >= 0:
            print("Осталось расшифровать еще: " + str(counter + 1) + " файлов!")
            lastfilesize = fileio.size(fileio.getFileByID(path, counter - 1))
            filesize = fileio.size(fileio.getFileByID(path, counter))
            nextfilesize = fileio.size(fileio.getFileByID(path, counter + 1))
            currentfile = open(fileio.getFileByID(path, counter), "r+b")
            seekpos = 0
            tellpos = 0
            nextfile = open(fileio.getFileByID(path, counter + 1), "rb")
            if lastfilesize > 0 and nextfilesize > 0:
                nextfile.seek(lastfilesize % nextfilesize)
            tempsize = filesize
            while tempsize > 0:
                if tempsize >= fileio.RAM:
                    data1 = currentfile.read(fileio.RAM)
                    tempsize -= fileio.RAM
                else:
                    data1 = currentfile.read(tempsize)
                    tempsize -= tempsize
                arr = bytearray(data1)
                i = 0
                if nextfilesize > 0:
                    while i < len(arr):
                        if (nextfile.tell() >= nextfilesize):
                            nextfile.seek(0)
                        t = nextfile.read(1)
                        arr[i] = (arr[i] - t[0]) % 256
                        i += 1
                tellpos = currentfile.tell()
                currentfile.seek(seekpos)
                currentfile.write(arr)
                currentfile.seek(tellpos)
                seekpos = tellpos
            currentfile.flush()
            currentfile.close()
            counter -= 1

    # далее пойдут некоторые базовые функции для работы с папками и файлами

    def isDir(path):
        return os.path.isdir(path)

    def isFile(path):
        return os.path.isfile(path)

    def createFile(path):
        file = open(path, "w")
        file.close()

    def createDir(path):
        if not fileio.exists(path):
            os.mkdir(path)

    def exists(path):
        return os.path.exists(path)

    def delete(path):
        if fileio.isDir(path):
            shutil.rmtree(path)  # удаляем всё дерево каталога, то есть папку со всем содержимым в ней
        else:
            os.remove(path)  # удаляем файл

    def size(path):
        if fileio.isFile(path):
            return os.path.getsize(path)
        else:
            size = 0
            for subdir, dirs, files in os.walk(
                    path):  # здесь и далее, везде где есть строка с os.walk - там перебор всех папок и файлов в родительской папке path
                for f in files:
                    fp = os.path.join(subdir, f)  # тоже самое, как и subdir + "\\" + f.name
                    size += os.path.getsize(fp)  # суммирование размеров всех файлов
            return size

    def getAbsolutePath(path):
        return os.path.abspath(path)

    def read(path, seek, size):
        f = open(path, "r")
        f.seek(seek)
        data = f.read(size)
        f.close()
        return data

    def rewrite(path, data):  # перезапись файла
        out_file = open(path, "w")
        out_file.write(data)
        out_file.close()

    def append(path, data):  # дозапись в конец файла
        out_file = open(path, "a")
        out_file.write(data)
        out_file.close()

    def rename(path1, path2):
        os.rename(path1, path2)

    def copy(path1, path2):
        if fileio.isFile(path1):
            shutil.copy2(path1, path2)
        else:
            shutil.copytree(path1, path2)

    def move(path1, path2):
        shutil.move(path1, path2)

    def countfiles(path):
        counter = 0;
        for subdir, dirs, files in os.walk(path):
            for f in files:
                counter += 1
        return counter

    def getFileByID(path, fileid):
        if fileid > fileio.countfiles(path) - 1 or fileid < 0:
            fileid = fileid % fileio.countfiles(path)
        counter = 0;
        for subdir, dirs, files in os.walk(path):
            for f in files:
                if counter == fileid:
                    return subdir + "\\" + f
                counter += 1
        return ""


def interface():  # здесь находится интерфейс
    print("Добро пожаловать в программу перекрёстного шифрования данных CrosEnSys!")
    print("Посмотреть список команд можно командой \"commands\"")
    isRun = True
    command = ""
    while isRun:
        command = input("\n---> ")
        print()
        if command == "commands":
            print("Список команд CrosEnSys:")
            print("commands - пулучить список команд")
            print("information - получить информацию о программе")
            print("instruction - получить инструкцию к программе")
            print("encrypt - зашифровать все файлы в указанной папке")
            print("decrypt - расшифровать все файлы в указанной папке")
            print("evaluate - выполненить однострочную команду в интерпретаторе Python")
            print("system - выполненить однострочную команду в системной консоли")
            print("getram - получить размер буфера")
            print("setram - установить размер буфера")
            print("isdir - проверка принадлежности указанного пути к папке")
            print("isfile - проверка принадлежности указанного пути к файлу")
            print("createfile - создать новый файл")
            print("createdir - создать новую папку")
            print("exists - проверка папки или файла на существование")
            print("countfiles - посчитать, сколько файлов в указанной папке")
            print("getfile - получить путь к файлу по его порядковому номеру в указанной папке (индексация от нуля)")
            print("clear - очистить файл")
            print("delete - удалить папку или файл")
            print("size - определить размер папки или файла")
            print("getabsolutepath - получить абсолютный путь к папке или файлу")
            print("read - прочитать файл")
            print("rewrite - перезаписать файл")
            print("write - дозаписать в файл")
            print("append - дозаписать в файл")
            print("rename - переименовать папку или файл")
            print("copy - скопировать папку или файл")
            print("move - переместить папку или файл")
            print("! - игнорировать следующее сообщение")
            print("exit - выйти из программы")
            print("stop - выйти из программы")
        elif command == "information":
            print("******* Информация *******")
            print("  Версия: 1.0 Release")
            print("  Почта: Sasha.kuzmenko.2001@mail.ru")
            print("  Задача:")
            print(
                "        Основной задачей данного проекта является перекрёстное шифрование и дешифрование файлов в указанной папке.")
        elif command == "instruction":
            print("Инструкция:")
            print(
                "    Необходимо запустить программу и ознакомиться с данной инструкцией, информацией и списком команд, после чего можно работать с программой. Шифровать и дешифровать папку, в которой находится всего лишь один файл - недопустимо! Шифровать и дешифровать пустую папку - бессмысленно!")
        elif command == "encrypt":
            path = input("Введите путь к папке --> ")
            if fileio.exists(path):
                if fileio.isDir(path):
                    fileio.encrypt(path)
                    print("Файлы успешно зашифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command == "decrypt":
            path = input("Введите путь к папке --> ")
            if fileio.exists(path):
                if fileio.isDir(path):
                    fileio.decrypt(path)
                    print("Файлы успешно дешифрованы!")
                else:
                    print("Нужно указать папку, а не файл!")
            else:
                print("Указанной папки не существует!")
        elif command == "evaluate":
            eval(input("eval --> "))
        elif command == "system":
            print(os.system(input("system --> ")))
        elif command == "setram":
            fileio.RAM = int(input("Введите размер буфера в байтах --> "))
        elif command == "getram":
            print("Размер буфера в байтах " + str(fileio.RAM))
        elif command == "isfile":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    print("По указанному пути находится файл!")
                else:
                    print("По указанному пути находится не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "isdir":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isDir(path):
                    print("По указанному пути находится папка!")
                else:
                    print("По указанному пути находится не папка!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "createfile":
            fileio.createFile(input("Введите путь к файлу --> "))
            print("Файл создан!")
        elif command == "createdir":
            fileio.createDir(input("Введите путь к папке --> "))
            print("Папка создана!")
        elif command == "exists":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    print("Файл найден!")
                else:
                    print("Папка найдена!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "countfiles":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isDir(path):
                    print("Всего в указанной папке " + str(fileio.countfiles(path)) + " файлов!")
                else:
                    print("Требуется указать папку, а не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "getfile":
            path = input("Введите путь --> ")
            fileid = input("Введите порядковый номер файла (от нуля)")
            if fileio.exists(path):
                if fileio.isDir(path):
                    print("Путь к указанному по порядковому номеру файлу: " + fileio.getFileByID(path, fileid))
                else:
                    print("Требуется указать папку, а не файл!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "clear":
            path = input("Введите путь к файлу --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.rewrite(path, "");
                    print("Файл очищен!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command == "delete":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.delete(path)
                    print("Файл по указанному пути успешно удалён!")
                else:
                    fileio.delete(path)
                    print("Папка по указанному пути успешно удалена со всем содержимым!")
            else:
                print("По указанному пути ничего не найдено")
        elif command == "size":
            path = input("Введите путь к файлу --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    print("Размер файла в байтах: " + str(fileio.size(path)))
                else:
                    print("Размер папки в байтах: " + str(fileio.size(path)))
            else:
                print("Путь указан не верно")
        elif command == "getabsolutepath":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    print("Абсолютный путь к указанному файлу: " + fileio.getAbsolutePath(path))
                else:
                    print("Абсолютный путь к указанной папке: " + fileio.getAbsolutePath(path))
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "read":
            path = input("Введите путь к файлу --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    size = int(input("Сколько символов нужно считать --> "))
                    seek = int(input("Сколько символов пропустить перед считыванием --> "))
                    if size > -1:
                        if seek > -1:
                            if size <= fileio.size(path):
                                if seek <= fileio.size(path):
                                    if seek + size <= fileio.size(path):
                                        print("Начало сообщения:")
                                        print(fileio.read(path, seek, size))
                                        print("Конец сообщения!")
                                    else:
                                        print("Область считывания выходит за границы файла!")
                                else:
                                    print("Недопустимо пропускать количество байтов, большее размера файла")
                            else:
                                print("Недопустимо считать количество байтов, большее размера файла")
                        else:
                            print("Недопустимо пропускать отрицательное количество байтов!")
                    else:
                        print("Недопустимо считать отрицательное количество байтов!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command == "rewrite":
            path = input("Введите путь к файлу --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.rewrite(path, input("Введите сообщение --> "));
                    print("Файл успешно перезаписан!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command == "write" or command == "append":
            path = input("Введите путь к файлу --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.append(path, input("Введите сообщение --> "));
                    print("Данные успешно дозаписаны в файл!")
                else:
                    print("Требуется указать файл, а не папку!")
            else:
                print("Файл по указанному пути не найден!")
        elif command == "rename":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.rename(path, input("Введите путь к файлу вместе с новым именем --> "))
                    print("Файл успешно переименован!")
                else:
                    fileio.rename(path, input("Введите путь к папке с новым наименованием --> "))
                    print("Папка успешно переименована!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "copy":
            path = input("Введите путь --> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.copy(path, input("Куда скопировать файл --> "))
                    print("Файл успешно скопирован!")
                else:
                    fileio.copy(path, input("Куда скопировать папку --> "))
                    print("Папка успешно скопирована!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "move":
            path = input("Введите путь--> ")
            if fileio.exists(path):
                if fileio.isFile(path):
                    fileio.move(path, input("Куда переместить файл --> "))
                    print("Файл успешно перемещён!")
                else:
                    fileio.move(path, input("Куда переместить папку --> "))
                    print("Папка успешно перемещена!")
            else:
                print("По указанному пути ничего не найдено!")
        elif command == "":
            print()
        elif command == "!":
            input("\n--> ");
            print()
        elif command == "exit" or command == "stop":
            isRun = False
            print("Выход из программы CrosEnSys...\n")
            time.sleep(3)
        else:
            print("Неизвестная команда!")


def main():  # главный метод main
    interface()  # весь интерфейс программы


main()  # запуск главного метода main
