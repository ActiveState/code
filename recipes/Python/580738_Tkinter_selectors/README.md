## Tkinter selectors  
Originally published: 2016-12-25 23:16:58  
Last updated: 2017-01-24 20:45:34  
Author: Miguel Martínez López  
  
Tkinter selectors like beautifulsoup selectors or jquery selectors.

It makes easy to select elements at runtime. The selectors use the same syntax than the option database.

Please let me now if you find a bug.

This is the provided API:

    toplevel_titles(widget)

    window_titles(widget)

    full_name_of_widgets(root)

    find_toplevel_by_title(widget, title)

    find_widgets_by_name(root, name)

    find_widget_by_name(root, name)

    find_widgets_by_class(root, class_)

    find_widget_by_class(root, class_)

    find(root, selector, callback, async=True)

    find_all(root, selector, callback, async=True)

    config(root, selector, **kwargs)

    config_async(root, selector, **kwargs)

    config_all(root, selector, **kwargs)

    config_all_async(root, selector, **kwargs)

    tk_print(root, name=True, class_= True, indent="\t")