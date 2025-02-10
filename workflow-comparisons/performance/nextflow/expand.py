import re

def make_process(old_text):
    (_, _, i) = old_text.split(" ")
    return f'''
process f{i} {{
    publishDir "${{params.outdir}}", mode: 'copy'

    input:
    path inputfile

    output:
    path "output-{i}.txt"

    script:
    """
    python3 ${{projectDir}}/mock.py ${{inputfile}} output-{i}.txt
    """
}}
// PROCESS {str(int(i)+1)}'''

def make_pipe(old_text):
    (_, _, i) = old_text.split(" ")
    return f'''
    x{i} = f{i}(x{str(int(i)-1)})
    // PIPE {str(int(i)+1)}'''

with open("main.nf", "r") as fh:
    main_text = fh.read()

main_text = re.sub(r'// PROCESS \d+', lambda m: make_process(m.group(0)), main_text, count=1)

main_text = re.sub(r'// PIPE \d+', lambda m: make_pipe(m.group(0)), main_text, count=1)

with open("main.nf", "w") as fh:
    fh.write(main_text)
