# Makefile

# Définir le compilateur C++
CXX = g++

# Options de compilation
CXXFLAGS = -DLIKWID_PERFMON -fopenmp -Wall -O0 -g -std=c++11

# Options de linkage
LDFLAGS = -fopenmp
LIBS = -llikwid

# Fichiers sources
SRCS = main.cpp Expgen.cpp RecSys.cpp GraphMatrix.cpp pageRank.cpp Evaluation.cpp utils.cpp

# Fichiers objets
OBJS = $(SRCS:.cpp=.o)

# Nom de l'exécutable
TARGET = GraFC2T2_unoptimized

# Règle par défaut
all: $(TARGET)

# Génération de l'exécutable
$(TARGET): $(OBJS)
	$(CXX) $(OBJS) -o $@ $(LDFLAGS) $(LIBS)

# Compilation des fichiers objets
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Nettoyage
clean:
	rm -f $(OBJS) $(TARGET)
