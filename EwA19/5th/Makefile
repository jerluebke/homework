CC 		= g++
CFLAGS 	= -Wall -Wextra -I./include -O3 -std=c++11
LDFLAGS = -lm

SRCDIR 	:= src/
OBJDIR 	:= obj/

SRCFILES:= $(shell find $(SRCDIR) -name "*.cpp")
OBJFILES:= $(patsubst $(SRCDIR)%.cpp, $(OBJDIR)%.obj, $(SRCFILES))

BIN 	:= main.out

.PHONY: test

test: $(OBJFILES) $(MAINOBJ)
	$(CC) $(CFLAGS) main.cpp $^ $(LDFLAGS) -o $(BIN)

$(OBJDIR)%.obj: $(SRCDIR)%.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(OBJFILES) $(BIN)
