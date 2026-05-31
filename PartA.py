"""
Course Code: CPT 212 - Design & Analysis of Algorithms
Assignment 2 - Part A: Boyer-Moore Algorithm Implementation
"""

def preprocess_bad_character(pattern):
    """
    Creates a lookup table of each character's last occurrence in the pattern.
    Time Complexity: O(m), Space Complexity: O(σ) where m = pattern length, σ = alphabet size
    """
    bad_char_table = {}
    m = len(pattern)
    
    # Store the rightmost position of each character for fast lookup
    for i in range(m):
        bad_char_table[pattern[i]] = i
        
    return bad_char_table


def preprocess_good_suffix(pattern):
    """
    Computes border positions and shift table for the good suffix rule.
    Time Complexity: O(m), Space Complexity: O(m) where m = pattern length
    """
    m = len(pattern)
    
    # bpos[i]: starting index of border for suffix at index i
    bpos = [0] * (m + 1)
    # shift_table[i]: shift distance if mismatch occurs at pattern index i
    shift_table = [0] * (m + 1)
    
    # Phase 1: Calculate borders for suffixes
    i = m
    j = m + 1
    bpos[i] = j
    
    while i > 0:
        while j <= m and pattern[i - 1] != pattern[j - 1]:
            if shift_table[j] == 0:
                shift_table[j] = j - i
            j = bpos[j]
        i -= 1
        j -= 1
        bpos[i] = j
        
    # Phase 2: Complete shift table for remaining positions
    j = bpos[0]
    for i in range(m + 1):
        if shift_table[i] == 0:
            shift_table[i] = j
        if i == j:
            j = bpos[j]
            
    return bpos, shift_table


def boyer_moore_search(text, pattern):
    """
    Boyer-Moore string matching: compares from right to left using bad character and good suffix rules.
    Time Complexity: O(n/m) best case; O(nm) worst case. Space Complexity: O(m + σ)
    """
    n = len(text)
    m = len(pattern)
    
    bad_char_table = preprocess_bad_character(pattern)
    bpos, good_suffix_table = preprocess_good_suffix(pattern)
    
    s = 0  # alignment pointer
    match_indices = []
    
    while s <= (n - m):
        # Compare pattern from right to left
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
            
        if j < 0:
            # Match found
            match_indices.append(s)
            s += good_suffix_table[0]
        else:
            # Mismatch: use max of bad character and good suffix shifts
            mismatched_char = text[s + j]
            last_occ = bad_char_table.get(mismatched_char, -1)
            bad_char_shift = j - last_occ
            good_suffix_shift = good_suffix_table[j + 1]
            s += max(bad_char_shift, good_suffix_shift)
        
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