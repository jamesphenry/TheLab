# Directories
INC_DIR = include
SRC_DIR = src
TST_DIR = test
PROJECT_DIR = projects
OBJ_DIR = obj
BIN_DIR = bin

# Compiler and flags
CC = gcc
CFLAGS += -std=c17 -Wall -Wextra -Werror -I$(INC_DIR)
LDFLAGS ?=

# Source files
INC = $(wildcard $(INC_DIR)/*.h)
SRC = $(wildcard $(SRC_DIR)/*.c)
TST = $(wildcard $(TST_DIR)/*.test.c)

# Main application
OBJ = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/src/%.o,$(SRC))
TARGET = $(BIN_DIR)/c-skeleton
DEBUG_TARGET = $(BIN_DIR)/c-skeleton-debug

# Discover immediate subdirectories of projects/
PROJECT_DIRS = $(wildcard $(PROJECT_DIR)/*/)
PROJECTS = $(patsubst $(PROJECT_DIR)/%/,%,$(PROJECT_DIRS))

# Build everything in the main skeleton only.
.PHONY: all
all: $(TARGET) ## Build the main application

# Main application link rule
$(TARGET): $(OBJ)
	mkdir -p $(BIN_DIR)
	$(CC) $(OBJ) -o $@ $(LDFLAGS)

# Main application object rule
$(OBJ_DIR)/src/%.o: $(SRC_DIR)/%.c $(INC)
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Build a single project using:
#   make hello
#
# Build all projects using:
#   make projects
#
# Each project must contain source files in projects/<name>/src/.
define PROJECT_template

PROJECT_$(1)_SRC = $$(wildcard $(PROJECT_DIR)/$(1)/src/*.c)
PROJECT_$(1)_INC = $$(wildcard $(PROJECT_DIR)/$(1)/include/*.h)
PROJECT_$(1)_OBJ = $$(patsubst $(PROJECT_DIR)/$(1)/src/%.c,$(OBJ_DIR)/projects/$(1)/%.o,$$(PROJECT_$(1)_SRC))

.PHONY: $(1)
$(1): $(BIN_DIR)/$(1) ## Build project $(1)

$(BIN_DIR)/$(1): $$(PROJECT_$(1)_OBJ)
	mkdir -p $(BIN_DIR)
	$$(CC) $$(PROJECT_$(1)_OBJ) -o $$@ $$(LDFLAGS)

$$(OBJ_DIR)/projects/$(1)/%.o: $(PROJECT_DIR)/$(1)/src/%.c $$(PROJECT_$(1)_INC)
	mkdir -p $$(dir $$@)
	$$(CC) $$(CFLAGS) -I$(PROJECT_DIR)/$(1)/include -c $$< -o $$@

endef

$(foreach project,$(PROJECTS),$(eval $(call PROJECT_template,$(project))))

.PHONY: projects
projects: $(addprefix $(BIN_DIR)/,$(PROJECTS)) ## Build every project

.PHONY: list-projects
list-projects: ## List available projects
	@printf '%s\n' $(PROJECTS)

# Run the main application
.PHONY: run
run: $(TARGET) ## Build and run the main application
	./$(TARGET)

# Run an individual project
# Example: make run-hello
define PROJECT_run_template

.PHONY: run-$(1)
run-$(1): $(BIN_DIR)/$(1) ## Build and run project $(1)
	./$(BIN_DIR)/$(1)

endef

$(foreach project,$(PROJECTS),$(eval $(call PROJECT_run_template,$(project))))

# Debug build
# Uses separate object files so debug flags cannot reuse normal objects.
DEBUG_OBJ = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/debug/src/%.o,$(SRC))

.PHONY: debug
debug: $(DEBUG_TARGET) ## Build the main application with debug flags

$(DEBUG_TARGET): $(DEBUG_OBJ)
	mkdir -p $(BIN_DIR)
	$(CC) $(DEBUG_OBJ) -o $@ -g $(LDFLAGS)

$(OBJ_DIR)/debug/src/%.o: $(SRC_DIR)/%.c $(INC)
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -g -Og -DDEBUG -c $< -o $@

.PHONY: run-debug
run-debug: $(DEBUG_TARGET) ## Build and run the debug version
	./$(DEBUG_TARGET)

# Run tests
.PHONY: test
test: ## Run tests
	CFLAGS="$(CFLAGS) -g -Og -I. -DTEST" sh $(TST_DIR)/test-runner/test-runner.sh $(TST)

# Fast tests without Valgrind
.PHONY: test-quick
test-quick: ## Run fast tests (no Valgrind)
	RUNNER=command CFLAGS="$(CFLAGS) -g -Og -I. -DTEST" sh $(TST_DIR)/test-runner/test-runner.sh $(TST)

.PHONY: tests
tests: test ## Alias for test

.PHONY: tests-quick
tests-quick: test-quick ## Alias for test-quick

# Syntax-check source files
ALL_SRC = $(SRC) $(foreach p,$(PROJECTS),$(wildcard $(PROJECT_DIR)/$(p)/src/*.c))

.PHONY: lint
lint: ## Lint and syntax-check sources
	$(CC) -fsyntax-only $(CFLAGS) -pedantic $(ALL_SRC)

# Run Valgrind on the main application
.PHONY: valgrind
valgrind: $(TARGET) ## Run Valgrind on the main application
	valgrind -v --leak-check=full ./$(TARGET)

# Strip symbols from the main executable
.PHONY: strip
strip: $(TARGET) ## Strip symbols from the main executable
	strip $(TARGET)

# Remove generated objects and executables
.PHONY: clean
clean: ## Remove compiled files
	rm -rf $(OBJ_DIR) $(BIN_DIR)

# Watch files for changes
.PHONY: watch
watch: ## Rebuild and test when files change
	while true; do 
		fswatch -o $(SRC) $(INC) $(TST) $(PROJECT_DIR) Makefile | 
		while read num; do 
			$(MAKE) && $(MAKE) test; 
		done; 
	done

# Display available targets
.PHONY: help
help: ## Display this help section
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "\033[32m%-24s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
