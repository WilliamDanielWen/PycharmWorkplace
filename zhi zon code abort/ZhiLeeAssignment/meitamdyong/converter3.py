
import sys
import csv
import os
import argparse

reload(sys)
sys.setdefaultencoding("utf-8")


def main():
    parser = argparse.ArgumentParser(description="Change the txt file to csv.")
    parser.add_argument("-i", action="store", dest="infile")
    parser.add_argument("-o", action="store", dest="outfile")
    parser_argument = parser.parse_args()
    all_argument = [parser_argument.infile, parser_argument.outfile]

    fatherdir = os.getcwd()  # 代码所在目录
    # 输入txt文件
    if parser_argument.infile:
        infilepaths = os.path.split(parser_argument.infile)
        # 'C:\User\lenovo\Desktop\pakistan.txt' ---> ['C:\User\lenovo\Desktop','pakistan.txt']
        if infilepaths[0]:  # 完整路径
            inputfile = parser_argument.infile
            fatherdir = infilepaths[0]
            # 'pakistan.txt' ---> ['','pakistan.txt']
        else:  # 只给一个文件名
            inputfile = fatherdir + '/' + parser_argument.infile
            # 输出csv文件
    if parser_argument.outfile:
        outfilepaths = os.path.split(parser_argument.outfile)
        if outfilepaths[0]:  # 完整路径
            outputfile = parser_argument.outfile
        else:  # 不完整
            outputfile = fatherdir + '/' + parser_argument.outfile
    else:
        outputfile = fatherdir + '/txt2csv.csv'
    parse(inputfile, outputfile)


def parse(inputfile, outputfile):
    csvcontent = file(outputfile, 'wb')
    writer = csv.writer(csvcontent)

    for line in open(inputfile).readlines():
        writer.writerow([a for a in line.split('\t')])

    csvcontent.close()


if __name__ == '__main__':
    main()
