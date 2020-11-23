/*
 * Extends obj1 by adding obj2's properties.
 */
function extend(obj1, obj2) {
    for (key in obj2) {
        /* Don't copy over properties that were part of a parent's prototype. */
        if (obj2.hasOwnProperty(key)) {
            obj1[key] = obj2[key];
        }
    }

    /* Returning this allows 'chains' to be used,
     * i.e. extend(extend(obj, {...}), {...}). */
    return obj1;
}
