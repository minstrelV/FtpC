import os, time
from ftplib import FTP
import shutil

def checkFileDir(ftp,file_name):
    """
    判断当前目录下的文件与文件夹
    :param ftp: 实例化的FTP对象
    :param file_name: 文件名/文件夹名
    :return:返回字符串“File”为文件，“Dir”问文件夹，“Unknow”为无法识别
    """
    rec = ""
    try:
        rec = ftp.cwd(file_name)   # 需要判断的元素
        ftp.cwd("..")   # 如果能通过路劲打开必为文件夹，在此返回上一级
    except ftplib.error_perm as fe:
        rec = fe # 不能通过路劲打开必为文件，抓取其错误信息
    finally:
        if "Not a directory" in str(rec):
            return "File"
        elif "successful" in str(rec):
            return "Dir"
        else:
            return "Unknow"

ftp = FTP('130.130.26.225')
print ("Automated FTP Maintainance")
print ('Logging in.')
ftp.login('datahub1','datahub1')

# This is the directory that we want to go to
path = r'EFUT2SAP_SHEET_SELL_GYLN/ARCHIVE/'
print ('Changing to:' + path)
ftp.cwd(path)
#files = ftp.retrlines('NLST')
#print ('List of Files:' + files)
#--everything works fine until here!...

ls = []
#--The Logic which shall delete the files after the are 7 days old--
# for ftpfile in ftp.nlst():
#     ls = str(ftpfile).split(' ')
#     filename = ls[-1];
#     if "MSXF" in str(filename):
#         continue
#     if checkFileDir(ftp, filename) != 'Dir' :
#         L = list(ftp.sendcmd('MDTM ' + "EFUT2SAP_SHEET_SELL_GYLN/ARCHIVE/%s" % ls[-1]))
#         dir_t = L[4] + L[5] + L[6] + L[7] + '-' + L[8] + L[9] + '-' + L[10] + L[11] + ' ' + L[12] + L[13] + ':' + L[
#             14] + L[15] + ':' + L[16] + L[17]
#         timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
#         # 转换为时间戳:
#         timeStamp = int(time.mktime(timeArray))
#         atime = int(time.time())
#         if atime - timeStamp > 7 * 86400:
#             print('delete file ' + ls[-1])
#             ftp.delete(ls[-1])

for ftpfile in ftp.nlst():
    ls = str(ftpfile).split(' ')
    filename = ls[-1];
    if "MT_POS_SALES_DATA-20200720104021-44129784919939822" in str(filename):
        L = list(ftp.sendcmd('MDTM ' + ls[-1]))
        dir_t = L[4] + L[5] + L[6] + L[7] + '-' + L[8] + L[9] + '-' + L[10] + L[11] + ' ' + L[12] + L[13] + ':' + L[
            14] + L[15] + ':' + L[16] + L[17]
        timeArray = time.strptime(dir_t, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳:
        timeStamp = int(time.mktime(timeArray))
        atime = int(time.time())
         print('delete file ' + ls[-1])
        ftp.delete(ls[-1])
        break

print ('Closing FTP connection')
ftp.close()




