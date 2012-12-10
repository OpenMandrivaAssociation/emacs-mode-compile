;; -*- Mode: Emacs-Lisp -*-
; Copyright (C) 2000 by Chmouel Boudjnah
; 
; Redistribution of this file is permitted under the terms of the GNU 
; Public License (GPL)
;

(if (string-match "GNU Emacs" (version))
    (autoload '%{rname} "emacs-%{rname}" nil t)
  )