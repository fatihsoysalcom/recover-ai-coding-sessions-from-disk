import re
import os
import tempfile

def simulate_disk_data():
    """
    Simulates raw data found on a disk, containing fragmented AI coding sessions.
    This data would typically be recovered from a disk image or raw sector data.
    """
    data = """
    Some random system logs and unrelated data...
    --- CLAUDE SESSION START ---
    User: How do I implement a quicksort algorithm in Python?
    Claude: Here's a basic implementation of quicksort:
    def quicksort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quicksort(left) + middle + quicksort(right)
    print(quicksort([3,6,8,10,1,2,1]))
    --- CLAUDE SESSION END ---
    More junk data...
    --- CODEX SESSION START ---
    User: Write a simple Flask endpoint for user registration.
    Codex: Sure, here's an example:
    from flask import Flask, request, jsonify
    app = Flask(__name__)
    @app.route('/register', methods=['POST'])
    def register_user():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        # In a real app, you'd hash the password and save to a DB
        print(f"User {username} registered successfully.")
        return jsonify({'message': 'User registered', 'username': username}), 201
    if __name__ == '__main__':
        app.run(debug=True)
    --- CODEX SESSION END ---
    Even more unrelated binary data or corrupted sectors...
    --- CLAUDE SESSION START ---
    User: Can you refactor the quicksort to be in-place?
    Claude: An in-place quicksort is a bit more complex. Here's a common approach:
    def partition(arr, low, high):
        i = (low - 1)
        pivot = arr[high]
        for j in range(low, high):
            if arr[j] <= pivot:
                i = i + 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return (i + 1)
    def quicksort_inplace(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort_inplace(arr, low, pi - 1)
            quicksort_inplace(arr, pi + 1, high)
    my_arr = [10, 7, 8, 9, 1, 5]
    n = len(my_arr)
    quicksort_inplace(my_arr, 0, n - 1)
    print("Sorted array is:", my_arr)
    --- CLAUDE SESSION END ---
    Final footer data.
    """
    return data

def recover_sessions(disk_data_path):
    """
    Reads simulated disk data and extracts AI coding sessions based on predefined markers.
    This simulates the 'recovery' process by parsing raw data for known patterns.
    """
    recovered_sessions = []
    # Regex to find sessions: looks for a START marker, captures everything non-greedily,
    # and ends with an END marker. (?s) makes '.' match newlines.
    claude_pattern = re.compile(r'(?s)--- CLAUDE SESSION START ---\n(.*?)\n--- CLAUDE SESSION END ---')
    codex_pattern = re.compile(r'(?s)--- CODEX SESSION START ---\n(.*?)\n--- CODEX SESSION END ---')

    with open(disk_data_path, 'r', encoding='utf-8') as f:
        content = f.read()

        # Find all Claude sessions by matching the defined pattern
        for match in claude_pattern.finditer(content):
            session_content = match.group(1).strip()
            recovered_sessions.append({'type': 'Claude', 'content': session_content})

        # Find all Codex sessions by matching the defined pattern
        for match in codex_pattern.finditer(content):
            session_content = match.group(1).strip()
            recovered_sessions.append({'type': 'Codex', 'content': session_content})

    return recovered_sessions

if __name__ == "__main__":
    # 1. Simulate "disk" data and write it to a temporary file
    simulated_data = simulate_disk_data()
    temp_file_path = None
    try:
        # Create a temporary file to represent raw data on disk
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_f:
            temp_f.write(simulated_data)
            temp_file_path = temp_f.name
        print(f"Simulated disk data written to: {temp_file_path}\n")

        # 2. Recover sessions from the simulated disk data
        print("Attempting to recover AI coding sessions...\n")
        sessions = recover_sessions(temp_file_path)

        # 3. Display recovered sessions
        if sessions:
            print(f"Successfully recovered {len(sessions)} AI coding sessions:\n")
            # Sort sessions by type for consistent output (optional)
            sessions.sort(key=lambda x: x['type'])
            for i, session in enumerate(sessions):
                print(f"--- RECOVERED {session['type']} SESSION {i+1} ---")
                print(session['content'])
                print(f"--- END OF RECOVERED {session['type']} SESSION {i+1} ---\n")
        else:
            print("No AI coding sessions found or recovered.")

    finally:
        # Clean up the temporary file to avoid leaving artifacts
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")
