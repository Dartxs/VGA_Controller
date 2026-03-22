TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
	../../RTL/char_selector.sv \
	../../package/vga_controller_pkg.sv

TOPLEVEL = char_selector
COCOTB_TEST_MODULES = test_char_selector

EXTRA_ARGS += --trace --trace-structs
EXTRA_ARGS += -I../../package

export PYTHONPATH := ..:$(PYTHONPATH)

include $(shell cocotb-config --makefiles)/Makefile.sim