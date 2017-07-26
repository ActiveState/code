;; This code can go into the .emacs file
;; This works with python-mode.el version 1.0

(defun py-insert-super ()
  (interactive)
  (let (methodname classname)
    (save-excursion
      (or (py-go-up-tree-to-keyword "def")
          (error "Enclosing def not found"))
      (or (looking-at "[ \t]*def[ \t]+\\([a-zA-Z0-9_]+\\)")
          (error "Can't determine method name"))
      (setq methodname (match-string 1))
      (or (py-go-up-tree-to-keyword "class")
          (error "Enclosing class not found"))
      (or (looking-at "[ \t]*class[ \t]+\\([a-zA-Z0-9_]+\\)")
          (error "Can't determine class name"))
      (setq classname (match-string 1)))
    (insert (format "super(%s,self).%s()" classname methodname))
    (backward-char)))

;; Add a hook to bind a key to this function for Python buffers

(defun bind-super-key ()
  (local-set-key "\C-c\C-f" 'py-insert-super))

(add-hook 'python-mode-hook 'bind-super-key)
