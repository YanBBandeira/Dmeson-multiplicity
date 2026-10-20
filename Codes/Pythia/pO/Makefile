FC = g++ -std=c++20

LIB_DIR = /home/yan/Documents/PhD/Repo/build_tmdlib2211/lib
LHAPDFS_LIBs = `lhapdf-config --cflags --libs` -lstdc++
PYTHIA8 ?= /home/yan/Documents/PhD/Repo/build_pythia8316
PYTHIA_LIB_DIR = $(PYTHIA8)/lib
PYTHIA_LIBs = -L$(PYTHIA_LIB_DIR) -lpythia8
PYTHIA_INCLUDE = $(PYTHIA8)/include
ROOT_CFLAGS = `root-config --cflags`
ROOT_LIBS = `root-config --libs`

EXEC1 = Hard_pO
SRC1 = Hard_pO.cc

EXEC2 = Soft_pO
SRC2 = Soft_pO.cc


# O laço no terminal deve ser: for ecm in 5020 9620 13000; do ./Hard_pO $ecm done
# Lista de todos os alvos (executáveis)
EXECS = $(EXEC1) $(EXEC2) 

# Declara alvos falsos (evita conflito se houver arquivos chamados 'all' ou 'clean')
.PHONY: all clean

# A primeira regra é a padrão quando você digita apenas 'make'
all: $(EXECS)


# Regras para compilar cada executável
$(EXEC1): $(SRC1)
	$(FC) $(SRC1) -I$(PYTHIA_INCLUDE) $(ROOT_CFLAGS) $(LHAPDFS_LIBs) $(PYTHIA_LIBs) $(ROOT_LIBS) -Wl,-rpath,$(PYTHIA_LIB_DIR) -o $(EXEC1)

$(EXEC2): $(SRC2)
	$(FC) $(SRC2) -I$(PYTHIA_INCLUDE) $(ROOT_CFLAGS) $(LHAPDFS_LIBs) $(PYTHIA_LIBs) $(ROOT_LIBS) -Wl,-rpath,$(PYTHIA_LIB_DIR) -o $(EXEC2)



# Limpeza dos arquivos gerados
clean:
	rm -f $(EXECS)