def dismiss_popup(callback, popup):
    if callback is not None:
        callback()
    popup.dismiss()
