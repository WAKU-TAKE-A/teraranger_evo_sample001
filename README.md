# teraranger_evo_sample001

Sample of TeraRanger Evo Mini.

PySerial is required. Execute "pip install pyserial".

Copy "Teraranger_evo.py" to the Lib folder.

"Teraranger_evo.py" is a module that measures distance in the mode of "PRINT OUT MODE = TEXT / PIXEL MODE = PIXEL1 / RANGE MODE = LONG".

Try the following.

```
import teraranger_evo as evo

conn = evo.TeraRangerEvoMini('COM1')
conn.getLength()
```
