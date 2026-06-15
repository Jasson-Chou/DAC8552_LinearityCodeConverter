import re

def parse_input_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    condition = {}
    daccoderange = (0, 0)
    values = []

    section = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('[') and line.endswith(']'):
            section = line[1:-1].lower()
            continue

        if section == 'condition':
            if '=' in line:
                k, v = line.split('=')
                condition[k.strip()] = v.strip()
        elif section == 'outputlimit':
            m = re.match(r'daccoderange=(\d+):(\d+)', line)
            if m:
                daccoderange = (int(m.group(1)), int(m.group(2)))
        elif section == 'value':
            try:
                values.append(float(line))
            except:
                pass

    return condition, daccoderange, values

def value_to_code(value, condition):
    resolution = int(condition.get('resolution', 16))
    vref_p = float(condition.get('+vref', 5.0))
    vref_n = float(condition.get('-vref', 0.0))
    code = round((value - vref_n) / (vref_p - vref_n) * (2**resolution - 1))
    return code

def code_to_bitlist(code, resolution, bit_order):
    bitstring = format(code, f'0{resolution}b')
    if bit_order == 'lsb':
        bitstring = bitstring[::-1]
    return list(bitstring)

def main(input_path, output_path):
    condition, daccoderange, values = parse_input_file(input_path)
    code_min, code_max = daccoderange
    resolution = int(condition.get('resolution', 16))
    output_format = condition.get('output_format', 'serial').lower()
    bit_order = condition.get('bit_order', 'msb').lower() if output_format == 'serial' else 'msb'

    header = []
    header.append('[condition]')
    for k, v in condition.items():
        header.append(f"{k}={v}")
    header.append('\n[outputlimit]')
    header.append(f"daccoderange={code_min}:{code_max}")
    header.append('\n[result]')

    results = []

    if output_format == 'serial':
        for value in values:
            code = value_to_code(value, condition)
            code += code_min  # offset
            exceeded = False
            if code > code_max:
                code = code_max
                exceeded = True
            bits = code_to_bitlist(code, resolution, bit_order)
            if exceeded:
                results.append(f"! value = {value}, exceed daccoderange, digital_code={code}")
            else:
                results.append(f"! value = {value}")
            results.extend(bits)
            results.append("")  # 空行分隔
    elif output_format == 'parallel':
        results.append('value,digital_code,bit_code,remark')
        for value in values:
            code = value_to_code(value, condition)
            code += code_min  # offset
            remark = ''
            if code > code_max:
                code = code_max
                remark = 'exceed daccoderange'
            # 用 MSB -> LSB 排列
            bit_code = format(code, f'0{resolution}b')
            results.append(f"{value},{code},{bit_code},{remark}")

    else:
        raise ValueError(f'Unknown output_format: {output_format}')

    with open(output_path, 'w') as f:
        for line in header:
            f.write(line + '\n')
        for line in results:
            f.write(str(line) + '\n')

if __name__ == '__main__':
    main('input.txt', 'output.txt')
