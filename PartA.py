"""
Course Code: CPT 212 - Design & Analysis of Algorithms
Assignment 2 - Part A: Boyer-Moore Algorithm Implementation
"""

def preprocess_bad_character(pattern):
    """
    Phase 1a: Preprocessing Bad Character Rule
    Creates a lookup mechanism recording the last occurrence index of each character.
    
    Algorithm Logic:
    - Iterate through the pattern from left to right
    - Store the index of each character (overwrites if character appears multiple times)
    - This creates a fast lookup table for character positions
    
    Time Complexity: O(m + σ) where m = pattern length, σ = alphabet size
    Space Complexity: O(σ)
    
    Args:
        pattern (str): The pattern string to preprocess
        
    Returns:
        dict: Dictionary mapping each character to its last occurrence index in pattern
        
    Example:
        >>> preprocess_bad_character("PATTERN")
        {'P': 0, 'A': 2, 'T': 3, 'E': 5, 'R': 4, 'N': 6}
    """
    bad_char_table = {}
    m = len(pattern)
    
    # Build the bad character table: for each character, store its rightmost position
    # If a character appears multiple times, only the last (rightmost) index is stored
    # This allows fast lookup when mismatch occurs
    for i in range(m):
        bad_char_table[pattern[i]] = i
        
    return bad_char_table


def preprocess_good_suffix(pattern):
    """
    Phase 1b: Preprocessing Good Suffix Rule
    Constructs the shift tables by processing structural properties of suffixes.
    This is the most complex part of Boyer-Moore, computing optimal shifts for mismatches.
    
    Algorithm Logic:
    - Case 1: Finds borders (suffix that also appears as prefix)
    - Case 2: For suffixes without full match, finds largest border
    - Case 3: For remaining positions, uses a valid prefix for alignment
    
    The algorithm uses two arrays:
    - bpos[i]: Starting position of the border for suffix starting at position i
    - shift_table[i]: How much to shift if mismatch occurs at position i
    
    Time Complexity: O(m) where m = pattern length
    Space Complexity: O(m)
    
    Args:
        pattern (str): The pattern string to preprocess
        
    Returns:
        tuple: (bpos, shift_table) where bpos stores border positions and shift_table stores shifts
        
    Example:
        >>> preprocess_good_suffix("ABAB")
        ([4, 3, 2, 1, 0], [2, 1, 1, 1, 4])
    """
    m = len(pattern)
    
    # bpos[i] stores the starting index of the border for the suffix beginning at index i
    # A "border" is a substring that is both a suffix and prefix of the pattern substring
    bpos = [0] * (m + 1)
    
    # shift_table[i] stores the shift distance if a mismatch occurs at pattern index i
    # shift_table[0] is used when a complete match is found
    shift_table = [0] * (m + 1)
    
    # ---- Phase 1: Calculate Borders (Case 1: Internal Repetitions) ----
    # This phase identifies where suffixes match internal substrings
    # Uses a sliding window approach to find borders efficiently
    i = m
    j = m + 1
    bpos[i] = j
    
    # Iterate backwards through the pattern to find borders for each suffix
    while i > 0:
        # When characters don't match, move j to find a potential border match
        # bpos[j] represents the next candidate position for border alignment
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            # First time this shift position is set, record the shift distance
            if shift_table[j] == 0:
                shift_table[j] = j - i
            # Move to next candidate border position
            j = bpos[j]
        # Move both pointers left for next iteration
        i -= 1
        j -= 1
        bpos[i] = j
        
    # ---- Phase 2: Complete Shift Table (Case 2 & 3: Prefix Matching & Default Shifts) ----
    # Case 2: For each unset position, find the largest valid prefix border
    # Case 3: Use a valid prefix as fallback when no better shift exists
    j = bpos[0]
    for i in range(m + 1):
        # If no shift has been assigned for this position, use prefix border distance
        if shift_table[i] == 0:
            shift_table[i] = j
        # After processing, update j to next valid prefix if we just processed a border position
        if i == j:
            j = bpos[j]
            
    return bpos, shift_table


def boyer_moore_search(text, pattern):
    """
    Phase 2: Search Phase - Main Boyer-Moore String Matching Algorithm
    Scans the text using both precomputed heuristics to skip blocks of data aggressively.
    
    Algorithm Logic:
    1. Preprocess pattern using both Bad Character and Good Suffix rules
    2. Initialize alignment pointer at pattern length (right-aligned)
    3. For each alignment:
       a) Compare pattern characters from RIGHT to LEFT (key difference from naive search)
       b) If complete match found: record match index, apply good suffix shift
       c) If mismatch found: calculate max(bad_char_shift, good_suffix_shift) and apply
    4. Continue until pattern alignment goes past text end
    
    Advantages Over Naive Algorithm:
    - Right-to-left comparison allows larger shifts based on mismatches
    - Bad character rule: skip based on non-matching character
    - Good suffix rule: skip based on matched suffix pattern
    - Best case: O(n/m) - only looks at n/m text characters
    - Worst case: O(nm) - but rare in practice
    
    Time Complexity: O(n + m + σ) average case; O(nm) worst case where σ = alphabet size
    Space Complexity: O(m + σ)
    
    Args:
        text (str): The text to search in
        pattern (str): The pattern to find
        
    Returns:
        list: Indices where pattern matches occur in text (empty list if no matches)
        
    Example:
        >>> boyer_moore_search("ABAWPGDA", "AWP")
        [2]
    """
    n = len(text)
    m = len(pattern)
    
    # Run the Preprocessing Phase to compute shift tables
    bad_char_table = preprocess_bad_character(pattern)
    bpos, good_suffix_table = preprocess_good_suffix(pattern)
    
    # Initialize alignment pointer (position where pattern starts in text)
    s = 0 
    # Store all match indices found during search
    match_indices = []
    # Track iterations for detailed output
    loop_count = 1
    
    # Initialize alignment pointer (position where pattern starts in text)
    s = 0 
    # Store all match indices found during search
    match_indices = []
    
    while s <= (n - m):
        # KEY INSIGHT: Compare pattern characters from RIGHT to LEFT
        # This allows us to make larger jumps when mismatches occur
        j = m - 1
        
        # Comparison loop: start from rightmost character of pattern
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        # Check if complete pattern match was found (j == -1 after comparison)
        if j < 0:
            # Perfect match found at position s
            match_indices.append(s)
            
            # Calculate shift for potential overlapping matches using good suffix rule
            s += good_suffix_table[0]
        else:
            # Mismatch occurred at pattern position j
            # The mismatched character in text is at position s + j
            mismatched_char = text[s + j]
            
            # Calculate shift using Bad Character Rule
            # If character not in pattern, last_occ = -1, shift = j - (-1) = j + 1
            last_occ = bad_char_table.get(mismatched_char, -1)
            bad_char_shift = j - last_occ
            
            # Calculate shift using Good Suffix Rule
            # Uses precomputed table for position j + 1
            good_suffix_shift = good_suffix_table[j + 1]
            
            # Boyer-Moore strategy: take MAXIMUM shift from both rules
            # This ensures we never miss a potential match while maximizing progress
            actual_shift = max(bad_char_shift, good_suffix_shift)
            
            # Apply the shift to new alignment position
            s += actual_shift
        
    return match_indices


def display_bad_character_table(pattern, bad_char_table):
    """
    Displays the Bad Character Rule preprocessing table in a formatted table.
    
    Args:
        pattern (str): The pattern string
        bad_char_table (dict): The preprocessed bad character table
    """
    print("\nBAD CHARACTER RULE TABLE")
    print("┌────────────┬───────────────────────┐")
    print("│ Character  │ Last Occurrence Index │")
    print("├────────────┼───────────────────────┤")
    
    # Get sorted characters for consistent display
    characters = sorted(bad_char_table.keys())
    
    # Display each character and its last occurrence
    for char in characters:
        index = bad_char_table[char]
        print(f"│ {char:^10} │ {index:^20}  │")
    
    print("└────────────┴───────────────────────┘")


def display_good_suffix_table(pattern, bpos, good_suffix_table):
    """
    Displays the Good Suffix Rule preprocessing table showing Index, Bpos, and Shift.
    
    Args:
        pattern (str): The pattern string
        bpos (list): The border position array
        good_suffix_table (list): The preprocessed good suffix table
    """
    print("\nGOOD SUFFIX RULE TABLE")
    print("┌──────────┬─────────────────────┬──────────┐")
    print("│ Index    │ Border Position     │ Shift    │")
    print("├──────────┼─────────────────────┼──────────┤")
    
    m = len(pattern)
    
    # Display each position with its bpos and shift values
    for i in range(len(good_suffix_table)):
        print(f"│ {i:^8} │ {bpos[i]:^8}            │ {good_suffix_table[i]:^8} │")
    
    print("└──────────┴─────────────────────┴──────────┘")


def interactive_boyer_moore():
    """
    Interactive Boyer-Moore Algorithm Interface
    Allows user to input text and pattern, displays preprocessing tables and search results.
    """
    print("\n═════════════════════════════════════════════════")
    print(" BOYER-MOORE STRING MATCHING - PREPROCESSING    ")
    print("═════════════════════════════════════════════════")
    
    # Get user input
    text = input("\nEnter the text to search in: ").strip()
    pattern = input("Enter the pattern you want to find: ").strip()
    
    # Validate input
    if not text or not pattern:
        print("\n❌ Error: Text and pattern cannot be empty!")
        return
    
    if len(pattern) > len(text):
        print("\n❌ Error: Pattern length cannot exceed text length!")
        return
    
    # Run preprocessing
    bad_char_table = preprocess_bad_character(pattern)
    bpos, good_suffix_table = preprocess_good_suffix(pattern)
    
    # Display preprocessing tables
    display_bad_character_table(pattern, bad_char_table)
    display_good_suffix_table(pattern, bpos, good_suffix_table)
    
    # Run the search
    results = boyer_moore_search(text, pattern)
    
    # Display search results
    print()
    if results:
        for idx in results:
            print(f"Pattern is found in index {idx} of the text")
    else:
        print("No match pattern found")
    print()


# --- Execution Sandbox ---
if __name__ == "__main__":
    try:
        interactive_boyer_moore()
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("\nPlease try again with valid input.")