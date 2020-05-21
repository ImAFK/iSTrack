module.exports = {
    checkIfContainsHTML: function (text) {
        if (text.includes('&amp;') || text.includes('&lt;') || text.includes('&quot;') || text.includes('&#039;'))
            return true;
        else
            return false;
    },


}
