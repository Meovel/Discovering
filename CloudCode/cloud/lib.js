// exports
var exports = {
    "findAll": findAll
};
module.exports = exports;

/**
 * Gets all the objects of the table, under the terms of the request.
 * It accepts a request object. Recursively calls itself until it receives all of the objects.
 * @param query
 * @param results
 * @param skip
 * @returns []
 */
function findAll(/*object*/query, /*array*/results, /*integer*/skip) {

    if (!results) {
        results = [];
    }
    if (!skip) {
        skip = 0;
    }
    var parseLimit = 1000;
    query.skip(skip);
    query.limit(parseLimit);
    return  query.find()
        .then(function(result){
            results = results.concat(result);
            if (result.length == parseLimit) {
                skip += parseLimit;
                return findAll(query, results, skip);
            }
            return results;
        });
}