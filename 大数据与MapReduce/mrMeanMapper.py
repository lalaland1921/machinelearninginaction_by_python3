import sys
from numpy import mat,mean,power
def read_input(file):
    for line in file:
        yield line.rstrip()

input=read_input(sys.stdin)
input=[float(line) for line in input]
numInput=len(input)
input=mat(input)
sqInput=power(input,2)
print("%d\t%f\t%f"%(numInput,mean(input),mean(sqInput)))
print("report:still alive",file=sys.stderr)  #注意，在python3中写法，
                                      # 意思是将字符串写入file文件,这样keep alive不会进入到下一个输入中


'''succeeded'''