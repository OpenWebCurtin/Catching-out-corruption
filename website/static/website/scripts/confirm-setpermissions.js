/*
 * Wrap all the functionality inside a closure to prevent data leakage.
 *
 * The "undefined" variable is not specified because undefined is the default
 * value, and by declaring it like this we ensure that undefined is not overwritten
 * as undefined = true for example.
 */
(function (window, document, undefined) {
    /* "Constants" */
    var SETPERMISSIONS_CONFIRM_MSG = "Warning! Changing permissions takes effect "
        + "immediately and will enable or disable privileged functions. "
        + "Are you sure you want to change this user's permissions?";

    /*
     * Add the on-load listener for the document. We need to wait for the document
     * to load before we can attach listeners.
     *
     * Note that different browsers implement this differently, so we should use
     * the jQuery library to implement it in a cross-browser fashion.
     */
    $(document).ready(function () {

        /*
         * When the file deletion "submit" button is clicked, check if the user
         * actually wants to change the permissions. If not, we should cancel it.
         */
        $("#submit").click(function () {
            /*
             * If this function returns false, the form will not submit.
             * It's convenient that confirm() returns false if the user
             * chooses to cancel.
             */
            return window.confirm(SETPERMISSIONS_CONFIRM_MSG);
        });
    });
}(window, window.document));
