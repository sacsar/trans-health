transHealthApp.service('resultsService', function ($http, $routeParams) {
    var service = {};
    
    service.getPlans = function (state, query) {
    	console.log(state, query)
        return $http.get('/api/v1/search', {params: {'state': state}});
    }
    
    return service;
});