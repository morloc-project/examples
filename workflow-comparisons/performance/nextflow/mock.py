import click

def mockpy(x):
    return x

def read_file(filename):
    with open(filename, "r") as fh:
        data = fh.read()
    return data

def write_file(x, filename):
    with open(filename, "w") as fh:
        fh.write(x)


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--inputfile",
    type=str,
    help="The input data file"
)
@click.option(
    "--outputfile",
    type=str,
    help="The output data file",
)

def cli(inputfile, outputfile):
    write_file(mockpy(read_file(inputfile)), outputfile)


if __name__ == "__main__":
    cli()
