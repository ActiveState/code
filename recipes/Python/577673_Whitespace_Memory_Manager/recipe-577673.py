# HEAP[0] = temporary memory for anyone.
# HEAP[-1] = beginning of dynamic memory.
# HEAP[-2] = number of blocks allocated.

################################################################################

# Untested Functions:
#     print_stack_c_string()
#     raise(error)
#     trace(reference)

# Standard Memory Functions:
#     malloc(cells) -> pointer
#     calloc(block_count, block_size) -> pointer
#     free(pointer)
#     realloc(pointer, cells) -> pointer

# Debugging Memory Functions:
#     memory_manager_size(pointer) -> block_size
#     memory_manager_blocks() -> block_count
#     memory_manager_cells() -> used_memory
#     memory_manager_pointers(include_self) -> pointer_array
#     memory_manager_find(address) -> pointer
#     memory_manager_hash() -> hash_number

# Utility Memory Functions:
#     clear(start_address, end_address)
#     copy(from_start, from_end, to_start, to_end)
#     compare_cells(addr_a, addr_b) -> -1, 0, +1
#     compare_memory(a, b, length) -> -1, 0, +1
#     range(address, start, stop, step)
#     mark(pointer)
#     sum_length_array(array) -> sum

# Private Memory Functions:
#     memory_manager_append_cell(start, end)
#     memory_manager_get_cell(index) -> start, end
#     memory_manager_insert_cell(start, end, index)
#     malloc_check_beginning(cells) -> enough_space
#     malloc_check_ranges(cells) -> index
#     malloc_ranges(cells) -> pointer
#     memory_manager_search(pointer) -> index
#     memory_manager_pop_cell(index) -> start, end
#     memory_manager_get_block_size(index) -> size
#     memory_manager_set_cell(start, end, index)
#     memory_manager_deflate_block(cells, index)
#     memory_manager_inflate_cell(cells, index)
#     memory_manager_potential_after(index) -> size
#     memory_manager_potential_before(index) -> size
#     memory_manager_compress(index) -> address
#     memory_manager_inflate_before(pointer, cells, index) -> pointer
#     memory_manager_inflate_move(pointer, cells, index) -> pointer
#     memory_manager_inflate_block(pointer, cells, index) -> pointer

# Stack Helper Functions:
#     rotate_3_down()
#     rotate_3_up()
#     save_stack(size) -> pointer
#     load_stack(pointer, size)

# Number Manipulation Functions:
#     abs_diff(a, b) -> number
#     get_addr(offset, start, end) -> address
#     direction(number) -> -1, 0, +1
#     uint_cast(number) -> uint
#     left_shift(number, shift) -> number
#     right_shift(number, shift) -> number
#     divmod(x, y) -> div, mod
#     value_to_array(value, base) -> array
#     array_to_value(array, base) -> value
#     uint_bits(number) -> bits
#     uint_xor(a, b) -> xor_value

################################################################################

# Error 1   = Copy's two ranges are not equal.
# Error 2   = abs_diff(2, 1) != 1
# Error 3   = abs_diff(1, 2) != 1
# Error 4   = get_addr(1, 1, 4) != 2
# Error 5   = get_addr(2, 1, 4) != 3
# Error 6   = get_addr(1, 4, 1) != 3
# Error 7   = get_addr(2, 4, 1) != 2
# Error 8   = heap[1] != 0 after clear()
# Error 9   = heap[2] != 0 after clear()
# Error 10  = heap[1] != 0 after clear()
# Error 11  = heap[2] != 0 after clear()
# Error 12  = heap[3] != 1 after copy(1, 2, 3, 4)
# Error 13  = heap[4] != 2 after copy(1, 2, 3, 4)
# Error 14  = heap[3] != 2 after copy(1, 2, 4, 3)
# Error 15  = heap[4] != 1 after copy(1, 2, 4, 3)
# Error 16  = heap[3] != 1 after copy(2, 1, 4, 3)
# Error 17  = heap[4] != 2 after copy(2, 1, 4, 3)
# Error 18  = heap[3] != 2 after copy(2, 1, 3, 4)
# Error 19  = heap[4] != 1 after copy(2, 1, 3, 4)
# Error 20  = heap[-2] != 0
# Error 21  = heap[-2] != 1
# Error 22  = heap[-3] != 100
# Error 23  = heap[-4] != 200
# Error 24  = heap[-2] != 2
# Error 25  = heap[-5] != 300
# Error 26  = heap[-6] != 400
# Error 27  = Memory manager cell is out of range.
# Error 28  = MM[0][0] != 80
# Error 29  = MM[0][1] != 90
# Error 30  = MM[1][0] != 100
# Error 31  = MM[1][1] != 110
# Error 32  = MM_insert_cell had negative index.
# Error 33  = MM[3][1] != 40
# Error 34  = MM[3][0] != 31
# Error 35  = MM[2][1] != 30
# Error 36  = MM[2][0] != 21
# Error 37  = MM[1][1] != 20
# Error 38  = MM[1][0] != 11
# Error 39  = MM[0][1] != 10
# Error 40  = MM[0][0] != 1
# Error 41  = There was a request for zero or less cells.
# Error 42  = malloc_check_beginning accepted invalid range.
# Error 43  = malloc_check_beginngng did not accept valid range.
# Error 44  = MM[1][1] != 20
# Error 45  = MM[1][0] != 11
# Error 46  = MM[0][1] != 10
# Error 47  = MM[0][0] != 1
# Error 48  = malloc_check_ranges found space.
# Error 49  = malloc_check_ranges found space.
# Error 50  = malloc_check_ranges found space.
# Error 51  = malloc_check_ranges did not insert at MM[1].
# Error 52  = malloc_check_ranges did not insert at MM[2].
# Error 53  = MM[2][1] != 30
# Error 54  = MM[2][0] != 26
# Error 55  = MM[1][1] != 25
# Error 56  = MM[1][0] != 21
# Error 57  = malloc_ranges failed head insert.
# Error 58  = malloc_ranges failed body insert.
# Error 59  = mallox_ranges failed tail insert.
# Error 60  = MM[4][1] != 50
# Error 61  = MM[4][0] != 41
# Error 62  = MM[2][1] != 30
# Error 63  = MM[2][0] != 21
# Error 64  = MM[0][1] != 10
# Error 65  = MM[0][0] != 1
# Error 66  = malloc(1) produced bad pointer.
# Error 67  = malloc(2) produced bad pointer.
# Error 68  = malloc(3) produced bad pointer.
# Error 69  = malloc(4) produced bad pointer.
# Error 70  = Memory manager does not have four blocks.
# Error 71  = Block four does not have the correct end.
# Error 72  = calloc produced bad pointer.
# Error 73  = Allocated block has bad end.
# Error 74  = Block found in empty array.
# Error 75  = Binary search did not find first block.
# Error 76  = Binary search did not find middle block.
# Error 77  = Binary search did not find last block.
# Error 78  = Block found before allocations.
# Error 79  = Block found after allocations.
# Error 80  = Tried to free unknown memory block.
# Error 81  = Tried getting cell at negative index.
# Error 82  = Tried popping cell at negative index.
# Error 83  = Tried popping cell beyond memory array.
# Error 84  = memory_manager_pop_cell(0)[1] != 30
# Error 85  = memory_manager_pop_cell(0)[0] != 21
# Error 86  = memory_manager_pop_cell(1)[1] != 40
# Error 87  = memory_manager_pop_cell(1)[0] != 31
# Error 88  = memory_manager_pop_cell(0)[1] != 20
# Error 89  = memory_manager_pop_cell(0)[0] != 11
# Error 90  = memory_manager_pop_cell(-1)[1] != 50
# Error 91  = memory_manager_pop_cell(-1)[0] != 41
# Error 92  = MM[0][0] != 1
# Error 93  = MM[1][0] != 51
# Error 94  = MM[2][0] != 76
# Error 95  = MM[3][0] != 101
# Error 96  = MM[4][0] != 201
# Error 97  = MM[5][0] != 251
# Error 98  = MM[6][0] != 276
# Error 99  = MM[6][1] != 375
# Error 100 = HEAP[-2] != 0
# Error 101 = Tried realloc unknown block.
# Error 102 = Did not get correct block size.
# Error 103 = Cannot deflate block to requested size.
# Error 104 = Tried setting a negative cell.
# Error 105 = Tried setting cell beyond array end.
# Error 106 = MM[0][1] != 20
# Error 107 = MM[0][0] != 11
# Error 108 = Could not deflate block size.
# Error 109 = Cannot inflate block to requested size.
# Error 110 = Could not inflate block size.
# Error 111 = Potential after was not calculated correctly.
# Error 112 = Potential before (0) was not calculated correctly.
# Error 113 = Potential before (1) was not calculated correctly.
# Error 114 = Compression vector (0) was not calculated correctly.
# Error 115 = Compression vector (1) was not calculated correctly.
# Error 116 = Wrong number of blocks allocated (should be 4).
# Error 117 = Wrong number of blocks allocated (should be 3).
# Error 118 = Memory does not compare equal.
# Error 119 = Wrong number of blocks allocated (should be 0).
# Error 120 = compare_memory given negative length.
# Error 121 = Cells did not evaluate to equal.
# Error 122 = !(Cell A > Cell B)
# Error 123 = !(Cell A < Cell B)
# Error 124 = Empty comparison does not return equal.
# Error 125 = Same address does not return equal.
# Error 126 = Same values do not return equal.
# Error 127 = First memory does not return greater than.
# Error 128 = First memory does not return less than.
# Error 129 = range has bad argument directions.
# Error 130 = Negative number should have negative direction.
# Error 131 = Zero number should have zero direction.
# Error 132 = Positive number should have positive direction.
# Error 133 = First range did not fill correctly.
# Error 134 = Second range did not fill correctly.
# Error 135 = Third range did not fill correctly.
# Error 136 = Fourth range did not fill correctly.
# Error 137 = Could not find block by pointer.
# Error 138 = First block size is incorrect.
# Error 139 = Second block size is incorrect.
# Error 140 = Third block size is incorrect.
# Error 141 = Mark did not perform correctly.
# Error 142 = Memory was not copied correctly.
# Error 143 = Block (h) does not have correct size.
# Error 144 = Block (j) does not have correct size.
# Error 145 = Blocks do not have same content.
# Error 146 = Block addresses do not match.
# Error 147 = stack[-1] was not correct.
# Error 148 = stack[-2] was not correct.
# Error 149 = stack[-3] was not correct.
# Error 150 = stack[-1] was not correct.
# Error 151 = stack[-2] was not correct.
# Error 152 = stack[-3] was not correct.
# Error 153 = Block should not have been moved.
# Error 154 = Size was not set correctly.
# Error 155 = Block should not have been moved.
# Error 156 = Size was not set correctly.
# Error 157 = Block should have been moved to front of memory.
# Error 158 = Size was not set correctly.
# Error 159 = Block was not correctly copied.
# Error 160 = Block was not moved to end of memory.
# Error 161 = Memory does not appear the same.
# Error 162 = Memory was not freed.
# Error 163 = Memory was not freed.
# Error 164 = Same memory was not returned.
# Error 165 = Memory size should not have changed.
# Error 166 = Same memory was not returned.
# Error 167 = Memory size is not correct.
# Error 168 = Memory was not moved to correct place.
# Error 169 = Memory size is not correct.
# Error 170 = Correct number of blocks not returned.
# Error 171 = Correct number of blocks not returned.
# Error 172 = Used memory not returned correctly.
# Error 173 = Used memory not returned correctly.
# Error 174 = Used memory not returned correctly.
# Error 175 = Negative argument not accepted.
# Error 176 = Array should have been empty.
# Error 177 = Array should have one value.
# Error 178 = Second item should refer to self.
# Error 179 = array and test should be the same.
# Error 180 = There should be two items in array.
# Error 181 = Second item should refer to array.
# Error 182 = Third item should refer to self.
# Error 183 = Null pointer should have been returned.
# Error 184 = Null pointer should have been returned.
# Error 185 = Pointer to first cell was not returned.
# Error 186 = Pointer to first cell was not returned.
# Error 187 = Pointer to first cell was not returned.
# Error 188 = Null pointer should have been returned.
# Error 189 = Null pointer should have been returned.
# Error 190 = Null pointer should have been returned.
# Error 191 = Pointer to second cell was not returned.
# Error 192 = Pointer to second cell was not returned.
# Error 193 = Pointer to second cell was not returned.
# Error 194 = Null pointer should have been returned.
# Error 195 = Null pointer should have been returned.
# Error 196 = Null pointer should have been returned.
# Error 197 = Pointer to third cell was not returned.
# Error 198 = Pointer to third cell was not returned.
# Error 199 = Pointer to third cell was not returned.
# Error 200 = Null pointer should have been returned.
# Error 201 = Cast should have returned 0.
# Error 202 = Cast should have returned 0.
# Error 203 = Cast should have returned 0.
# Error 204 = Cast should have returned 1.
# Error 205 = Cast should have returned 1.
# Error 206 = Cast should have returned 1.
# Error 207 = Cast should have returned 4294967295.
# Error 208 = Cast should have returned 4294967295.
# Error 209 = Cast should have returned 4294967295.
# Error 210 = Zero left shift was incorrect.
# Error 211 = Zero right shift was incorrect.
# Error 212 = Shift left by two was incorrect.
# Error 213 = Shift right by two was incorrect.
# Error 214 = Negative left shift was incorrect.
# Error 215 = Negative right shift was incorrect.
# Error 216 = value_to_array received a bad base.
# Error 217 = array_to_value received a bad base.
# Error 218 = Digit was too high for base.
# Error 219 = Cannot save stack size less than 1.
# Error 220 = Cannot load stack size less than 1.
# Error 221 = There is nothing in the array.
# Error 222 = Cannot load more than what is in array.
# Error 223 = Array length is not correct.
# Error 224 = Fourth element was not correct.
# Error 225 = Array length is not correct.
# Error 226 = First element was not correct.
# Error 227 = Sentinel value was not correct.
# Error 228 = Sanity check failed for save_stack.
# Error 229 = Full reload of stack failed.
# Error 230 = Full reload of stack failed.
# Error 231 = Single reload of stack failed.
# Error 232 = Double reload of stack failed.
# Error 233 = Array resize operation failed.
# Error 234 = Unexpected sum was detected.
# Error 235 = First div was not correct.
# Error 236 = First mod was not correct.
# Error 235 = Second div was not correct.
# Error 236 = Second mod was not correct.
# Error 235 = Third div was not correct.
# Error 236 = Third mod was not correct.
# Error 237 = First sum was not correct.
# Error 238 = Second sum was not correct.
# Error 239 = Third sum was not correct.
# Error 240 = Fourth sum was not correct.
# Error 241 = Fifth sum was not correct.
# Error 242 = Sixth sum was not correct.
# Error 243 = Length was not written correctly.
# Error 244 = Least significant digit is incorrect.
# Error 245 = Middle digit is incorrect.
# Error 246 = Most significant digit is incorrect.
# Error 247 = Second value was incorrect.
# Error 248 = Third value was incorrect.
# Error 249 = Fourth value was incorrect.
# Error 250 = Fifth value was incorrect.
# Error 251 = Zero was expected but not found.
# Error 252 = One through zero was expected but not found.
# Error 253 = Date in base thirteen was expected but not found.
# Error 254 = One hundred across bases was expected but not found.
# Error 255 = Value from bases two to three was expected but not found.
# Error 256 = First bit is not one.
# Error 257 = Last bit is not one.
# Error 258 = First bit is not zero.
# Error 259 = Last bit is not zero.
# Error 260 = The expected value (7) was not returned.
# Error 261 = The expected value (255) was not returned.
# Error 262 = The expected value (92051) was not returned.
# Error 263 = The expected value (1033010045) was not returned.
# Error 264 = The expected value (2554936947) was not returned.
# Error 265 = The expected value (1747467773) was not returned.
# Error 266 = The expected value (0) was not returned.
# Error 267 = The expected value (2153645760) was not returned.
# Error 268 = The expected value (4048040839) was not returned.
# Error 269 = The expected value (265376592) was not returned.
# Error 270 = The expected value (880511209) was not returned.

################################################################################

     call "self_test"
     exit

# def self_test():
#     test_abs_diff()
#     test_get_addr()
#     test_clear()
#     test_copy()
#     test_memory_manager_append_cell()
#     test_memory_manager_get_cell()
#     test_memory_manager_insert_cell()
#     test_malloc_check_beginning()
#     test_malloc_check_ranges()
#     test_malloc_ranges()
#     test_malloc()
#     test_calloc()
#     test_memory_manager_search()
#     test_memory_manager_pop_cell()
#     test_free()
#     test_memory_manager_get_block_size()
#     test_memory_manager_set_cell()
#     test_memory_manager_deflate_block()
#     test_memory_manager_inflate_cell()
#     test_memory_manager_potential_after()
#     test_memory_manager_potential_before()
#     test_memory_manager_compress()
#     test_compare_cells()
#     test_compare_memory()
#     test_direction()
#     test_range()
#     test_memory_manager_size()
#     test_mark()
#     test_memory_manager_inflate_before()
#     test_rotate_3_down()
#     test_rotate_3_up()
#     test_memory_manager_inflate_move()
#     test_memory_manager_inflate_block()
#     test_realloc()
#     test_memory_manager_blocks()
#     test_memory_manager_cells()
#     test_memory_manager_pointers()
#     test_memory_manager_find()
#     test_uint_cast()
#     test_shift()
#     test_save_stack()
#     test_load_stack()
#     test_divmod()
#     test_sum_length_array()
#     test_value_to_array()
#     test_array_to_value()
#     test_uint_bits()
#     test_uint_xor()
#     test_memory_manager_hash()
#     print('All 49 tests have passed.')
part "self_test"
     call "test_abs_diff"
     call "test_get_addr"
     call "test_clear"
     call "test_copy"
     call "test_memory_manager_append_cell"
     call "test_memory_manager_get_cell"
     call "test_memory_manager_insert_cell"
     call "test_malloc_check_beginning"
     call "test_malloc_check_ranges"
     call "test_malloc_ranges"
     call "test_malloc"
     call "test_calloc"
     call "test_memory_manager_search"
     call "test_memory_manager_pop_cell"
     call "test_free"
     call "test_memory_manager_get_block_size"
     call "test_memory_manager_set_cell"
     call "test_memory_manager_deflate_block"
     call "test_memory_manager_inflate_cell"
     call "test_memory_manager_potential_after"
     call "test_memory_manager_potential_before"
     call "test_memory_manager_compress"
     call "test_compare_cells"
     call "test_compare_memory"
     call "test_direction"
     call "test_range"
     call "test_memory_manager_size"
     call "test_mark"
     call "test_memory_manager_inflate_before"
     call "test_rotate_3_down"
     call "test_rotate_3_up"
     call "test_memory_manager_inflate_move"
     call "test_memory_manager_inflate_block"
     call "test_realloc"
     call "test_memory_manager_blocks"
     call "test_memory_manager_cells"
     call "test_memory_manager_pointers"
     call "test_memory_manager_find"
     call "test_uint_cast"
     call "test_shift"
     call "test_save_stack"
     call "test_load_stack"
     call "test_divmod"
     call "test_sum_length_array"
     call "test_value_to_array"
     call "test_array_to_value"
     call "test_uint_bits"
     call "test_uint_xor"
     call "test_memory_manager_hash"
     push 0
     push 46
     push 100
     push 101
     push 115
     push 115
     push 97
     push 112
     push 32
     push 101
     push 118
     push 97
     push 104
     push 32
     push 115
     push 116
     push 115
     push 101
     push 116
     push 32
     push 57
     push 52
     push 32
     push 108
     push 108
     push 65
     call "print_stack_c_string"
     back

################################################################################

# def print_stack_c_string():
#     while True:
#         value = stack[-1]
#         if not value:
#             stack.pop()
#             return
#         print(chr(stack.pop()), end='')
part "print_stack_c_string"
     copy
     zero "__print_stack_c_string_return"
     ochr
     goto "print_stack_c_string"
part "__print_stack_c_string_return"
     away
     back
# def raise(error):
#     print('Error:', error)
#     sys.exit()
part "raise"
     push 0
     push 32
     push 58
     push 114
     push 111
     push 114
     push 114
     push 69
     push 10
     call "print_stack_c_string"
     oint
     push 10
     ochr
     exit
# def trace(reference):
#     print('Trace:', reference)
part "trace"
     push 0
     push 32
     push 58
     push 101
     push 99
     push 97
     push 114
     push 84
     push 10
     call "print_stack_c_string"
     oint
     push 10
     ochr
     back

################################################################################

# def abs_diff(a, b):
#     c = a - b
#     if c < 0:
#         return 0 - c
#     return c
part "abs_diff"
     sub
     copy
     less "__abs_diff_sign"
     back
part "__abs_diff_sign"
     push 0
     swap
     sub
     back
# def get_addr(offset, start, end):
#     if end < start:
#         return start - offset
#     return offset + start
part "get_addr"
     copy 1
     sub
     less "__get_addr_reverse"
     add
     back
part "__get_addr_reverse"
     swap
     sub
     back
# clear(start_addr, end_addr):
#     if start_addr < end_addr:
#         start_addr, end_addr = end_addr, start_addr
#     while True:
#         heap[end_addr] = 0
#         if start_addr == end_addr:
#             return
#         end_addr += 1
part "clear"
     copy 1
     copy 1
     sub
     less "__clear_swap"
part "__clear_loop"
     copy
     push 0
     set
     copy 1
     copy 1
     sub
     zero "__clear_return"
     push 1
     add
     goto "__clear_loop"
part "__clear_swap"
     swap
     goto "__clear_loop"
part "__clear_return"
     away
     away
     back
# def copy(from_start, from_end, to_start, to_end):
#     if abs_diff(from_start, from_end) != abs_diff(to_start, to_end):
#         raise Exception(1)
#     offset = 0
#     while True:
#         to_addr = get_addr(offset, to_start, to_end)
#         from_addr = get_addr(offset, from_start, from_end)
#         heap[to_addr] = heap[from_addr]
#         if to_addr == to_end:
#             return
#         offset += 1
part "copy"
     copy 3
     copy 3
     call "abs_diff"
     copy 2
     copy 2
     call "abs_diff"
     sub
     zero "__copy_no_arg_error"
     push 1
     call "raise"
part "__copy_no_arg_error"
     push 0
part "__copy_loop"
     copy
     copy 3
     copy 3
     call "get_addr"
     copy
     copy 2
     copy 7
     copy 7
     call "get_addr"
     get
     set
     copy 2
     sub
     zero "__copy_return"
     push 1
     add
     goto "__copy_loop"
part "__copy_return"
     away 4
     away
     back
# def memory_manager_append_cell(start, end):
#     heap[-2] += 1
#     addr = -2 * heap[-2] - 1
#     heap[addr] = start
#     heap[addr - 1] = end
part "memory_manager_append_cell"
     push -2
     copy
     copy
     copy
     get
     push 1
     add
     set
     get
     mul
     push 1
     sub
     copy
     copy 3
     set
     push 1
     sub
     swap
     set
     away
     back
# def memory_manger_get_cell(index):
#     if index < 0:
#         raise Exception(81)
#     if index < HEAP[-2]:
#         address = -2 * index - 3
#         start_addr = HEAP[address]
#         stop_addr = HEAP[address - 1]
#         return start_addr, stop_addr
#     raise Exception(27)
part "memory_manager_get_cell"
     copy
     less "__memory_manager_get_cell_under_zero"
     copy
     push -2
     get
     sub
     less "__memory_manager_get_cell_in_range"
     push 27
     call "raise"
part "__memory_manager_get_cell_under_zero"
     push 81
     call "raise"
part "__memory_manager_get_cell_in_range"
     push -2
     mul
     push 3
     sub
     copy
     get
     swap
     push 1
     sub
     get
     back
# def memory_manager_insert_cell(start, end, index):
#     if index < 0:
#         raise Exception(32)
#     if index - HEAP[-2] < 0:
#         address = -2 * index - 3
#         from_end = (HEAP[-2] + 1) * -2
#         from_start, from_end = from_end, address
#         to_start = address - 2
#         to_end = from_end - 2
#         copy(from_start, from_end, to_start, to_end)
#         HEAP[address - 1] = end
#         HEAP[address] = start
#         HEAP[-2] += 1
#     else:
#         memory_manager_append_cell(start, end)
part "memory_manager_insert_cell"
     copy
     less "__memory_manager_insert_cell_bad_index"
     copy
     push -2
     get
     sub
     less "__memory_manager_insert_cell_continue"
     away
     call "memory_manager_append_cell"
     back
part "__memory_manager_insert_cell_bad_index"
     push 32
     call "raise"
part "__memory_manager_insert_cell_continue"
     push -2
     mul
     push 3
     sub
     copy
     push -2
     push 1
     push -2
     get
     add
     mul
     swap
     copy 1
     push 2
     sub
     copy 1
     push 2
     sub
     call "copy"
     swap
     copy 1
     push 1
     sub
     swap
     set
     swap
     set
     push -2
     copy
     get
     push 1
     add
     set
     back
# def malloc_check_beginning(cells):
#     start = memory_manager_get_cell(0)[0]
#     open_space = start - HEAP[-1]
#     if cells > open_space:
#         return False
#     start = HEAP[-1]
#     end = cells + start - 1
#     memory_manager_insert_cell(start, end, 0)
#     return True
part "malloc_check_beginning"
     copy
     push 0
     call "memory_manager_get_cell"
     away
     push -1
     get
     sub
     sub
     copy
     less "__malloc_check_beginning_insert"
     copy
     zero "__malloc_check_beginning_insert"
     push 0
     away 2
     back
part "__malloc_check_beginning_insert"
     away
     push -1
     get
     swap
     copy 1
     add
     push 1
     sub
     push 0
     call "memory_manager_insert_cell"
     push 1
     back
# def malloc_check_ranges(cells):
#     if HEAP[-2] >= 2:
#         index = 0
#         while index + 1 < HEAP[-2]:
#             end = memory_manager_get_cell(index)[1]
#             start = memory_manager_get_cell(index + 1)[0]
#             empty_space = end - start
#             excess = empty_space + cells
#             if excess < 0:
#                 location = index + 1
#                 end = memory_manager_get_cell(index)[1]
#                 new_end = end + cells
#                 new _start = end + 1
#                 memory_manager_insert_cell(new_start, new_end, location)
#                 return location
#             index += 1
#     return -1
part "malloc_check_ranges"
     push -2
     copy
     get
     add
     less "__malloc_check_ranges_unable"
     push 0
part "__malloc_check_ranges_loop_check"
     copy
     push 1
     add
     push -2
     get
     sub
     less "__malloc_check_ranges_loop_body"
     away
part "__malloc_check_ranges_unable"
     away
     push -1
     back
part "__malloc_check_ranges_loop_body"
     copy
     call "memory_manager_get_cell"
     away 1
     copy 1
     push 1
     add
     call "memory_manager_get_cell"
     away
     sub
     copy 2
     add
     less "__malloc_check_ranges_found"
     push 1
     add
     goto "__malloc_check_ranges_loop_check"
part "__malloc_check_ranges_found"
     copy
     push 1
     add
     swap
     call "memory_manager_get_cell"
     away 1
     copy
     copy 3
     add
     swap
     push 1
     add
     swap
     copy 2
     call "memory_manager_insert_cell"
     away 1
     back
# def malloc_ranges(cells):
#     if malloc_check_beginning(cells):
#         return HEAP[-1]
#     index = malloc_check_ranges(cells)
#     if index == -1:
#         address = -2 * HEAP[-2] - 2
#         end = HEAP[address]
#         new_end = end + cells
#         new start = end + 1
#         memory_manager_append_cell(new_start, new_end)
#         return new_start
#     return memory_manager_get_cell(index)[0]
part "malloc_ranges"
     copy
     call "malloc_check_beginning"
     zero "__malloc_ranges_not_beginning"
     away
     push -1
     get
     back
part "__malloc_ranges_not_beginning"
     copy
     call "malloc_check_ranges"
     copy
     push 1
     add
     zero "__malloc_ranges_append"
     call "memory_manager_get_cell"
     swap
     away 2
     back
part "__malloc_ranges_append"
     away
     push -2
     copy
     copy
     get
     mul
     add
     get
     swap
     copy 1
     add
     swap
     push 1
     add
     swap
     copy 1
     swap
     call "memory_manager_append_cell"
     back
# def malloc(cells):
#     if cells <= 0:
#         raise Exception(41)
#     if not heap[-2]:
#         start = heap[-1]
#         end = start + cells - 1
#         memory_manager_append_cell(start, end)
#         return start
#     return malloc_ranges(cells)
part "malloc"
     copy
     less "__malloc_bad_argument"
     copy
     zero "__malloc_bad_argument"
     push -2
     get
     zero "__malloc_start"
     call "malloc_ranges"
     back
part "__malloc_bad_argument"
     push 41
     call "raise"
part "__malloc_start"
     push -1
     get
     copy
     copy
     copy 3
     add
     push 1
     sub
     call "memory_manager_append_cell"
     away 1
     back
# def calloc(block_count, block_size):
#     return malloc(block_count * block_size)
part "calloc"
     mul
     call "malloc"
     back
# def memory_manager_search(pointer):
#     size = HEAP[-2]
#     if not size:
#         return -1
#     last = size - 1
#     first = 0
#     while first <= last:
#         index = (last + first) // 2
#         value = memory_manager_get_cell(index)[0]
#         if value < pointer:
#             first = index + 1
#         elif value == pointer:
#             return index
#         else:
#             last = index - 1
#     return -1
part "memory_manager_search"
     push -2
     get
     copy
     zero "__memory_manager_search_not_found"
     push 1
     sub
     push 0
part "__memory_manager_search_loop_test"
     copy
     copy 2
     sub
     copy
     less "__memory_manager_search_loop_body_away"
     zero "__memory_manager_search_loop_body"
     goto "__memory_manager_search_not_found_away"
part "__memory_manager_search_loop_body_away"
     away
part "__memory_manager_search_loop_body"
     copy 1
     copy 1
     add
     push 2
     div
     copy
     call "memory_manager_get_cell"
     away
     copy 4
     sub
     copy
     less "__memory_manager_search_high"
     zero "__memory_manager_search_return"
     push 1
     sub
     swap
     push 0
     swap
     set
     away 1
     push 0
     get
     goto "__memory_manager_search_loop_test"
part "__memory_manager_search_return"
     away 3
     back
part "__memory_manager_search_high"
     away
     away 1
     push 1
     add
     goto "__memory_manager_search_loop_test"
part "__memory_manager_search_not_found_away"
     away
part "__memory_manager_search_not_found"
     push -1
     away 2
     back
# def memory_manager_pop_cell(index):
#     if index == -1:
#         index = HEAP[-2] - 1
#     if index < 0:
#         raise Exception(82)
#     if index < HEAP[-2]:
#         a, b = memory_manager_get_cell(index)
#         HEAP[-2] -= 1
#         if index != HEAP[-2]:
#             from_start = -2 * index - 5
#             from_end = (HEAP[-2] + 2) * -2
#             to_start = from_start + 2
#             to_end = from_end + 2
#             copy(from_start, from_end, to_start, to_end)
#         start = -2 * HEAP[-2] - 3
#         end = start - 1
#         clear(start, end)
#         return a, b
#     raise Exception(83)
part "memory_manager_pop_cell"
     copy
     push 1
     add
     zero "__memory_manager_pop_cell_last_cell"
part "__memory_manager_pop_cell_negative_index_check"
     copy
     less "__memory_manager_pop_cell_negative_index_raise"
     copy
     push -2
     get
     sub
     less "__memory_manager_pop_cell_index_okay"
     push 83
     call "raise"
part "__memory_manager_pop_cell_index_okay"
     copy
     call "memory_manager_get_cell"
     push -1
     push -2
     get
     add
     copy
     push -2
     swap
     set
     copy
     copy 4
     sub
     zero "__memory_manager_pop_cell_clear_end"
     push -5
     push -2
     copy 5
     mul
     add
     push -2
     push 2
     copy 3
     add
     mul
     copy 1
     push 2
     add
     copy 1
     push 2
     add
     call "copy"
part "__memory_manager_pop_cell_clear_end"
     push -2
     mul
     push 3
     sub
     copy
     push 1
     sub
     call "clear"
     push 0
     swap
     set
     away 1
     push 0
     get
     back
part "__memory_manager_pop_cell_negative_index_raise"
     push 82
     call "raise"
part "__memory_manager_pop_cell_last_cell"
     push -2
     get
     add
     goto "__memory_manager_pop_cell_negative_index_check"
# def free(pointer):
#     index = memory_manager_search(pointer)
#     if index == -1:
#         raise Exception(80)
#     memory_manager_pop_cell(index)
part "free"
     call "memory_manager_search"
     copy
     push 1
     add
     zero "__free_not_found"
     call "memory_manager_pop_cell"
     away
     away
     back
part "__free_not_found"
     push 80
     call "raise"
     back
# def memory_manager_get_block_size(index):
#     start, end = memory_manager_get_cell(index)
#     return end - start + 1
part "memory_manager_get_block_size"
     call "memory_manager_get_cell"
     swap
     sub
     push 1
     add
     back
# def memory_manager_set_cell(start, end, index):
#     if index < 0:
#         raise Exception(104)
#     if index < HEAP[-2]:
#         address = -2 * index - 4
#         HEAP[address] = end
#         HEAP[address + 1] = start
#         return
#     raise Exception(105)
part "memory_manager_set_cell"
     copy
     less "__memory_manager_set_cell_negative"
     copy
     push -2
     get
     sub
     less "__memory_manager_set_cell_in_range"
     push 105
     call "raise"
part "__memory_manager_set_cell_negative"
     push 104
     call "raise"
part "__memory_manager_set_cell_in_range"
     push -2
     mul
     push 4
     sub
     copy
     copy 2
     set
     push 1
     add
     away 1
     swap
     set
     back
# def memory_manager_deflate_block(cells, index):
#     size = memory_manager_get_block_size(index)
#     if cells < size:
#         start, end = memory_manager_get_cell(index)
#         end = start + cells - 1
#         memory_manager_set_cell(start, end, index)
#         return
#     raise Exception(103)
part "memory_manager_deflate_block"
     copy
     call "memory_manager_get_block_size"
     copy 2
     swap
     sub
     less "__memory_manager_deflate_block_continue"
     push 103
     call "raise"
part "__memory_manager_deflate_block_continue"
     copy
     call "memory_manager_get_cell"
     away
     copy
     copy 3
     push 1
     sub
     add
     copy 2
     call "memory_manager_set_cell"
     away
     away
     back
# def memory_manager_inflate_cell(cells, index):
#     size = memory_manager_get_block_size(index)
#     if size < cells:
#         start, end = memory_manager_get_cell(index)
#         end = start + cells - 1
#         memory_manager_set_cell(start, end, index)
#         return
#     raise Exception(109)
part "memory_manager_inflate_cell"
     copy
     call "memory_manager_get_block_size"
     copy 2
     sub
     less "__memory_manager_inflate_cell_continue"
     push 109
     call "raise"
part "__memory_manager_inflate_cell_continue"
     copy
     call "memory_manager_get_cell"
     away
     copy
     copy 3
     push 1
     sub
     add
     copy 2
     call "memory_manager_set_cell"
     away
     away
     back
# def memory_manager_potential_after(index):
#     size = memory_manager_get_block_size(index)
#     start = memory_manager_get_cell(index + 1)[0]
#     end = memory_manager_get_cell(index)[1]
#     empty = start - end - 1
#     return size + empty
part "memory_manager_potential_after"
     copy
     call "memory_manager_get_block_size"
     copy 1
     push 1
     add
     call "memory_manager_get_cell"
     away
     copy 2
     call "memory_manager_get_cell"
     away 1
     sub
     push 1
     sub
     add
     away 1
     back
# def memory_manager_potential_before(index):
#     if index == 0:
#         head = HEAP[-3]
#         start = HEAP[-1]
#         space = head - start
#     else:
#         start = memory_manager_get_cell(index)[0]
#         end = memory_manager_get_cell(index - 1)[1]
#         space = start - end - 1
#     return space + memory_manager_potential_after(index)
part "memory_manager_potential_before"
     copy
     zero "__memory_manager_potential_before_head"
     copy
     call "memory_manager_get_cell"
     away
     copy 1
     push 1
     sub
     call "memory_manager_get_cell"
     away 1
     sub
     push 1
     sub
     goto "__memory_manager_potential_before_total"
part "__memory_manager_potential_before_head"
     push -3
     get
     push -1
     get
     sub
part "__memory_manager_potential_before_total"
     copy 1
     call "memory_manager_potential_after"
     add
     away 1
     back
# def memory_manager_compress(index):
#     if index == 0:
#         return HEAP[-1]
#     return memory_manager_get_cell(index - 1)[1] + 1
part "memory_manager_compress"
     copy
     zero "__memory_manager_compress_start"
     push 1
     sub
     call "memory_manager_get_cell"
     away 1
     push 1
     add
     back
part "__memory_manager_compress_start"
     away
     push -1
     get
     back
# compare_cells(addr_a, addr_b):
#    b = HEAP[addr_b]
#    a = HEAP[addr_a]
#    if b == a:
#        return 0
#    if b < a:
#        return 1
#    return -1 
part "compare_cells"
     get
     swap
     get
     sub
     copy
     zero "__compare_cells_equal"
     less "__compare_cells_greater"
     push -1
     back
part "__compare_cells_greater"
     push 1
     back
part "__compare_cells_equal"
     push 0
     away 1
     back
# def compare_memory(a, b, length):
#     if length < 0:
#         raise Exception(120)
#     if length == 0:
#         return 0
#     if a == b:
#         return 0
#     offset = 0
#     while offset < length:
#         addr_a = a + offset
#         addr_b = b + offset
#         value = compare_cells(addr_a, addr_b)
#         if value == 0:
#             offset += 1
#         elif value < 0:
#             return -1
#         else:
#             return 1
#     return 0
part "compare_memory"
     copy
     less "__compare_memory_negative_length"
     copy
     zero "__compare_memory_equal_buffers"
     copy 2
     copy 2
     sub
     zero "__compare_memory_equal_buffers"
     push 0
part "__compare_memory_loop_test"
     copy
     copy 2
     sub
     less "__compare_memory_loop_body"
     away
part "__compare_memory_equal_buffers"
     push 0
     away 3
     back
part "__compare_memory_negative_length"
     push 120
     call "raise"
part "__compare_memory_loop_body"
     copy 3
     copy 1
     add
     copy 3
     copy 2
     add
     call "compare_cells"
     copy
     zero "__compare_memory_inc_offset"
     less "__compare_memory_less_than"
     push 1
     away 4
     back
part "__compare_memory_less_than"
     push -1
     away 4
     back
part "__compare_memory_inc_offset"
     away
     push 1
     add
     goto "__compare_memory_loop_test"
# def direction(number):
#     if number:
#         if number > 0:
#             return 1
#         return -1
#     return number
part "direction"
     copy
     zero "__direction_zero"
     less "__direction_negative"
     push 1
     back
part "__direction_negative"
     push -1
part "__direction_zero"
     back
# def range(address, start, stop, step):
#     if direction(stop - start) != direction(step):
#         raise Exception(129)
#     value = start
#     while (value > stop) if direction(step) < 0 else (value < stop):
#         offset = (value - start) // step
#         HEAP[offset + address] = value
#         value += step
part "range"
     copy 1
     copy 3
     sub
     call "direction"
     copy 1
     call "direction"
     sub
     zero "__range_loop_setup"
     push 129
     call "raise"
part "__range_loop_setup"
     copy 2
part "__range_loop_test"
     copy
     copy 3
     copy 3
     call "direction"
     less "__range_switch_compare"
part "__range_do_compare"
     sub
     less "__range_loop_body"
     away 4
     away
     back
part "__range_switch_compare"
     swap
     goto "__range_do_compare"
part "__range_loop_body"
     copy
     copy 4
     sub
     copy 2
     div
     copy 5
     add
     copy 1
     set
     copy 1
     add
     goto "__range_loop_test"
# def memory_manager_size(pointer):
#     index = memory_manager_search(pointer)
#     if index < 0:
#         raise Exception(137)
#     a, b = memory_manager_get_cell(index)
#     return b - a + 1
part "memory_manager_size"
     call "memory_manager_search"
     copy
     less "__memory_manager_size_not_found"
     call "memory_manager_get_cell"
     swap
     sub
     push 1
     add
     back
part "__memory_manager_size_not_found"
     push 137
     call "raise"
     back
# def mark(pointer):
#     size = memory_manager_size(pointer)
#     range(pointer, 1, size + 1, 1)
part "mark"
     push 1
     copy 1
     call "memory_manager_size"
     push 1
     add
     push 1
     call "range"
     back
# def memory_manager_inflate_before(pointer, cells, index):
#     from_start, from_end = memory_manager_get_cell(index)
#     to_start = memory_manager_compress(index)
#     to_end = to_start + from_end - from_start
#     copy(from_start, from_end, to_start, to_end)
#     to_end = to_start + cells - 1
#     memory_manager_set_cell(to_start, to_end, index)
#     return to_start
part "memory_manager_inflate_before"
     copy
     call "memory_manager_get_cell"
     copy 2
     call "memory_manager_compress"
     copy
     copy 2
     copy 4
     sub
     add
     push 0
     copy 2
     set
     call "copy"
     push 0
     get
     copy
     copy
     copy 4
     add
     push 1
     sub
     copy 3
     call "memory_manager_set_cell"
     away 3
     back
# def rotate_3_down():
#     HEAP[0] = stack.pop()
#     stack[-1], stack[-2] = stack[-2], stack[-1]
#     stack.push(HEAP[0])
#     stack[-1], stack[-2] = stack[-2], stack[-1]
part "rotate_3_down"
     push 0
     swap
     set
     swap
     push 0
     get
     swap
     back
# def rotate_3_up():
#     stack[-1], stack[-2] = stack[-2], stack[-1]
#     HEAP[0] = stack.pop()
#     stack[-1], stack[-2] = stack[-2], stack[-1]
#     stack.push(HEAP[0])
part "rotate_3_up"
     swap
     push 0
     swap
     set
     swap
     push 0
     get
     back
# def memory_manager_inflate_move(pointer, cells, index):
#     from_start, from_end = memory_manager_get_cell(index)
#     new = malloc(cells)
#     to_start = new
#     to_end = new + from_end - from_start
#     copy(from_start, from_end, to_start, to_end)
#     free(pointer)
#     return new
part "memory_manager_inflate_move"
     call "memory_manager_get_cell"
     call "rotate_3_down"
     call "malloc"
     call "rotate_3_up"
     copy 2
     copy
     copy 2
     add
     copy 3
     sub
     call "copy"
     swap
     call "free"
     back
# def memory_manager_inflate_block(pointer, cells, index):
#     if index == HEAP[-2] - 1:
#         memory_manager_inflate_cell(cells, index)
#         return pointer
#     potential = memory_manager_potential_after(index)
#     if potential < cells:
#         potential = memory_manager_potential_before(index)
#         if potential < cells:
#             return memory_manager_inflate_move(pointer, cells, index)
#         return memory_manager_inflate_before(pointer, cells, index)
#     memory_manager_inflate_cell(cells, index)
#     return pointer
part "memory_manager_inflate_block"
     copy
     push -2
     get
     push 1
     sub
     sub
     zero "__memory_manager_inflate_block_cell"
     copy
     call "memory_manager_potential_after"
     copy 2
     sub
     less "__memory_manager_inflate_block_not_after"
part "__memory_manager_inflate_block_cell"
     call "memory_manager_inflate_cell"
     back
part "__memory_manager_inflate_block_not_after"
     copy
     call "memory_manager_potential_before"
     copy 2
     sub
     less "__memory_manager_inflate_block_not_before"
     call "memory_manager_inflate_before"
     back
part "__memory_manager_inflate_block_not_before"
     call "memory_manager_inflate_move"
     back
# def realloc(pointer, cells):
#     if cells <= 0:
#         free(pointer)
#         return 0
#     index = memory_manager_search(pointer)
#     if index == -1:
#         raise Exception(101)
#     size = memory_manager_get_block_size(index)
#     if cells == size:
#         return pointer
#     if cells < size:
#         memory_manager_deflate_block(cells, index)
#         return pointer
#     return memory_manager_inflate_block(pointer, cells, index)
part "realloc"
     copy
     less "__realloc_free"
     copy
     zero "__realloc_free"
     copy 1
     call "memory_manager_search"
     copy
     push 1
     add
     zero "__realloc_not_found"
     copy
     call "memory_manager_get_block_size"
     copy 2
     swap
     sub
     copy
     zero "__realloc_return_pointer"
     less "__realloc_return_deflate"
     call "memory_manager_inflate_block"
     back
part "__realloc_free"
     away
     call "free"
     push 0
     back
part "__realloc_not_found"
     push 101
     call "raise"
part "__realloc_return_pointer"
     away 2
     away
     back
part "__realloc_return_deflate"
     call "memory_manager_deflate_block"
     back
# def memory_manager_blocks():
#     return HEAP[-2]
part "memory_manager_blocks"
     push -2
     get
     back
# def memory_manager_cells():
#     blocks = HEAP[-2]
#     index = 0
#     total = 0
#     while index < blocks:
#         addr = (index + 2) * -2
#         end = HEAP[addr]
#         start = HEAP[addr + 1]
#         size = end - start + 1
#         total += size
#         index += 1
#     return total
part "memory_manager_cells"
     push -2
     get
     push 0
     push 0
part "__memory_manager_cells_loop_test"
     copy 1
     copy 3
     sub
     less "__memory_manager_cells_loop_body"
     away 2
     back
part "__memory_manager_cells_loop_body"
     copy 1
     push 2
     add
     push -2
     mul
     copy
     get
     swap
     push 1
     add
     get
     sub
     push 1
     add
     add
     swap
     push 1
     add
     swap
     goto "__memory_manager_cells_loop_test"
# def memory_manager_pointers(include_self):
#     bool = direction(include_self)
#     if bool < 0:
#         raise Exception(175)
#     pointer_count = HEAP[-2] + bool
#     array_length = pointer_count + 1
#     array = malloc(array_length)
#     HEAP[array] = pointer_count
#     mm_size = HEAP[-2]
#     array_address = array + 1
#     index = 0
#     while index < mm_size:
#         mm_addr = -2 * index - 3
#         pointer = HEAP[mm_addr]
#         if pointer != array or bool:
#             HEAP[array_address] = pointer
#             array_address += 1
#         index += 1
#     return array
part "memory_manager_pointers"
     call "direction"
     copy
     less "__memory_manager_pointers_bad_bool"
     copy
     push -2
     get
     add
     copy
     push 1
     add
     call "malloc"
     swap
     copy 1
     swap
     set
     push -2
     get
     copy 1
     push 1
     add
     push 0
part "__memory_manager_pointers_loop_test"
     copy
     copy 3
     sub
     less "__memory_manager_pointers_loop_body"
     away
     away
     away
     away 1
     back
part "__memory_manager_pointers_bad_bool"
     push 175
     call "raise"
part "__memory_manager_pointers_loop_body"
     copy
     push -2
     mul
     push 3
     sub
     get
     copy
     copy 5
     sub
     zero "__memory_manager_pointers_check_bool"
part "__memory_manager_pointers_add_pointer"
     copy 2
     swap
     set
     swap
     push 1
     add
     swap
part "__memory_manager_pointers_inc_index"
     push 1
     add
     goto "__memory_manager_pointers_loop_test"
part "__memory_manager_pointers_check_bool"
     copy 5
     zero "__memory_manager_pointers_away_inc_index"
     goto "__memory_manager_pointers_add_pointer"
part "__memory_manager_pointers_away_inc_index"
     away
     goto "__memory_manager_pointers_inc_index"
# def memory_manager_find(address):
#     size = HEAP[-2]
#     if not size:
#         return 0
#     last = size - 1
#     first = 0
#     while first <= last:
#         index = (last + first) // 2
#         addr = -2 * index - 4
#         b = HEAP[addr]
#         a = HEAP[addr + 1]
#         if a <= address <= b:
#             return a
#         if a < address:
#             first = index + 1
#         else:
#             last = index - 1
#     return 0
part "memory_manager_find"
     push -2
     get
     copy
     zero "__memory_manager_find_null"
     push 1
     sub
     push 0
part "__memory_manager_find_loop_test"
     copy
     copy 2
     sub
     copy
     less "__memory_manager_find_loop_body_away"
     zero "__memory_manager_find_loop_body"
     away
part "__memory_manager_find_null"
     push 0
     away 2
     back
part "__memory_manager_find_loop_body_away"
     away
part "__memory_manager_find_loop_body"
     copy 1
     copy 1
     add
     push 2
     div
     copy
     push -2
     mul
     push 4
     sub
     copy
     get
     swap
     push 1
     add
     get
     copy
     copy 6
     sub
     copy
     less "__memory_manager_find_check_b_away"
     zero "__memory_manager_find_check_b"
     away 1
part "__memory_manager_find_divide"
     copy 4
     sub
     less "__memory_manager_find_upper"
     push 1
     sub
     push 0
     swap
     set
     away 1
     push 0
     get
     swap
     goto "__memory_manager_find_loop_test"
part "__memory_manager_find_upper"
     away 1
     push 1
     add
     goto "__memory_manager_find_loop_test"
part "__memory_manager_find_check_b_away"
     away
part "__memory_manager_find_check_b"
     swap
     copy 5
     swap
     sub
     copy
     less "__memory_manager_find_return_away"
     zero "__memory_manager_find_return"
     goto "__memory_manager_find_divide"
part "__memory_manager_find_return_away"
     away
part "__memory_manager_find_return"
     away 4
     back
# def uint_cast(number):
#     return number % 4294967296
part "uint_cast"
     push 4294967296
     mod
     back
# def left_shift(number, shift):
#     if not shift:
#         return number
#     if shift < 0:
#         return right_shift(number, -shift)
#     while shift:
#         number *= 2
#         shift -= 1
#     return number
part "left_shift"
     copy
     zero "__left_shift_return"
     copy
     less "__left_shift_reverse"
part "__left_shift_loop"
     copy
     zero "__left_shift_return"
     swap
     push 2
     mul
     swap
     push 1
     sub
     goto "__left_shift_loop"
part "__left_shift_return"
     away
     back
part "__left_shift_reverse"
     push 0
     swap
     sub
     call "right_shift"
     back
# def right_shift(number, shift):
#     if not shift:
#         return number
#     if shift < 0:
#         return left_shift(number, -shift)
#     while shift:
#         number //= 2
#         shift -= 1
#     return number
part "right_shift"
     copy
     zero "__right_shift_return"
     copy
     less "__right_shift_reverse"
part "__right_shift_loop"
     copy
     zero "__right_shift_return"
     swap
     push 2
     div
     swap
     push 1
     sub
     goto "__right_shift_loop"
part "__right_shift_return"
     away
     back
part "__right_shift_reverse"
     push 0
     swap
     sub
     call "left_shift"
     back
# def save_stack(size):
#     if size < 1:
#         raise Exception(219)
#     array = malloc(size + 1)
#     array[0] = size
#     temp = malloc(3)
#     temp[0] = array          // array
#     temp[1] = size           // size
#     temp[2] = 1              // offset
#     while temp[2] <= temp[1]:
#         temp[0][temp[2]] = stack.pop()
#         temp[2] += 1
#     array = temp[0]
#     free(temp)
#     return array
part "save_stack"
     copy
     push 1
     sub
     less "__save_stack_bad_size"
     copy
     push 1
     add
     call "malloc"
     copy
     copy 2
     set
     push 3
     call "malloc"
     swap
     copy 1
     swap
     set
     swap
     copy 1
     push 1
     add
     swap
     set
     copy
     push 2
     add
     push 1
     set
part "__save_stack_loop_test"
     copy
     push 2
     add
     get
     copy 1
     push 1
     add
     get
     sub
     copy
     less "__save_stack_loop_body_away"
     zero "__save_stack_loop_body"
     copy
     get
     swap
     call "free"
     back
part "__save_stack_bad_size"
     push 219
     call "raise"
part "__save_stack_loop_body_away"
     away
part "__save_stack_loop_body"
     copy
     get
     copy 1
     push 2
     add
     get
     add
     call "rotate_3_down"
     set
     copy
     push 2
     add
     copy
     get
     push 1
     add
     set
     goto "__save_stack_loop_test"
# def load_stack(array, size):
#     if size < 1:
#         raise Exception(220)
#     array_size = array[0]
#     if array_size < 1:
#         raise Exception(221)
#     if array_size < size:
#         raise Exception(222)
#     addr = array + array_size
#     temp = malloc(3)
#     temp[0] = addr
#     temp[1] = size
#     temp[2] = array
#     while temp[1] != 0:
#         addr = temp[0]
#         value = HEAP[addr]
#         stack.push(value)
#         temp[0] -= 1
#         temp[1] -= 1
#     array = temp[2]
#     diff = array - temp[0]
#     if diff < 0:
#         array[0] = -diff
#     else:
#         free(array)
#     free(temp)
part "load_stack"
     copy
     push 1
     sub
     less "__load_stack_bad_size"
     copy 1
     get
     copy
     push 1
     sub
     less "__load_stack_bad_array"
     copy
     copy 2
     sub
     less "__load_stack_size_greater_than_array"
     copy 2
     add
     push 3
     call "malloc"
     swap
     copy 1
     swap
     set
     swap
     copy 1
     push 1
     add
     swap
     set
     swap
     copy 1
     push 2
     add
     swap
     set
part "__load_stack_loop_test"
     copy
     push 1
     add
     get
     zero "__load_stack_end_loop"
     copy
     get
     get
     swap
     copy
     copy
     get
     push 1
     sub
     set
     copy
     push 1
     add
     copy
     get
     push 1
     sub
     set
     goto "__load_stack_loop_test"
part "__load_stack_bad_size"
     push 220
     call "raise"
part "__load_stack_bad_array"
     push 221
     call "raise"
part "__load_stack_size_greater_than_array"
     push 222
     call "raise"
part "__load_stack_end_loop"
     copy
     push 2
     add
     get
     copy
     copy 2
     get
     sub
     copy
     less "__load_stack_set_length"
     away
     call "free"
     call "free"
     back
part "__load_stack_set_length"
     push -1
     mul
     set
     call "free"
     back
# def divmod(a, b):
#     x = a // b
#     y = a % b
#     return x, y
part "divmod"
     copy 1
     copy 1
     div
     call "rotate_3_up"
     mod
     back
# def sum_length_array(array):
#     index = 1
#     total = 0
#     while index <= array[0]:
#         total += array[index]
#         index += 1
#     return total
part "sum_length_array"
     push 1
     push 0
part "__sum_length_array_loop_test"
     copy 1
     copy 3
     get
     sub
     copy
     less "__sum_length_array_loop_body_away"
     zero "__sum_length_array_loop_body"
     away 2
     back
part "__sum_length_array_loop_body_away"
     away
part "__sum_length_array_loop_body"
     copy 2
     copy 2
     add
     get
     add
     swap
     push 1
     add
     swap
     goto "__sum_length_array_loop_test"
# def value_to_array(value, base):
#     if base < 2:
#         raise Exception(216)
#     size = 8 + 1
#     array = malloc(size)
#     offset = 1
#     while value:
#         if offset == size:
#             size = size * 2 - 1
#             array = realloc(array, size)
#         value, digit = divmod(value, base)
#         array[offset] = digit
#         offset += 1
#     if size != offset:
#         array = realloc(array, offset)
#     array[0] = offset - 1
#     return array
part "value_to_array"
     copy
     push 2
     sub
     less "__value_to_array_bad_base"
     swap
     push 8
     push 1
     add
     swap
     copy 1
     call "malloc"
     swap
     push 1
     swap
part "__value_to_array_loop_test"
     copy
     zero "__value_to_array_loop_end"
     copy 1
     copy 4
     sub
     zero "__value_to_array_adjust_array_size"
part "__value_to_array_get_digit"
     copy 4
     call "divmod"
     copy 3
     copy 3
     add
     swap
     set
     swap
     push 1
     add
     swap
     goto "__value_to_array_loop_test"
part "__value_to_array_bad_base"
     push 216
     call "raise"
part "__value_to_array_loop_end"
     copy 3
     copy 2
     sub
     zero "__value_to_array_skip_resize"
     call "rotate_3_down"
     copy 2
     call "realloc"
     call "rotate_3_up"
part "__value_to_array_skip_resize"
     away
     copy 1
     copy 1
     push 1
     sub
     set
     away
     away 2
     back
part "__value_to_array_adjust_array_size"
     push 3
     call "save_stack"
     swap
     push 2
     mul
     push 1
     sub
     swap
     copy
     push 1
     call "load_stack"
     copy 2
     call "realloc"
     swap
     push 2
     call "load_stack"
     goto "__value_to_array_get_digit"
# def array_to_value(array, base):
#     if base < 2:
#         raise Exception(217)
#     if array[0] == 0:
#         return 0
#     addr = array + array[0]
#     value = 0
#     while addr != array:
#         value *= base
#         tentative = HEAP[addr]
#         if tentative < base:
#             value += tentative
#             addr -= 1
#         else:
#             raise Exception(218)
#     return value
part "array_to_value"
     copy
     push 2
     sub
     less "__array_to_value_bad_base"
     copy 1
     get
     zero "__array_to_value_return_zero"
     copy 1
     copy
     get
     add
     push 0
part "__array_to_value_loop_test"
     copy 3
     copy 2
     sub
     zero "__array_to_value_return"
     copy 2
     mul
     copy 1
     get
     copy
     copy 4
     sub
     less "__array_to_value_loop_continue"
     push 218
     call "raise"
part "__array_to_value_loop_continue"
     add
     swap
     push 1
     sub
     swap
     goto "__array_to_value_loop_test"
part "__array_to_value_bad_base"
     push 217
     call "raise"
part "__array_to_value_return_zero"
     push 0
     away 2
     back
part "__array_to_value_return"
     away 3
     back
# def uint_bits(number):
#     integer = uint_cast(number)
#     array = value_to_array(integer, 2)
#     size = array[0]
#     bits = malloc(32)
#     clear(bits, bits + 31)
#     if size != 0:
#         from_start = array + 1
#         from_end = array + size
#         to_start = bits
#         to_end = bits + size - 1
#         copy(from_start, from_end, to_start, to_end)
#     free(array)
#     return bits
part "uint_bits"
     call "uint_cast"
     push 2
     call "value_to_array"
     copy
     get
     push 32
     call "malloc"
     copy
     copy
     push 31
     add
     call "clear"
     copy 1
     zero "__uint_bits_skip_copy"
     copy 2
     push 1
     add
     copy 3
     copy 3
     add
     copy 2
     copy
     copy 5
     add
     push 1
     sub
     call "copy"
part "__uint_bits_skip_copy"
     away 1
     swap
     call "free"
     back
# def uint_xor(a, b):
#     b = uint_bits(b)
#     a = uint_bits(a)
#     xor = malloc(33)
#     xor[0] = 32
#     offset = 0
#     while offset < 32:
#         b_bit = b[offset]
#         a_bit = a[offset]
#         offset += 1
#         if b_bit != a_bit:
#             xor[offset] = True
#         else:
#             xor[offset] = False
#     free(a)
#     free(b)
#     value = array_to_value(xor, 2)
#     free(xor)
#     return value
part "uint_xor"
     call "uint_bits"
     swap
     call "uint_bits"
     push 33
     call "malloc"
     copy
     push 32
     set
     push 0
part "__uint_xor_loop_test"
     copy
     push 32
     sub
     less "__uint_xor_loop_body"
     away
     call "rotate_3_up"
     call "free"
     call "free"
     copy
     push 2
     call "array_to_value"
     swap
     call "free"
     back
part "__uint_xor_loop_body"
     copy 3
     copy 1
     add
     get
     copy 3
     copy 2
     add
     get
     sub
     swap
     push 1
     add
     swap
     zero "__uint_xor_bit_is_false"
     copy 1
     copy 1
     add
     push 1
     set
     goto "__uint_xor_loop_test"
part "__uint_xor_bit_is_false"
     copy 1
     copy 1
     add
     push 0
     set
     goto "__uint_xor_loop_test"
# def memory_manager_hash():
#     length = HEAP[-2]
#     if length == 0:
#         return 0
#     length *= 2
#     hash = uint_cast(left_shift(HEAP[-3], 7))
#     offset = 0
#     while offset < length:
#         hash = uint_cast(hash * 1000003)
#         hash = uint_xor(hash, HEAP[-3 - offset])
#         offset += 1
#     return uint_xor(hash, HEAP[-2])
part "memory_manager_hash"
     push -2
     get
     copy
     zero "__memory_manager_hash_return"
     push 2
     mul
     push -3
     get
     push 7
     call "left_shift"
     call "uint_cast"
     push 0
part "__memory_manager_hash_loop_test"
     copy
     copy 3
     sub
     less "__memory_manager_hash_loop_body"
     away
     away 1
     push -2
     get
     call "uint_xor"
part "__memory_manager_hash_return"
     back
part "__memory_manager_hash_loop_body"
     swap
     push 1000003
     mul
     call "uint_cast"
     push -3
     copy 2
     sub
     get
     call "uint_xor"
     swap
     push 1
     add
     goto "__memory_manager_hash_loop_test"

################################################################################

# def test_abs_diff():
#     if abs_diff(2, 1) != 1:
#         raise Exception(2)
#     if abs_diff(1, 2) != 1:
#         raise Exception(3)
part "test_abs_diff"
     push 1
     push 2
     push 1
     call "abs_diff"
     sub
     zero "__test_abs_diff_okay"
     push 2
     call "raise"
part "__test_abs_diff_okay"
     push 1
     push 1
     push 2
     call "abs_diff"
     sub
     zero "__test_abs_diff_return"
     push 3
     call "raise"
part "__test_abs_diff_return"
     back
# get test_get_addr():
#     if get_addr(1, 1, 4) != 2:
#         raise Exception(4)
#     if get_addr(2, 1, 4) != 3:
#         raise Exception(4)
#     if get_addr(1, 4, 1) != 3:
#         raise Exception(4)
#     if get_addr(2, 4, 1) != 2:
#         raise Exception(4)
part "test_get_addr"
     push 2
     push 1
     push 1
     push 4
     call "get_addr"
     sub
     zero "__test_get_addr_2"
     push 4
     call "raise"
part "__test_get_addr_2"
     push 3
     push 2
     push 1
     push 4
     call "get_addr"
     sub
     zero "__test_get_addr_3"
     push 5
     call "raise"
part "__test_get_addr_3"
     push 3
     push 1
     push 4
     push 1
     call "get_addr"
     sub
     zero "__test_get_addr_4"
     push 6
     call "raise"
part "__test_get_addr_4"
     push 2
     push 2
     push 4
     push 1
     call "get_addr"
     sub
     zero "__test_get_addr_return"
     push 7
     call "raise"
part "__test_get_addr_return"
     back
# def test_clear():
#     heap[1] = 1
#     heap[2] = 2
#     clear(1, 2)
#     if heap[1]:
#         raise Exception(8)
#     if heap[2]:
#         raise Exception(9)
#     heap[1] = 1
#     heap[2] = 2
#     clear(2, 1)
#     if heap[1]:
#         raise Exception(10)
#     if heap[2]:
#         raise Exception(11)
part "test_clear"
     push 1
     push 1
     set
     push 2
     push 2
     set
     push 1
     push 2
     call "clear"
     push 1
     get
     zero "__test_clear_2"
     push 8
     call "raise"
part "__test_clear_2"
     push 2
     get
     zero "__test_clear_3"
     push 9
     call "raise"
part "__test_clear_3"
     push 1
     push 1
     set
     push 2
     push 2
     set
     push 2
     push 1
     call "clear"
     push 1
     get
     zero "__test_clear_4"
     push 10
     call "raise"
part "__test_clear_4"
     push 2
     get
     zero "__test_clear_return"
     push 11
     call "raise"
part "__test_clear_return"
     back
# def test_copy():
#     heap[1] = 1
#     heap[2] = 2
#     copy(1, 2, 3, 4)
#     if heap[3] != 1:
#         raise Exception(12)
#     if heap[4] != 2:
#         raise Exception(13)
#     copy(1, 2, 4, 3)
#     if heap[3] != 2:
#         raise Exception(14)
#     if heap[4] != 1:
#         raise Exception(15)
#     copy(2, 1, 4, 3)
#     if heap[3] != 1:
#         raise Exception(16)
#     if heap[4] != 2:
#         raise Exception(17)
#     copy(2, 1, 3, 4)
#     if heap[3] != 2:
#         raise Exception(18)
#     if heap[4] != 1:
#         raise Exception(19)
#     clear(1, 4)
part "test_copy"
     push 1
     push 1
     set
     push 2
     push 2
     set
     push 1
     push 2
     push 3
     push 4
     call "copy"
     push 1
     push 3
     get
     sub
     zero "__test_copy_2"
     push 12
     call "raise"
part "__test_copy_2"
     push 2
     push 4
     get
     sub
     zero "__test_copy_3"
     push 13
     call "raise"
part "__test_copy_3"
     push 1
     push 2
     push 4
     push 3
     call "copy"
     push 2
     push 3
     get
     sub
     zero "__test_copy_4"
     push 14
     call "raise"
part "__test_copy_4"
     push 1
     push 4
     get
     sub
     zero "__test_copy_5"
     push 15
     call "raise"
part "__test_copy_5"
     push 2
     push 1
     push 4
     push 3
     call "copy"
     push 1
     push 3
     get
     sub
     zero "__test_copy_6"
     push 16
     call "raise"
part "__test_copy_6"
     push 2
     push 4
     get
     sub
     zero "__test_copy_7"
     push 17
     call "raise"
part "__test_copy_7"
     push 2
     push 1
     push 3
     push 4
     call "copy"
     push 2
     push 3
     get
     sub
     zero "__test_copy_8"
     push 18
     call "raise"
part "__test_copy_8"
     push 1
     push 4
     get
     sub
     zero "__test_copy_return"
     push 19
     call "raise"
part "__test_copy_return"
     push 1
     push 4
     call "clear"
     back
# def test_memory_manager_append_cell():
#     if heap[-2]:
#         raise Exception(20)
#     memory_manager_append_cell(100, 200)
#     if heap[-2] != 1:
#         raise Exception(21)
#     if heap[-3] != 100:
#         raise Exception(22)
#     if heap[-4] != 200:
#         raise Exception(23)
#     memory_manager_append_cell(300, 400)
#     if heap[-2] != 2:
#         raise Exception(24)
#     if heap[-5] != 300:
#         raise Exception(25)
#     if heap[-6] != 400:
#         raise Exception(26)
#     clear(-2, -6)
part "test_memory_manager_append_cell"
     push -2
     get
     zero "__test_memory_manager_append_cell_2"
     push 20
     call "raise"
part "__test_memory_manager_append_cell_2"
     push 100
     push 200
     call "memory_manager_append_cell"
     push 1
     push -2
     get
     sub
     zero "__test_memory_manager_append_cell_3"
     push 21
     call "raise"
part "__test_memory_manager_append_cell_3"
     push 100
     push -3
     get
     sub
     zero "__test_memory_manager_append_cell_4"
     push 22
     call "raise"
part "__test_memory_manager_append_cell_4"
     push 200
     push -4
     get
     sub
     zero "__test_memory_manager_append_cell_5"
     push 23
     call "raise"
part "__test_memory_manager_append_cell_5"
     push 300
     push 400
     call "memory_manager_append_cell"
     push 2
     push -2
     get
     sub
     zero "__test_memory_manager_append_cell_6"
     push 24
     call "raise"
part "__test_memory_manager_append_cell_6"
     push 300
     push -5
     get
     sub
     zero "__test_memory_manager_append_cell_7"
     push 25
     call "raise"
part "__test_memory_manager_append_cell_7"
     push 400
     push -6
     get
     sub
     zero "__test_memory_manager_append_cell_return"
     push 26
     call "raise"
part "__test_memory_manager_append_cell_return"
     push -2
     push -6
     call "clear"
     back
# def test_memory_manager_get_cell():
#     memory_manager_append_cell(80, 90)
#     memory_manager_append_cell(100, 110)
#     d, c = memory_manager_get_cell(1)
#     b, a = memory_manager_get_cell(0)
#     if a != 80:
#         raise Exception(28)
#     if b != 90:
#         raise Exception(29)
#     if c != 100:
#         raise Exception(30)
#     if d != 110:
#         raise Exception(31)
#     clear(-2, -6)
part "test_memory_manager_get_cell"
     push 100
     push 110
     push 80
     push 90
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     push 1
     call "memory_manager_get_cell"
     swap
     push 0
     call "memory_manager_get_cell"
     swap
     push 80
     sub
     zero "__test_memory_manager_get_cell_2"
     push 28
     call "raise"
part "__test_memory_manager_get_cell_2"
     push 90
     sub
     zero "__test_memory_manager_get_cell_3"
     push 29
     call "raise"
part "__test_memory_manager_get_cell_3"
     push 100
     sub
     zero "__test_memory_manager_get_cell_4"
     push 30
     call "raise"
part "__test_memory_manager_get_cell_4"
     push 110
     sub
     zero "__test_memory_manager_get_cell_return"
     push 31
     call "raise"
part "__test_memory_manager_get_cell_return"
     push -2
     push -6
     call "clear"
     back
# def test_memory_manager_insert_cell():
#     memory_manager_insert_cell(11, 20, 0)
#     memory_manager_insert_cell(31, 40, 1)
#     memory_manager_insert_cell(21, 30, 1)
#     memory_manager_insert_cell(1, 10, 0)
#     h, g = memory_manger_get_cell(0)
#     f, e = memory_manger_get_cell(1)
#     c, d = memory_manger_get_cell(2)
#     b, a = memory_manger_get_cell(3)
#     if a != 40:
#         raise Exception(33)
#     if a != 31:
#         raise Exception(34)
#     if a != 30:
#         raise Exception(35)
#     if a != 21:
#         raise Exception(36)
#     if a != 20:
#         raise Exception(37)
#     if a != 11:
#         raise Exception(38)
#     if a != 10:
#         raise Exception(39)
#     if a != 1:
#         raise Exception(40)
#     clear(-2, -10)
part "test_memory_manager_insert_cell"
     push 11
     push 20
     push 0
     call "memory_manager_insert_cell"
     push 31
     push 40
     push 1
     call "memory_manager_insert_cell"
     push 21
     push 30
     push 1
     call "memory_manager_insert_cell"
     push 1
     push 10
     push 0
     call "memory_manager_insert_cell"
     push 0
     call "memory_manager_get_cell"
     push 1
     call "memory_manager_get_cell"
     push 2
     call "memory_manager_get_cell"
     push 3
     call "memory_manager_get_cell"
     push 40
     sub
     zero "__test_memory_manager_insert_cell_2"
     push 33
     call "raise"
part "__test_memory_manager_insert_cell_2"
     push 31
     sub
     zero "__test_memory_manager_insert_cell_3"
     push 34
     call "raise"
part "__test_memory_manager_insert_cell_3"
     push 30
     sub
     zero "__test_memory_manager_insert_cell_4"
     push 35
     call "raise"
part "__test_memory_manager_insert_cell_4"
     push 21
     sub
     zero "__test_memory_manager_insert_cell_5"
     push 36
     call "raise"
part "__test_memory_manager_insert_cell_5"
     push 20
     sub
     zero "__test_memory_manager_insert_cell_6"
     push 37
     call "raise"
part "__test_memory_manager_insert_cell_6"
     push 11
     sub
     zero "__test_memory_manager_insert_cell_7"
     push 38
     call "raise"
part "__test_memory_manager_insert_cell_7"
     push 10
     sub
     zero "__test_memory_manager_insert_cell_8"
     push 39
     call "raise"
part "__test_memory_manager_insert_cell_8"
     push 1
     sub
     zero "__test_memory_manager_insert_cell_return"
     push 40
     call "raise"
part "__test_memory_manager_insert_cell_return"
     push -2
     push -10
     call "clear"
     back
# def test_malloc_check_beginning():
#     HEAP[-1] = 1
#     memory_manager_append_cell(11, 20)
#     if malloc_check_beginning(11):
#         raise Exception(42)
#     if malloc_check_beginning(10) != 1:
#         raise Exception(43)
#     d, c = memory_manager_get_cell(0)
#     b, a = memory_manager_get_cell(1)
#     if a != 20:
#         raise Exception(44)
#     if a != 11:
#         raise Exception(45)
#     if a != 10:
#         raise Exception(46)
#     if a != 1:
#         raise Exception(47)
#     clear(-1, -6)
part "test_malloc_check_beginning"
     push -1
     push 1
     set
     push 11
     push 20
     call "memory_manager_append_cell"
     push 11
     call "malloc_check_beginning"
     zero "__test_malloc_check_beginning_2"
     push 42
     call "raise"
part "__test_malloc_check_beginning_2"
     push 10
     call "malloc_check_beginning"
     push 1
     sub
     zero "__test_malloc_check_beginning_3"
     push 43
     call "raise"
part "__test_malloc_check_beginning_3"
     push 0
     call "memory_manager_get_cell"
     push 1
     call "memory_manager_get_cell"
     push 20
     sub
     zero "__test_malloc_check_beginning_4"
     push 44
     call "raise"
part "__test_malloc_check_beginning_4"
     push 11
     sub
     zero "__test_malloc_check_beginning_5"
     push 45
     call "raise"
part "__test_malloc_check_beginning_5"
     push 10
     sub
     zero "__test_malloc_check_beginning_6"
     push 46
     call "raise"
part "__test_malloc_check_beginning_6"
     push 1
     sub
     zero "__test_malloc_check_beginning_return"
     push 47
     call "raise"
part "__test_malloc_check_beginning_return"
     push -1
     push -6
     call "clear"
     back
# def test_malloc_check_ranges():
#     if malloc_check_ranges(10) != -1:
#         raise Exception(48)
#     memory_manager_append_cell(11, 20)
#     if malloc_check_ranges(10) != -1:
#         raise Exception(49)
#     memory_manager_append_cell(31, 40)
#     if malloc_check_ranges(20) != -1:
#         raise Exception(50)
#     if malloc_check_ranges(5) != 1:
#         raise Exception(51)
#     if malloc_check_ranges(5) != 2:
#         raise Exception(52)
#     d, c = memory_manager_get_cell(1)
#     b, a = memory_manager_get_cell(2)
#     if a != 30:
#         raise Exception(53)
#     if b != 26:
#         raise Exception(54)
#     if c != 25:
#         raise Exception(55)
#     if d != 21:
#         raise Exception(56)
#     clear(-2, -10)
part "test_malloc_check_ranges"
     push 10
     call "malloc_check_ranges"
     push 1
     add
     zero "__test_malloc_check_ranges_2"
     push 48
     call "raise"
part "__test_malloc_check_ranges_2"
     push 11
     push 20
     call "memory_manager_append_cell"
     push 10
     call "malloc_check_ranges"
     push 1
     add
     zero "__test_malloc_check_ranges_3"
     push 49
     call "raise"
part "__test_malloc_check_ranges_3"
     push 31
     push 40
     call "memory_manager_append_cell"
     push 20
     call "malloc_check_ranges"
     push 1
     add
     zero "__test_malloc_check_ranges_4"
     push 50
     call "raise"
part "__test_malloc_check_ranges_4"
     push 5
     call "malloc_check_ranges"
     push 1
     sub
     zero "__test_malloc_check_ranges_5"
     push 51
     call "raise"
part "__test_malloc_check_ranges_5"
     push 5
     call "malloc_check_ranges"
     push 2
     sub
     zero "__test_malloc_check_ranges_6"
     push 52
     call "raise"
part "__test_malloc_check_ranges_6"
     push 1
     call "memory_manager_get_cell"
     push 2
     call "memory_manager_get_cell"
     push 30
     sub
     zero "__test_malloc_check_ranges_7"
     push 53
     call "raise"
part "__test_malloc_check_ranges_7"
     push 26
     sub
     zero "__test_malloc_check_ranges_8"
     push 54
     call "raise"
part "__test_malloc_check_ranges_8"
     push 25
     sub
     zero "__test_malloc_check_ranges_9"
     push 55
     call "raise"
part "__test_malloc_check_ranges_9"
     push 21
     sub
     zero "__test_malloc_check_ranges_return"
     push 56
     call "raise"
part "__test_malloc_check_ranges_return"
     push -2
     push -10
     call "clear"
     back
# def test_malloc_ranges():
#     HEAP[-1] = 1
#     memory_manager_append_cell(11, 20)
#     memory_manager_append_cell(31, 40)
#     if malloc_ranges(10) != 1:
#         raise Exception(57)
#     if malloc_ranges(10) != 21:
#         raise Exception(58)
#     if malloc_ranges(10) != 41:
#         raise Exception(59)
#     f, e = memory_manager_get_cell(0)
#     d, c = memory_manager_get_cell(2)
#     b, a = memory_manager_get_cell(4)
#     if a != 50:
#         raise Exception(60)
#     if b != 41:
#         raise Exception(61)
#     if c != 30:
#         raise Exception(62)
#     if d != 21:
#         raise Exception(63)
#     if e != 10:
#         raise Exception(64)
#     if f != 1:
#         raise Exception(65)
#     clear(-1, -12)
part "test_malloc_ranges"
     push 31
     push 40
     push 11
     push 20
     push -1
     push 1
     set
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     push 10
     call "malloc_ranges"
     push 1
     sub
     zero "__test_malloc_ranges_2"
     push 57
     call "raise"
part "__test_malloc_ranges_2"
     push 10
     call "malloc_ranges"
     push 21
     sub
     zero "__test_malloc_ranges_3"
     push 58
     call "raise"
part "__test_malloc_ranges_3"
     push 10
     call "malloc_ranges"
     push 41
     sub
     zero "__test_malloc_ranges_4"
     push 59
     call "raise"
part "__test_malloc_ranges_4"
     push 0
     call "memory_manager_get_cell"
     push 2
     call "memory_manager_get_cell"
     push 4
     call "memory_manager_get_cell"
     push 50
     sub
     zero "__test_malloc_ranges_5"
     push 60
     call "raise"
part "__test_malloc_ranges_5"
     push 41
     sub
     zero "__test_malloc_ranges_6"
     push 61
     call "raise"
part "__test_malloc_ranges_6"
     push 30
     sub
     zero "__test_malloc_ranges_7"
     push 62
     call "raise"
part "__test_malloc_ranges_7"
     push 21
     sub
     zero "__test_malloc_ranges_8"
     push 63
     call "raise"
part "__test_malloc_ranges_8"
     push 10
     sub
     zero "__test_malloc_ranges_9"
     push 64
     call "raise"
part "__test_malloc_ranges_9"
     push 1
     sub
     zero "__test_malloc_ranges_return"
     push 65
     call "raise"
part "__test_malloc_ranges_return"
     push -1
     push -12
     call "clear"
     back
# def test_malloc():
#     HEAP[-1] = 1
#     if malloc(1) != 1:
#         raise Exception(66)
#     if malloc(2) != 2:
#         raise Exception(67)
#     if malloc(3) != 4:
#         raise Exception(68)
#     if malloc(4) != 7:
#         raise Exception(69)
#     if HEAP[-2] != 4:
#         raise Exception(70)
#     if HEAP[-10] != 10:
#         raise Exception(71)
#     clear(-1, -10)
part "test_malloc"
     push -1
     push 1
     set
     push 1
     call "malloc"
     push 1
     sub
     zero "__test_malloc_2"
     push 66
     call "raise"
part "__test_malloc_2"
     push 2
     call "malloc"
     push 2
     sub
     zero "__test_malloc_3"
     push 67
     call "raise"
part "__test_malloc_3"
     push 3
     call "malloc"
     push 4
     sub
     zero "__test_malloc_4"
     push 68
     call "raise"
part "__test_malloc_4"
     push 4
     call "malloc"
     push 7
     sub
     zero "__test_malloc_5"
     push 69
     call "raise"
part "__test_malloc_5"
     push -2
     get
     push 4
     sub
     zero "__test_malloc_6"
     push 70
     call "raise"
part "__test_malloc_6"
     push -10
     copy
     get
     add
     zero "__test_malloc_return"
     push 71
     call "raise"
part "__test_malloc_return"
     push -1
     push -10
     call "clear"
     back
# def test_calloc():
#     HEAP[-1] = 1
#     if calloc(10, 10) != 1:
#         raise Exception(72)
#     if HEAP[-4] != 100:
#         raise Exception(73)
#     clear(-1, -4)
part "test_calloc"
     push -1
     push 1
     set
     push 10
     copy
     call "calloc"
     push 1
     sub
     zero "__test_calloc_2"
     push 72
     call "raise"
part "__test_calloc_2"
     push 100
     push -4
     get
     sub
     zero "__test_calloc_return"
     push 73
     call "raise"
part "__test_calloc_return"
     push -1
     push -4
     call "clear"
     back
# def test_memory_manager_search():
#     if memory_manager_search(1) != -1:
#         raise Exception(74)
#     memory_manager_append_cell(1, 10)
#     memory_manager_append_cell(11, 20)
#     memory_manager_append_cell(21, 30)
#     memory_manager_append_cell(31, 40)
#     memory_manager_append_cell(41, 50)
#     memory_manager_append_cell(51, 60)
#     memory_manager_append_cell(61, 70)
#     if memory_manager_search(1) != 0:
#         raise Exception(75)
#     if memory_manager_search(31) != 3:
#         raise Exception(76)
#     if memory_manager_search(61) != 6:
#         raise Exception(77)
#     if memory_manager_search(0) != -1:
#         raise Exception(78)
#     if memory_manager_search(62) != -1:
#         raise Exception(79)
#     clear(-2, -16)
part "test_memory_manager_search"
     push 1
     copy
     call "memory_manager_search"
     add
     zero "__test_memory_manager_search_2"
     push 74
     call "raise"
part "__test_memory_manager_search_2"
     push 61
     push 70
     push 51
     push 60
     push 41
     push 50
     push 31
     push 40
     push 21
     push 30
     push 11
     push 20
     push 1
     push 10
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     push 1
     call "memory_manager_search"
     zero "__test_memory_manager_search_3"
     push 75
     call "raise"
part "__test_memory_manager_search_3"
     push 31
     call "memory_manager_search"
     push 3
     sub
     zero "__test_memory_manager_search_4"
     push 76
     call "raise"
part "__test_memory_manager_search_4"
     push 61
     call "memory_manager_search"
     push 6
     sub
     zero "__test_memory_manager_search_5"
     push 77
     call "raise"
part "__test_memory_manager_search_5"
     push 0
     call "memory_manager_search"
     push 1
     add
     zero "__test_memory_manager_search_6"
     push 78
     call "raise"
part "__test_memory_manager_search_6"
     push 62
     call "memory_manager_search"
     push 1
     add
     zero "__test_memory_manager_search_return"
     push 79
     call "raise"
part "__test_memory_manager_search_return"
     push -2
     push -16
     call "clear"
     back
# def test_memory_manager_pop_cell():
#     memory_manager_append_cell(11, 20)
#     memory_manager_append_cell(21, 30)
#     memory_manager_append_cell(31, 40)
#     memory_manager_append_cell(41, 50)
#     h, g = memory_manager_pop_cell(-1)
#     f, e = memory_manager_pop_cell(0)
#     d, c = memory_manager_pop_cell(1)
#     b, a = memory_manager_pop_cell(0)
#     if a != 30:
#         raise Exception(84)
#     if b != 21:
#         raise Exception(85)
#     if c != 40:
#         raise Exception(86)
#     if d != 31:
#         raise Exception(87)
#     if e != 20:
#         raise Exception(88)
#     if f != 11:
#         raise Exception(89)
#     if g != 50:
#         raise Exception(90)
#     if h != 41:
#         raise Exception(91)
part "test_memory_manager_pop_cell"
     push 41
     push 50
     push 31
     push 40
     push 21
     push 30
     push 11
     push 20
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     push -1
     call "memory_manager_pop_cell"
     push 0
     call "memory_manager_pop_cell"
     push 1
     call "memory_manager_pop_cell"
     push 0
     call "memory_manager_pop_cell"
     push 30
     sub
     zero "__test_memory_manager_pop_cell_2"
     push 84
     call "raise"
part "__test_memory_manager_pop_cell_2"
     push 21
     sub
     zero "__test_memory_manager_pop_cell_3"
     push 85
     call "raise"
part "__test_memory_manager_pop_cell_3"
     push 40
     sub
     zero "__test_memory_manager_pop_cell_4"
     push 86
     call "raise"
part "__test_memory_manager_pop_cell_4"
     push 31
     sub
     zero "__test_memory_manager_pop_cell_5"
     push 87
     call "raise"
part "__test_memory_manager_pop_cell_5"
     push 20
     sub
     zero "__test_memory_manager_pop_cell_6"
     push 88
     call "raise"
part "__test_memory_manager_pop_cell_6"
     push 11
     sub
     zero "__test_memory_manager_pop_cell_7"
     push 89
     call "raise"
part "__test_memory_manager_pop_cell_7"
     push 50
     sub
     zero "__test_memory_manager_pop_cell_8"
     push 90
     call "raise"
part "__test_memory_manager_pop_cell_8"
     push 41
     sub
     zero "__test_memory_manager_pop_cell_return"
     push 91
     call "raise"
part "__test_memory_manager_pop_cell_return"
     back
# def test_free():
#     HEAP[-1] = 1
#     a = malloc(100)
#     b = malloc(100)
#     free(a)
#     c = malloc(50)
#     d = malloc(50)
#     e = malloc(50)
#     free(d)
#     f = malloc(25)
#     g = malloc(25)
#     h = malloc(25)
#     free(b)
#     i = malloc(25)
#     j = malloc(100)
#     if memory_manager_get_cell(0)[0] != 1:
#         raise Exception(92)
#     if memory_manager_get_cell(1)[0] != 51:
#         raise Exception(93)
#     if memory_manager_get_cell(2)[0] != 76:
#         raise Exception(94)
#     if memory_manager_get_cell(3)[0] != 101:
#         raise Exception(95)
#     if memory_manager_get_cell(4)[0] != 201:
#         raise Exception(96)
#     if memory_manager_get_cell(5)[0] != 251:
#         raise Exception(97)
#     if memory_manager_get_cell(6)[0] != 276:
#         raise Exception(98)
#     if memory_manager_get_cell(6)[1] != 375:
#         raise Exception(99)
#     free(j)
#     free(i)
#     free(h)
#     free(g)
#     free(f)
#     free(e)
#     free(c)
#     if HEAP[-2] != 0:
#         raise Exception(100)
#     clear(-1, 0)
part "test_free"
     push -1
     push 1
     set
     push 100
     call "malloc"
     push 100
     call "malloc"
     swap
     call "free"
     push 50
     call "malloc"
     push 50
     call "malloc"
     push 50
     call "malloc"
     swap
     call "free"
     push 25
     call "malloc"
     push 25
     call "malloc"
     push 25
     call "malloc"
     copy 5
     call "free"
     push 25
     call "malloc"
     push 100
     call "malloc"
     push 0
     call "memory_manager_get_cell"
     away
     push 1
     sub
     zero "__test_free_2"
     push 92
     call "raise"
part "__test_free_2"
     push 1
     call "memory_manager_get_cell"
     away
     push 51
     sub
     zero "__test_free_3"
     push 93
     call "raise"
part "__test_free_3"
     push 2
     call "memory_manager_get_cell"
     away
     push 76
     sub
     zero "__test_free_4"
     push 94
     call "raise"
part "__test_free_4"
     push 3
     call "memory_manager_get_cell"
     away
     push 101
     sub
     zero "__test_free_5"
     push 95
     call "raise"
part "__test_free_5"
     push 4
     call "memory_manager_get_cell"
     away
     push 201
     sub
     zero "__test_free_6"
     push 96
     call "raise"
part "__test_free_6"
     push 5
     call "memory_manager_get_cell"
     away
     push 251
     sub
     zero "__test_free_7"
     push 97
     call "raise"
part "__test_free_7"
     push 6
     call "memory_manager_get_cell"
     away
     push 276
     sub
     zero "__test_free_8"
     push 98
     call "raise"
part "__test_free_8"
     push 6
     call "memory_manager_get_cell"
     away 1
     push 375
     sub
     zero "__test_free_9"
     push 99
     call "raise"
part "__test_free_9"
     call "free"
     call "free"
     call "free"
     call "free"
     call "free"
     call "free"
     call "free"
     away
     push -2
     get
     zero "__test_free_return"
     push 100
     call "raise"
part "__test_free_return"
     push -1
     push 0
     call "clear"
     back
# def test_memory_manager_get_block_size():
#     HEAP[-1] = 1
#     a = malloc(123)
#     if memory_manager_get_block_size(0) != 123:
#         raise Exception(102)
#     free(a)
#     clear(-1, 0)
part "test_memory_manager_get_block_size"
     push -1
     push 1
     set
     push 123
     call "malloc"
     push 0
     call "memory_manager_get_block_size"
     push 123
     sub
     zero "__test_memory_manager_get_block_size_return"
     push 102
     call "raise"
part "__test_memory_manager_get_block_size_return"
     call "free"
     push -1
     push 0
     call "clear"
     back
# def test_memory_manager_set_cell():
#     memory_manager_append_cell(1, 10)
#     memory_manager_set_cell(11, 20, 0)
#     b, a = memory_manager_get_cell(0)
#     if a != 20:
#         raise Exception(106)
#     if b != 11:
#         raise Exception(107)
#     clear(-2, -4)
part "test_memory_manager_set_cell"
     push 0
     push 11
     push 20
     push 0
     push 1
     push 10
     call "memory_manager_append_cell"
     call "memory_manager_set_cell"
     call "memory_manager_get_cell"
     push 20
     sub
     zero "__test_memory_manager_set_cell_2"
     push 106
     call "raise"
part "__test_memory_manager_set_cell_2"
     push 11
     sub
     zero "__test_memory_manager_set_cell_return"
     push 107
     call "raise"
part "__test_memory_manager_set_cell_return"
     push -2
     push -4
     call "clear"
     back
# def test_memory_manager_deflate_block():
#     memory_manager_append_cell(1, 100)
#     memory_manager_deflate_block(50, 0)
#     if memory_manager_get_block_size(0) != 50:
#         raise Exception(108)
#     clear(-2, -4)
part "test_memory_manager_deflate_block"
     push 1
     push 100
     call "memory_manager_append_cell"
     push 50
     push 0
     call "memory_manager_deflate_block"
     push 0
     call "memory_manager_get_block_size"
     push 50
     sub
     zero "__test_memory_manager_deflate_block_return"
     push 108
     call "raise"
part "__test_memory_manager_deflate_block_return"
     push -2
     push -4
     call "clear"
     back
# def test_memory_manager_inflate_cell():
#     memory_manager_append_cell(1, 50)
#     memory_manager_inflate_cell(100, 0)
#     if memory_manager_get_block_size(0) != 100:
#         raise Exception(110)
#     clear(-2, -4)
part "test_memory_manager_inflate_cell"
     push 1
     push 50
     call "memory_manager_append_cell"
     push 100
     push 0
     call "memory_manager_inflate_cell"
     push 0
     call "memory_manager_get_block_size"
     push 100
     sub
     zero "__test_memory_manager_inflate_cell_return"
     push 110
     call "raise"
part "__test_memory_manager_inflate_cell_return"
     push -2
     push -4
     call "clear"
     back
# def test_memory_manager_potential_after():
#     memory_manager_append_cell(101, 200)
#     memory_manager_append_cell(251, 300)
#     if memory_manager_potential_after(0) != 150:
#         raise Exception(111)
#     clear(-2, -6)
part "test_memory_manager_potential_after"
     push -2
     push -6
     push 150
     push 0
     push 251
     push 300
     push 101
     push 200
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_potential_after"
     sub
     zero "__test_memory_manager_potential_after_return"
     push 111
     call "raise"
part "__test_memory_manager_potential_after_return"
     call "clear"
     back
# def test_memory_manager_potential_before():
#     HEAP[-1] = 51
#     memory_manager_append_cell(101, 250)
#     memory_manager_append_cell(301, 325)
#     memory_manager_append_cell(351, 400)
#     if memory_manager_potential_before(0) != 250:
#         raise Exception(112)
#     if memory_manager_potentail_before(1) != 100:
#         raise Exception(113)
#     clear(-1, -8)
part "test_memory_manager_potential_before"
     push -1
     push -8
     push 100
     push 1
     push 250
     push 0
     push 351
     push 400
     push 301
     push 325
     push 101
     push 250
     push -1
     push 51
     set
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_potential_before"
     sub
     zero "__test_memory_manager_potential_before_2"
     push 112
     call "raise"
part "__test_memory_manager_potential_before_2"
     call "memory_manager_potential_before"
     sub
     zero "__test_memory_manager_potential_before_return"
     push 113
     call "raise"
part "__test_memory_manager_potential_before_return"
     call "clear"
     back
# def test_memory_manager_compress():
#     HEAP[-1] = 101
#     memory_manager_append_cell(201, 300)
#     memory_manager_append_cell(401, 500)
#     if memory_manager_compress(0) != 101:
#         raise Exception(114)
#     if memory_manager_compress(1) != 301:
#         raise Exception(115)
#     clear(-1, -6)
part "test_memory_manager_compress"
     push -1
     push -6
     push 301
     push 1
     push 101
     push 0
     push 401
     push 500
     push 201
     push 300
     push -1
     push 101
     set
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_compress"
     sub
     zero "__test_memory_manager_compress_2"
     push 114
     call "raise"
part "__test_memory_manager_compress_2"
     call "memory_manager_compress"
     sub
     zero "__test_memory_manager_compress_return"
     push 115
     call "raise"
part "__test_memory_manager_compress_return"
     call "clear"
     back
# def test_compare_cells():
#     HEAP[1] = 1
#     HEAP[2] = 1
#     if compare_cells(1, 2) != 0:
#         raise Exception(121)
#     HEAP[1] = 2
#     if compare_cells(1, 2) != 1:
#         raise Exception(122)
#     if compare_cells(2, 1) != -1:
#         raise Exception(123)
#     clear(1, 2)
part "test_compare_cells"
     push 1
     push 2
     push -1
     push 2
     push 1
     push 1
     push 1
     push 2
     push 1
     push 2
     push 1
     push 2
     push 2
     push 1
     push 1
     push 1
     set
     set
     call "compare_cells"
     zero "__test_compare_cells_2"
     push 121
     call "raise"
part "__test_compare_cells_2"
     set
     call "compare_cells"
     sub
     zero "__test_compare_cells_3"
     push 122
     call "raise"
part "__test_compare_cells_3"
     call "compare_cells"
     sub
     zero "__test_compare_cells_return"
     push 123
     call "raise"
part "__test_compare_cells_return"
     call "clear"
     back
# def test_compare_memory():
#     if compare_memory(0, 1, 0) != 0:
#         raise Exception(124)
#     if compare_memory(1, 1, 1) != 0:
#         raise Exception(125)
#     HEAP[1] = 100
#     HEAP[2] = 200
#     HEAP[3] = 100
#     HEAP[4] = 200
#     if compare_memory(1, 3, 2) != 0:
#         raise Exception(126)
#     HEAP[2] = 300
#     if compare_memory(1, 3, 2) != 1:
#         raise Exception(127)
#     HEAP[4] = 400
#     if compare_memory(1, 3, 2) != -1:
#         raise Exception(128)
#     clear(1, 4)
part "test_compare_memory"
     push 1
     push 4
     push -1
     push 1
     push 3
     push 2
     push 4
     push 400
     push 1
     push 1
     push 3
     push 2
     push 2
     push 300
     push 1
     push 3
     push 2
     push 4
     push 200
     push 3
     push 100
     push 2
     push 200
     push 1
     push 100
     push 1
     push 1
     push 1
     push 0
     push 1
     push 0
     call "compare_memory"
     zero "__test_compare_memory_2"
     push 124
     call "raise"
part "__test_compare_memory_2"
     call "compare_memory"
     zero "__test_compare_memory_3"
     push 125
     call "raise"
part "__test_compare_memory_3"
     set
     set
     set
     set
     call "compare_memory"
     zero "__test_compare_memory_4"
     push 126
     call "raise"
part "__test_compare_memory_4"
     set
     call "compare_memory"
     sub
     zero "__test_compare_memory_5"
     push 127
     call "raise"
part "__test_compare_memory_5"
     set
     call "compare_memory"
     sub
     zero "__test_compare_memory_return"
     push 128
     call "raise"
part "__test_compare_memory_return"
     call "clear"
     back
# test_direction():
#     if direction(-100) != -1:
#         raise Exception(130)
#     if direction(0) != 0:
#         raise Exception(131)
#     if direction(100) != 1:
#         raise Exception(132)
part "test_direction"
     push 1
     push 100
     push 0
     push -1
     push -100
     call "direction"
     sub
     zero "__test_direction_2"
     push 130
     call "raise"
part "__test_direction_2"
     call "direction"
     zero "__test_direction_3"
     push 131
     call "raise"
part "__test_direction_3"
     call "direction"
     sub
     zero "__test_direction_return"
     push 132
     call "raise"
part "__test_direction_return"
     back
# def test_range():
#     range(1, 1, 4, 1)
#     HEAP[4] = 1
#     HEAP[5] = 2
#     HEAP[6] = 3
#     if compare_memory(1, 4, 3) != 0:
#         raise Exception(133)
#     range(1, 0, -3, -1)
#     HEAP[4] = 0
#     HEAP[5] = -1
#     HEAP[6] = -2
#     if compare_memory(1, 4, 3) != 0:
#         raise Exception(134)
#     range(1, 0, 6, 2)
#     HEAP[5] = 2
#     HEAP[6] = 4
#     if compare_memory(1, 4, 3) != 0:
#         raise Exception(135)
#     range(1, 8, 3, -2)
#     HEAP[4] = 8
#     HEAP[5] = 6
#     if compare_memory(1, 4, 3) != 0:
#         raise Exception(136)
#     clear(1, 6)
part "test_range"
     push 1
     push 6
     push 1
     push 4
     push 3
     push 5
     push 6
     push 4
     push 8
     push 1
     push 8
     push 3
     push -2
     push 1
     push 4
     push 3
     push 6
     push 4
     push 5
     push 2
     push 1
     push 0
     push 6
     push 2
     push 1
     push 4
     push 3
     push 6
     push -2
     push 5
     push -1
     push 4
     push 0
     push 1
     push 0
     push -3
     push -1
     push 1
     push 4
     push 3
     push 6
     push 3
     push 5
     push 2
     push 4
     push 1
     push 1
     push 1
     push 4
     push 1
     call "range"
     set
     set
     set
     call "compare_memory"
     zero "__test_range_2"
     push 133
     call "raise"
part "__test_range_2"
     call "range"
     set
     set
     set
     call "compare_memory"
     zero "__test_range_3"
     push 134
     call "raise"
part "__test_range_3"
     call "range"
     set
     set
     call "compare_memory"
     zero "__test_range_4"
     push 135
     call "raise"
part "__test_range_4"
     call "range"
     set
     set
     call "compare_memory"
     zero "__test_range_return"
     push 136
     call "raise"
part "__test_range_return"
     call "clear"
     back
# def test_memory_manager_size():
#     HEAP[-1] = 1
#     a = malloc(123)
#     b = malloc(456)
#     c = malloc(789)
#     if memory_manager_size(a) != 123:
#         raise Exception(138)
#     if memory_manager_size(b) != 456:
#         raise Exception(139)
#     if memory_manager_size(c) != 789:
#         raise Exception(140)
#     free(c)
#     free(b)
#     free(a)
#     clear(-1, 0)
part "test_memory_manager_size"
     push -1
     push 1
     set
     push 123
     call "malloc"
     push 456
     call "malloc"
     push 789
     call "malloc"
     copy 2
     call "memory_manager_size"
     push 123
     sub
     zero "__test_memory_manager_size_2"
     push 138
     call "raise"
part "__test_memory_manager_size_2"
     copy 1
     call "memory_manager_size"
     push 456
     sub
     zero "__test_memory_manager_size_3"
     push 139
     call "raise"
part "__test_memory_manager_size_3"
     copy
     call "memory_manager_size"
     push 789
     sub
     zero "__test_memory_manager_size_return"
     push 140
     call "raise"
part "__test_memory_manager_size_return"
     call "free"
     call "free"
     call "free"
     push -1
     push 0
     call "clear"
     back
# def test_mark():
#     HEAP[-1] = 1
#     a = malloc(1500)
#     mark(a)
#     range(3001, 1, 1501, 1)
#     if compare_memory(a, 3001, 3000) != 0:
#         raise Exception(141)
#     free(a)
#     clear(-1, 4500)
part "test_mark"
     push -1
     push 1
     set
     push 1500
     call "malloc"
     copy
     call "mark"
     push 3001
     push 1
     push 1501
     push 1
     call "range"
     copy
     push 3001
     push 3000
     call "compare_memory"
     zero "__test_mark_return"
     push 141
     call "raise"
part "__test_mark_return"
     call "free"
     push -1
     push 4500
     call "clear"
     back
# def test_memory_manager_inflate_before():
#     HEAP[-1] = 101
#     a = malloc(10)
#     b = malloc(10)
#     c = malloc(10)
#     d = malloc(10)
#     if HEAP[-2] != 4:
#         raise Exception(116)
#     mark(d)
#     mark(c)
#     mark(b)
#     free(a)
#     b = memory_manager_inflate_before(b, 15, 0)
#     c = memory_manager_inflate_before(c, 15, 1)
#     if HEAP[-2] != 3:
#         raise Exception(117)
#     e = malloc(40)
#     range(e, 1, 11, 1)
#     range(e + 10, 1, 6, 1)
#     range(e + 15, 1, 6, 1)
#     range(e + 20, 6, 11, 1)
#     range(e + 25, 6, 11, 1)
#     range(e + 30, 1, 11, 1)
#     if compare_memory(b, e, 40) != 0:
#         raise Exception(118)
#     free(e)
#     free(c)
#     free(b)
#     free(d)
#     if HEAP[-2] != 0:
#         raise Exception(119)
#     HEAP[-1] = 0
#     HEAP[0] = 0
#     clear(101, 180)
part "test_memory_manager_inflate_before"
     push -1
     push 101
     set
     push 10
     call "malloc"
     push 10
     call "malloc"
     push 10
     call "malloc"
     push 10
     call "malloc"
     push 4
     push -2
     get
     sub
     zero "__test_memory_manager_inflate_before_2"
     push 116
     call "raise"
part "__test_memory_manager_inflate_before_2"
     copy 3
     copy 3
     copy 3
     copy 3
     call "mark"
     call "mark"
     call "mark"
     call "free"
     copy 2
     push 15
     push 0
     call "memory_manager_inflate_before"
     copy 2
     push 15
     push 1
     call "memory_manager_inflate_before"
     push 3
     push -2
     get
     sub
     zero "__test_memory_manager_inflate_before_3"
     push 117
     call "raise"
part "__test_memory_manager_inflate_before_3"
     push 40
     call "malloc"
     copy
     push 1
     push 11
     push 1
     call "range"
     copy
     push 10
     add
     push 1
     push 6
     push 1
     call "range"
     copy
     push 15
     add
     push 1
     push 6
     push 1
     call "range"
     copy
     push 20
     add
     push 6
     push 11
     push 1
     call "range"
     copy
     push 25
     add
     push 6
     push 11
     push 1
     call "range"
     copy
     push 30
     add
     push 1
     push 11
     push 1
     call "range"
     copy 2
     copy 1
     push 40
     call "compare_memory"
     zero "__test_memory_manager_inflate_before_4"
     push 118
     call "raise"
part "__test_memory_manager_inflate_before_4"
     call "free"
     call "free"
     call "free"
     call "free"
     push -2
     away 3
     get
     zero "__test_memory_manager_inflate_before_return"
     push 119
     call "raise"
part "__test_memory_manager_inflate_before_return"
     push 101
     push 180
     push 0
     push 0
     push -1
     push 0
     set
     set
     call "clear"
     back
# def test_rotate_3_down():
#     stack.extend((1, 2, 3))
#     rotate_3_down()
#     if stack.pop() != 1:
#         raise Exception(147)
#     if stack.pop() != 3:
#         raise Exception(148)
#     if stack.pop() != 2:
#         raise Exception(149)
#     HEAP[0] = 0
part "test_rotate_3_down"
     push 1
     push 2
     push 3
     call "rotate_3_down"
     push 1
     sub
     zero "__test_rotate_3_down_2"
     push 147
     call "raise"
part "__test_rotate_3_down_2"
     push 3
     sub
     zero "__test_rotate_3_down_3"
     push 148
     call "raise"
part "__test_rotate_3_down_3"
     push 2
     sub
     zero "__test_rotate_3_down_return"
     push 149
     call "raise"
part "__test_rotate_3_down_return"
     push 0
     push 0
     set
     back
# def test_rotate_3_up():
#     stack.extend((1, 2, 3))
#     rotate_3_down()
#     if stack.pop() != 2:
#         raise Exception(150)
#     if stack.pop() != 1:
#         raise Exception(151)
#     if stack.pop() != 3:
#         raise Exception(152)
#     HEAP[0] = 0
part "test_rotate_3_up"
     push 1
     push 2
     push 3
     call "rotate_3_up"
     push 2
     sub
     zero "__test_rotate_3_up_2"
     push 150
     call "raise"
part "__test_rotate_3_up_2"
     push 1
     sub
     zero "__test_rotate_3_up_3"
     push 151
     call "raise"
part "__test_rotate_3_up_3"
     push 3
     sub
     zero "__test_rotate_3_up_return"
     push 152
     call "raise"
part "__test_rotate_3_up_return"
     push 0
     push 0
     set
     back
# def test_memory_manager_inflate_move():
#     HEAP[-1] = 1
#     a = malloc(10)
#     b = malloc(25)
#     c = malloc(10)
#     d = malloc(5)
#     e = malloc(10)
#     f = malloc(5)
#     g = malloc(10)
#     free(b)
#     free(d)
#     free(f)
#     mark(e)
#     h = memory_manager_inflate_move(e, 25, 2)
#     if compare_memory(1, e - 10, 50) != 0:
#         raise Exception(142)
#     i = malloc(5)
#     free(g)
#     j = malloc(25)
#     if memory_manager_size(h) != 25:
#         raise Exception(143)
#     if memory_manager_size(j) != 25:
#         raise Exception(144)
#     if compare_memory(h, j, 25) != 0:
#         raise Exception(145)
#     if j != e:
#         raise Exception(146)
#     free(j)
#     free(i)
#     free(h)
#     free(c)
#     free(a)
#     clear(-1, 0)
#     clear(11, 20)
#     clear(51, 60)
part "test_memory_manager_inflate_move"
     push -1
     push 1
     set
     push 10
     call "malloc"
     push 25
     call "malloc"
     push 10
     call "malloc"
     push 5
     call "malloc"
     push 10
     call "malloc"
     push 5
     call "malloc"
     push 10
     call "malloc"
     copy 2
     copy 2
     copy 5
     copy 8
     call "free"
     call "free"
     call "free"
     call "mark"
     copy 2
     push 25
     push 2
     call "memory_manager_inflate_move"
     push 1
     copy 4
     push 10
     sub
     push 50
     call "compare_memory"
     zero "__test_memory_manager_inflate_move_2"
     push 142
     call "raise"
part "__test_memory_manager_inflate_move_2"
     push 5
     call "malloc"
     copy 2
     call "free"
     push 25
     call "malloc"
     copy 2
     call "memory_manager_size"
     push 25
     sub
     zero "__test_memory_manager_inflate_move_3"
     push 143
     call "raise"
part "__test_memory_manager_inflate_move_3"
     copy
     call "memory_manager_size"
     push 25
     sub
     zero "__test_memory_manager_inflate_move_4"
     push 144
     call "raise"
part "__test_memory_manager_inflate_move_4"
     copy 2
     copy 1
     push 25
     call "compare_memory"
     zero "__test_memory_manager_inflate_move_5"
     push 145
     call "raise"
part "__test_memory_manager_inflate_move_5"
     copy
     copy 6
     sub
     zero "__test_memory_manager_inflate_move_return"
     push 146
     call "raise"
part "__test_memory_manager_inflate_move_return"
     call "free"
     call "free"
     away 4
     call "free"
     call "free"
     away
     call "free"
     push -1
     push 0
     call "clear"
     push 11
     push 20
     call "clear"
     push 51
     push 60
     call "clear"
     back
# def test_memory_manager_inflate_block():
#     HEAP[-1] = 1
#     a = malloc(10)
#     b = memory_manager_inflate_block(a, 20, 0)
#     if a != b:
#         raise Exception(153)
#     if memory_manager_size(a) != 20:
#         raise Exception(154)
#     c = malloc(10)
#     d = malloc(10)
#     free(c)
#     e = memory_manager_inflate_block(a, 30, 0)
#     if a != e:
#         raise Exception(155)
#     if memory_manager_size(a) != 30:
#         raise Exception(156)
#     f = malloc(10)
#     free(a)
#     mark(d)
#     g = memory_manager_inflate_block(d, 40, 0)
#     if a != g:
#         raise Exception(157)
#     if memory_manager_size(a) != 40:
#         raise Exception(158)
#     if compare_memory(1, 31, 10) != 0:
#         raise Exception(159)
#     h = memory_manager_inflate_block(a, 50, 0)
#     if h != f + memory_manager_size(f):
#         raise Exception(160)
#     if compare_memory(1, 51, 50) != 0:
#         raise Exception(161)
#     free(h)
#     free(f)
#     clear(-1, 90)
part "test_memory_manager_inflate_block"
     push -1
     push 1
     set
     push 10
     call "malloc"
     copy
     push 20
     push 0
     call "memory_manager_inflate_block"
     copy 1
     sub
     zero "__test_memory_manager_inflate_block_2"
     push 153
     call "raise"
     back
part "__test_memory_manager_inflate_block_2"
     copy
     call "memory_manager_size"
     push 20
     sub
     zero "__test_memory_manager_inflate_block_3"
     push 154
     call "raise"
part "__test_memory_manager_inflate_block_3"
     push 10
     call "malloc"
     push 10
     call "malloc"
     swap
     call "free"
     copy 1
     push 30
     push 0
     call "memory_manager_inflate_block"
     copy 2
     sub
     zero "__test_memory_manager_inflate_block_4"
     push 155
     call "raise"
part "__test_memory_manager_inflate_block_4"
     copy 1
     call "memory_manager_size"
     push 30
     sub
     zero "__test_memory_manager_inflate_block_5"
     push 156
     call "raise"
part "__test_memory_manager_inflate_block_5"
     push 10
     call "malloc"
     copy 2
     call "free"
     copy 1
     copy
     call "mark"
     push 40
     push 0
     call "memory_manager_inflate_block"
     copy 3
     sub
     zero "__test_memory_manager_inflate_block_6"
     push 157
     call "raise"
part "__test_memory_manager_inflate_block_6"
     copy 2
     call "memory_manager_size"
     push 40
     sub
     zero "__test_memory_manager_inflate_block_7"
     push 158
     call "raise"
part "__test_memory_manager_inflate_block_7"
     push 1
     push 31
     push 10
     call "compare_memory"
     zero "__test_memory_manager_inflate_block_8"
     push 159
     call "raise"
part "__test_memory_manager_inflate_block_8"
     copy 2
     push 50
     push 0
     call "memory_manager_inflate_block"
     copy
     copy 2
     copy
     call "memory_manager_size"
     add
     sub
     zero "__test_memory_manager_inflate_block_9"
     push 160
     call "raise"
part "__test_memory_manager_inflate_block_9"
     push 1
     push 51
     push 50
     call "compare_memory"
     zero "__test_memory_manager_inflate_block_return"
     push 161
     call "raise"
part "__test_memory_manager_inflate_block_return"
     call "free"
     away 2
     call "free"
     push -1
     push 90
     call "clear"
     back
# def test_realloc():
#     HEAP[-1] = 1
#     a = malloc(3)
#     if realloc(a, 0) != 0:
#         raise Exception(162)
#     a = malloc(3)
#     if realloc(a, -1) != 0:
#         raise Exception(163)
#     a = malloc(3)
#     if realloc(a, 3) != a:
#         raise Exception(164)
#     if memory_manager_size(a) != 3:
#         raise Exception(165)
#     if realloc(a, 2) != a:
#         raise Exception(166)
#     if memory_manager_size(a) != 2:
#         raise Exception(167)
#     b = malloc(3)
#     if realloc(a, 3) != 6:
#         raise Exception(168)
#     if memory_manager_size(6) != 3:
#         raise Exception(169)
#     free(b)
#     free(6)
#     clear(-1, 0)
part "test_realloc"
     push -1
     push 1
     set
     push 3
     call "malloc"
     push 0
     call "realloc"
     zero "__test_realloc_2"
     push 162
     call "raise"
part "__test_realloc_2"
     push 3
     call "malloc"
     push -1
     call "realloc"
     zero "__test_realloc_3"
     push 163
     call "raise"
part "__test_realloc_3"
     push 3
     call "malloc"
     copy
     copy
     copy
     push 3
     call "realloc"
     sub
     zero "__test_realloc_4"
     push 164
     call "raise"
part "__test_realloc_4"
     call "memory_manager_size"
     push 3
     sub
     zero "__test_realloc_5"
     push 165
     call "raise"
part "__test_realloc_5"
     copy
     copy
     copy
     push 2
     call "realloc"
     sub
     zero "__test_realloc_6"
     push 166
     call "raise"
part "__test_realloc_6"
     call "memory_manager_size"
     push 2
     sub
     zero "__test_realloc_7"
     push 167
     call "raise"
part "__test_realloc_7"
     push 3
     call "malloc"
     swap
     push 3
     call "realloc"
     push 6
     sub
     zero "__test_realloc_8"
     push 168
     call "raise"
part "__test_realloc_8"
     push 3
     push 6
     call "memory_manager_size"
     sub
     zero "__test_realloc_return"
     push 169
     call "raise"
part "__test_realloc_return"
     call "free"
     push 6
     call "free"
     push -1
     push 0
     call "clear"
     back
# def test_memory_manager_blocks():
#     HEAP[-1] = 1
#     a = malloc(10)
#     b = malloc(10)
#     c = malloc(10)
#     if memory_manager_blocks() != 3:
#         raise Exception(170)
#     free(c)
#     free(b)
#     free(a)
#     if memory_manager_blocks() != 0:
#         raise Exception(171)
#     clear(-1, 0)
part "test_memory_manager_blocks"
     push -1
     push 1
     set
     push 10
     call "malloc"
     push 10
     call "malloc"
     push 10
     call "malloc"
     call "memory_manager_blocks"
     push 3
     sub
     zero "__test_memory_manager_blocks_2"
     push 170
     call "raise"
part "__test_memory_manager_blocks_2"
     call "free"
     call "free"
     call "free"
     call "memory_manager_blocks"
     zero "__test_memory_manager_blocks_return"
     push 171
     call "raise"
part "__test_memory_manager_blocks_return"
     push -1
     push 0
     call "clear"
     back
# def test_memory_manager_cells():
#     memory_manager_append_cell(11, 20)
#     memory_manager_append_cell(31, 40)
#     if memory_manager_cells() != 20:
#         raise Exception(172)
#     memory_manager_pop_cell(-1)
#     if memory_manager_cells() != 10:
#         raise Exception(173)
#     memory_manager_pop_cell(-1)
#     if memory_manager_cells() != 0:
#         raise Exception(174)
#     HEAP[0] = 0
part "test_memory_manager_cells"
     push 0
     push 0
     push -1
     push 10
     push -1
     push 20
     push 31
     push 40
     push 11
     push 20
     call "memory_manager_append_cell"
     call "memory_manager_append_cell"
     call "memory_manager_cells"
     sub
     zero "__test_memory_manager_cells_2"
     push 172
     call "raise"
part "__test_memory_manager_cells_2"
     call "memory_manager_pop_cell"
     away
     away
     call "memory_manager_cells"
     sub
     zero "__test_memory_manager_cells_3"
     push 173
     call "raise"
part "__test_memory_manager_cells_3"
     call "memory_manager_pop_cell"
     away
     away
     call "memory_manager_cells"
     zero "__test_memory_manager_cells_return"
     push 174
     call "raise"
part "__test_memory_manager_cells_return"
     set
     back
# def test_memory_manager_pointers():
#     HEAP[-1] = 1025
#     array = memory_manager_pointers(False)
#     if array[0] != 0:
#         raise Exception(176)
#     free(array)
#     array = memory_manager_pointers(True)
#     if array[0] != 1:
#         raise Exception(177)
#     if array[1] != array:
#         raise Exception(178)
#     test = memory_manager_pointers(False)
#     if compare_memory(array, test, 2) != 0:
#         raise Exception(179)
#     free(test)
#     test = memory_manager_pointers(True)
#     if test[0] != 2:
#         raise Exception(180)
#     if test[1] != array:
#         raise Exception(181)
#     if test[2] != test:
#         raise Exception(182)
#     free(test)
#     free(array)
#     clear(-1, 0)
#     clear(1025, 1029)
part "test_memory_manager_pointers"
     push -1
     push 1025
     set
     push 0
     call "memory_manager_pointers"
     copy
     get
     zero "__test_memory_manager_pointers_2"
     push 176
     call "raise"
part "__test_memory_manager_pointers_2"
     call "free"
     push 1
     call "memory_manager_pointers"
     copy
     get
     push 1
     sub
     zero "__test_memory_manager_pointers_3"
     push 177
     call "raise"
part "__test_memory_manager_pointers_3"
     copy
     copy
     push 1
     add
     get
     sub
     zero "__test_memory_manager_pointers_4"
     push 178
     call "raise"
part "__test_memory_manager_pointers_4"
     push 0
     call "memory_manager_pointers"
     copy 1
     copy 1
     push 2
     call "compare_memory"
     zero "__test_memory_manager_pointers_5"
     push 179
     call "raise"
part "__test_memory_manager_pointers_5"
     call "free"
     push 1
     call "memory_manager_pointers"
     copy
     get
     push 2
     sub
     zero "__test_memory_manager_pointers_6"
     push 180
     call "raise"
part "__test_memory_manager_pointers_6"
     copy 1
     copy 1
     push 1
     add
     get
     sub
     zero "__test_memory_manager_pointers_7"
     push 181
     call "raise"
part "__test_memory_manager_pointers_7"
     copy
     copy
     push 2
     add
     get
     sub
     zero "__test_memory_manager_pointers_return"
     push 182
     call "raise"
part "__test_memory_manager_pointers_return"
     call "free"
     call "free"
     push 1025
     push 1029
     push -1
     push 0
     call "clear"
     call "clear"
     back
# def test_memory_manager_find():
#     if memory_manager_find(1) != 0:
#         raise Exception(183)
#     memory_manager_append_cell(1, 10)
#     memory_manager_append_cell(21, 30)
#     memory_manager_append_cell(41, 50)
#     if memory_manager_find(0) != 0:
#         raise Exception(184)
#     if memory_manager_find(1) != 1:
#         raise Exception(185)
#     if memory_manager_find(5) != 1:
#         raise Exception(186)
#     if memory_manager_find(10) != 1:
#         raise Exception(187)
#     if memory_manager_find(11) != 0:
#         raise Exception(188)
#     if memory_manager_find(15) != 0:
#         raise Exception(189)
#     if memory_manager_find(20) != 0:
#         raise Exception(190)
#     if memory_manager_find(21) != 21:
#         raise Exception(191)
#     if memory_manager_find(25) != 21:
#         raise Exception(192)
#     if memory_manager_find(30) != 21:
#         raise Exception(193)
#     if memory_manager_find(31) != 0:
#         raise Exception(194)
#     if memory_manager_find(35) != 0:
#         raise Exception(195)
#     if memory_manager_find(40) != 0:
#         raise Exception(196)
#     if memory_manager_find(41) != 41:
#         raise Exception(197)
#     if memory_manager_find(45) != 41:
#         raise Exception(198)
#     if memory_manager_find(50) != 41:
#         raise Exception(199)
#     if memory_manager_find(51) != 0:
#         raise Exception(200)
#     clear(-8, 0)
part "test_memory_manager_find"
     push 1
     call "memory_manager_find"
     zero "__test_memory_manager_find_2"
     push 183
     call "raise"
part "__test_memory_manager_find_2"
     push 1
     push 10
     call "memory_manager_append_cell"
     push 21
     push 30
     call "memory_manager_append_cell"
     push 41
     push 50
     call "memory_manager_append_cell"
     push 0
     call "memory_manager_find"
     zero "__test_memory_manager_find_3"
     push 184
     call "raise"
part "__test_memory_manager_find_3"
     push 1
     call "memory_manager_find"
     push 1
     sub
     zero "__test_memory_manager_find_4"
     push 185
     call "raise"
part "__test_memory_manager_find_4"
     push 5
     call "memory_manager_find"
     push 1
     sub
     zero "__test_memory_manager_find_5"
     push 186
     call "raise"
part "__test_memory_manager_find_5"
     push 10
     call "memory_manager_find"
     push 1
     sub
     zero "__test_memory_manager_find_6"
     push 187
     call "raise"
part "__test_memory_manager_find_6"
     push 11
     call "memory_manager_find"
     zero "__test_memory_manager_find_7"
     push 188
     call "raise"
part "__test_memory_manager_find_7"
     push 15
     call "memory_manager_find"
     zero "__test_memory_manager_find_8"
     push 189
     call "raise"
part "__test_memory_manager_find_8"
     push 20
     call "memory_manager_find"
     zero "__test_memory_manager_find_9"
     push 190
     call "raise"
part "__test_memory_manager_find_9"
     push 21
     call "memory_manager_find"
     push 21
     sub
     zero "__test_memory_manager_find_10"
     push 191
     call "raise"
part "__test_memory_manager_find_10"
     push 25
     call "memory_manager_find"
     push 21
     sub
     zero "__test_memory_manager_find_11"
     push 192
     call "raise"
part "__test_memory_manager_find_11"
     push 30
     call "memory_manager_find"
     push 21
     sub
     zero "__test_memory_manager_find_12"
     push 193
     call "raise"
part "__test_memory_manager_find_12"
     push 31
     call "memory_manager_find"
     zero "__test_memory_manager_find_13"
     push 194
     call "raise"
part "__test_memory_manager_find_13"
     push 35
     call "memory_manager_find"
     zero "__test_memory_manager_find_14"
     push 195
     call "raise"
part "__test_memory_manager_find_14"
     push 40
     call "memory_manager_find"
     zero "__test_memory_manager_find_15"
     push 196
     call "raise"
part "__test_memory_manager_find_15"
     push 41
     call "memory_manager_find"
     push 41
     sub
     zero "__test_memory_manager_find_16"
     push 197
     call "raise"
part "__test_memory_manager_find_16"
     push 45
     call "memory_manager_find"
     push 41
     sub
     zero "__test_memory_manager_find_17"
     push 198
     call "raise"
part "__test_memory_manager_find_17"
     push 50
     call "memory_manager_find"
     push 41
     sub
     zero "__test_memory_manager_find_18"
     push 199
     call "raise"
part "__test_memory_manager_find_18"
     push 51
     call "memory_manager_find"
     zero "__test_memory_manager_find_return"
     push 200
     call "raise"
part "__test_memory_manager_find_return"
     push -8
     push 0
     call "clear"
     back
# def test_uint_cast():
#     if uint_cast(0) != 0:
#         raise Exception(201)
#     if uint_cast(4294967296) != 0:
#         raise Exception(202)
#     if uint_cast(-4294967296) != 0:
#         raise Exception(203)
#     if uint_cast(1) != 1
#         raise Exception(204)
#     if uint_cast(4294967297) != 1:
#         raise Exception(205)
#     if uint_cast(-4294967295) != 1:
#         raise Exception(206)
#     if uint_cast(-1) != 4294967295:
#         raise Exception(207)
#     if uint_cast(4294967295) != 4294967295:
#         raise Exception(208)
#     if uint_cast(-4294967297) != 4294967295:
#         raise Exception(209)
part "test_uint_cast"
     push 4294967295
     push -4294967297
     push 4294967295
     push 4294967295
     push 4294967295
     push -1
     push 1
     push -4294967295
     push 1
     push 4294967297
     push 1
     push 1
     push -4294967296
     push 4294967296
     push 0
     call "uint_cast"
     zero "__test_uint_cast_2"
     push 201
     call "raise"
part "__test_uint_cast_2"
     call "uint_cast"
     zero "__test_uint_cast_3"
     push 202
     call "raise"
part "__test_uint_cast_3"
     call "uint_cast"
     zero "__test_uint_cast_4"
     push 203
     call "raise"
part "__test_uint_cast_4"
     call "uint_cast"
     sub
     zero "__test_unint_cast_5"
     push 204
     call "raise"
part "__test_unint_cast_5"
     call "uint_cast"
     sub
     zero "__test_unint_cast_6"
     push 205
     call "raise"
part "__test_unint_cast_6"
     call "uint_cast"
     sub
     zero "__test_unint_cast_7"
     push 206
     call "raise"
part "__test_unint_cast_7"
     call "uint_cast"
     sub
     zero "__test_unint_cast_8"
     push 207
     call "raise"
part "__test_unint_cast_8"
     call "uint_cast"
     sub
     zero "__test_unint_cast_9"
     push 208
     call "raise"
part "__test_unint_cast_9"
     call "uint_cast"
     sub
     zero "__test_unint_cast_return"
     push 209
     call "raise"
part "__test_unint_cast_return"
     back
# def test_shift():
#     if left_shift(100, 0) != 100:
#         raise Exception(210)
#     if right_shift(100, 0) != 100:
#         raise Exception(211)
#     if left_shift(100, 2) != 400:
#         raise Exception(212)
#     if right_shift(100, 2) != 25:
#         raise Exception(213)
#     if left_shift(100, -2) != 25:
#         raise Exception(214)
#     if right_shift(100, -2) != 400:
#         raise Exception(215)
part "test_shift"
     push 400
     push 100
     push -2
     push 25
     push 100
     push -2
     push 25
     push 100
     push 2
     push 400
     push 100
     push 2
     push 100
     push 100
     push 0
     push 100
     push 100
     push 0
     call "left_shift"
     sub
     zero "__test_shift_2"
     push 210
     call "raise"
part "__test_shift_2"
     call "right_shift"
     sub
     zero "__test_shift_3"
     push 211
     call "raise"
part "__test_shift_3"
     call "left_shift"
     sub
     zero "__test_shift_4"
     push 212
     call "raise"
part "__test_shift_4"
     call "right_shift"
     sub
     zero "__test_shift_5"
     push 213
     call "raise"
part "__test_shift_5"
     call "left_shift"
     sub
     zero "__test_shift_6"
     push 214
     call "raise"
part "__test_shift_6"
     call "right_shift"
     sub
     zero "__test_shift_return"
     push 215
     call "raise"
part "__test_shift_return"
     back
# def test_save_stack():
#     HEAP[-1] = 1
#     stack.push(0)
#     stack.push(2)
#     stack.push(3)
#     stack.push(5)
#     stack.push(7)
#     stack.push(11)
#     stack.push(13)
#     stack.push(17)
#     stack.push(19)
#     array = save_stack(4)
#     if array[0] != 4:
#         raise Exception(223)
#     if array[4] != 11:
#         raise Exception(224)
#     free(array)
#     array = save_stack(4)
#     if array[0] != 4:
#         raise Exception(225)
#     if array[1] != 7:
#         raise Exception(226)
#     free(array)
#     if stack.pop() != 0:
#         raise Exception(227)
#     clear(-1, 8)
part "test_save_stack"
     push -1
     push 1
     set
     push 0
     push 2
     push 3
     push 5
     push 7
     push 11
     push 13
     push 17
     push 19
     push 4
     call "save_stack"
     copy
     get
     push 4
     sub
     zero "__test_save_stack_2"
     push 223
     call "raise"
part "__test_save_stack_2"
     copy
     push 4
     add
     get
     push 11
     sub
     zero "__test_save_stack_3"
     push 224
     call "raise"
part "__test_save_stack_3"
     call "free"
     push 4
     call "save_stack"
     copy
     get
     push 4
     sub
     zero "__test_save_stack_4"
     push 225
     call "raise"
part "__test_save_stack_4"
     copy
     push 1
     add
     get
     push 7
     sub
     zero "__test_save_stack_5"
     push 226
     call "raise"
part "__test_save_stack_5"
     call "free"
     zero "__test_save_stack_return"
     push 227
     call "raise"
part "__test_save_stack_return"
     push -1
     push 8
     call "clear"
     back
# def test_load_stack():
#     HEAP[-1] = 1
#     stack.push(0)
#     stack.push(2)
#     stack.push(3)
#     stack.push(5)
#     stack.push(7)
#     stack.push(11)
#     stack.push(13)
#     stack.push(17)
#     stack.push(19)
#     array = save_stack(3)
#     if stack[-1] != 11:
#         raise Exception(228)
#     load_stack(array, 3)
#     if stack.pop() != 19:
#         raise Exception(229)
#     del stack[-1]
#     if stack.pop() != 13:
#         raise Exception(230)
#     array = save_stack(3)
#     load_stack(array, 1)
#     if stack.pop() != 5:
#         raise Exception(231)
#     load_stack(array, 2)
#     if stack.pop() != 11:
#         raise Exception(232)
#     del stack[-1]
#     array = save_stack(2)
#     load_stack(array, 1)
#     del stack[-1]
#     if array[0] != 1:
#         raise Exception(233)
#     load_stack(array, 1)
#     if stack[-2] + stack[-1] != 3:
#         raise Exception(234)
#     clear(-1, 7)
part "test_load_stack"
     push -1
     push 1
     set
     push 0
     push 2
     push 3
     push 5
     push 7
     push 11
     push 13
     push 17
     push 19
     push 3
     call "save_stack"
     copy 1
     push 11
     sub
     zero "__test_load_stack_2"
     push 228
     call "raise"
part "__test_load_stack_2"
     push 3
     call "load_stack"
     push 19
     sub
     zero "__test_load_stack_3"
     push 229
     call "raise"
part "__test_load_stack_3"
     away
     push 13
     sub
     zero "__test_load_stack_4"
     push 230
     call "raise"
part "__test_load_stack_4"
     push 3
     call "save_stack"
     copy
     push 1
     call "load_stack"
     push 5
     sub
     zero "__test_load_stack_5"
     push 231
     call "raise"
part "__test_load_stack_5"
     push 2
     call "load_stack"
     push 11
     sub
     zero "__test_load_stack_6"
     push 232
     call "raise"
part "__test_load_stack_6"
     away
     push 2
     call "save_stack"
     copy
     push 1
     call "load_stack"
     away
     copy
     get
     push 1
     sub
     zero "__test_load_stack_7"
     push 233
     call "raise"
part "__test_load_stack_7"
     push 1
     call "load_stack"
     add
     push 3
     sub
     zero "__test_load_stack_return"
     push 234
     call "raise"
part "__test_load_stack_return"
     push -1
     push 7
     call "clear"
     back
# def test_divmod():
#     a, b = divmod(99, 2)
#     if b != 1:
#         raise Exception(235)
#     if a != 49:
#         raise Exception(236)
#     a, b = divmod(5, 10)
#     if b != 5:
#         raise Exception(237)
#     if a != 0:
#         raise Exception(238)
#     a, b = divmod(27, 3)
#     if b != 0:
#         raise Exception(239)
#     if a != 9:
#         raise Exception(240)
#     HEAP[0] = 0
part "test_divmod"
     push 99
     push 2
     call "divmod"
     push 1
     sub
     zero "__test_divmod_2"
     push 235
     call "raise"
part "__test_divmod_2"
     push 49
     sub
     zero "__test_divmod_3"
     push 236
     call "raise"
part "__test_divmod_3"
     push 5
     push 10
     call "divmod"
     push 5
     sub
     zero "__test_divmod_4"
     push 237
     call "raise"
part "__test_divmod_4"
     zero "__test_divmod_5"
     push 238
     call "raise"
part "__test_divmod_5"
     push 27
     push 3
     call "divmod"
     zero "__test_divmod_6"
     push 239
     call "raise"
part "__test_divmod_6"
     push 9
     sub
     zero "__test_divmod_return"
     push 240
     call "raise"
part "__test_divmod_return"
     push 0
     push 0
     set
     back
# def test_sum_length_array():
#     HEAP[-1] = 1
#     array = malloc(3)
#     array[0] = 2
#     array[1] = 3
#     array[2] = 4
#     if sum_length_array(array) != 7:
#         raise Exception(237)
#     array[1] = 5
#     array[2] = 2
#     if sum_length_array(array) != 7:
#         raise Exception(238)
#     array = realloc(array, 4)
#     array[3] = 3
#     if sum_length_array(array) != 7:
#         raise Exception(239)
#     array[0] = 3
#     if sum_length_array(array) != 10:
#         raise Exception(240)
#     range(array + 1, 1, 4, 1)
#     if sum_length_array(array) != 6:
#         raise Exception(241)
#     range(array + 1, 100, 373, 91)
#     if sum_length_array(array) != 573:
#         raise Exception(242)
#     free(array)
#     clear(-1, 4)
part "test_sum_length_array"
     push -1
     push 1
     set
     push 3
     call "malloc"
     copy
     push 2
     set
     copy
     push 1
     add
     push 3
     set
     copy
     push 2
     add
     push 4
     set
     copy
     call "sum_length_array"
     push 7
     sub
     zero "__test_sum_length_array_2"
     push 237
     call "raise"
part "__test_sum_length_array_2"
     copy
     push 1
     add
     push 5
     set
     copy
     push 2
     add
     push 2
     set
     copy
     call "sum_length_array"
     push 7
     sub
     zero "__test_sum_length_array_3"
     push 238
     call "raise"
part "__test_sum_length_array_3"
     push 4
     call "realloc"
     copy
     push 3
     add
     push 3
     set
     copy
     call "sum_length_array"
     push 7
     sub
     zero "__test_sum_length_array_4"
     push 239
     call "raise"
part "__test_sum_length_array_4"
     copy
     push 3
     set
     copy
     call "sum_length_array"
     push 10
     sub
     zero "__test_sum_length_array_5"
     push 240
     call "raise"
part "__test_sum_length_array_5"
     copy
     push 1
     add
     push 1
     push 4
     push 1
     call "range"
     copy
     call "sum_length_array"
     push 6
     sub
     zero "__test_sum_length_array_6"
     push 241
     call "raise"
part "__test_sum_length_array_6"
     copy
     push 1
     add
     push 100
     push 373
     push 91
     call "range"
     copy
     call "sum_length_array"
     push 573
     sub
     zero "__test_sum_length_array_return"
     push 242
     call "raise"
part "__test_sum_length_array_return"
     call "free"
     push -1
     push 4
     call "clear"
     back
# def test_value_to_array():
#     HEAP[-1] = 1
#     array = value_to_array(7, 2)
#     if array[0] != 3:
#         raise Exception(243)
#     if array[1] != 1:
#         raise Exception(244)
#     if array[2] != 1:
#         raise Exception(245)
#     if array[3] != 1:
#         raise Exception(246)
#     free(array)
#     array = value_to_array(100, 3)
#     if sum_length_array(array) != 4:
#         raise Exception(247)
#     free(array)
#     array = value_to_array(123456789, 7)
#     if sum_length_array(array) != 27:
#         raise Exception(248)
#     free(array)
#     array = value_to_array(123456789, 13)
#     if sum_length_array(array) != 45:
#         raise Exception(249)
#     free(array)
#     array = value_to_array(100000, 5)
#     if sum_length_array(array) != 4:
#         raise Exception(250)
#     free(array)
#     clear(-1, 24)
part "test_value_to_array"
     push -1
     push 1
     set
     push 7
     push 2
     call "value_to_array"
     copy
     get
     push 3
     sub
     zero "__test_value_to_array_2"
     push 243
     call "raise"
part "__test_value_to_array_2"
     copy
     push 1
     add
     get
     push 1
     sub
     zero "__test_value_to_array_3"
     push 244
     call "raise"
part "__test_value_to_array_3"
     copy
     push 2
     add
     get
     push 1
     sub
     zero "__test_value_to_array_4"
     push 245
     call "raise"
part "__test_value_to_array_4"
     copy
     push 3
     add
     get
     push 1
     sub
     zero "__test_value_to_array_5"
     push 246
     call "raise"
part "__test_value_to_array_5"
     call "free"
     push 100
     push 3
     call "value_to_array"
     copy
     call "sum_length_array"
     push 4
     sub
     zero "__test_value_to_array_6"
     push 247
     call "raise"
part "__test_value_to_array_6"
     call "free"
     push 123456789
     push 7
     call "value_to_array"
     copy
     call "sum_length_array"
     push 27
     sub
     zero "__test_value_to_array_7"
     push 248
     call "raise"
part "__test_value_to_array_7"
     call "free"
     push 123456789
     push 13
     call "value_to_array"
     copy
     call "sum_length_array"
     push 45
     sub
     zero "__test_value_to_array_8"
     push 249
     call "raise"
part "__test_value_to_array_8"
     call "free"
     push 100000
     push 5
     call "value_to_array"
     copy
     call "sum_length_array"
     push 4
     sub
     zero "__test_value_to_array_return"
     push 250
     call "raise"
part "__test_value_to_array_return"
     call "free"
     push -1
     push 24
     call "clear"
     back
# def test_array_to_value():
#     HEAP[-1] = 1
#     array = value_to_array(0, 10)
#     if array_to_value(array, 10) != 0:
#         raise Exception(251)
#     free(array)
#     array = value_to_array(1234567890, 13)
#     if array_to_value(array, 13) != 1234567890:
#         raise Exception(252)
#     free(array)
#     array = value_to_array(19850126, 12)
#     if array_to_value(array, 13) != 31824236:
#         raise Exception(253)
#     free(array)
#     array = value_to_array(100, 8)
#     if array_to_value(array, 16) != 324:
#         raise Exception(254)
#     free(array)
#     array = value_to_array(341, 2)
#     if array_to_value(array, 3) != 7381:
#         raise Exception(255)
#     free(array)
#     clear(-1, 23)
part "test_array_to_value"
     push -1
     push 1
     set
     push 0
     push 10
     call "value_to_array"
     copy
     push 10
     call "array_to_value"
     zero "__test_array_to_value_2"
     push 251
     call "raise"
part "__test_array_to_value_2"
     call "free"
     push 1234567890
     push 13
     call "value_to_array"
     copy
     push 13
     call "array_to_value"
     push 1234567890
     sub
     zero "__test_array_to_value_3"
     push 252
     call "raise"
part "__test_array_to_value_3"
     call "free"
     push 19850126
     push 12
     call "value_to_array"
     copy
     push 13
     call "array_to_value"
     push 31824236
     sub
     zero "__test_array_to_value_4"
     push 253
     call "raise"
part "__test_array_to_value_4"
     call "free"
     push 100
     push 8
     call "value_to_array"
     copy
     push 16
     call "array_to_value"
     push 324
     sub
     zero "__test_array_to_value_5"
     push 254
     call "raise"
part "__test_array_to_value_5"
     call "free"
     push 341
     push 2
     call "value_to_array"
     copy
     push 3
     call "array_to_value"
     push 7381
     sub
     zero "__test_array_to_value_return"
     push 255
     call "raise"
part "__test_array_to_value_return"
     call "free"
     push -1
     push 23
     call "clear"
     back
# def test_uint_bits():
#     HEAP[-1] = 1
#     number = left_shift(1, 32)
#     bits = uint_bits(number - 1)
#     if bits[0] != 1:
#         raise Exception(256)
#     if bits[31] != 1:
#         raise Exception(257)
#     free(bits)
#     bits = uint_bits(number)
#     if bits[0] != 0:
#         raise Exception(258)
#     if bits[31] != 0:
#         raise Exception(259)
#     free(bits)
#     clear(-1, 78)
part "test_uint_bits"
     push -1
     push 1
     set
     push 1
     push 32
     call "left_shift"
     copy
     push 1
     sub
     call "uint_bits"
     copy
     get
     push 1
     sub
     zero "__test_uint_bits_2"
     push 256
     call "raise"
part "__test_uint_bits_2"
     copy
     push 31
     add
     get
     push 1
     sub
     zero "__test_uint_bits_3"
     push 257
     call "raise"
part "__test_uint_bits_3"
     call "free"
     call "uint_bits"
     copy
     get
     zero "__test_uint_bits_4"
     push 258
     call "raise"
part "__test_uint_bits_4"
     copy
     push 31
     add
     get
     zero "__test_uint_bits_return"
     push 259
     call "raise"
part "__test_uint_bits_return"
     call "free"
     push -1
     push 78
     call "clear"
     back
# def test_uint_xor():
#     HEAP[-1] = 1
#     if uint_xor(123, 124) != 7:
#         raise Exception(260)
#     if uint_xor(127, 128) != 255:
#         raise Exception(261)
#     if uint_xor(19891229, 19850126) != 92051:
#         raise Exception(262)
#     if uint_xor(3558890251, 3920765046) != 1033010045:
#         raise Exception(263)
#     if uint_xor(2010047493, 4018657910) != 2554936947:
#         raise Exception(264)
#     if uint_xor(83517729861, 159352312248) != 1747467773:
#         raise Exception(265)
#     clear(-1, 109)
part "test_uint_xor"
     push -1
     push 1
     set
     push 123
     push 124
     call "uint_xor"
     push 7
     sub
     zero "__test_uint_xor_2"
     push 260
     call "raise"
part "__test_uint_xor_2"
     push 127
     push 128
     call "uint_xor"
     push 255
     sub
     zero "__test_uint_xor_3"
     push 261
     call "raise"
part "__test_uint_xor_3"
     push 19891229
     push 19850126
     call "uint_xor"
     push 92051
     sub
     zero "__test_uint_xor_4"
     push 262
     call "raise"
part "__test_uint_xor_4"
     push 3558890251
     push 3920765046
     call "uint_xor"
     push 1033010045
     sub
     zero "__test_uint_xor_5"
     push 263
     call "raise"
part "__test_uint_xor_5"
     push 2010047493
     push 4018657910
     call "uint_xor"
     push 2554936947
     sub
     zero "__test_uint_xor_6"
     push 264
     call "raise"
part "__test_uint_xor_6"
     push 83517729861
     push 159352312248
     call "uint_xor"
     push 1747467773
     sub
     zero "__test_uint_xor_return"
     push 265
     call "raise"
part "__test_uint_xor_return"
     push -1
     push 109
     call "clear"
     back
# def test_memory_manager_hash():
#     HEAP[-1] = 1
#     if memory_manager_hash() != 0:
#         raise Exception(266)
#     memory_manager_append_cell(1, 2)
#     if memory_manager_hash() != 2153645760:
#         raise Exception(267)
#     memory_manager_append_cell(3, 5)
#     if memory_manager_hash() != 4048040839:
#         raise Exception(268)
#     memory_manager_append_cell(7, 11)
#     if memory_manager_hash() != 265376592:
#         raise Exception(269)
#     memory_manager_append_cell(1000033, 1000037)
#     if memory_manager_hash() != 880511209:
#         raise Exception(270)
#     clear(-10, 141)
part "test_memory_manager_hash"
     push -1
     push 1
     set
     call "memory_manager_hash"
     zero "__test_memory_manager_hash_2"
     push 266
     call "raise"
part "__test_memory_manager_hash_2"
     push 1
     push 2
     call "memory_manager_append_cell"
     call "memory_manager_hash"
     push 2153645760
     sub
     zero "__test_memory_manager_hash_3"
     push 267
     call "raise"
part "__test_memory_manager_hash_3"
     push 3
     push 5
     call "memory_manager_append_cell"
     call "memory_manager_hash"
     push 4048040839
     sub
     zero "__test_memory_manager_hash_4"
     push 268
     call "raise"
part "__test_memory_manager_hash_4"
     push 7
     push 11
     call "memory_manager_append_cell"
     call "memory_manager_hash"
     push 265376592
     sub
     zero "__test_memory_manager_hash_5"
     push 269
     call "raise"
part "__test_memory_manager_hash_5"
     push 1000033
     push 1000037
     call "memory_manager_append_cell"
     call "memory_manager_hash"
     push 880511209
     sub
     zero "__test_memory_manager_hash_return"
     push 270
     call "raise"
part "__test_memory_manager_hash_return"
     push -10
     push 141
     call "clear"
     back
