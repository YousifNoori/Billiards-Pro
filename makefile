CC = clang
CFLAGS = -Wall -pedantic -std=c99 
LDFLAGS = -shared
PYTHON_INCLUDE = -I/usr/include/python3.11


_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) $(LDFLAGS) phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

phylib_wrap.c: phylib.i
	swig -python phylib.i	

libphylib.so: phylib.o
	$(CC) $(LDFLAGS) -o libphylib.so phylib.o -lm

phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o


phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c $(PYTHON_INCLUDE) -fPIC -o phylib_wrap.o


.PHONY: clean
clean:
	rm -f *.o *.so phylib_wrap.c phylib.py *.svg