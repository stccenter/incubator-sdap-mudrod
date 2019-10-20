import re
import time
import os
import threading
from datetime import datetime

def SwithtoNum(time):
    if time.find("Jan") != -1:
        time = time.replace("Jan", "1")
    elif time.find("Feb") != -1:
        time = time.replace("Feb", "2")
    elif time.find("Mar") != -1:
        time = time.replace("Mar", "3")
    elif time.find("Apr") != -1:
        time = time.replace("Apr", "4")
    elif time.find("May") != -1:
        time = time.replace("May", "5")
    elif time.find("Jun"):
        time = time.replace("Jun", "6")
    elif time.find("Jul") != -1:
        time = time.replace("Jul", "7")
    elif time.find("Aug") != -1:
        time = time.replace("Aug", "8")
    elif time.find("Sep") != -1:
        time = time.replace("Sep", "9")
    elif time.find("Oct") != -1:
        time = time.replace("Oct", "10")
    elif time.find("Nov") != -1:
        time = time.replace("Nov", "11")
    elif time.find("Dec") != -1:
        time = time.replace("Dec", "12")
    return time


def SwithtoMonth(time):
    time = time.replace("/07/", "/Jul/")
    return time


def ReadHttp(inputFile, num):
    logs = []
    intervals = []

    preTime = ''
    with open(inputFile) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            s = re.search(r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}", line)
            curTime = SwithtoNum(s.group(0))
            # print(curTime)
            curDateTime = datetime.strptime(curTime, '%d/%m/%Y:%H:%M:%S')

            if preTime != '':
                preDateTime = datetime.strptime(preTime, '%d/%m/%Y:%H:%M:%S')
                elapsedTime = curDateTime - preDateTime
                inteval = elapsedTime.total_seconds()
                # inteval/=100;
                intervals.append(inteval)
            else:
                startTime = curDateTime

            logs.append(line)
            preTime = curTime
            cnt += 1
            if cnt > num:
                break
    return logs, intervals, startTime


def ReadFTP(inputFile, num):
    logs = []
    intervals = []
    preTime = ''
    with open(inputFile) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            tmp = line.split()
            time = tmp[1] + ":" + tmp[2] + ":" + tmp[3] + ":" + tmp[4];
            curTime = SwithtoNum(time)
            # print(curTime)
            curDateTime = datetime.strptime(curTime, '%m:%d:%H:%M:%S:%Y')

            if preTime != '':
                preDateTime = datetime.strptime(preTime, '%m:%d:%H:%M:%S:%Y')
                elapsedTime = curDateTime - preDateTime
                inteval = elapsedTime.total_seconds()
                # inteval/=100;
                intervals.append(inteval)
            else:
                startTime = curDateTime

            logs.append(line)
            preTime = curTime
            cnt += 1
            if cnt > num:
                break

    return logs, intervals, startTime


def WriteHTTPLog(logs, intervals, outputDirectory, sleep):
    time.sleep(sleep)
    i = 0
    fileIndex = 0
    currentFileTS = time.time()
    while i < len(logs) - 1:
        if time.time() - currentFileTS > 3:
            currentFileTS = time.time()
            fileIndex += 1
            if fileIndex > 2:
                os.remove(os.path.join(outputDirectory, "http_" + str(fileIndex - 3)))

        f = open(os.path.join(outputDirectory, "http_" + str(fileIndex)), "a")
        log = logs[i]
        s = re.search(r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}", log)
        logTime = s.group(0);
        a = datetime.now().strftime("%d/%m/%Y:%H:%M:%S")
        a = SwithtoMonth(a)
        log = log.replace(logTime, a)
        print(log)
        print(intervals[i])
        f.write(log)
        f.flush()
        f.close()
        time.sleep(intervals[i])
        i += 1
    f.close()


def WriteFTPLog(logs, intervals, outputDirectory, sleep):
    time.sleep(sleep)
    i = 0
    fileIndex = 0
    currentFileTS = time.time()
    while i < len(logs) - 1:
        if time.time() - currentFileTS > 3:
            currentFileTS = time.time()
            fileIndex += 1
            if fileIndex > 2:
                os.remove(os.path.join(outputDirectory, "ftp_" + str(fileIndex - 3)))

        f = open(os.path.join(outputDirectory, "ftp_" + str(fileIndex)), "a")
        log = logs[i]
        tmp = log.split()
        logTime = tmp[1] + "  " + tmp[2] + " " + tmp[3] + " " + tmp[4];
        print(logTime)
        # Mon Feb  2 00:00:01 2015
        # 27/Jul/2018:13:43:47
        a = datetime.now().strftime("%m %d %H:%M:%S %Y")
        a = SwithtoMonth(a)
        a = a.replace("07 ", "Jul  ")
        print(a)
        log = log.replace(logTime, a)
        print(log)
        print(intervals[i])
        f.write(log)
        f.flush()
        f.close()
        time.sleep(intervals[i])
        i += 1;
    f.close()


def synLog(httpFile, ftpFile, outputDirectory, line):
    httplogs, httpIntervals, httpStart = ReadHttp(httpFile, line);
    ftplogs, ftpIntervals, ftpStart = ReadFTP(ftpFile, line);

    interval = ftpStart - httpStart
    seconds = interval.total_seconds()
    # print(ftpStart)
    # print(httpStart)
    # print(seconds)

    # ftpDir = outputDirectory+"\\ftp"
    # httpDir = outputDirectory+"\\http"
    httpsleep = 0
    ftpsleep = 0
    if seconds > 0:
        print("http first")
        ftpsleep = seconds
        # ftpsleep = 3
    else:
        print("ftp first")
        httpsleep = 0 - seconds
        # httpsleep = 4

    print(httpsleep)
    print(ftpsleep)
    t = threading.Thread(target=WriteFTPLog, args=(ftplogs, ftpIntervals, outputDirectory, ftpsleep,))
    t.setDaemon(False)
    t.start()

    t = threading.Thread(target=WriteHTTPLog, args=(httplogs, httpIntervals, outputDirectory, httpsleep,))
    t.setDaemon(False)
    t.start()

httpPath = 'stream_source/HTTP'
ftpPath = 'stream_source/FTP'
outputDirectory = 'stream_output'
synLog(httpPath, ftpPath, outputDirectory, 50)
