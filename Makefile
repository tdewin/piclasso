EMCC ?= emcc

EMCCFLAGS = -Os
EMCCFLAGS += -sSINGLE_FILE=1 -sEXPORTED_FUNCTIONS=_pikchr,_free,_malloc -sEXPORTED_RUNTIME_METHODS=ccall,getValue 
EMCCFLAGS += -sEXPORT_NAME=PikchrModule -sMALLOC=emmalloc -sMODULARIZE=1 -sENVIRONMENT=web -sSTRICT=1

all: pikchr.js

pikchr.js: pikchr.c
	$(EMCC) $(EMCCFLAGS) -o $@ $<