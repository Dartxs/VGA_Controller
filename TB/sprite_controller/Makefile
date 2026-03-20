TOPLEVEL_LANG = verilog
SIM = verilator

VERILOG_SOURCES = \
	../../RTL/sprite_controller.sv \
	../../package/vga_controller_pkg.sv

TOPLEVEL = sprite_controller
COCOTB_TEST_MODULES = test_sprite_controller

EXTRA_ARGS += --trace --trace-structs
EXTRA_ARGS += -I../../package
EXTRA_ARGS += -GMOVE_FREQ=100000000

export PYTHONPATH := ..:$(PYTHONPATH)

include $(shell cocotb-config --makefiles)/Makefile.sim