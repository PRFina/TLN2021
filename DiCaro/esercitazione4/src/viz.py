import numpy as np
import matplotlib.pyplot as plt
import src.data_manager as dm

def block_similarity_plot(ax, document, valleys, similarities):

    x = np.arange(len(similarities))

    ax.plot(x, similarities, "-o") # main curve
    ax.plot(valleys, similarities[valleys], "X") # highlights valleys

    ax.set_xticks(x)
    [ax.axvline(breakpt, linestyle='--', alpha=0.7) for breakpt in valleys] # highlights valleys

    title = document.title.split(".")[0] # heuristic for good title
    ax.set(xlabel = "block Gap",
           ylabel = "block Similarity",
           title = f'Block Similarity  Plot of doc: "{title} ..."')
           

def valleys_to_breakpoints(valleys, blocks):
    chunks=[]

    # split blocks spans by founded valleys
    for split in np.array_split(blocks, valleys):
        # transofrm blocks span into a flat list of chunks
        for block in split:
            chunks.extend(block)
        # keep track of valleys but at chunks level
        chunks.append(dm.Document.BLOCK_SEPARATOR)
    chunks = chunks[0:-1] # remove last separator since is not an actual breakpoints
    
    # Search only for breakpoints
    sep_pos = [i for i,chunk in enumerate(chunks) 
                    if chunk == dm.Document.BLOCK_SEPARATOR]
    # crate breakpoints position info pairs   
    breakpoints_pos = [(pos-1, pos) for pos in sep_pos]

    return breakpoints_pos, chunks

def block_span_plot(ax, document, true_breakpoints, system_breakpoints):
    # layout
    true_center = 0.7
    system_center = 0.3
    center_offset = 0.05
    bar_width = 0.12

    # colors
    true_color = '#61b04c'
    system_color = '#4c72b0'

    # ticks
    ax.set_yticks([true_center, system_center])
    ax.set_yticklabels(["True", "System"])
    ax.set_xticks(np.arange(1,len(document.get_chunks()) + 1, step=9))
    
    # labels
    title = document.title.split(".")[0] # heuristic for good title
    ax.set(xlabel = "# Chunks",
           ylabel = "Blocks",
           title = f'Block Span Plot Plot of doc: "{title} ..."')

    n_chunks = np.arange(1, len(document.get_chunks()) + 1)

    true_blocks = np.array_split(n_chunks, true_breakpoints)
    system_blocks = np.array_split(n_chunks, system_breakpoints)

    # true blocks spans
    [ax.axvspan(block[0], block[-1]+0.5,
                true_center-center_offset, 
                true_center+bar_width-center_offset,
                color=true_color) for block in true_blocks]

    # true blocks spans
    [ax.axvspan(block[0], block[-1]+0.5,
                system_center-center_offset,
                system_center+bar_width-center_offset,
                color=system_color) for block in system_blocks if len(block) > 0]

    # true blocks projection lines
    [ax.axvline(block[0], 
                true_center-(true_center-system_center)-center_offset, 
                true_center,
                linestyle='--', color='#a7b04c', alpha=0.5) for block in true_blocks]

 
