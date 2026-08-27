from pathlib import Path
import re

source_file = Path("sparql_queries_20260616.txt")
output_dir = Path("sparql")

output_dir.mkdir(exist_ok=True)

with source_file.open(encoding="utf-8") as f:
    lines = f.readlines()

current_name = None
current_query = []

for line in lines:
    line = line.rstrip("\n")

    # Separator line
    if line.startswith("="):
        if current_name:
            safe_name = re.sub(r'[\\/:*?"<>|()]', '', current_name)
            safe_name = re.sub(r'\s+', '_', safe_name)

            output_file = output_dir / f"{safe_name}.rq"

            with output_file.open("w", encoding="utf-8") as out:
                out.write("\n".join(current_query).strip() + "\n")

            print(f"Created: {output_file}")

            current_name = None
            current_query = []

        continue

    # First non-empty line becomes query name
    if current_name is None and line.strip():
        current_name = line.strip()
        continue

    # Query content
    if current_name:
        current_query.append(line)

# Save last query
if current_name:
    safe_name = re.sub(r'[\\/:*?"<>|()]', '', current_name)
    safe_name = re.sub(r'\s+', '_', safe_name)

    output_file = output_dir / f"{safe_name}.rq"

    with output_file.open("w", encoding="utf-8") as out:
        out.write("\n".join(current_query).strip() + "\n")

    print(f"Created: {output_file}")

print("Done.")