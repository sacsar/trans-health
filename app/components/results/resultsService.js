transHealthApp.service('resultsService', function ($http, $routeParams) {
    var service = {};
    
    service.getPlans = function (state, query) {
        return $http.get('data/search.json');
    }
    
    return service;
});