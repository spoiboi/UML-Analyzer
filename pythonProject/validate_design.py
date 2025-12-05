warning_messages = []
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

def get_uml_entities(lines):
    index = 0
    for line in lines:
        index += 1



def validate_start(lines):
    if "@startuml" not in lines:
        warning_messages.append("Warning: '@startuml' is missing")
    elif lines[0].lower() != "@startuml":
        warning_messages.append("Warning: first line must be '@startuml'")

def validate_end(lines):
    if "@enduml" not in lines:
        warning_messages.append("Warning: '@enduml' is missing")
    elif lines[-1].lower() != "@enduml":
        warning_messages.append("Warning: last line must be '@enduml'")

def validate_design(lines):
    validate_start(lines)
    validate_end(lines)
    print_warning_messages()

def print_warning_messages():
    for warning_message in warning_messages:
        print(warning_message)

parsed_uml = parse_plantuml("plantuml_export.txt")
validate_design(parsed_uml)

