warnings = []
warning_messages = warnings
tables = []

def parse_plantuml(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            line = line.replace("\n", "")
            line = line.strip()
            if line != "":
                lines.append(line.strip())
    return lines


def _parse_class_name(line: str) -> str | None:
    remainder = line[5:].strip()
    if not remainder:
        return None

    for sep in ["<<", "{", "(", " "]:
        if sep in remainder:
            remainder = remainder.split(sep)[0]
    remainder = remainder.strip()
    return remainder or None


def _get_uml_bounds(lines):
    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if line.lower() == "@startuml":
            start_idx = i + 1
            break

    for i in range(len(lines) - 1, -1, -1):
        if lines[i].lower() == "@enduml":
            end_idx = i
            break

    return start_idx, end_idx


def validate_uml_entities(lines):
    global tables
    tables.clear()

    start_idx, end_idx = _get_uml_bounds(lines)

    i = start_idx
    while i < end_idx:
        line = lines[i]

        if line.lower().startswith("class "):
            class_name = _parse_class_name(line)
            if not class_name:
                warnings.append(
                    f"Warning (line {i+1}): 'class' keyword must be followed by a name."
                )
                i += 1
                continue

            opened = False
            brace_balance = 0
            first_open_idx = None
            end_block_idx = None
            error_in_block = False

            for j in range(i, end_idx):
                cur_line = lines[j]
                opens = cur_line.count("{")
                closes = cur_line.count("}")

                if not opened and opens > 0:
                    opened = True
                    first_open_idx = j

                brace_balance += opens
                brace_balance -= closes

                if brace_balance < 0:
                    warnings.append(
                        f"Warning (line {j+1}): '}}' appears before matching '{{' "
                        f"in class '{class_name}'."
                    )
                    error_in_block = True
                    break

                if opened and brace_balance == 0:
                    end_block_idx = j
                    break

            if not opened:
                warnings.append(
                    f"Warning (line {i+1}): class '{class_name}' has no opening '{{'."
                )
                i += 1
                continue

            if not error_in_block and end_block_idx is None:
                warnings.append(
                    f"Warning (line {i+1}): class '{class_name}' has an unmatched '{{'."
                )
                i += 1
                continue

            if error_in_block:
                i = j + 1
                continue

            attributes = []

            if first_open_idx == end_block_idx:
                body_line = lines[first_open_idx]
                open_pos = body_line.find("{")
                close_pos = body_line.rfind("}")
                inner = body_line[open_pos + 1 : close_pos].strip()
                if inner:
                    attributes.append(inner)
            else:
                for k in range(first_open_idx + 1, end_block_idx):
                    attr_line = lines[k].strip()
                    if attr_line and attr_line not in ("{", "}"):
                        attributes.append(attr_line)

            tables.append(
                {
                    "name": class_name,
                    "attributes": attributes,
                }
            )

            i = end_block_idx + 1
            continue

        if "{" in line or "}" in line:
            warnings.append(
                f"Warning (line {i+1}): brace found outside of a class declaration: '{line}'"
            )

        i += 1


def get_uml_entities(lines):
    validate_uml_entities(lines)
    return tables


def validate_start(lines):
    if "@startuml" not in [l.lower() for l in lines]:
        warnings.append("Warning: '@startuml' is missing")
    elif lines[0].lower() != "@startuml":
        warnings.append("Warning: first line must be '@startuml'")


def validate_end(lines):
    if "@enduml" not in [l.lower() for l in lines]:
        warnings.append("Warning: '@enduml' is missing")
    elif lines[-1].lower() != "@enduml":
        warnings.append("Warning: last line must be '@enduml'")


def validate_design(lines):
    validate_start(lines)
    validate_end(lines)
    validate_uml_entities(lines)
    print_warning_messages()


def _parse_relationship_line(line: str):
    operators = ["<|--", "-->", "<--", "o--", "*--", "--", "..>", ".."]
    for op in operators:
        if op in line:
            left, right = line.split(op, 1)
            left = left.strip()
            right = right.strip()
            if not left or not right:
                return None

            left_name = left.split()[0]
            right_name = right.split()[0]
            return left_name, right_name
    return None


def parse_relationships(lines):
    start_idx, end_idx = _get_uml_bounds(lines)
    rels = []

    for i in range(start_idx, end_idx):
        line = lines[i]
        if line.lower().startswith("class "):
            continue
        if line.startswith("'"):
            continue

        parsed = _parse_relationship_line(line)
        if parsed is not None:
            rels.append(parsed)

    return rels


def compare_uml_models(correct_classes, correct_rels, user_classes, user_rels):
    correct_class_names = {c["name"] for c in correct_classes}
    user_class_names = {c["name"] for c in user_classes}

    missing_classes = sorted(correct_class_names - user_class_names)
    extra_classes = sorted(user_class_names - correct_class_names)

    for name in missing_classes:
        warnings.append(f"Warning: class '{name}' is missing in user UML.")
    for name in extra_classes:
        warnings.append(f"Warning: extra class '{name}' found in user UML.")

    correct_by_name = {c["name"]: c for c in correct_classes}
    user_by_name = {c["name"]: c for c in user_classes}

    for name in sorted(correct_class_names & user_class_names):
        correct_attrs = set(a.strip() for a in correct_by_name[name]["attributes"])
        user_attrs = set(a.strip() for a in user_by_name[name]["attributes"])

        missing_attrs = sorted(correct_attrs - user_attrs)
        extra_attrs = sorted(user_attrs - correct_attrs)

        for attr in missing_attrs:
            warnings.append(
                f"Warning: in class '{name}', attribute '{attr}' is missing in user UML."
            )
        for attr in extra_attrs:
            warnings.append(
                f"Warning: in class '{name}', extra attribute '{attr}' found in user UML."
            )

    def _canonical_rel_set(rels):
        canon = set()
        for a, b in rels:
            if a and b:
                canon.add(tuple(sorted((a, b))))
        return canon

    correct_rel_set = _canonical_rel_set(correct_rels)
    user_rel_set = _canonical_rel_set(user_rels)

    missing_rels = sorted(correct_rel_set - user_rel_set)
    extra_rels = sorted(user_rel_set - correct_rel_set)

    for a, b in missing_rels:
        warnings.append(
            f"Warning: relationship '{a} -- {b}' is missing in user UML."
        )
    for a, b in extra_rels:
        warnings.append(
            f"Warning: extra relationship '{a} -- {b}' found in user UML."
        )


def print_warning_messages(count):
    print_string = ""
    warning_count = len(warnings)
    for warning_message in warnings:
        print_string += f"{warning_message}\n"
    if print_string:
        print(print_string)
    else:
        print("No warnings found.")
    similarity_score = (((count - warning_count) / count) * 100)
    similarity_score = round(similarity_score, 2)
    print("Similarity Score: " + str(similarity_score) + "%")

def build_uml_model_from_file(filename):
    lines = parse_plantuml(filename)
    count = len(lines)
    validate_start(lines)
    validate_end(lines)
    validate_uml_entities(lines)
    classes = [
        {"name": t["name"], "attributes": list(t["attributes"])}
        for t in tables
    ]
    relationships = parse_relationships(lines)
    return classes, relationships, count


def validate_file(file_name):
    warnings.clear()
    tables.clear()
    correct_classes, correct_rels, count = build_uml_model_from_file("plantuml_export.txt")
    user_classes, user_rels, count2 = build_uml_model_from_file(file_name)
    compare_uml_models(correct_classes, correct_rels, user_classes, user_rels)
    print_warning_messages(count2)
