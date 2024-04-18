# PyASM by 410-dev
PyASM is written for fun and is not for production purpose.

.pasm file can be run using the following command:
```bash
python3 pyasm.py <file.pasm>
```
To run in debug mode,
```bash
python3 pyasm.py --debug <file.pasm>
```
Running in debugging mode will create stackdump.txt in the working directory.

I have [calculator example](examples/calculator.pasm) in the examples folder. You can run it using the following command:
```bash
python3 pyasm.py examples/calculator.pasm
```