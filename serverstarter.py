import httpServerMT, sys
try:
    PORT=int(sys.argv[1])
except:
    PORT=8200
try:
    TIMEOUT=int(sys.argv[2])
except:
    TIMEOUT=0.25
run=httpServerMT.httpServerMT(PORT,TIMEOUT)
run.ServerActivation()
raw_input()
