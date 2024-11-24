
import copy
from tabulate import tabulate
from itertools import zip_longest

def firstfit(block, proc):
    allocated_blocks = []  # Blocks allocated
    unallocated_processes = []  # Processes not allocated
    allocated_processes = []  # Processes allocated
    remaining_block_sizes = copy.deepcopy(block)  # Copy of block list
    allocated_indices = set()  # Track allocated block indices to avoid duplicates

    for p in proc:
        fit = False
        for i in range(len(remaining_block_sizes)):
            if remaining_block_sizes[i] >= p and i not in allocated_indices:
                allocated_blocks.append(block[i])  # Record original block size only once
                remaining_block_sizes[i] -= p  # Update block size after allocation
                allocated_indices.add(i)  # Mark block as allocated
                allocated_processes.append(p)  # Record process allocated
                fit = True
                break
        if not fit:
            unallocated_processes.append(p)  # Process not allocated

    return allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes


def bestfit(block, proc):
    sorted_blocks = copy.deepcopy(block)
    sorted_blocks.sort()  # Sort blocks for best fit
    allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes = firstfit(sorted_blocks, proc)
    return allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes


def worstfit(block, proc):
    sorted_blocks = copy.deepcopy(block)
    sorted_blocks.sort(reverse=True)  # Sort blocks for worst fit
    allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes = firstfit(sorted_blocks, proc)
    return allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes


def nextfit(block, proc):
    allocated_blocks = []  # Blocks allocated
    unallocated_processes = []  # Processes not allocated
    allocated_processes = []  # Processes allocated
    remaining_block_sizes = copy.deepcopy(block)  # Copy of block list
    last_allocated_index = 0  # Start from the first block
    used_blocks = set()  # To track blocks that have already been allocated

    for p in proc:
        fit = False
        for _ in range(len(remaining_block_sizes)):  # Loop through all blocks circularly
            if last_allocated_index not in used_blocks and remaining_block_sizes[last_allocated_index] >= p:
                allocated_blocks.append(block[last_allocated_index])  # Record original block size
                remaining_block_sizes[last_allocated_index] -= p  # Update block size after allocation
                allocated_processes.append(p)  # Record process allocated
                used_blocks.add(last_allocated_index)  # Mark block as reserved
                fit = True
                break
            last_allocated_index = (last_allocated_index + 1) % len(remaining_block_sizes)  # Move to next block
        if not fit:
            unallocated_processes.append(p)  # Process not allocated

    return allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes



def pb():
    block = []
    n = int(input("\nEnter number of blocks: "))
    print("\nEnter block sizes: ")
    for i in range(0, n):
        e = int(input())
        block.append(e)

    proc = []
    n = int(input("\nEnter number of processes: "))
    print("\nEnter process sizes: ")
    for i in range(0, n):
        e = int(input())
        proc.append(e)
    return block, proc


def display_results(method, allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes):
    # Align all rows to the same length for proper tabulation
    max_length = max(len(remaining_block_sizes), len(allocated_blocks), len(allocated_processes), len(unallocated_processes))
    data = list(
        zip_longest(
            ["Blocks allocated"] + allocated_blocks,
            ["Processes allocated"] + allocated_processes,
            ["Processes not allocated"] + unallocated_processes,
            fillvalue=""
        )
    )
    print(tabulate(data, headers=[method], tablefmt="fancy_grid"))


# Main Program
n = True
while n:
    print("\nFor first fit press 1 \nFor best fit press 2 \nFor worst fit press 3 \nFor next fit press 4 \nTo quit press 0 ")
    x = int(input())

    match x:
        case 1:
            block, proc = pb()
            allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes = firstfit(block, proc)
            display_results("First fit method", allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes)
        case 2:
            block, proc = pb()
            allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes = bestfit(block, proc)
            display_results("Best fit method", allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes)
        case 3:
            block, proc = pb()
            allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes = worstfit(block, proc)
            display_results("Worst fit method", allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes)
        case 4:
            block, proc = pb()
            allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes = nextfit(block, proc)
            display_results("Next fit method", allocated_blocks, unallocated_processes, allocated_processes, remaining_block_sizes)
        case 0:
            print("\nThank you! Bye")
            n = False
        case _:
            print("\nPlease enter a valid value for x\n")

exit()

