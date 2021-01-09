#lang racket/base

(define symbols
  (sort
    (map symbol->string
         (namespace-mapped-symbols (make-base-namespace)))
    string<?))

(call-with-output-file*
  "/tmp/racket-dict.vim"
  (lambda (out)
    (for-each
      (lambda (symbol) (displayln symbol out))
      symbols))
  #:exists 'replace)
