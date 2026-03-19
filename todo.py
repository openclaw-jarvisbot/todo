#!/usr/bin/env python3
"""
Simple Todo CLI - A lightweight todo manager
Usage: python3 todo.py <command> [args]
"""

import json
import os
import sys
import uuid
from datetime import datetime, timezone

# Store todos.json in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TODO_FILE = os.path.join(SCRIPT_DIR, "todos.json")


def load_todos():
    """Load todos from JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_todos(todos):
    """Save todos to JSON file."""
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)


def add_todo(content, priority=5):
    """Add a new todo."""
    todos = load_todos()
    todo = {
        "id": str(uuid.uuid4())[:8],  # Short UUID for readability
        "content": content,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "priority": priority
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Added: [{todo['id']}] {content} (priority: {priority})")


def list_todos(min_priority=1, limit=None):
    """List todos sorted by priority (desc) then created_at (desc)."""
    todos = load_todos()
    
    # Filter by min_priority
    filtered = [t for t in todos if t["priority"] >= min_priority]
    
    # Sort by priority (desc), then created_at (desc)
    filtered.sort(key=lambda x: (-x["priority"], x["created_at"]))
    
    if limit:
        filtered = filtered[:limit]
    
    if not filtered:
        print("No todos found.")
        return
    
    for t in filtered:
        print(f"[{t['id']}] p{t['priority']} | {t['content']}")


def update_todo(todo_id, priority):
    """Update a todo's priority."""
    todos = load_todos()
    found = False
    for t in todos:
        if t["id"] == todo_id:
            t["priority"] = priority
            found = True
            break
    
    if found:
        save_todos(todos)
        print(f"Updated todo {todo_id} priority to {priority}")
    else:
        print(f"Todo {todo_id} not found.")


def delete_todo(todo_id):
    """Delete a todo by ID."""
    todos = load_todos()
    original_len = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]
    
    if len(todos) < original_len:
        save_todos(todos)
        print(f"Deleted todo {todo_id}")
    else:
        print(f"Todo {todo_id} not found.")


def show_important(limit=5):
    """Show important todos (highest priority first)."""
    list_todos(min_priority=7, limit=limit)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 todo.py <command> [args]")
        print("")
        print("Commands:")
        print('  add "todo text" --priority 1-10    Add a new todo (default priority 5)')
        print("  list [--min-priority N] [--limit N]  List todos")
        print("  update <id> --priority N             Update todo priority")
        print("  delete <id>                           Delete a todo")
        print("  important [N]                         Show top priority todos")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        # Find the todo text (in quotes) and optional --priority
        content = None
        priority = 5
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i].startswith("--priority"):
                if "=" in sys.argv[i]:
                    priority = int(sys.argv[i].split("=")[1])
                elif i + 1 < len(sys.argv):
                    priority = int(sys.argv[i + 1])
                    i += 1
            else:
                content = sys.argv[i]
            i += 1
        
        if not content:
            print("Error: Please provide todo content")
            sys.exit(1)
        
        # Remove quotes if present
        content = content.strip('"').strip("'")
        add_todo(content, priority)
    
    elif cmd == "list":
        min_priority = 1
        limit = None
        
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--min-priority" and i + 1 < len(sys.argv):
                min_priority = int(sys.argv[i + 1])
                i += 1
            elif sys.argv[i].startswith("--min-priority="):
                min_priority = int(sys.argv[i].split("=")[1])
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 1
            elif sys.argv[i].startswith("--limit="):
                limit = int(sys.argv[i].split("=")[1])
            i += 1
        
        list_todos(min_priority, limit)
    
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Usage: python3 todo.py update <id> --priority N")
            sys.exit(1)
        
        todo_id = sys.argv[2]
        
        # Handle --priority N or --priority=N
        priority_arg = sys.argv[3]
        if priority_arg.startswith("--priority="):
            priority = int(priority_arg.split("=")[1])
        elif priority_arg == "--priority" and len(sys.argv) > 4:
            priority = int(sys.argv[4])
        else:
            print("Usage: python3 todo.py update <id> --priority N")
            sys.exit(1)
        
        update_todo(todo_id, priority)
    
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("Usage: python3 todo.py delete <id>")
            sys.exit(1)
        
        delete_todo(sys.argv[2])
    
    elif cmd == "important" or cmd == "top":
        limit = 5
        if len(sys.argv) > 2:
            try:
                limit = int(sys.argv[2])
            except ValueError:
                pass
        show_important(limit)
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
