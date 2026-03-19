# Todo CLI

A lightweight todo manager for the command line.

## Usage

```bash
python3 todo.py <command> [args]
```

## Commands

- `add "todo text" --priority 1-10` — Add a new todo (default priority 5)
- `list [--min-priority N] [--limit N]` — List todos
- `update <id> --priority N` — Update todo priority
- `delete <id>` — Delete a todo
- `important [N]` — Show top priority todos (default: top 5)

## Notes

- Todos are stored in `todos.json` (not committed to git)
- IDs are short UUIDs (first 8 characters)
- Sorting: priority (desc), then created_at (desc)
