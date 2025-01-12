#!/usr/bin/env nextflow

// PROCESS 1

workflow {
    // Check if input parameter is provided
    if (!params.input) {
        error "Input file parameter is required: --input <path to input file>"
    }

    // Check if output directory parameter is provided
    if (!params.outdir) {
        error "Output directory parameter is required: --outdir <path to output directory>"
    }

    x0 = Channel.fromPath(params.input)

    // PIPE 1
}
