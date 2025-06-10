import yaml


def generate_powershell_script(yaml_content, inputs):
    instructions = yaml.safe_load(yaml_content)

    ps_script_lines = []

    # Define step101 (pingblocked)
    ps_script_lines.append("""
function step101 {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Server,

        [int]$Count = 4
    )

    $result = Test-Connection -ComputerName $Server -Count $Count -Quiet
    return $result
}
""")

    # Define step102 (port test)
    ps_script_lines.append("""
function step102 {
    param (
        [Parameter(Mandatory = $true)]
        [string]$Server,

        [Parameter(Mandatory = $true)]
        [int]$Port
    )

    $result = Test-NetConnection -ComputerName $Server -Port $Port
    return $result.TcpTestSucceeded
}
""")

    # Initial call (step101)
    initial = instructions[0]
    key = list(initial.keys())[0]  # 'pingblocked'
    step_to_execute = initial[key]['execute']
    ps_script_lines.append(f"$pingBlockedResult = {step_to_execute} -Server \"{inputs['Server']}\"")

    # Conditional logic
    condition = instructions[1]
    if_condition = condition['if']
    then_step = condition['then'][0]['execute']

    ps_script_lines.append(f"if (-not $pingBlockedResult) {{")  # Only run next step if ping failed
    ps_script_lines.append(f"    $portCheck = {then_step} -Server \"{inputs['Server']}\" -Port {inputs['Port']}")
    ps_script_lines.append(f"    Write-Output \"Port test result: $portCheck\"")
    ps_script_lines.append("} else { Write-Output \"Ping succeeded. Skipping port check.\" }")

    return "\n".join(ps_script_lines)


# Sample YAML content
yaml_content = """
- pingblocked:
    execute: step101

- if: pingblocked
  then:
    - execute: step102
"""

# Sample input values
inputs = {
    "Server": "google.com",
    "Port": 80
}

# Generate PowerShell script
ps_script = generate_powershell_script(yaml_content, inputs)

# Print or save the script
print(ps_script)

# Optional: save to a .ps1 file
with open("generated_script.ps1", "w") as f:
    f.write(ps_script)
