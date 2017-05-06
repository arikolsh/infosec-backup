import assemble
import string
import itertools
import re


GENERAL_REGISTERS = [
    'eax', 'ebx', 'ecx', 'edx', 'esi', 'edi'
]


ALL_REGISTERS = GENERAL_REGISTERS + [
    'esp', 'eip', 'ebp'
]


class GadgetSearch(object):
    def __init__(self, dump_path, start_addr):
        self.dump_path = dump_path
        self.start_addr = start_addr

    def get_format_count(self, gadget_format):
        place_holders = []
        count = 0
        for x in string.Formatter().parse(gadget_format):
            # check if valid place holder and wasnt counted already
            if x[1] is not None and x[1] not in place_holders:
                count += 1
                place_holders.append(x[1])
        return count

    def get_register_combos(self, nregs, registers):
        combos = []
        # generate permutations with repetition
        perms = [p for p in itertools.product(registers, repeat=nregs)]
        # convert tuples to arrays and put all in one big combos array
        for perm in perms:
            combos.append([perm[i] for i in range(nregs)])
        return combos

    def format_all_gadgets(self, gadget_format, registers):
        # get number of place holders
        num_p_holders = self.get_format_count(gadget_format)
        # get all possible combos of filling the place holders
        combos = self.get_register_combos(num_p_holders, registers)
        gadgets = []
        for combo in combos:
            gadgets.append((gadget_format.format(*combo)))
        return gadgets

    def find_all(self, gadget):
        # open dump file
        dump_file = open(self.dump_path, 'r')
        # put contents of file in dump
        dump = dump_file.read()
        # construct gadget with ret which we want to search
        gadget_asm = assemble.assemble_data(gadget + '; ret')
        positions = []
        # construct list with all positions relative to start addr of gadget
        index = 0
        while(index < len(dump)):
            index = dump.find(gadget_asm, index)
            if index == -1:
                break
            positions.append(self.start_addr + index)
            index += len(gadget_asm)
        # close file
        dump_file.close()
        return positions

    def find(self, gadget, condition=None):
        """
        Return the first result of find_all. If condition is specified, only
        consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(addr for addr in self.find_all(gadget) if condition(addr))
        except StopIteration:
            raise ValueError("Couldn't find matching address for " + gadget)

    def find_all_formats(self, gadget_format, registers=GENERAL_REGISTERS):
        result = []
        # construct all possible gadgets with given registers
        gadgets = self.format_all_gadgets(gadget_format, registers)
        # for each gadget find first address in dump if any
        for gadget in gadgets:
            try:
                result.append((gadget, self.find(gadget)))
            except Exception:
                pass
        return result

    def find_format(self, gadget_format, registers=GENERAL_REGISTERS, condition=None):
        """
        Return the first result of find_all_formats. If condition is specified,
        only consider addresses that meet the condition.
        """
        condition = condition or (lambda x: True)
        try:
            return next(
                addr for addr in self.find_all_formats(gadget_format, registers)
                if condition(addr))
        except StopIteration:
            raise ValueError(
                "Couldn't find matching address for " + gadget_format)


x = GadgetSearch("libc.bin", 0xb7c39750)
