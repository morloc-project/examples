process SQR {
  input: val x
  output: path "result"
  script: template "foo.py"
}
workflow { SQR( 2 ) }
