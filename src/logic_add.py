#
# A very complicated way of adding two integer numbers: simulating
# logic gates.
#
# Copyright (C) 2018 Ariel Ortiz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

#----------------------------------------------------------
class Observable:
    '''An observable (subject) base class for implementing
    the Observer Design Pattern (Gamma, et al. 1994).
    '''

    def __init__(self):
        '''Initialize an observable instance.
        '''
        self.__observers = []

    def add_observer(self, observer):
        '''Add an observer to this observable object.
        '''
        self.__observers.append(observer)

    def notify_observers(self, *args):
        '''Notify all the observers by calling their
        `update` method.
        '''
        for observer in self.__observers:
            observer.update(*args)

#----------------------------------------------------------
class Wire(Observable):
    '''Represents wire objects to connect components.

    An instance of this class is an observable object,
    thus multiple observers can be registered in order to
    be notified when its value is set.

    >>> wire = Wire()
    >>> Display('out1', wire)
    <...>
    >>> Display('out2', wire)
    <...>
    >>> wire.set(0)
    out1: 0
    out2: 0
    '''

    def set(self, value):
        '''Set the `value` property to 1 or 0 and notify
        all its observers.
        '''
        assert value in [0, 1]
        self.__value = value
        self.notify_observers()

    def is_set(self):
        '''Check if the `value` property has been set.
        '''
        try:
            self.__value
            return True
        except AttributeError:
            return False

    def get_value(self):
        '''Get the `value` property.
        '''
        return self.__value

    value = property(get_value)

#----------------------------------------------------------
class Display:
    '''A class for displaying the single bit value when a
    wire is set.

    >>> wire1 = Wire()
    >>> Display('wire1', wire1)
    <...>
    >>> wire1.set(0)
    wire1: 0

    >>> wire2 = Wire()
    >>> Display('wire2', wire2)
    <...>
    >>> wire2.set(1)
    wire2: 1
    '''

    def __init__(self, name, wire):
        '''Initialize a display object with a name and an
        input wire.

        This display object will be registered as an
        observer of its input wire.
        '''
        self.__name = name
        self.__wire = wire
        wire.add_observer(self)

    def update(self):
        '''Called automatically when its input wire is
        set.
        '''
        print('{0}: {1}'.format(self.__name,
                                self.__wire.value))

#----------------------------------------------------------
class DoubleInputGate:
    '''Base clase for a logic gate with two inputs.
    '''

    def __init__(self, input1, input2, output):
        '''Initialize a gate with two input and one output
        wires.

        This gate will be registered as an observer of the
        two input wires.
        '''
        self.__input1 = input1
        self.__input2 = input2
        self.__output = output
        input1.add_observer(self)
        input2.add_observer(self)

    def update(self):
        '''Called automatically when one of the input
        wires is set.

        Sets the corresponding output wire to the expected
        result only when both input wires have been set.
        '''
        if self.__input1.is_set() and self.__input2.is_set():
            self.__output.set(
                self.operation(self.__input1.value,
                               self.__input2.value))

#----------------------------------------------------------
class AndGate(DoubleInputGate):
    '''Represents an AND logic gate.

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> AndGate(in1, in2, out)
    <...>
    >>> Display('Out', out)
    <...>
    >>> in1.set(1)
    >>> in2.set(1)
    Out: 1

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> AndGate(in1, in2, out)
    <...>
    >>> Display('Out', out)
    <...>
    >>> in1.set(1)
    >>> in2.set(0)
    Out: 0
    '''

    def operation(self, x, y):
        '''Returns x AND y.

        x and y should be 1 or 0.
        '''
        return x & y

#----------------------------------------------------------
class OrGate(DoubleInputGate):
    '''Represents an OR logic gate.

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> OrGate(in1, in2, out)
    <...>
    >>> Display('Out', out)
    <...>
    >>> in1.set(1)
    >>> in2.set(0)
    Out: 1

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> OrGate(in1, in2, out)
    <...>
    >>> Display('Out', out)
    <...>
    >>> in1.set(0)
    >>> in2.set(0)
    Out: 0
    '''

    def operation(self, x, y):
        '''Returns x OR y.

        x and y should be 1 or 0.
        '''
        return x | y

#----------------------------------------------------------
class XorGate(DoubleInputGate):
    '''Represents an XOR logic gate.

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> XorGate(in1, in2, out)
    <...>
    >>> Display('Out', out)
    <...>
    >>> in1.set(1)
    >>> in2.set(0)
    Out: 1

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> XorGate(in1, in2, out)
    <...>
    >>> Display('Out', out)
    <...>
    >>> in1.set(1)
    >>> in2.set(1)
    Out: 0
    '''

    def operation(self, x, y):
        '''Returns x XOR y.

        x and y should be 1 or 0.
        '''
        return x ^ y

#----------------------------------------------------------
class HalfAdder:
    '''Represents a half adder for summing two bits and
    producing a one bit result and a one bit carry.

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> out = Wire()
    >>> carry = Wire()
    >>> HalfAdder(in1, in2, out, carry)
    <...>
    >>> Display('Sum', out)
    <...>
    >>> Display('Carry', carry)
    <...>
    >>> in1.set(1)
    >>> in2.set(1)
    Sum: 0
    Carry: 1
    '''

    def __init__(self, input1, input2, output, carry_out):
        '''Initialize a half adder with two input bits,
        the output bit of the addition and a carry.
        '''
        XorGate(input1, input2, output)
        AndGate(input1, input2, carry_out)

#----------------------------------------------------------
class FullAdder:
    '''Represents a full adder for adding three bits (two
    input bits and one carry input bit) and producing a one
    bit result and a one bit carry.

    >>> in1 = Wire()
    >>> in2 = Wire()
    >>> carry_in = Wire()
    >>> out = Wire()
    >>> carry_out = Wire()
    >>> FullAdder(in1, in2, carry_in, out, carry_out)
    <...>
    >>> Display('Sum', out)
    <...>
    >>> Display('Carry', carry_out)
    <...>
    >>> in1.set(1)
    >>> in2.set(1)
    >>> carry_in.set(1)
    Sum: 1
    Carry: 1
    '''

    def __init__(self, input1, input2, carry_in,
                 output, carry_out):
        '''Initialize a full adder with two inputs, an
        input carry, the output of the addition and a
        carry.
        '''
        wire1 = Wire()
        wire2 = Wire()
        wire3 = Wire()
        HalfAdder(input1, input2, wire1, wire2)
        HalfAdder(carry_in, wire1, output, wire3)
        OrGate(wire3, wire2, carry_out)

#----------------------------------------------------------
def to_binary(n, num_bits):
    '''Create a list of num_bits binary digits equal to n.

    Least significant bits are at the beginning of the
    resulting list, which is always of size num_bits.
    Most significant bits are truncated if result doesn't
    fit in num_bits.

    >>> to_binary(8, 4)
    [0, 0, 0, 1]

    >>> to_binary(15, 8)
    [1, 1, 1, 1, 0, 0, 0, 0]

    >>> to_binary(256, 8)
    [0, 0, 0, 0, 0, 0, 0, 0]

    >>> to_binary(256, 9)
    [0, 0, 0, 0, 0, 0, 0, 0, 1]
    '''
    result = []
    while len(result) < num_bits:
        result.append(n & 1)
        n >>= 1
    return result

#----------------------------------------------------------
def from_binary(lst):
    '''Compute the numeric value of a list of binary
    digits.

    Least significant bits are assumed to be at the
    beginning of lst.

    >>> from_binary([0, 0, 0, 1])
    8

    >>> from_binary([0, 1, 0, 0, 0, 0, 0, 0])
    2

    >>> from_binary([])
    0
    '''
    result = 0
    for d in lst[::-1]:
        result <<= 1
        result |= d
    return result

#----------------------------------------------------------
def build_circuit(n):
    '''Builds the complete circuit for performing the
    addition of two integer numbers of size n bits each.

    The funtion creates and wires together n full adders.
    It returns a three element tuple with the following:
    - A list of n wires for the first number to add.
    - A list of n wires for the second number to add.
    - A list of n wires for the result of the addition.
    The carry of the addition of the two most significant
    bits is always discarded.
    '''
    inputs1 = []
    inputs2 = []
    outputs = []
    first_carry = Wire()
    first_carry.set(0)
    previous_carry = first_carry
    for i in range(n):
        inputs1.append(Wire())
        inputs2.append(Wire())
        outputs.append(Wire())
        new_carry = Wire()
        FullAdder(inputs1[i],
                  inputs2[i],
                  previous_carry,
                  outputs[i],
                  new_carry)
        previous_carry = new_carry
    return inputs1, inputs2, outputs

#----------------------------------------------------------
class Converter:
    '''A class for converting a series of bits represented
    as a list of wires into its corresponding integer
    value.

    Least significant bits are at the beginning of the
    specified wire list.

    >>> wires = [Wire(), Wire(), Wire()]
    >>> r = Converter(wires)
    >>> wires[0].set(0)
    >>> wires[1].set(0)
    >>> wires[2].set(1)
    >>> r.result
    4
    '''

    def __init__(self, outputs):
        '''Initialize a converter object with the specified
        list of output wires.

        This converter will be registered as an observer of
        each wire in the outputs list.
        '''
        self.__outputs = outputs
        for output in outputs:
            output.add_observer(self)

    def update(self):
        '''Called automatically when any of its wires is
        set.

        Sets the `result` property when all the wires have
        been set.
        '''
        if all([output.is_set() for output in self.__outputs]):
            binary_list = [output.value
                            for output in self.__outputs]
            self.__result = from_binary(binary_list)
            self.__sign = binary_list[-1]

    def get_result(self):
        '''Get the `result` property.
        '''
        return self.__result

    result = property(get_result)

    def get_sign(self):
        '''Get the `sign` property.
        '''
        return self.__sign

    sign = property(get_sign)

#----------------------------------------------------------
def add(a, b, num_bits=32):
    '''Computes the addition of a plus b using the
    specified number of bits.

    Builds a circuit made of num_bits full adders to
    perform the binary addition of the two input numbers.
    Values are assumed to be in two's complement, that
    means that the most significant bit is considered the
    sign bit.

    >>> add(1, 2)
    3
    >>> add(255, 1, 8)
    0
    >>> add(100, 200, 8)
    44
    >>> add(-42, 42)
    0
    >>> add(-1000, -1)
    -1001
    >>> add(1, -1000)
    -999
    >>> add(127, 128, 8)
    -1
    >>> add(1, 1, 2)
    -2
    >>> add(add(add(add(add(4, 8), 15), 16), 23), 42)
    108
    '''
    inputs1, inputs2, outputs = build_circuit(num_bits)
    r = Converter(outputs)
    for input1, input2, dig1, dig2 in zip(inputs1,
                                          inputs2,
                                          to_binary(a, num_bits),
                                          to_binary(b, num_bits)):
        input1.set(dig1)
        input2.set(dig2)
    if r.sign == 1:
        return -(2 ** num_bits - r.result)
    else:
        return r.result

#----------------------------------------------------------
# Run unit tests if this file isn't loaded as a module.
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
