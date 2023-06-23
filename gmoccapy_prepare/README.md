# Notes for [DISPLAY] = gmoccapy

Gmoccapy intercepts MANUAL-MDI-AUTO mode switching events and closes the Probe Screen.
To avoid this, editing with root rights of the system file /usr/bin/gmoccapy is required
in next points

1.
   ```sh
    def on_hal_status_mode_manual(self, widget):
        print ("MANUAL Mode")
        if self.widgets.tbtn_user_tabs.get_active():
            return
        self.widgets.rbt_manual.set_active(True)
        # if setup page is activated, we must leave here, otherwise the pages will be reset
    ...
   ```
2.
   ```sh
    def on_hal_status_mode_mdi(self, widget):
        print ("MDI Mode", self.tool_change)

        if self.widgets.tbtn_user_tabs.get_active():
            return

        # if the edit offsets button is active, we do not want to change
        # pages, as the user may want to edit several axis values
        if self.touch_button_dic["edit_offsets"].get_active():
            return
    ...
   ```
3.
   ```sh
    def on_hal_status_mode_auto(self, widget):
        print ("AUTO Mode")
        if self.widgets.tbtn_user_tabs.get_active():
            return
        # if Auto button is not sensitive, we are not ready for AUTO commands
        # so we have to abort external commands and get back to manual mode
        # This will happen mostly, if we are in settings mode, as we do disable the mode button
        if not self.widgets.rbt_auto.get_sensitive():
    ...
   ```

This is not an ideal solution. As a result, you will need to press the mode buttons on the right once again when exiting the Probe Screen.
If more competent proposals come, I will immediately apply them.