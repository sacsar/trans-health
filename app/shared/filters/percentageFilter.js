transHealthApp.filter('percentage', function () {
    return function (input) {
       return Math.floor(input * 100) + '%';
    }
}); 